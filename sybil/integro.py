"""
Implemention of the Integro protocol

Input:
    1) An undirected OSN graph as networkx.Graph() Objekt.
        Nodes within graph need to contain 'prob_victim' attribute
        nodes need to have ids 0..n-1
    2) a kwarg 'seeds' containing a tuple of trusted nodes' ids
    3) a kwarg 'BETA' containing the BETA scaling parameter. Default value = 2
    4) a kwarg 'trust' containing a value >=1 denoting the total amount of trust. Default value = 1

"""

import networkx as nx, numpy as np
from math import ceil
from sklearn import metrics
from scipy import sparse
import random

def merge_and_renumber(a,b):
	mapping = dict(zip(b.nodes(), list(range(len(a.nodes()), len(a.nodes()) + len(b.nodes())))))
	temp = nx.relabel_nodes(b, mapping, copy=True)
	f = nx.compose(a, temp)
	return f


def set_weights_and_start_seed(g, seeds=None, BETA=2, trust=1):
	#get number of nodes
	#set edge weights
	weight_list = []
	for i,j in g.edges_iter():

		prob_i = g.node[i]['prob_victim']
		prob_j = g.node[j]['prob_victim']

		if prob_i > 0.5 or prob_j > 0.5:
			w = min(1, BETA*(1-max(prob_i, prob_j)))
		else:
			w = 1
		weight_list.append((i, j, w))

	g.add_weighted_edges_from(weight_list)

	#add self loop for nodes with deg < 1 to normalize them to deg = 1
	#also add starting trust value
	nx.set_node_attributes(g, 'init_trust', 0)
	for n in g.nodes_iter():
		neighbors = g.neighbors(n)
		deg = sum(g[n][x]['weight'] for x in neighbors)
		if deg < 1:
			g.add_weighted_edges_from([(n, n, (1-deg)/2)])
		if n in seeds:
			g.node[n]['init_trust'] = trust/len(seeds)

def calc_weighted_degrees(g):
	"!!! Experimental! not actual Integro implementation!!!"
	degrees = {}
	for n in g.nodes():
		neighbors = g.neighbors(n)
		deg = sum(g[n][x]['weight'] for x in neighbors)
		if n in neighbors:
			deg += g[n][n]['weight']
		degrees[n] = deg
		#degrees[n] = g.degree(n)
	return degrees

# construct propagation matrix:
def construct_transition_matrix(g):
	N = len(g.nodes())
	#a = np.zeros((N, N))
	a = sparse.lil_matrix((N,N))
	nx.set_node_attributes(g,'degree', 0)
	degrees = calc_weighted_degrees(g)
	nx.set_node_attributes(g,'degree', degrees)
	for from_node, to_node in g.edges_iter():
		a[from_node,to_node] = g[from_node][to_node]['weight'] / g.node[from_node]['degree']
		a[to_node,from_node] = g[from_node][to_node]['weight'] / g.node[to_node]['degree']

		if to_node == from_node:
			a[from_node,to_node] *= 2
	return a

def getValues(n,auc):
	l = [x/n for x in range(n)]
	r = []
	for e in l:
		r.append(dist_func(e,auc))
	return r

def dist_func(e,auc):
	h1 = (1-auc)*4
	h2 = 4*auc-0.5*h1
	if e >=0 and e<=0.25:
		return e * h2*4
	elif e>0.25 and e<=0.5:
		return e * (h1-h2)*4-h1+2*h2
	elif e > 0.5 and e < 1:
		return  -2*(h1*e-h1)


def get_probs(real, auc=0.7):
	pred = []
	precision = 100000
	n = len(real)
	val = np.array(getValues(precision, auc))
	val = val / sum(val)
	y = np.cumsum(val)
	x = np.array(range(precision)) / precision

	rand = [random.random() for x in range(n)]

	sample = np.interp(rand, y, x)

	for i in range(n):
		if real[i] == 1:
			pred.append(1-sample[i])
		else:
			pred.append(sample[i])
	return(real,pred)

def add_apriori(g, auc=0.7, mode='soft'):

	""" if mode == soft probabilities will be set according to triangle distribution
		if mode == hard probabilities will be set to 0.1 for detected sybil and 0.9
		for detected honest. FR==NR==auc.
	"""

	real = []
	#get list with entries denoting if node is a victim (1) or not (0)
	for i in g.nodes():
		if g.node[i]['label'] == 0:
			n = g.neighbors(i)
			node_type = 0
			for j in n:
				if g.node[j]['label'] == 1:
					node_type = 1
			real.append(node_type)
		else:
			real.append(0)
	if mode == 'soft':
		probs = get_probs(real, auc=auc)
		for i in range(len(g.nodes())):
			g.node[i]['prob_victim'] = probs[1][i]

	elif mode == 'hard':
		for i in range(len(real)):
			r = random.random()
			if (r < auc and real[i] == 1) or (r >= auc and real[i] == 0):
				g.node[i]['prob_victim'] = 0.9
			else:
				g.node[i]['prob_victim'] = 0.1

def get_ranks(g):
	a = sparse.csc_matrix(construct_transition_matrix(g))
	v_0 = [g.node[x]['init_trust'] for x in g.nodes()]
	v_0 = np.array(v_0)
	raw = v_0
	for i in range(ceil(np.log2(len(g.nodes())))):
		raw = raw * a
	"""
	for i, val in enumerate(raw):
		if val == 0:
			print('zero rank at: '.format(i))
			print(g.node[i])
	"""
	degrees = calc_weighted_degrees(g)
	rank = raw / np.array(list(degrees.values()))
	return rank

def calc_auc(g):
	rank = get_ranks(g)
	real = list(map(lambda x, g=g: 0 if g.node[x]['label'] == 0 else 1, g.nodes()))
	rankInverse = 1 / rank
	return metrics.roc_auc_score(np.array(real), rankInverse)


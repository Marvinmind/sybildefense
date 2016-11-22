__author__ = 'Martin'
import pickle
import networkx as nx
import numpy as np
from util.keys import SF_Keys
from attacks import attacks_votetrust
from math import sqrt
from collections import defaultdict
import sklearn.linear_model as linmod
import multiprocessing


g_glob = 42
""""HIGHLY SUSPICIOUS!!!
Experimental parallel Version.
"""
def worker(node_arr, edge_arr, n_list, q):
	messages = {}
	for n in n_list:
		e_slice = edge_arr[edge_arr[:,1]==n]
		n = node_arr[node_arr[:,0]==n]
		message = {1: 0, -1: 0}
		for l in e_slice:
			for v in (1, -1):
				for u in (1, -1):
					edge_pot = l
					node_pot = g.node[x][SF_Keys.Potential][u]
					prod = edge_pot * node_pot
					for f in in_edges:
						if f[0] != y:
							prod *= g[f[0]][f[1]][SF_Keys.Message][u]
					message[v] += prod
			messages[e] = normalize(message)
	q.put(messages)
	return

def inferPosteriorsParallel(g, d=5):
	g_temp = g

	"""
	for n in g_temp.nodes_iter():
		g_temp[n][SF_Keys.Potential] = {1:g.node[n][SF_Keys.Potential](1), -1:g.node[n][SF_Keys.Potential](-1)}

	for x,y in g.edges_iter():
		g_temp[x][y][SF_Keys.Potential] = {(0,0): g[x][y][SF_Keys.Potential](0,0), (0,1): g[x][y][SF_Keys.Potential](0,1), (1,0): g[x][y][SF_Keys.Potential](1,0), (1,1): g[x][y][SF_Keys.Potential](1,1)}
	"""
	for u,v in g.edges():
		g_temp[u][v][SF_Keys.Message] = {1: 1, -1: 1}

	node_arr = np.array(len(g.edges()),6)
	edge_arr = np.array(len(g.nodes()),3)
	for i,(u,v) in enumerate(g.edges_iter()):
		edge_arr[i,0] = u
		edge_arr[i,1] = v
		edge_arr[i,2] = g[u][v][SF_Keys.Potential](1,1)
		edge_arr[i,3] = g[u][v][SF_Keys.Potential](1,-1)
		edge_arr[i,4] = g[u][v][SF_Keys.Potential](-1,1)
		edge_arr[i,5] = g[u][v][SF_Keys.Potential](-1,-1)

	for i,n in enumerate(g.nodes_iter()):
		node_arr[i][0] = g[n][SF_Keys.Potential](1)
		node_arr[i][0] = g[n][SF_Keys.Potential](-1)

	for i in range(d):

		new_messages = {}
		queue = multiprocessing.Queue()
		procs = []
		edges_sep = defaultdict(lambda :[])

		for i, e in enumerate(g_temp.edges_iter()):
			edges_sep[i%4].append(e)
		print('start setup')
		for i in range(4):
			p = multiprocessing.Process(target=worker, args=(node_arr, edge_arr, edges_sep[i], queue))
			procs.append(p)
			p.start()
		print('setup done')
		for i in procs:
			new_messages.update(queue.get())
		for p in procs:
			p.join()

		for f, t in g.edges_iter():
			g[f][t][SF_Keys.Message] = new_messages[(f,t)]
	print('all done')
	""" calc beliefs """
	for n in g.nodes():
		message = {1: 1, -1: 1}
		for e in g_temp.in_edges(n):
			message[1] *= g_temp[e[0]][e[1]][SF_Keys.Message][1]
			message[-1] *= g_temp[e[0]][e[1]][SF_Keys.Message][-1]
		message[1] *= g_temp.node[n][SF_Keys.Potential][1]
		message[-1] *= g_temp.node[n][SF_Keys.Potential][-1]
		belief = normalize(message)
		g.node[n][SF_Keys.Belief] = belief


def inferPosteriorsEdgeImprove(g, d=5):
	for u,v in g.edges():
		g[u][v][SF_Keys.Message] = defaultdict(lambda: 1)
	for i in range(d):
		#print('new round')
		new_messages = {}
		in_edge_prod = {}
		for i in g.nodes_iter():
			one_prob = 1
			minus_prob = 1
			in_edges = g.in_edges(i)
			for x,y in in_edges:
				one_prob *= g[x][y][SF_Keys.Message][1]
				minus_prob *= g[x][y][SF_Keys.Message][-1]
			in_edge_prod[i] = (one_prob, minus_prob)

		for e in g.edges_iter():
			in_edges = g.in_edges(e[0])
			message = {1: 0, -1: 0}
			for v in (1, -1):
				for u in (1, -1):
					edge_pot = g[e[0]][e[1]][SF_Keys.Potential](u,v)
					node_pot = g.node[e[0]][SF_Keys.Potential](u)
					prod = edge_pot * node_pot
					prod *= in_edge_prod[e[0]][u]
					message[v] += prod
			new_messages[e] = normalize(message)
		#print(message)
		for f, t in g.edges_iter():
			g[f][t][SF_Keys.Message] = new_messages[(f,t)]

	""" calc beliefs """
	for n in g.nodes():
		message = {1: 1, -1: 1}
		for e in g.in_edges(n):
			message[1] *= g[e[0]][e[1]][SF_Keys.Message][1]
			message[-1] *= g[e[0]][e[1]][SF_Keys.Message][-1]
		message[1] *= g.node[n][SF_Keys.Potential](1)
		message[-1] *= g.node[n][SF_Keys.Potential](-1)
		belief = normalize(message)
		g.node[n][SF_Keys.Belief] = belief

def inferPosteriors(g, d=5):
	for u,v in g.edges():
		g[u][v][SF_Keys.Message] = defaultdict(lambda: 1)
	for i in range(d):
		#print('new round')
		new_messages = {}
		for e in g.edges_iter():
			in_edges = g.in_edges(e[0])
			message = {1: 0, -1: 0}
			for v in (1, -1):
				for u in (1, -1):
					edge_pot = g[e[0]][e[1]][SF_Keys.Potential](u,v)
					node_pot = g.node[e[0]][SF_Keys.Potential](u)
					prod = edge_pot * node_pot
					for f in in_edges:
						if f[0] != e[1]:
							prod *= g[f[0]][f[1]][SF_Keys.Message][u]
					message[v] += prod
			new_messages[e] = normalize(message)
		#print(message)
		for f, t in g.edges_iter():
			g[f][t][SF_Keys.Message] = new_messages[(f,t)]

	""" calc beliefs """
	for n in g.nodes():
		message = {1: 1, -1: 1}
		for e in g.in_edges(n):
			message[1] *= g[e[0]][e[1]][SF_Keys.Message][1]
			message[-1] *= g[e[0]][e[1]][SF_Keys.Message][-1]
		message[1] *= g.node[n][SF_Keys.Potential](1)
		message[-1] *= g.node[n][SF_Keys.Potential](-1)
		belief = normalize(message)
		g.node[n][SF_Keys.Belief] = belief


def create_edge_func(prior):
	def pot_func(u,v):
		if u*v==1:
			return prior
		else:
			return 1-prior
	return pot_func

def create_node_func(prior):
	def pot_func(x):
		if x==1:
			return prior
		else:
			return 1-prior
	return pot_func

def normalize(message):
	sumProbs = message[-1] + message[1]
	if sumProbs == 0:
		message[-1] = 0.5
		message[1] = 0.5
	else:
		message[-1] /= sumProbs
		message[1] /= sumProbs

	return message

def jaccard_index(g,u,v):
	n_u = g.neighbors(u)
	n_v = g.neighbors(v)

	len_intersect = len(set(n_u).intersection(set(n_v)))
	return len_intersect/len(set(n_u).union(set(n_v)))

def get_edge_priors_linreg(g):
	positives = []
	negatives = []
	for e in g.edges():
		index = jaccard_index(g,e[0],e[1])
		if g.node[e[0]]['label'] == g.node[e[1]]['label']:
			positives.append(index)
		else:
			negatives.append(index)
	negatives = negatives*1000
	num_positive = len(positives)
	num_negative = len(negatives)

	positives.extend(negatives)
	model = linmod.LogisticRegression()
	y = list([1]*num_positive)
	y.extend([0]*num_negative)
	y = np.array(y).astype(np.float)
	x = np.array(positives)
	x = x.reshape((len(x),1))

	model.fit(x,y)
	for e in g.edges():
		index = jaccard_index(g,e[0],e[1])
		g[e[0]][e[1]][SF_Keys.Potential] = create_edge_func(model.predict(np.array(index)))
	#samples = np.array([0.0,0.9]).reshape((2,1))
	#print(model.predict_proba(samples))

def train_edge_classifier(n, d):
	NUM_NODES = 4000
	NUM_SYBILS = 1
	g = nx.watts_strogatz_graph(NUM_NODES, n, d)
	""" labels: 0-> honest 1-> sybil"""
	nx.set_node_attributes(g, 'label', 0)

	for i in range(200):
		attacks_votetrust.attack_most_common_friends(g, 40, mode='strict', system='sybilframe')

	positives = []
	negatives = []
	for e in g.edges():
		index = jaccard_index(g,e[0],e[1])
		if g.node[e[0]]['label'] == g.node[e[1]]['label']:
			positives.append(index)
		else:
			negatives.append(index)
	model = linmod.LogisticRegression()
	num_positive = len(positives)
	num_negative = len(negatives)
	positives.extend(negatives)

	y = list([1]*num_positive)
	y.extend([0]*num_negative)
	y = np.array(y).astype(np.float)
	x = np.array(positives)
	x = x.reshape((len(x),1))
	print(x.shape)
	print(y.shape)
	model.fit(x,y)
	return model

def getRanks(g):
	ranks = []
	for i in g.nodes_iter():
		ranks.append(g.node[i][SF_Keys.Belief][1])
	return np.array(ranks)


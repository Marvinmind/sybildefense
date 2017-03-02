import networkx as nx
from math import ceil, log2, pow, exp
from scipy import stats
import time
import numpy as np
import random
import scipy.sparse as sparse
import json

paras = json.load(open('../evaluations/baseparameters.json','r'))
MIN_LIMIT = 0.01

def vote_aggregation(g):
	nx.set_node_attributes(g, 'p', 0.5)
	p_sum_old = 0.5*len(g.nodes())
	neighbors = []
	for n in g.nodes_iter():
		neighbors.append(tuple(g.out_edges(n)))
	neighbors = tuple(neighbors)
	while True:
		p_sum_new = 0
		for n, data in g.nodes_iter(data=True):
			nominator = 0
			denominator = 0
			if len(neighbors[n]) == 0 or sum([g.node[v[1]]['vote_capacity'] for v in neighbors[n]]) == 0:
				data['p'] = 0.5
			else:
				for i, v in neighbors[n]:
					if g[n][v]['trust'] == 1:
						nominator += g.node[v]['vote_capacity'] * g.node[v]['p']
					denominator += g.node[v]['vote_capacity'] * g.node[v]['p']
				p_roof = nominator/denominator
				data['p'] = wilsonScore(p_roof, len(neighbors[n]))
			p_sum_new += data['p']
		if abs(p_sum_new-p_sum_old) < MIN_LIMIT:
			break
		else:
			p_sum_old = p_sum_new

def wilsonScore(p, n, alpha=0.05):
	norm = 3.8414588206941254
	#return (p + (1/(2*n))*norm)/(1+(1/n)*norm)
	if n==0:
		return 0.5
	else:
		return (p + (1/(2*n))*pow(stats.norm.ppf(1-alpha/2),2))/(1+(1/n)*pow(stats.norm.ppf(1-alpha/2),2))

def wilsonScoreExp(tup, alpha=0.05):
	norm = 3.8414588206941254
	if tup[1]==0:
		return 0.5
	else:
		return (tup[0] + (1/(2*tup[1]))*norm)/(1+(1/tup[1])*norm)
	#return (p + (1/(2*n))*pow(stats.norm.ppf(1-alpha/2),2))/(1+(1/n)*pow(stats.norm.ppf(1-alpha/2),2))


def getTrustByProb(f, k=0.3, start=0.2):
	prob = 1-(1-start)*exp(-1*k*f)
	r = random.random()
	if r < prob:
		return 1
	else:
		return -1


def getFriends(g, n):
	edges = g.edges()
	friends = []
	for e in edges:
		if n in e:
			if g[e[0]][e[1]]['trust'] == 1:
				if e[0] == n:
					friends.append(e[1])
				else:
					friends.append(e[0])
	return friends


def vote_assignment(g, initials):
	nx.set_node_attributes(g, 'initial_trust', 0)
	for n, data in g.nodes_iter(data=True):
		if n in initials:
			data['initial_trust'] = len(g.nodes())/len(initials)
		else:
			data['initial_trust'] = 0


def vote_propagation_mat(g, d=paras['d']):
	""" create adjacency matrix"""
	shape = len(g.nodes())
	a = np.zeros((shape, shape))
	v = np.zeros(shape)
	initial = np.array([g.node[x]['initial_trust'] for x in sorted(g.nodes())])*(1-d)
	for i in g.nodes_iter():
		edges = g.out_edges(i)
		length = len(edges)
		for e in edges:
			a[i][e[1]] = 1/length
	a = sparse.csc_matrix(a)
	while True:
		v_new = (d*v)*a
		v_new = v_new+initial
		diffs = v - v_new
		sum_diffs = sum(list(map(lambda x: x if x>=0 else x*-1,diffs)))
		if sum_diffs < MIN_LIMIT:
			v = v_new
			break
		else:
			v = v_new
	for i, data in g.nodes_iter(data=True):
		data['vote_capacity'] = v[i]

def vote_combined(g, d = paras['d']):
	""" create out edge list"""
	neighbors = []
	for n in g.nodes_iter():
		neighbors.append(len((g.out_edges(n))))
	neighbors = tuple(neighbors)

	""" create adjacency matrix"""
	shape = len(g.nodes())
	a = sparse.dok_matrix((shape, shape))
	b = sparse.dok_matrix((shape, shape))
	v = np.zeros(shape)
	initial = np.array([g.node[x]['initial_trust'] for x in sorted(g.nodes())]) * (1 - d)

	for i in g.nodes_iter():
		edges = g.out_edges(i)
		length = len(edges)
		for e in edges:
			a.update({(i, e[1]) : 1 / length})
			b.update({(i, e[1]) : g[e[0]][e[1]]['trust']})

	b = sparse.csc_matrix(b)
	count = 0
	a = sparse.csc_matrix(a)
	while True:
		v_new = (d * v)*a
		v_new = v_new + initial
		diffs = v - v_new
		sum_diffs = sum(abs(diffs))
		if sum_diffs < MIN_LIMIT:
			v = v_new
			break
		else:
			v = v_new
			count+=1
	a = a.T > 0
	b = b.T > 0
	p_old = 0
	p = np.ones(len(v)) * 0.5

	while True:
		nom = (p*v)*b
		denom = (p*v)*a
		mask = denom == 0
		denom += mask*2
		nom += mask
		rat = nom/denom
		p = np.apply_along_axis(wilsonScoreExp, 1, np.array(list(zip(rat,neighbors))))
		if sum(abs(p - p_old)) < MIN_LIMIT:
			break
		else:
			p_old = p
	return p

def getRanks(g):
	ranks=[]
	for i in g.nodes_iter():
		ranks.append(g.node[i]['p'])
	return np.array(ranks)
import networkx as nx
from math import ceil, log2, pow, exp
from scipy import stats
import numpy as np
import random
import scipy.sparse as sparse

MIN_LIMIT = 0.001


def vote_aggregation(g):
	nx.set_node_attributes(g, 'p', 0.5)
	p_sum_old = 0.5*len(g.nodes())
	while True:
		for n, data in g.nodes_iter(data=True):
			neighbors = g.out_edges(n)
			nominator = 0
			denominator = 0
			if len(neighbors) == 0 or sum([g.node[v[1]]['vote_capacity'] for v in neighbors]) == 0:
				#g.node[n]['p'] = 0.5
				#print('exception:')
				pass
			else:
				for i, v in neighbors:
					if g[n][v]['trust'] == 1:
						nominator += g.node[v]['vote_capacity'] * g.node[v]['p']
					denominator += g.node[v]['vote_capacity'] * g.node[v]['p']
				p_roof = nominator/denominator
				g.node[n]['p'] = wilsonScore(p_roof, len(neighbors))
		p_sum_new = sum([g.node[x]['p'] for x in g.nodes_iter()])
		if abs(p_sum_new-p_sum_old) < MIN_LIMIT:
			break
		else:
			p_sum_old = p_sum_new


def wilsonScore(p, n, alpha=0.05):
	return (p + (1/(2*n))*pow(stats.norm.ppf(1-alpha/2),2))/(1+(1/n)*pow(stats.norm.ppf(1-alpha/2),2))


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


def vote_propagation(g, d=0.8):
	nx.set_node_attributes(g, 'vote_capacity', 0)
	cap_old = [0 for x in g.nodes_iter()]
	while True:
		cap_new = []
		new_capacity = {}
		for n, data in g.nodes_iter(data=True):
			sum_in_edges = 0
			for edge in g.in_edges(n):
				node = g.node[edge[0]]
				sum_in_edges += node['vote_capacity'] / g.out_degree(edge[0])
			new_capacity[n] = d * sum_in_edges + (1-d) * data['initial_trust']
			cap_new.append(g.node[n]['vote_capacity'])
		cap_old = np.array(cap_old)
		cap_new = np.array(cap_new)
		diffs = cap_old - cap_new
		summ_diffs = sum(list(map(lambda x: x if x>=0 else x*-1,diffs)))

		nx.set_node_attributes(g, 'vote_capacity', new_capacity)
		if summ_diffs < MIN_LIMIT:
			break
		else:
			cap_old = cap_new


def vote_propagation_mat(g, d=0.8):
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
	a = sparse.csr_matrix(a)
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


def getRanks(g):
	ranks=[]
	for i in g.nodes_iter():
		ranks.append(g.node[i]['p'])
	return np.array(ranks)


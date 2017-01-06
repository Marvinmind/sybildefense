__author__ = 'Martin'
import numpy as np
from util.keys import SF_Keys
from math import ceil
from collections import defaultdict
from scipy import sparse
import time

def inferPosteriorsEdgeImprove(g, d=5):
	for u,v in g.edges():
		g[u][v][SF_Keys.Message] = defaultdict(lambda: np.array(1, dtype='float64'))
	for i in range(d):
		#print('new round')
		new_messages = {}
		in_edge_prod = {}
		for i in g.nodes_iter():
			one_prob = np.array(1, dtype='float64')
			minus_prob = np.array(1, dtype='float64')
			in_edges = g.in_edges(i)
			for x,y in in_edges:
				one_prob *= g[x][y][SF_Keys.Message][1]
				minus_prob *= g[x][y][SF_Keys.Message][-1]
			in_edge_prod[i] = {1: one_prob, -1: minus_prob}
		for e in g.edges_iter():
			message = {1: 0, -1: 0}
			for v in (1, -1):
				for u in (1, -1):
					edge_pot = np.array(g[e[0]][e[1]][SF_Keys.Potential](u,v), dtype='float64')
					node_pot = np.array(g.node[e[0]][SF_Keys.Potential](u), dtype='float64')
					prod = edge_pot * node_pot
					prod *= in_edge_prod[e[0]][u]/g[e[1]][e[0]][SF_Keys.Message][u]
					message[v] += prod
			new_messages[e] = normalize(message)
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


def inferPosteriorsEdgeImproveNew(g, d=5):
	graphHealthCheck(g)

	numNodes = len(g.nodes())

	"Messages"
	zeroM = sparse.dok_matrix((numNodes, numNodes), dtype='float64')
	oneM = sparse.dok_matrix((numNodes, numNodes), dtype='float64')

	"Edge Potentials"
	sameP = sparse.dok_matrix((numNodes, numNodes), dtype='float64')
	diffP = sparse.dok_matrix((numNodes, numNodes), dtype='float64')

	"Node Potentials"
	zeroP = np.empty(numNodes, dtype='float64')
	oneP = np.empty(numNodes, dtype='float64')
	t = time.clock()
	for u,v, data in g.edges_iter(data=True):

		zeroM.update({(v,u) : 0.5})
		oneM.update({(v,u) : 0.5})

		diffP.update({(v,u) : data[SF_Keys.Potential](1,-1)})
		sameP.update({(v,u) : data[SF_Keys.Potential](1,1)})

	for n, data in g.nodes_iter(data=True):
		oneP[n] = data[SF_Keys.Potential](1)
		zeroP[n] = data[SF_Keys.Potential](-1)
	print('update duration: {}'.format(time.clock()-t))

	zeroM = sparse.csr_matrix(zeroM, dtype='float64')
	oneM = sparse.csr_matrix(oneM, dtype='float64')
	sameP = sparse.csr_matrix(sameP, dtype='float64')
	diffP = sparse.csr_matrix(diffP, dtype='float64')


	for i in range(d):
		t = time.clock()
		r, c, v = sparse.find(oneM)  # a is input sparse matrix
		outOne = np.bincount(r, np.log(v), minlength=oneM.shape[0])
		r, c, v = sparse.find(zeroM)  # a is input sparse matrix
		outZero = np.bincount(r, np.log(v), minlength=oneM.shape[0])
		ratio = np.exp(np.array(outZero, dtype='float64') - np.array(outOne, dtype='float64'))
		if np.min(ratio)==0:
			print('underflow. god damit')
		zeroMV = ratio * zeroP
		oneMV = oneP
		print('mult message duration: {}'.format(time.clock() - t))

		oneMT = oneM.T

		r, c, v = sparse.find(oneMT)

		t = time.clock()

		one1 = (sparse.spdiags(oneMV, 0, len(oneMV), len(oneMV)) * sameP.T).T
		one2 = (sparse.spdiags(zeroMV, 0, len(zeroMV), len(zeroMV)) * diffP.T).T
		zero1 = (sparse.spdiags(zeroMV, 0, len(zeroMV), len(zeroMV)) * sameP.T).T
		zero2 = (sparse.spdiags(oneMV, 0, len(oneMV), len(oneMV)) * diffP.T).T

		one1[r,c] /= oneM.T[r,c]
		one2[r,c] /= zeroM.T[r,c]
		zero1[r,c] /= zeroM.T[r,c]
		zero2[r,c] /= oneM.T[r,c]

		oneM = one1 + one2
		zeroM = zero1 + zero2

		r1, c1, v1 = sparse.find(zeroM)
		r2, c2, v2 = sparse.find(oneM)

		zeroM[r1, c1] /= v1+v2
		oneM[r2, c2] /= v1+v2

		zeroM = sparse.csr_matrix(zeroM, dtype='float64')
		oneM = sparse.csr_matrix(oneM, dtype='float64')

		print('matrix mult duration: {}'.format(time.clock() - t))
	t = time.clock()
	""" calc beliefs """
	r, c, v = sparse.find(oneM)
	v = v.astype('float64')
	oneB = np.exp(np.bincount(r, np.log(v), minlength=oneM.shape[0]))
	r, c, v = sparse.find(zeroM)
	v = v.astype('float64')

	zeroB = np.exp(np.bincount(r, np.log(v), minlength=zeroM.shape[0]))
	for n in g.nodes():
		message = {1: None, -1: None}
		message[1] = oneB[n] * oneP[n]
		message[-1] = zeroB[n] * zeroP[n]
		belief = normalize(message)
		g.node[n][SF_Keys.Belief] = belief
	print('message collection duration: {}'.format(time.clock() - t))


def inferPosteriors(g, d=5):
	for u,v in g.edges():
		g[u][v][SF_Keys.Message] = defaultdict(lambda: 1)
	for i in range(d):
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



def getRanks(g):
	ranks = []
	for i in g.nodes_iter():
		ranks.append(g.node[i][SF_Keys.Belief][1])
	return np.array(ranks)

def graphHealthCheck(g):
	message = []
	for n, d in g.nodes(data=True):
		if g.degree(n)==0:
			message.append = 'node has zero degree: {}'.format(n)
		if d[SF_Keys.Potential](1) <= 0 or d[SF_Keys.Potential](-1) <= 0:
			message.append = 'node has zero or smaller node pot: {} {}'.format(n, d[SF_Keys.Potential])
	for start, end, d in g.edges(data=True):
		if start not in g[end]:
			message.append('not back and forth')
		if d[SF_Keys.Potential](0,0) <= 0 or d[SF_Keys.Potential](0,1) <= 0 or d[SF_Keys.Potential](1,0) <= 0 or d[SF_Keys.Potential](1,1) <= 0:
			message.append = 'edge has zero or smaller edge pot: {} {}'.format((start, end), d[SF_Keys.Potential])

	if len(message) == 0:
		print('graph healthy')
	else:
		print(message)

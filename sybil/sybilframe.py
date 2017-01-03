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
from scipy import sparse
import sys



def inferPosteriorsEdgeImprove(g, d=5):
	for u,v in g.edges():
		g[u][v][SF_Keys.Message] = defaultdict(lambda: np.array(1, dtype='float128'))
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
					edge_pot = np.array(g[e[0]][e[1]][SF_Keys.Potential](u,v), dtype='float128')
					node_pot = np.array(g.node[e[0]][SF_Keys.Potential](u), dtype='float128')
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
	#graphHealthCheck(g)
	numNodes = len(g.nodes())

	"Messages"
	zeroM = sparse.lil_matrix((numNodes, numNodes))
	oneM = sparse.lil_matrix((numNodes, numNodes))

	"Edge Potentials"
	sameP = sparse.lil_matrix((numNodes, numNodes))
	diffP = sparse.lil_matrix((numNodes, numNodes))

	"Node Potentials"
	zeroP = np.empty(numNodes)
	oneP = np.empty(numNodes)

	for u,v, data in g.edges_iter(data=True):
		zeroM[v, u] = 1
		oneM[v, u] = 1

		diffP[v, u] = data[SF_Keys.Potential](1,-1)
		sameP[v, u] = data[SF_Keys.Potential](1,1)

	for n, data in g.nodes_iter(data=True):
		oneP[n] = data[SF_Keys.Potential](1)
		zeroP[n] = data[SF_Keys.Potential](-1)

	zeroM = sparse.csc_matrix(zeroM, dtype='float128')
	oneM = sparse.csc_matrix(oneM, dtype='float128')
	sameP = sparse.csc_matrix(sameP, dtype='float128')
	diffP = sparse.csc_matrix(diffP, dtype='float128')


	for i in range(d):
		""""
		print(oneM.toarray())
		r, c, v = sparse.find(zeroM)
		zeroMV = np.exp(np.bincount(r, np.log(v), minlength=zeroM.shape[0]))
		zeroMV[np.setdiff1d(np.arange(zeroM.shape[0]), r)] = 0
		#zeroMV += np.finfo(np.dtype('float64')).eps

		zeroMV = zeroMV * zeroP


		r, c, v = sparse.find(oneM)
		oneMV = np.exp(np.bincount(r, np.log(v), minlength=oneM.shape[0]))
		oneMV[np.setdiff1d(np.arange(oneM.shape[0]), r)] = 0
		#oneMV += np.finfo(np.dtype('float64')).eps
		print('old')
		print(oneMV)
		oneMV = oneMV * oneP
		"""

		zeroMT = zeroM.T
		r, c, v = sparse.find(zeroMT)
		out = np.zeros(zeroMT.shape[1], dtype=zeroM.dtype)
		unqr, shift_idx = np.unique(c, return_index=1)
		out[unqr] = np.multiply.reduceat(v, shift_idx)
		zeroMV = out * zeroP

		oneMT = oneM.T
		r, c, v = sparse.find(oneMT)
		out = np.zeros(oneMT.shape[1], dtype=oneM.dtype)
		unqr, shift_idx = np.unique(c, return_index=1)

		out[unqr] = np.multiply.reduceat(v, shift_idx)
		oneMV = out * oneP

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
		"""

		oneMd = oneM.toarray()
		oneMd[oneMd==0]=1

		zeroMd = zeroM.toarray()
		zeroMd[zeroMd==0]=1

		oneV = oneMd.prod(1)
		zeroV = zeroMd.prod(1)
		print(oneV[oneV==0])
		print(zeroV[zeroV==0])
		freak = np.flatnonzero(zeroV == 0)
		print(freak)
		freakRow = zeroMd[freak,:]
		print(len(freakRow[freakRow<1]))
		print(min(freakRow[freakRow<1]))
		"""


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

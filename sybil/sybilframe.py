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
			in_edge_prod[i] = {1:one_prob, -1: minus_prob}

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

def inferPosteriorsEdgeImproveNew(g, d=5):
	graphHealthCheck(g)
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
		zeroM[v,u] = 1
		oneM[v,u] = 1

		diffP[v,u] = data[SF_Keys.Potential](1,-1)
		sameP[v,u] = data[SF_Keys.Potential](1,1)

	for n, data in g.nodes_iter(data=True):
		oneP[n] = data[SF_Keys.Potential](1)
		zeroP[n] = data[SF_Keys.Potential](-1)

	zeroM = sparse.csc_matrix(zeroM)
	oneM = sparse.csc_matrix(oneM)
	sameP = sparse.csc_matrix(sameP)
	diffP = sparse.csc_matrix(diffP)
	zeroM = sparse.csc_matrix(zeroM)
	oneM = sparse.csc_matrix(oneM)


	for i in range(d):
		r, c, v = sparse.find(zeroM)
		zeroMV = np.exp(np.bincount(r, np.log(v), minlength=zeroM.shape[0])) * zeroP
		r, c, v = sparse.find(oneM)
		oneMV = np.exp(np.bincount(r, np.log(v), minlength=oneM.shape[0])) * oneP

		#oneM, zeroM = np.multiply(oneMV, sameP)/oneM.T + np.multiply(zeroMV, diffP)/zeroM.T, np.multiply(zeroMV, sameP)/zeroM.T + np.multiply(oneMV, diffP)/oneM.T
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
		"normalize"
		divMat = oneM+zeroM
		divMat[divMat==0] = 1

		zeroM /= divMat
		oneM /= divMat

		zeroM[zeroM==0] = 1
		oneM[oneM==0] = 1
		"""

	""" calc beliefs """
	r, c, v = sparse.find(oneM)
	oneB = np.exp(np.bincount(r, np.log(v), minlength=oneM.shape[0]))
	r, c, v = sparse.find(zeroM)
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
		if d[SF_Keys.Potential](0,0) <= 0 or d[SF_Keys.Potential](0,1) <= 0 or d[SF_Keys.Potential](1,0) <= 0 or d[SF_Keys.Potential](1,1) <= 0:
			message.append = 'edge has zero or smaller edge pot: {} {}'.format((start, end), d[SF_Keys.Potential])

	if len(message) == 0:
		print('graph healthy')
	else:
		print(message)

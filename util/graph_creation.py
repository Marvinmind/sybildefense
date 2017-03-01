__author__ = 'Martin'
import networkx as nx
import random
from math import floor
from util.keys import Systems
import sybil.integro as integro

def create_directed_smallWorld(n, e):
	# Create graph
	g = nx.watts_strogatz_graph(n, e, 0.02)
	g = nx.DiGraph(g)
	nx.set_node_attributes(g, 'type', 'honest')
	sorted_edges = sorted(g.edges(), key= lambda tup: tup[0])
	for e in sorted_edges:
		if e[0] < e[1]:
			r = random.random()
			if r < 0.5:
				g.remove_edge(e[0], e[1])
				g[e[1]][e[0]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
			else:
				g.remove_edge(e[1], e[0])
				g[e[0]][e[1]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
	to_remove = []
	for i in nx.strongly_connected_components(g):
		if len(i) == 1:
			print("WARNING: REMOVING NODES!!")
			to_remove.append(i.pop())
	for i in to_remove:
		g.remove_node(i)
	mapping = dict(zip(g.nodes(), range(len(g.nodes()))))
	nx.relabel_nodes(g, mapping, copy=False)

	return g

def add_sybil_region(g, SIZE_SYBIL, m):
	f = nx.barabasi_albert_graph(SIZE_SYBIL, m)
	oldEdges = f.edges()
	nx.set_edge_attributes(f, 'trust', 1)
	nx.set_node_attributes(f, 'label', 1)
	nx.set_node_attributes(f, 'seed', 0)

	f = nx.DiGraph(f)
	for e in oldEdges:
		r = random.random()
		if r<0.5:
			f.remove_edge(e[0],e[1])
		else:
			f.remove_edge(e[1],e[0])

	f = integro.merge_and_renumber(g, f)
	return f

def add_community(g, SIZE_SYBIL, NUMBER_IN, type='sybil', num_honest=None):
	### Add sybil region ###

	NUM_NODES = len(g.nodes())

	if num_honest == None:
			num_honest = NUM_NODES

	for i in range(SIZE_SYBIL):
		g.add_node(NUM_NODES + i)

	for i in range(SIZE_SYBIL):
		for j in range(SIZE_SYBIL):
			if j != i:
				g.add_edge(i + NUM_NODES, j + NUM_NODES)
				g[i + NUM_NODES][j + NUM_NODES]['trust'] = 1
		if type =='sybil':
			label = 1
		elif type == 'honest':
			label = 0
		g.node[i+NUM_NODES]['label'] = label

	selected = []
	r = 0
	for i in range(NUMBER_IN):
		while True:
			r = random.randint(0, num_honest-1)
			if r not in selected:
				selected.append(r)
				sybil = random.randint(NUM_NODES, SIZE_SYBIL + NUM_NODES-1)
				g.add_edge(r, sybil)
				break
	return r

def append_boosting_region(g, dummies):
	N = len(g.nodes())

	g.add_edge(N, N+1, {'trust':1})
	g.add_edge(N+1, N+2, {'trust':1})
	g.add_edge(N+2, N, {'trust':1})

	for dum in dummies:
		g.add_edge(dum, N, {'trust':1})


	g.add_edge(N+3, N, {'trust':1})
	g.add_edge(N+3, N+1, {'trust':1})
	g.add_edge(N+3, N+2, {'trust':1})

	for i in range(4):
		g.node[N+i]['label'] = 1

def undirected_to_directed(g):
	g = nx.DiGraph(g)

	sorted_edges = sorted(g.edges(), key = lambda tup: tup[0])
	for e in sorted_edges:
		if e[0] < e[1]:
			r = random.random()
			if r < 0.5:
				g.remove_edge(e[0], e[1])
				g[e[1]][e[0]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
			else:
				g.remove_edge(e[1], e[0])
				g[e[0]][e[1]]['trust'] = (lambda x: -1 if x < 0.2 else 1)(random.random())
	to_remove = []
	for i in g.nodes_iter():
		if g.degree(i) == 0:
			print("WARNING: REMOVING NODES!!")
			to_remove.append(i)
	for i in to_remove:
		g.remove_node(i)

	"label nodes from 0 to 1"
	mapping = dict(zip(g.nodes(), range(len(g.nodes()))))
	nx.relabel_nodes(g, mapping, copy=False)
	print("labels in undir to dir")
	print(g.nodes())
	return g

__author__ = 'Martin'
import unittest
import networkx as nx
import  numpy as np
from sybil import sybilframe, integro
from util import graph_creation
import random
from util.keys import SF_Keys



class sybilframe_tests(unittest.TestCase):
	def test_infer(self):
		g = nx.Graph()
		g.add_edge(0,1)
		g.add_edge(1,2)
		g.add_edge(2,3)
		g.add_edge(3,0)

		"""Wrong node potential """
		g.add_edge(0,4)
		g.add_edge(1,4)
		g.add_edge(2,4)
		g.add_edge(3,4)

		g[0][1][SF_Keys.Potential] = sybilframe.create_edge_func(0.1)
		g[1][2][SF_Keys.Potential] = sybilframe.create_edge_func(0.1)
		g[2][3][SF_Keys.Potential] = sybilframe.create_edge_func(0.1)
		g[3][0][SF_Keys.Potential] = sybilframe.create_edge_func(0.1)

		g[0][4][SF_Keys.Potential] = sybilframe.create_edge_func(0.1)
		g[1][4][SF_Keys.Potential] = sybilframe.create_edge_func(0.8)
		g[2][4][SF_Keys.Potential] = sybilframe.create_edge_func(0.1)
		g[3][4][SF_Keys.Potential] = sybilframe.create_edge_func(0.9)

		g.node[0][SF_Keys.Potential] = sybilframe.create_node_func(0.8)
		g.node[1][SF_Keys.Potential] = sybilframe.create_node_func(0.2)
		g.node[2][SF_Keys.Potential] = sybilframe.create_node_func(0.9)
		g.node[3][SF_Keys.Potential] = sybilframe.create_node_func(0.1)

		"This one is wrong on purpose"
		g.node[4][SF_Keys.Potential] = sybilframe.create_node_func(0.9)

		g = nx.DiGraph(g)
		sybilframe.inferPosteriorsEdgeImproveNew(g, 4)

		print(g.node[0][SF_Keys.Potential](1))
		print(g.node)

	def test_smallWorld(self):
		NUM_NODES = 2000
		NUM_SYBILS = 1
		g = nx.watts_strogatz_graph(NUM_NODES, 30, 0.02)

		graph_creation.add_sybil_region(g, NUM_SYBILS, 10)

		labels = [1]*NUM_NODES
		labels.extend([0]*NUM_SYBILS)
		priors = integro.get_probs(labels, auc=0.8)
		print(np.mean(list(priors[1])[0:NUM_NODES]))
		print(np.mean(list(priors[1])[NUM_NODES: NUM_NODES+NUM_SYBILS]))
		for i in range(NUM_NODES+NUM_SYBILS):
			g.node[i][sybilframe.Keys.Potential] = sybilframe.create_node_func(priors[1][i])
		edges = []
		classes = []
		for start, end in g.edges():
			edges.append((start,end))
			if (start < NUM_NODES and end < NUM_NODES) or (start >= NUM_NODES and end >= NUM_NODES):
				classes.append(1)
			else:
				classes.append(0)
		edge_prior = integro.get_probs(classes, auc=0.8)[1]

		for i, (start, end) in enumerate(edges):
			g[start][end][sybilframe.Keys.Potential] = sybilframe.create_edge_func(edge_prior[i])

		g = nx.DiGraph(g)
		sybilframe.inferPosteriors(g, d=4)

		sum_b = 0
		sum_s = 0
		for i in range(NUM_NODES+NUM_SYBILS):

			if g.node[i][sybilframe.Keys.Belief][1] > 0.5:
				if i<NUM_NODES:
					sum_b+=1
				else:
					sum_s+=1
		sum_b/=NUM_NODES
		sum_s/=NUM_SYBILS
		print(sum_b)
		print(sum_s)
		print(g.node[2000])

	def test_authors_attachement(self):
		NUM_HONEST = 1000
		NUM_SYBIL = 400
		FR = 0.5

		g_0 = nx.barabasi_albert_graph(NUM_HONEST, 10)
		g_1 = nx.barabasi_albert_graph(NUM_SYBIL, 10)

		g = integro.merge_and_renumber(g_0, g_1)
		attack_edges = []

		for i in range(1000):
			while True:
				h = random.randint(0,NUM_HONEST-1)
				s = random.randint(NUM_HONEST, NUM_HONEST+NUM_SYBIL-1)
				if (s,h) not in attack_edges:
					attack_edges.append((s,h))
					break
		print(len(attack_edges))
		g.add_edges_from(attack_edges)
		g_b = g.copy()
		correct = []
		accepted = []
		for i in range(3):
			for i in range(NUM_HONEST+NUM_SYBIL):
				r = random.random()
				if (r < FR and i < NUM_HONEST) or (r >= FR and i >= NUM_HONEST):
					g.node[i][sybilframe.Keys.Potential] = sybilframe.create_node_func(random.random()*0.4+0.1)
				else:
					g.node[i][sybilframe.Keys.Potential] = sybilframe.create_node_func(random.random()*0.4+0.5)

			for start, end in g.edges():
				g[start][end][sybilframe.Keys.Potential] = sybilframe.create_edge_func(0.9)

			g = nx.DiGraph(g)
			sybilframe.inferPosteriors(g, d=6)

			for i in range(NUM_SYBIL+NUM_HONEST):
				if g.node[i][sybilframe.Keys.Belief][1] > 0.5:
					if i < NUM_HONEST:
						correct.append(i)
					else:
						accepted.append(i)
			g = g_b.copy()
		print(len(accepted))
		print(len(correct))



	def test_new_dist(self):
		results = []
		for i in range(200):
			results.append(integro.dist_func(i/200, auc=0.5))
		print(results)

__author__ = 'Martin'
import unittest
from attacks import attacks_votetrust
from util import graph_creation
from sybil import sybilframe, integro
import numpy as np
import networkx as nx

class Sybilframe_attack_tests(unittest.TestCase):
	def breadth_first_test(self):
		NUM_NODES = 2000
		NUM_SYBILS = 1

		g = nx.watts_strogatz_graph(NUM_NODES, 40, 0.02)
		""" labels: 0-> honest 1-> sybil"""
		nx.set_node_attributes(g, 'label', 0)
		attacks_votetrust.attack_most_common_friends(g, 5, mode='strict', system='sybilframe')

		for i in range(NUM_NODES, NUM_NODES+NUM_SYBILS):
			g.node[i]['label'] = 1

		""" set node priors """
		labels = [1]*NUM_NODES
		labels.extend([0]*NUM_SYBILS)
		priors = integro.get_probs(labels, auc=0.8)
		print(np.mean(list(priors[1])[0:NUM_NODES]))
		print(np.mean(list(priors[1])[NUM_NODES: NUM_NODES+NUM_SYBILS]))
		for i in range(NUM_NODES+NUM_SYBILS):
			g.node[i][sybilframe.Keys.Potential] = sybilframe.create_node_func(priors[1][i])

		""" train predictor for edge priors """
		model = sybilframe.train_edge_classifier(40, 0.08)

		edges = []
		indices = []
		for start, end in g.edges():
			edges.append((start,end))
			indices.append(sybilframe.jaccard_index(g,start,end))

		samples = np.array(indices).reshape(len(indices),1)
		results = model.predict(samples)
		for i, e in enumerate(edges):
			g[e[0]][e[1]][sybilframe.Keys.Potential] = sybilframe.create_edge_func(results[i])

		print('start computing')
		g = nx.DiGraph(g)
		sybilframe.inferPosteriors(g, d=5)

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
		print(g.node[NUM_NODES])

	def test_smallword(self):
		g = nx.watts_strogatz_graph(2000, 40, 0.2)
		results = []
		for e in g.edges():
			results.append(sybilframe.jaccard_index(g,e[0],e[1]))
		print(sum(results)/len(results))
__author__ = 'Martin'
import numpy as np
import unittest
import random
from util import graph_creation, calc
from evaluations import parameters
import networkx as nx
from sybil import integro

class test_boosting(unittest.TestCase):
	def test_smallWorld(self):
		g = graph_creation.create_directed_smallWorld(4000, 40)
		g = nx.Graph(g)
		nx.set_node_attributes(g,'label', 0)
		NUM_NODES = len(g.nodes())
		NUM_SYBILS = 10

		"add boosting region"
		r = []
		for i in range(5):
			while True:
				h = random.randint(0,NUM_NODES-1)
				if h not in r:
					g.add_edge(h, NUM_NODES,{'trust':1})
					r.append(h)
					break

		g.add_edge(NUM_NODES, NUM_NODES+1,{'trust':1})
		g.add_edge(NUM_NODES+1, NUM_NODES+2,{'trust':1})
		g.add_edge(NUM_NODES+2, NUM_NODES,{'trust':1})

		for i in range(3):
			g.node[NUM_NODES+i]['label'] = 1

		""" set 10 sybil nodes"""
		for i in range(NUM_SYBILS):
			g.add_node(NUM_NODES+i+3,{'label':1})
			g.add_edge(NUM_NODES+i+3,NUM_NODES,{'trust': 1})
			g.add_edge(NUM_NODES+i+3,NUM_NODES+1,{'trust': 1})
			g.add_edge(NUM_NODES+i+3,NUM_NODES+2,{'trust': 1})


		victim_probs = calc.getNodeProbClosure(0.25)
		node_probs = calc.getNodeProbClosure(0.75)
		for n in r:
			g.node[n]['prob_victim'] = victim_probs()

		for i in g.nodes():
			if i not in r:
				g.node[i]['prob_victim'] = node_probs()

		seeds = [0,200,400]
		integro.set_weights_and_start_seed(g, seeds=seeds, trust=len(g.nodes()))
		ranks = integro.get_ranks(g)
		trust_h = []
		trust_s = []
		for i in range(NUM_NODES):
			trust_h.append(ranks[i])
		print('start sybil')
		for i in range(NUM_NODES, NUM_NODES+13):
			print(ranks[i])
			trust_s.append(ranks[i])

		print(len(g.nodes()))
		print(np.mean(trust_h))
		print(np.mean(trust_s))

from sybil import integro
from scipy import stats
import unittest
import networkx as nx
from math import floor, ceil
import random
from util import graph_creation
import numpy as np


class IntegroTests(unittest.TestCase):

	def test_transition_matrix(self):
		#create simple  matrix
		g = nx.Graph()
		nx.set_node_attributes(g, 'degree', 0)
		g.add_nodes_from(list(range(5)))
		for i in range(5):
			g.add_weighted_edges_from([(0,0,0.1), (0,1,0.8), (1,2,0.5),(1,3,0.5),(2,3,2),(3,4,1)])
		a = integro.construct_transition_matrix(g)
		expect = np.array([[0.2, 0.8, 0, 0, 0], [0.44, 0, 0.28, 0.28, 0], [0, 0.2, 0, 0.8, 0], [0, 0.14, 0.57, 0, 0.29], [0, 0, 0, 1, 0]])
		self.assertEqual((np.around(a, 2)-expect).any(), False)

	def test_weights(self):
		g = nx.Graph()
		g.add_edges_from([(0, 1), (1, 2), (0, 2)])
		g.add_edges_from([(0, 3), (1, 4), (2, 5)])
		g.add_edges_from([(3,6),(4,6),(5,6)])
		g.add_edges_from([(6,7)])

		for i in range(7):
			g.node[i]['label'] = 0
		g.node[7]['label'] = 1
		integro.add_apriori(g, auc=1, mode='hard')
		integro.set_weights_and_start_seed(g, seeds=(0, 1))

		#Make sure 6 is a victim and all others are not
		for i in g.nodes_iter():
			if i == 6:
				self.assertGreater(g.node[i]['prob_victim'], 0.5)
			else:
				self.assertLess(g.node[i]['prob_victim'], 0.5)

		for i in g.nodes():
			probi = g.node[i]['prob_victim']
			for j in g.neighbors(i):
				probj = g.node[j]['prob_victim']
				if probi > 0.5 or probj > 0.5:
					self.assertEqual(g[i][j]['weight'] < 1, True)
				elif i!=j:
					self.assertEqual(g[i][j]['weight'] == 1, True)

	def test_weights_frequencies(self):
		g = nx.Graph()
		""" 2 is a victim, 3 a sybil"""
		g.add_edges_from([(0,1),(1,2),(2,3)])
		nx.set_node_attributes(g, 'label', 0)
		g.node[3]['label'] = 1

		countHonest = 0
		countVictim = 0

		for i in range(10000):
			integro.add_apriori(g)
			integro.set_weights_and_start_seed(g, seeds=(0, 1))
			if g[0][1]['weight'] == 1:
				countHonest += 1
			if g[1][2]['weight'] == 1:
				countVictim += 1

		print(countHonest)
		print(countVictim)


	def test_weight_setting(self):
		g = nx.Graph()
		g.add_edges_from([(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9)])
		g.add_edges_from([(10,11),(11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,18),(18,19)])
		g.add_edges_from([(10,20),(11,20),(12,20),(13,20),(14,20),(15,20),(16,20),(17,20),(18,20),(19,20)])

		nx.set_node_attributes(g,'label',0)
		g.node[20]['label'] = 1
		integro.add_apriori(g, auc=1, mode='hard')

		vic = 0
		nonvic = 0
		for i in range(20):
			if i < 10:
				nonvic += g.node[i]['prob_victim']
			else:
				vic += g.node[i]['prob_victim']
				print(g.node[i]['prob_victim'])
		print('vic mean = {}'.format(vic/10))
		print('nonvic mean = {}'.format(nonvic / 10))

	def test_getprobs(self):
		real = []
		for i in range(1000000):
			r = random.random()
			if r<0.5:
				real.append(1)
			else:
				real.append(0)
		auc = 0.75
		real, pred = integro.get_probs(real,auc=auc)
		correct = 0
		for i, val in enumerate(real):
			if val==0:
				if pred[i] < 0.5:
					correct+=1
			else:
				if pred[i] >= 0.5:
					correct+=1
		self.assertEqual(auc, round(correct/1000000,2))


	def test_rank_authors(self):
		g_h = nx.watts_strogatz_graph(6136, 12, 0.05)
		g_s = nx.watts_strogatz_graph(3068, 24, 0.05)

		l_h = len(g_h.nodes())
		l_s = len(g_s.nodes())

		f = integro.merge_and_renumber(g_h, g_s)

		n = len(f.nodes())


		# label sybil and honest
		nx.set_node_attributes(f, 'label', 0)
		for i in range(n):
			if i >= l_h:
				f.node[i]['label'] = 1

		print('start edges')
		N_ATTACK_EDGES = 35306

		# random attack edges
		attack_edges = []

		for i in range(N_ATTACK_EDGES):
			while True:
				n1 = random.randint(0, l_h-1)
				n2 = random.randint(l_h, l_h+l_s-1)
				if (n1, n2) not in attack_edges:
					attack_edges.append((n1, n2))
					break


		f.add_edges_from(attack_edges)
		print('connection status: {}'.format(nx.is_connected(f)))
		integro.add_apriori(f, auc=1, mode='hard')
		integro.set_weights_and_start_seed(f, seeds=(0,200,1200,3000), trust=9204)
		ranks = integro.get_ranks(f)
		print(np.median(ranks[0:len(g_h)]))
		print(np.median(ranks[len(g_h):len(g_s)+len(g_h)]))

		print(integro.calc_auc(f))

	def test_rank_toy(self):

		g = nx.Graph()
		g.add_edges_from([(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(3,5)])
		nx.set_node_attributes(g, 'label', 0)

		for i in range(6):
			if i in (4, 5):
				g.node[i]['label'] = 1
			else:
				g.node[i]['label'] = 0

		print(integro.calc_auc(g))

	def test_peripheral_vs_little_connected(self):
		g = nx.watts_strogatz_graph(2000,30,0.05)
		NUM_NODES = len(g.nodes())
		NUM_LONELY = 10
		NUM_SYBIL = 20

		"""
		for i in range(NUM_LONELY):
			requested = []
			for j in range(5):
				while True:
					friend = random.randint(0, NUM_NODES-1)
					if friend not in requested:
						g.add_edge(NUM_NODES+i, friend)
						break
		"""

		nx.set_node_attributes(g, 'label', 0)

		for i in range(NUM_SYBIL):
			requested = []
			for j in range(5):
				while True:
					friend = random.randint(0, NUM_NODES-1)
					if friend not in requested:
						g.add_edge(NUM_NODES+i, friend)
						g.node[NUM_NODES+i]['label'] = 1
						break



		integro.add_apriori(g, auc=0.99, mode='hard')
		integro.set_weights_and_start_seed(g, seeds=(0,200,500), trust=NUM_NODES)

		print(g.node[NUM_NODES])
		""""
		print(np.mean(rank[0:NUM_NODES]))
		print(np.mean(rank[NUM_NODES:NUM_NODES+NUM_LONELY]))
		print(np.mean(rank[NUM_NODES+NUM_LONELY:NUM_NODES+NUM_LONELY+NUM_SYBIL]))
		"""
		print(integro.calc_auc(g))

	def test_sybil_region(self):
		g = nx.watts_strogatz_graph(2000, 30, 0.05)
		nx.set_node_attributes(g, 'label', 0)
		NUM_NODES = len(g.nodes())
		NUM_SYBIL = 300
		graph_creation.add_sybil_region(g, NUM_SYBIL, 100)
		integro.add_apriori(g, auc=0.7)
		integro.set_weights_and_start_seed(g, seeds=(0, 200, 500), trust=NUM_NODES)
		print(integro.calc_auc(g))

	def test_propagation(self):
		g = nx.Graph()
		g.add_edges_from([(0,1),(1,2),(2,3),(3,4)])
		nx.set_node_attributes(g, 'label', 0)
		g.node[3]['label'] = 1
		g.node[4]['label'] = 1


		integro.add_apriori(g, 1, mode='hard')
		integro.set_weights_and_start_seed(g, seeds=[0], trust=4)
		print(g.node)
		print(g.edges(data=True))
		print(integro.get_ranks(g))


	def test_com_v_sib(self):
		g = nx.Graph()
		g.add_edges_from([(0,1),(0,2),(1,3),(2,3)])
		nx.set_node_attributes(g, 'label', 0)

		graph_creation.add_community(g,5,1, type='honest', num_honest=4)
		graph_creation.add_community(g,5,1, type='sybil', num_honest=4)


		integro.add_apriori(g, auc=1, mode='hard')
		integro.set_weights_and_start_seed(g, seeds=(0, 3), trust=14)
		ranks = stats.rankdata(integro.get_ranks(g))

		print(g.edges(data=True))
		print(g.node)
		print(ranks[4:9])
		print(ranks[9:14])

	def test_merge_renumber(self):

		a = nx.Graph()
		b = nx.Graph()

		a.add_edges_from([(0,1),(0,2),(1,2)])
		b.add_edges_from([(0,1),(0,2),(1,2)])

		c = integro.merge_and_renumber(a,b)
		print(len(c.edges()))
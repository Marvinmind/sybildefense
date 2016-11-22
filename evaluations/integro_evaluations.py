from sybil import integro
import networkx as nx
import random
from util import graph_creation
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

def test_random():
	g = nx.watts_strogatz_graph(2000, 40, 0.05)
	nx.set_node_attributes(g, 'label', 0)
	NUM_NODES = len(g.nodes())
	NUM_SYBIL = 100
	g_b = g.copy()

	results = []
	for i in range(1,15):
		g = g_b.copy()
		for j in range(NUM_SYBIL):
			requested = []
			for k in range(i):
				while True:
					friend = random.randint(0, NUM_NODES - 1)
					if friend not in requested:
						g.add_edge(NUM_NODES + j, friend)
						g.node[NUM_NODES + j]['label'] = 1
						break

		integro.add_apriori(g, auc=0.99, mode='hard')
		integro.set_weights_and_start_seed(g, seeds=(0,200,500), trust=NUM_NODES)
		results.append(integro.calc_auc(g))
		#ranks = stats.rankdata(integro.get_ranks(g))
		#ranks_h = ranks[0:NUM_NODES]
		#ranks_s = ranks[NUM_NODES:NUM_NODES+NUM_SYBIL]
		#print(np.median(ranks_s))

	print(results)
	plt.plot(results)
	plt.ylabel('AUC')
	plt.xlabel('Number of Attack Edges pro attacker')
	plt.show()

def test_community_detection():
	g = nx.watts_strogatz_graph(2000, 40, 0.05)
	nx.set_node_attributes(g, 'label', 0)
	NUM_NODES = len(g.nodes())
	NUM_SYBIL = 100
	g_b = g.copy()

	collect_medianrank_h = []
	collect_medianrank_c = []
	collect_medianrank_s = []

	x = np.arange(1,400,40)

	for j in range(3):
		results = []
		collect_medianrank_h_t = []
		collect_medianrank_c_t = []
		collect_medianrank_s_t = []
		for i in x:
			g = g_b.copy()

			graph_creation.add_community(g, NUM_SYBIL, i, type='honest', num_honest=NUM_NODES)
			graph_creation.add_community(g, NUM_SYBIL, i, type='sybil', num_honest=NUM_NODES)

			integro.add_apriori(g, auc=0.9, mode='soft')
			integro.set_weights_and_start_seed(g, seeds=(0, 200, 500), trust=NUM_NODES)
			#results.append(integro.calc_auc(g))
			ranks = stats.rankdata(integro.get_ranks(g))
			collect_medianrank_h_t.append(np.median(ranks[0:NUM_NODES]))
			collect_medianrank_c_t.append(np.median(ranks[NUM_NODES:NUM_NODES+NUM_SYBIL]))
			collect_medianrank_s_t.append(np.median(ranks[NUM_NODES+NUM_SYBIL:NUM_NODES+NUM_SYBIL*2]))
		collect_medianrank_h.append(collect_medianrank_h_t)
		collect_medianrank_c.append(collect_medianrank_c_t)
		collect_medianrank_s.append(collect_medianrank_s_t)

	collect_medianrank_h = np.median(np.transpose(np.array(collect_medianrank_h)),1)
	collect_medianrank_c = np.median(np.transpose(np.array(collect_medianrank_c)),1)
	collect_medianrank_s = np.median(np.transpose(np.array(collect_medianrank_s)),1)

	print(collect_medianrank_h)
	print(collect_medianrank_c)
	print(collect_medianrank_s)


	plt.plot(x, collect_medianrank_h, 'r--', x, collect_medianrank_c, 'b--', x, collect_medianrank_s,'g--')
	plt.ylabel('AUC')
	plt.xlabel('Number of Attack Edges pro attacker')
	plt.show()

def test_community_vs_random():
	g = nx.watts_strogatz_graph(2000, 40, 0.05)
	nx.set_node_attributes(g, 'label', 0)
	NUM_NODES = len(g.nodes())
	NUM_COM = 20
	NUM_SYBIL = 2
	g_b = g.copy()


	median_rank_com = []
	median_rank_sib = []
	for i in range(1, 8):
		g = g_b.copy()
		graph_creation.add_community(g, NUM_COM, 10, type='honest')
		for j in range(NUM_NODES+NUM_COM, NUM_NODES+NUM_COM+NUM_SYBIL):
			requested = []
			for k in range(i):
				while True:
					friend = random.randint(0, NUM_NODES - 1)
					if friend not in requested:
						g.add_edge(j, friend)
						g.node[j]['label'] = 1
						break
		integro.add_apriori(g, auc=0.99, mode='hard')
		integro.set_weights_and_start_seed(g, seeds=(0, 200, 500), trust=NUM_NODES)
		ranks = stats.rankdata(integro.get_ranks(g))
		median_rank_com.append(np.median(ranks[NUM_NODES:NUM_NODES+NUM_COM]))
		median_rank_sib.append(np.median(ranks[NUM_NODES+NUM_COM:NUM_NODES + NUM_COM+NUM_SYBIL]))

	print(median_rank_com)
	print(median_rank_sib)


#test_random()
#test_community_detection(type='sybil')
test_community_detection()

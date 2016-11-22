__author__ = 'Martin'

import networkx as nx
import sybil.votetrust as votetrust
import csv
from util import graph_creation
from attacks import attacks_votetrust
from collections import defaultdict
import numpy as np

def eval_random():

	results = []
	g_0 = graph_creation.create_directed_smallWorld(2000, 40)
	ATTACKER = len(g_0.nodes())

	for i in range(20):
		n = i*5+1
		results.append([n])
		for j in range(10):
			print('run')
			g = g_0.copy()
			attacks_votetrust.attack_random(g,n)

			votetrust.vote_assignment(g, [0, 500, 1000])
			votetrust.vote_propagation_mat(g,d=0.99)
			votetrust.vote_aggregation(g)
			print(len(g.nodes()))
			results[i].append(g.node[ATTACKER]['p'])

	with open('../results/votetrust/random.csv','w+') as f:
		w = csv.writer(f)
		w.writerows(results)

def most_common(mode='strict'):

	results = []
	g_0 = graph_creation.create_directed_smallWorld(2000, 40)
	nx.set_node_attributes(g_0, 'label', 0)
	for i in range(5):
		n = i*5+1
		results.append([n])
		for j in range(1):
			g = g_0.copy()
			attacks_votetrust.attack_most_common_friends(g,n,mode=mode, boosting=True, dummies=[50])
			ATTACKER = len(g.nodes())-1
			votetrust.vote_assignment(g, [0, 90, 160])
			votetrust.vote_propagation_mat(g,d=0.99)
			votetrust.vote_aggregation(g)
			results[i].append(g.node[ATTACKER]['p'])
	print(results)
	"""
	if mode=='strict':
		with open('../results/votetrust/breadthFirst_boosting.csv','w+') as f:
			w = csv.writer(f, lineterminator='\n')
			w.writerows(results)
	else:
		with open('../results/votetrust/mostCommon_boosting.csv','w+') as f:
			w = csv.writer(f, lineterminator='\n')
			w.writerows(results)
	"""

def eval_most_common_friends():

	results = []
	g_0 = graph_creation.create_directed_smallWorld(2000, 40)
	ATTACKER = len(g_0.nodes())

	for i in range(20):
		n = i*5+1
		results.append([n])
		print('run')
		for j in range(10):
			g = g_0.copy()
			attacks_votetrust.attack_most_common_friends(g,n)

			votetrust.vote_assignment(g, [0, 500, 1000])
			votetrust.vote_propagation_mat(g,d=0.99)
			votetrust.vote_aggregation(g)
			results[i].append(g.node[ATTACKER]['p'])

	with open('../results/votetrust/mostCommon.csv','w+') as f:
		w = csv.writer(f, lineterminator='\n')
		w.writerows(results)

def calc_trust_distribution():
	g = graph_creation.create_directed_smallWorld(2000, 40)

	votetrust.vote_assignment(g, [0, 500, 1000])
	d = 1-3/len(g.nodes())
	votetrust.vote_propagation_mat(g,d)
	votetrust.vote_aggregation(g)

	votes = [x[1]['vote_capacity'] for x in list(g.node.items())]

	with open('../results/votetrust/trustDist.csv','w+') as f:
		w = csv.writer(f, lineterminator='\n')
		w.writerow(votes)

def potential_capacity_per_distance():
	seeds = (0, 500, 1000,1500)
	results = []
	for d in (0.8,0.9,0.95,0.99):
		per_distance = defaultdict(list)
		for i in range(10):
			g = graph_creation.create_directed_smallWorld(2000, 40)
			votetrust.vote_assignment(g, seeds)
			votetrust.vote_propagation_mat(g,d)

			for n in g.nodes_iter():
				shortest = 1000
				for s in seeds:
					length = len(nx.shortest_path(g,s,n))-1
					if length < shortest:
						shortest = length
				per_distance[shortest].append(g.node[n]['vote_capacity']/(len(g.out_edges(n))+1))

		for key, value in per_distance.items():
			per_distance[key] = np.mean(per_distance[key])
		result_d = list(per_distance.values())
		print(result_d)
		results.append(result_d)

	with open('../results/votetrust/seed_attack_turnout.csv','w+') as f:
		w = csv.writer(f, lineterminator='\n')
		w.writerows(results)

#eval_most_common_friends()
most_common(mode='non-strict')
#eval_random()
#potential_capacity_per_distance()
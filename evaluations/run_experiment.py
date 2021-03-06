__author__ = 'Martin'
import random
import pickle
import networkx as nx
from util import calc
from util.keys import SF_Keys
from evaluations import eval_systems, parameters
from sybil import integro, sybilframe
from collections import defaultdict
import os
import numpy as np
from util import graph_creation
import time

def run_experiment(paras, saveAs, systems=None):
	if systems==None:
		print('set systems default')
		systems = ('integro', 'votetrust', 'sybilframe')

	results_list = []
	return_package = (results_list, paras)

	" set parameters "
	getAcceptance = calc.getAcceptanceClosure(paras.acceptanceRatioLimits[0], paras.acceptanceRatioLimits[1])

	getVictimNodeProb = calc.getNodeProbClosure(paras.nodeProbVictim)
	getNonVictimNodeProb = calc.getNodeProbClosure(paras.nodeProbNonVictim)

	getSybilNodeProb = calc.getNodeProbClosure(paras.nodeProbSybil)
	getNonSybilNodeProb = calc.getNodeProbClosure(paras.nodeProbNonSybil)
	getSybilEdgeProb = calc.getNodeProbClosure(paras.edgeProbSybil)
	getNonSybilEdgeProb = calc.getNodeProbClosure(paras.edgeProbNonSybil)

	"create benign region from graph"
	t = time.clock()
	if paras.graph == 'smallWorld':
		g_org = graph_creation.create_directed_smallWorld(paras.sizeSmallWorld, paras.edgesSmallWorld)

	elif paras.graph == 'newOrleans':
		g_org = nx.read_edgelist(paras.datasetLocations[paras.graph])
		g_org = nx.convert_node_labels_to_integers(g_org)
		g_org = graph_creation.undirected_to_directed(g_org)
	elif paras.graph in ('david', 'pokec', 'slashdot', 'facebook'):
		print('start reading in')
		g_org = nx.read_edgelist(paras.datasetLocations[paras.graph], 'r')
		g_org = graph_creation.undirected_to_directed(g_org)


	print('done reading in {}'.format(time.clock()-t))

	nx.set_node_attributes(g_org, 'label', 0)
	NUM_HONEST = len(g_org.nodes())
	NUM_ATTACKERS = paras.numSybils
	if paras.scenario == 'SR':
		NUM_ATTACKERS = paras.sizeSybilRegion


	for i in range(paras.numRepeats):
		g = g_org.copy()

		"set seed attributes"
		seeds = []
		if paras.seedsStrategy == 'list':
			for s in paras.seedsList:
				seeds.append(s)
		elif paras.seedsStrategy == 'random':
			for i in range(paras.numSeeds):
				while True:
					r = random.randint(0, NUM_HONEST - 1)
					if r not in seeds:
						seeds.append(r)
						break

		nx.set_node_attributes(g, 'seed', 0)
		for s in seeds:
			g.node[s]['seed'] = 1

		"add boosting region"
		if paras.boosted == 'random':
			r = []
			for i in range(paras.numDummies):
				while True:
					h = random.randint(0, NUM_HONEST - 1)
					if h not in r and h not in seeds:
						g.add_edge(h, NUM_HONEST, {'trust': 1})
						r.append(h)
						break

			g.add_edge(NUM_HONEST, NUM_HONEST + 1, {'trust': 1})
			g.add_edge(NUM_HONEST + 1, NUM_HONEST + 2, {'trust': 1})
			g.add_edge(NUM_HONEST + 2, NUM_HONEST, {'trust': 1})

			for i in range(3):
				g.node[NUM_HONEST + i]['label'] = 1
				g.node[NUM_HONEST + i]['seed'] = 0

		if paras.boosted == 'seed':
			for n, data in g.nodes_iter(data=True):
				if data['seed'] == 1:
					print('seed found')
					s = n
					break

			g.add_edge(s, NUM_HONEST, {'trust': 1})

			g.add_edge(NUM_HONEST, NUM_HONEST + 1, {'trust': 1})
			g.add_edge(NUM_HONEST + 1, NUM_HONEST + 2, {'trust': 1})
			g.add_edge(NUM_HONEST + 2, NUM_HONEST, {'trust': 1})

			for i in range(3):
				g.node[NUM_HONEST + i]['label'] = 1
				g.node[NUM_HONEST + i]['seed'] = 0

		"add sybil nodes"
		attackers = []

		"create sybil region for sybil region scenario"
		if paras.scenario == 'SR':
			g = graph_creation.add_sybil_region(g, NUM_ATTACKERS, 15)
			for i in range(NUM_HONEST, NUM_HONEST+NUM_ATTACKERS):
				attackers.append(i)
			for i in range(NUM_HONEST):
				if g.node[i]['label'] != 0:
					print("honest node labeld as sybil")

			for i in range(NUM_HONEST, NUM_HONEST+NUM_ATTACKERS):
				if g.node[i]['label'] != 1:
					print("sybil node labeld as honest")
			print(g[attackers[0]])

		elif paras.scenario == 'P':
			"create peripheral sybils (including boosting if boosting) for peripheral scenario"
			offset = 0
			if paras.boosted:
				offset = 3

			for i in range(NUM_ATTACKERS):
				g.add_node(NUM_HONEST + i + offset, {'label': 1, 'seed': 0})
				if paras.boosted:
					g.add_edge(NUM_HONEST + i + offset, NUM_HONEST, {'trust': 1})
					g.add_edge(NUM_HONEST + i + offset, NUM_HONEST + 1, {'trust': 1})
					g.add_edge(NUM_HONEST + i + offset, NUM_HONEST + 2, {'trust': 1})
				attackers.append(NUM_HONEST+offset+i)

		""" set node prob"""
		print('set node probs')
		t = time.clock()
		for i in g.nodes_iter():
			prob_victim = getNonVictimNodeProb()
			if g.node[i]['label'] == 0:
				neighbors = g.neighbors(i)
				for n in neighbors:
					if g.node[n]['label'] == 1:
						prob_victim = getVictimNodeProb()

				prob_sybil = getNonSybilNodeProb()
			else:
				prob_sybil = getSybilNodeProb()

			g.node[i]['prob_victim'] = prob_victim
			g.node[i][SF_Keys.Potential] = sybilframe.create_node_func(prob_sybil)


		print('done nodeprobs in {}'.format(time.clock() - t))

		"create customized graph for each system"
		g_integro = nx.Graph(g)

		if 'votetrust' in systems:
			print(type(g))
			g_votetrust = g.copy()

		if 'sybilframe' in systems:
			print('start creating sybilframe')
			t = time.clock()
			g_sybilframe = nx.DiGraph(g_integro)


			print('done creating sybilframe in {}'.format(time.clock()-t))

		" set edge prob for sybilframe"
		t = time.clock()
		if 'sybilframe' in systems:
			for start, end in g.edges_iter():
				if g.node[start]['label'] == g.node[end]['label']:
					prob = getNonSybilEdgeProb()
				else:
					# print('ATTACK EDGE!!')
					prob = getSybilEdgeProb()
				func = sybilframe.create_edge_func(prob)
				g_sybilframe[start][end][SF_Keys.Potential] = func
				g_sybilframe[end][start][SF_Keys.Potential] = func

		print('done edgeprobs in {}'.format(time.clock() - t))

		"set pool for breadth first"
		if paras.strategy == 'twoPhase' or paras.strategy == "breadthFirst":
			pools = defaultdict(lambda : [])

		"set vuln pools for two phase strategy"
		if paras.strategy == 'twoPhase':
			pools_vuln = defaultdict(lambda : [])
			list_vuln = []
			for i in range(paras.numVuln):
				for j in attackers:
					while True:
						r = random.randint(0, NUM_HONEST-1)
						if r not in list_vuln:
							list_vuln.append(r)
							break
					pools_vuln[j].append(r)

		"successively add attack edges"
		requested = defaultdict(lambda: [])

		"container for results"
		results = {'integro': [], 'votetrust': [], 'sybilframe': []}

		for i in range(max(paras.evalAt)+1):
			"determine if systems should be run"
			if i in paras.evalAt or (not paras.evalAt and paras.evalInterval % i == 0):
				print('eval')
				if 'integro' in systems:
					results['integro'].append(eval_systems.eval_system(g_integro, system='integro', paras=paras))
				if 'votetrust' in systems:
					results['votetrust'].append(eval_systems.eval_system(g_votetrust, system='votetrust', paras=paras))
				if 'sybilframe' in systems:
					results['sybilframe'].append(eval_systems.eval_system(g_sybilframe, system='sybilframe', paras=paras))

			"Select new victims"
			for s in attackers:
				vuln_flag = False
				h = None
				if paras.strategy in ('breadthFirst', 'twoPhase'):
					if len(pools[s]) > 0:
						h = pools[s][0]
						pools[s].remove(h)

					elif paras.strategy == 'twoPhase':
						if len(pools_vuln[s]) > 0:
							h = pools_vuln[s][0]
							pools_vuln[s].remove(h)
							vuln_flag = True

				"select random honest node if strategy is random or specific strategies are out of targeted nodes"
				if h == None:
					while True:
						h = random.randint(0, NUM_HONEST - 1)
						if (h not in requested[s]) and (h not in seeds):
							break

				if vuln_flag:
					trust = calc.getSuccessByProb(paras.vulnAcceptanceProb)

				else:
					num_common_friends = len(set(g_integro.neighbors(h)).intersection(set(g_integro.neighbors(s))))
					trust = getAcceptance(num_common_friends)

				if 'votetrust' in systems:
					g_votetrust.add_edge(s, h, {'trust': trust})

				if trust == 1:
					if paras.strategy in ('breadthFirst', 'twoPhase'):
						friends_of_friend = g_integro.neighbors(h)
						if s in friends_of_friend:
							friends_of_friend.remove(s)
						pools[s].extend(friends_of_friend)

						""" magic list conversion to remove duplicates and seeds"""
						seen = set()
						seen_add = seen.add
						pools[s] = [x for x in pools[s] if not (x in seen or seen_add(x)) and x not in requested[s]+seeds]

					g_integro.node[h]['prob_victim'] = getVictimNodeProb()
					g_integro.add_edge(s, h)

					if 'sybilframe' in systems:
						g_sybilframe.add_edge(s, h, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})
						g_sybilframe.add_edge(h, s, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})

				requested[s].append(h)
		results_list.append(results)

	if not saveAs:
		"create filename from parameters"
		filename = 'res_'
		filename += paras.strategy+'_'

		if paras.boosted == 'random':
			filename += 'boosted_'
		elif paras.boosted == 'seed':
			filename += 'boostedseed_'
		else:
			filename += 'noboost_'

		filename += '{}_'.format(paras.graph)
		"change back to paras.scenario!"
		filename += paras.scenario+'.p'
	else:
		filename = saveAs

	"save results as file"
	pickle.dump(return_package, open("../pickles/"+filename, "wb+"))




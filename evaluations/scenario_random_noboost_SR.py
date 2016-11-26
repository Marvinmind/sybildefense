__author__ = 'Martin'
import random, pickle
import networkx as nx
from util import calc, graph_creation
from util.keys import SF_Keys
from evaluations import eval_systems, parameters
from sybil import integro, sybilframe
from collections import defaultdict

from util import graph_creation

paras = parameters.ParameterSettingRealistic(maxRequests=501, evalInterval=25, graph='facebook', numRepeats=4)
" set parameters "
beta = paras.beta
d = paras.d
getAcceptance = calc.getAcceptanceClosure(paras.acceptance[0], paras.acceptance[1])

getVictimNodeProb = calc.getNodeProbClosure(paras.nodeProbVictim)
getNonVictimNodeProb = calc.getNodeProbClosure(paras.nodeProbNonVictim)

getSybilNodeProb = calc.getNodeProbClosure(paras.nodeProbSybil)
getNonSybilNodeProb = calc.getNodeProbClosure(paras.nodeProbNonSybil)
getSybilEdgeProb = calc.getNodeProbClosure(paras.edgeProbSybil)
getNonSybilEdgeProb = calc.getNodeProbClosure(paras.edgeProbNonSybil)


results_list = []
return_package = (results_list, paras)

MAX_REQUESTS = paras.maxRequests

for j in range(paras.numRepeats):

	""" createGraph and set labels"""
	if paras.graph == 'smallWorld':
		g = graph_creation.create_directed_smallWorld(paras.sizeSmallWorld, paras.edgesSmallWorld)
	elif paras.graph == 'facebook':
		g = nx.read_adjlist('/home/martin/Downloads/facebook_combined.txt')
		g = graph_creation.undirected_to_directed(g)
	nx.set_node_attributes(g, 'label', 0)
	NUM_NODES = len(g.nodes())
	graph_creation.add_community(g, paras.sizeSybilRegion, 0, type='sybil')
	NUM_SYBIL = len(g.nodes()) - NUM_NODES
	for i in range(NUM_NODES, NUM_NODES + NUM_SYBIL):
		g.node[i]['label'] = 1

	""" set seeds"""
	for i in g.nodes_iter():
		if i in paras.seeds:
			seed = 1
		else:
			seed = 0
		g.node[i]['seed'] = seed

	""" set node prob"""
	for i in g.nodes_iter():
		if g.node[i]['label'] == 0:
			prob_victim = getNonVictimNodeProb()
			prob_sybil = getNonSybilNodeProb()
		else:
			prob_victim = getVictimNodeProb()
			prob_sybil = getSybilNodeProb()

		g.node[i]['prob_victim'] = prob_victim
		g.node[i][SF_Keys.Potential] = sybilframe.create_node_func(prob_sybil)

	g_votetrust = g.copy()
	g_sybilframe = nx.DiGraph(nx.Graph(g.copy()))
	" set edge prob for sybilframe"
	for start, end in g_sybilframe.edges_iter():
		if g.node[start]['label'] == g.node[end]['label']:
			prob = getNonSybilEdgeProb()
		else:
			print('ATTACK EDGE!')
			prob = getSybilEdgeProb()
		g_sybilframe[start][end][SF_Keys.Potential] = sybilframe.create_edge_func(prob)

	g = nx.Graph(g)
	for start, end in g.edges_iter():
		if g.node[start]['label'] != g.node[end]['label']:
			print('ATTACK EDGE AFTER UNDIRECTED!')

	results = {'integro': [], 'votetrust': [], 'sybilframe': []}
	requested = []

	for i in range(MAX_REQUESTS):

		if i % paras.evalInterval == 0:
			print('run')
			results['integro'].append(eval_systems.eval_system(g, system='integro'))
			results['votetrust'].append(eval_systems.eval_system(g_votetrust, system='votetrust'))
		# results['sybilframe'].append(eval_integro.eval(g))


		while True:
			h = random.randint(0, NUM_NODES-1)
			s = random.randint(NUM_NODES, NUM_NODES+NUM_SYBIL-1)
			if (h, s) not in requested and (h,s) not in paras.seeds:
				requested.append((h, s))
				break
		num_common_friends = len(set(g.neighbors(h)).intersection(set(g.neighbors(s))))
		trust = getAcceptance(num_common_friends)

		g_votetrust.add_edge(s, h, {'trust': trust})

		if trust == 1:
			g.add_edge(s, h)
			g_sybilframe.add_edge(s, h, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})
			g_sybilframe.add_edge(h, s, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})

	results_list.append(results)
if paras.graph == 'smallWorld':
	pickle.dump(return_package, open( "../pickles/results_random_noboost_SR_sm.p", "wb+"))
elif paras.graph == 'facebook':
	pickle.dump(return_package, open("../pickles/results_random_noboost_SR_fb.p", "wb+"))



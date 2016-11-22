__author__ = 'Martin'
import random, pickle
import networkx as nx
from util import calc
from util.keys import SF_Keys
from evaluations import eval_systems
from sybil import integro, sybilframe
from collections import defaultdict

from util import graph_creation
""" set parameters """
beta = 2
d = 0.8
getAcceptance = calc.getAcceptanceClosure(0.2, 0.8)

getVictimNodeProb = calc.getNodeProbClosure(0.25)
getNonVictimNodeProb = calc.getNodeProbClosure(0.75)

getSybilNodeProb = calc.getNodeProbClosure(0.69)
getNonSybilNodeProb = calc.getNodeProbClosure(0.08)
getSybilEdgeProb = calc.getNodeProbClosure(0.18)
getNonSybilEdgeProb = calc.getNodeProbClosure(0.1)

""" createGraph and set labels"""
g = graph_creation.create_directed_smallWorld(4000, 20)
nx.set_node_attributes(g, 'label', 0)
NUM_NODES = len(g.nodes())
graph_creation.add_community(g, 100, 0, type='sybil')
NUM_SYBIL = len(g.nodes())-NUM_NODES
for i in range(NUM_NODES, NUM_NODES+NUM_SYBIL):
	g.node[i]['label'] = 1

""" set seeds"""
for i in g.nodes_iter():
	if i in (0, 2, 3):
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
print(len(g.edges()))
g_sybilframe = nx.DiGraph(nx.Graph(g.copy()))
print(len(g_sybilframe.edges()))
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
print(nx.is_connected(g))

g_back = g.copy()
g_back_sybilframe = g_sybilframe.copy()
requested = []
results_list = []

MAX_REQUESTS = 2001

for j in range(5):
	g=g_back.copy()
	g_sybilframe = g_back_sybilframe.copy()
	results = {'integro': [], 'votetrust': [], 'sybilframe': []}

	for i in range(MAX_REQUESTS):

		if i % 50 == 0:
			print('run')
			results['integro'].append(eval_systems.eval_system(g, system='integro'))
			results['votetrust'].append(eval_systems.eval_system(g_votetrust, system='votetrust'))
		# results['sybilframe'].append(eval_integro.eval(g))


		while True:
			h = random.randint(0, NUM_NODES-1)
			s = random.randint(NUM_NODES, NUM_NODES+NUM_SYBIL-1)
			if (h, s) not in requested:
				requested.append((h, s))
				break
		num_common_friends = len(set(g.neighbors(h)).intersection(set(g.neighbors(s))))
		trust = getAcceptance(num_common_friends)

		g_votetrust.add_edge(s, h, {'trust': trust})
		g_sybilframe.add_edge(s, h, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})
		g_sybilframe.add_edge(h, s, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})

		if trust == 1:
			g.add_edge(s, h)

	results_list.append(results)
pickle.dump(results_list, open( "../pickles/resultsSybilRegion.p", "wb+"))

mergeAuc = defaultdict(lambda: 0)
for e in results_list:
	for i, x in enumerate(e['integro']):
		mergeAuc[i] += x.auc/len(results_list)

print(mergeAuc)



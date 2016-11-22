__author__ = 'Martin'
import random
import pickle
import networkx as nx
from util import calc
from util.keys import SF_Keys
from evaluations import eval_systems
from sybil import integro, sybilframe
from collections import defaultdict

from util import graph_creation
""" set parameters
Parameters are set according to the following pieces of information from literature

getAcceptance: Acceptance rises from 20% to 80% according to number of common friends ("The socialbot network: when bots socialize for fame and money"

Integro:
# Nodes are considered victims if victim probability is > 0.5

getVictimNodeProb: Classifier delivered an AUC of 0.76 on Tuenti data.
getNonVictimNodeProb: ""

SybilFrame:
#Prior >0.5 means node is more likely to be benign
#EdgePrior >0.5 mean nodes are more likely to take the same label

getSybilNodeProb: Node detection yielded 9.4% FPR and 31.8% FNR

getNonSybilNodeProb:

getSybilEdgeProb:   From Twitter Evaluation: 18% attack edges detected, FP Rate of 10%

getNonSybilEdgeProb: ""
"""
if __name__=='__main__':

	beta = 2
	d = 0.8
	getAcceptance = calc.getAcceptanceClosure(0.2, 0.8)

	getVictimNodeProb = calc.getNodeProbClosure(0.25)
	getNonVictimNodeProb = calc.getNodeProbClosure(0.75)

	getSybilNodeProb = calc.getNodeProbClosure(0.69)
	getNonSybilNodeProb = calc.getNodeProbClosure(0.08)
	getSybilEdgeProb = calc.getNodeProbClosure(0.18)
	getNonSybilEdgeProb = calc.getNodeProbClosure(0.1)

	results_list = []
	for j in range(2):
		""" createGraph and set labels"""
		g = graph_creation.create_directed_smallWorld(1000, 40)
		nx.set_node_attributes(g,'label', 0)
		NUM_NODES = len(g.nodes())
		NUM_SYBILS = 10
		"""
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
		"""
		""" set 10 sybil nodes"""
		for i in range(NUM_SYBILS):
			g.add_node(NUM_NODES+i+3,{'label':1})
			g.add_edge(NUM_NODES+i+3,NUM_NODES,{'trust': 1})
			g.add_edge(NUM_NODES+i+3,NUM_NODES+1,{'trust': 1})
			g.add_edge(NUM_NODES+i+3,NUM_NODES+2,{'trust': 1})

		""" set seeds"""
		for i in g.nodes_iter():
			if i in (0,3,20):
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
			temp = sybilframe.create_node_func(prob_sybil)
			g.node[i][SF_Keys.Potential] = sybilframe.create_node_func(prob_sybil)
			#g.node[i][SF_Keys.Potential] = {1:temp(1), -1:temp(-1)}

		g_votetrust = g.copy()
		g_sybilframe = nx.DiGraph(nx.Graph(g.copy()))

		" set edge prob for sybilframe"
		for start, end in g_sybilframe.edges_iter():
			if g.node[start]['label'] == g.node[end]['label']:
				prob = getNonSybilEdgeProb()
			else:
				print('ATTACK EDGE!!')
				prob = getSybilEdgeProb()
			temp = sybilframe.create_edge_func(prob)
			g_sybilframe[start][end][SF_Keys.Potential] = sybilframe.create_edge_func(prob)
			#g_sybilframe[start][end][SF_Keys.Potential] = {(1,1): temp(1,1), (1,-1):temp(1,-1), (-1,1):temp(-1,1), (-1,-1): temp(-1,-1)}



		g = nx.Graph(g)

		requested = defaultdict(lambda :[])
		results =  {'integro':[], 'votetrust':[], 'sybilframe':[]}
		MAX_REQUESTS = 21
		select_trust = []
		pool = defaultdict(lambda: [])

		g_back = g.copy()
		g_back_sybilframe = g_sybilframe.copy()



		for i in range(MAX_REQUESTS):
			if i % 10 == 0:
				print('eval')
				results['integro'].append(eval_systems.eval_system(g, system='integro'))
				results['votetrust'].append(eval_systems.eval_system(g_votetrust, system='votetrust'))
				#results['sybilframe'].append(eval_systems.eval_system(g_sybilframe, system='sybilframe'))

			for j in range(NUM_SYBILS):
				s = NUM_NODES+j
				if len(pool[j])==0:
					while True:
						h = random.randint(0, NUM_NODES-1)
						if (s, h) not in requested:
							break
				else:
					h = pool[j][0]
					pool[j].remove(h)
				num_common_friends = len(set(g.neighbors(h)).intersection(set(g.neighbors(s))))
				trust = getAcceptance(num_common_friends)
				select_trust.append(trust)
				g_votetrust.add_edge(s, h, {'trust': trust})
				if trust == 1:
					friends_of_friend = g.neighbors(h)
					pool[j].extend(friends_of_friend)
					if s in friends_of_friend:
						friends_of_friend.remove(s)
					""" magic list conversion to remove duplicates"""
					seen = set()
					seen_add = seen.add
					pool[j] = [x for x in pool[j] if not (x in seen or seen_add(x)) and x not in requested[j]]

					g.node[h]['prob_victim'] = getVictimNodeProb()
					temp = sybilframe.create_edge_func(getSybilEdgeProb())
					#g_sybilframe.add_edge(s, h, {SF_Keys.Potential: {(1,1): temp(1,1), (1,-1):temp(1,-1), (-1,1):temp(-1,1), (-1,-1): temp(-1,-1)}})
					#g_sybilframe.add_edge(h, s, {SF_Keys.Potential: {(1,1): temp(1,1), (1,-1):temp(1,-1), (-1,1):temp(-1,1), (-1,-1): temp(-1,-1)}})

					g_sybilframe.add_edge(s, h, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})
					g_sybilframe.add_edge(h, s, {SF_Keys.Potential: sybilframe.create_edge_func(getSybilEdgeProb())})
					g.add_edge(s, h)

				requested[j].append((s, h))
		results_list.append(results)

	pickle.dump(results_list, open( "../pickles/results.p", "wb+" ) )




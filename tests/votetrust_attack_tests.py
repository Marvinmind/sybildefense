__author__ = 'Martin'
import unittest
import networkx as nx
import random
from math import floor
from attacks import generic_attacks as attacks
from util import graph_creation, keys
from sybil import votetrust
from time import clock


class VoteTrustTests(unittest.TestCase):
	def test_breadth_first(self):
		g = graph_creation.create_directed_smallWorld(2000,40)
		nx.set_node_attributes(g, 'label', 0)

		attacks.attack_most_common_friends(g, 60, mode='strict', system= keys.Systems.Votetrust)

		ATTACKER = len(g.nodes())-1
		votetrust.vote_assignment(g, [0,500,1000])
		votetrust.vote_propagation_mat(g,0.995)
		votetrust.vote_aggregation(g)

		print([(g[ATTACKER][x],g.node[x]['vote_capacity']) for x in list(g[ATTACKER].keys())])
		print(g.node[ATTACKER])
		print(sum([1 for x in list(g[ATTACKER].items()) if x[1]['trust']==1]))

	def test_random(self):
		g = graph_creation.create_directed_smallWorld(2000,40)
		nx.set_node_attributes(g, 'label', 0)


		attacks.attack_random_peripheral(g, 50, boosting=True, dummies=[200,600], system=keys.Systems.Votetrust)

		votetrust.vote_assignment(g, [0])
		votetrust.vote_propagation_mat(g)
		votetrust.vote_aggregation(g)

		ATTACKER = len(g.nodes())-1

		print(g.node[ATTACKER])
		print(g[ATTACKER])

	def test_collusion(self):
		g = graph_creation.create_directed_smallWorld(4000,40)
		r_syb = graph_creation.add_sybil_region(g, 5, 1)
		ATTACKER = len(g.nodes())

		for i in range(5):
			g.add_edge(ATTACKER, ATTACKER-i-1, {'trust':1})

		requested =  []
		for i in range(5):
			while True:
				r = floor(random.random()*(len(g.nodes())-20))
				if r not in requested:
					g.add_edge(ATTACKER, r, {'trust':-1})
					requested.append(r)
					break

		votetrust.vote_assignment(g, [0])
		votetrust.vote_propagation_mat(g, d=0.995)
		votetrust.vote_aggregation(g)

		buddies = []
		for e in g.out_edges(ATTACKER):
			buddies.append((e[1],g.node[e[1]]['vote_capacity']))
		print(buddies)
		print(g.node[ATTACKER])
		print(len(g.out_edges(r_syb)))
		print(g.node[r_syb]['vote_capacity'])




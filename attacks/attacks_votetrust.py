__author__ = 'Martin'
import util.graph_creation as graph_creation
import networkx as nx
from sybil import votetrust
from random import random
from math import floor


def attack_most_common_friends(g, MAX_REQUESTS, mode='non-strict', boosting = False, dummies=[], system='votetrust'):
	getFriends = None
	if system=='votetrust':
		getFriends = votetrust.getFriends
	elif system=='sybilframe':
		getFriends = nx.neighbors

	NUM_NODES = 0
	for i in g.nodes_iter():
		if g.node[i]['label'] == 0:
			NUM_NODES+=1

	if boosting:
		graph_creation.append_boosting_region(g, dummies)
		ATTACKER = len(g.nodes())-1
	else:
		g.add_node(NUM_NODES, {'label':1})
	ATTACKER = len(g.nodes())-1

	count = 0
	requested = []
	potentials = []

	while count < MAX_REQUESTS:
		r = 0
		max_common_friends = 0
		if len(potentials) == 0:
			while True:
				r = floor(random()*NUM_NODES)
				if r not in requested:
					break
		else:
			attacker_friends = getFriends(g, ATTACKER)
			if mode == 'strict':
				best_choice = potentials[0]
				max_common_friends = len(set(getFriends(g, best_choice)).intersection(attacker_friends))

			else:
				best_choice = None
				for p in potentials:
					num_common_friends = len(set(getFriends(g, p)).intersection(attacker_friends))
					if num_common_friends > max_common_friends:
						best_choice = p
						max_common_friends = num_common_friends
			r = best_choice
			potentials.remove(r)

		trust = votetrust.getTrustByProb(max_common_friends)
		if system=='votetrust':
			g.add_edge(ATTACKER, r, {'trust': trust})
		elif system=='sybilframe':
			if trust==1:
				g.add_edge(ATTACKER, r)
		requested.append(r)
		if trust == 1:
			if system=='votetrust':
				friends_of_friend = getFriends(g, r)
			elif system=='sybilframe':
				friends_of_friend = nx.neighbors(g, r)
			if ATTACKER in friends_of_friend:
				friends_of_friend.remove(ATTACKER)
			potentials.extend(friends_of_friend)
			seen = set()
			seen_add = seen.add
			potentials = [x for x in potentials if not (x in seen or seen_add(x)) and x not in requested]

		count += 1

def attack_random(g, MAX_REQUESTS):

	NUM_NODES = len(g.nodes())
	ATTACKER = NUM_NODES
	requested = []
	friends = []

	for i in range(MAX_REQUESTS):
		r = None
		while True:
			r = floor(random()*NUM_NODES)
			if r not in requested:
				break
		friends_r = votetrust.getFriends(g, r)
		num_common = len(set(friends).intersection(set(friends_r)))
		trust =votetrust.getTrustByProb(num_common)
		g.add_edge(ATTACKER, r, {'trust': trust})
		requested.append(r)
		if trust == 1:
			friends.append(r)

def attack_boosting_random(g, dummies,d):
	N = len(g.nodes())
	graph_creation.append_boosting_region(g, dummies)
	votetrust.vote_assignment(g, [0,500,1000])
	votetrust.vote_propagation_mat(g, d)
	print(g.node[N]['vote_capacity'])

	friends = []
	requested = []
	r = 0
	while True:
		while True:
			r = floor(random()*N)
			if r not in requested:
				requested.append(r)
				break
		trust = votetrust.getTrustByProb(0)
		if trust == 1:
			friends.append(r)
		g.add_edge(N+3, r, {'trust':trust})
		g_b = g.copy()
		votetrust.vote_aggregation(g)
		print('{},{}'.format(trust, g.node[r]['vote_capacity']))
		if g.node[N+3]['p'] < 0.5:
			break
		g = g_b
	return len(requested), friends






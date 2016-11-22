from util import keys, graph_creation, calc
import networkx as nx
from sybil import votetrust
from random import random
from math import floor



def attack_most_common_friends(g, MAX_REQUESTS, mode='non-strict', boosting = False, dummies=[], system=keys.Systems.Votetrust):
	"""
	Perfoms a most common friend attack on a network of honest nodes
	g: undirected networkx graph holding benign nodes
	mode: non-strict for most common friend attack with full graph knowledge, strict only knowledge of friends of friends
	boosting: attack will add a boosting region first if True
	dummies: list of node ids from honest graph that will have edges to the boosting region
	system: system to be used (currently supported: votetrust, sybilframe)
	"""

	""" Set get_friends function to appropriate function"""
	get_friends = None
	if system == keys.Systems.Votetrust:
		get_friends = votetrust.getFriends
	elif system == keys.Systems.Sybilframe:
		get_friends = nx.neighbors

	""" get number of  nodes """
	NUM_NODES = sum([1 for x in g.nodes_iter() if g.node[x]['label'] == 0])

	""" if boosting is append boosting region"""
	if boosting:
		graph_creation.append_boosting_region(g, dummies)
	else:
		g.add_node(NUM_NODES, {'label':1})
	ATTACKER = len(g.nodes())-1

	requested = []
	potentials = []

	for i in range(MAX_REQUESTS):
		next_request = 0
		max_common_friends = 0
		attacker_friends = []
		if len(potentials) == 0:
			while True:
				next_request = floor(random()*NUM_NODES)
				if next_request not in requested:
					break
		else:
			if mode == 'strict':
				best_choice = potentials[0]
				max_common_friends = len(set(get_friends(g, best_choice)).intersection(attacker_friends))

			else:
				best_choice = None
				for p in potentials:
					num_common_friends = len(set(get_friends(g, p)).intersection(attacker_friends))
					if num_common_friends > max_common_friends:
						best_choice = p
						max_common_friends = num_common_friends
			next_request = best_choice
			potentials.remove(next_request)

		""" is attack edge successful"""
		trust = calc.getSuccessByProb(max_common_friends)
		if system == keys.Systems.Votetrust:
			g.add_edge(ATTACKER, next_request, {'trust': int(trust)})
		elif system == keys.Systems.Sybilframe:
			if trust:
				g.add_edge(ATTACKER, next_request)
		requested.append(next_request)
		if trust:
			if system == keys.Systems.Votetrust:
				friends_of_friend = get_friends(g, next_request)
			elif system == keys.Systems.Sybilframe:
				friends_of_friend = nx.neighbors(g, next_request)
			if ATTACKER in friends_of_friend:
				friends_of_friend.remove(ATTACKER)
			potentials.extend(friends_of_friend)
			attacker_friends.append(next_request)
			""" magic list conversion to remove duplicates"""
			seen = set()
			seen_add = seen.add
			potentials = [x for x in potentials if not (x in seen or seen_add(x)) and x not in requested]


def attack_random_peripheral(g, MAX_REQUESTS, boosting = False, dummies=[], system=keys.Systems.Votetrust):
	""" Set get_friends function to appropriate function"""
	get_friends = None
	if system == keys.Systems.Votetrust:
		get_friends = votetrust.getFriends
	elif (system == keys.Systems.Sybilframe) or (system == keys.Systems.Integro):
		get_friends = nx.neighbors

	""" get number of  nodes """
	NUM_NODES = sum([1 for x in g.nodes_iter() if g.node[x]['label'] == 0])

	""" if boosting is append boosting region"""
	if boosting:
		graph_creation.append_boosting_region(g, dummies)
	else:
		g.add_node(NUM_NODES, {'label': 1})
	ATTACKER = len(g.nodes()) - 1

	requested = []
	friends = []

	for i in range(MAX_REQUESTS):
		r = None
		while True:
			r = floor(random()*NUM_NODES)
			if r not in requested:
				break
		friends_r = get_friends(g, r)
		num_common = len(set(friends).intersection(set(friends_r)))
		trust = calc.getSuccessByProb(num_common)
		g.add_edge(ATTACKER, r)

		if system == keys.Systems.Votetrust:
			g[ATTACKER][r]['trust'] = int(trust)

		requested.append(r)
		if trust:
			friends.append(r)

attack_random_SR(g, MAX_REQUESTS, )
__author__ = 'Martin'

import timeit
from sybil import votetrust
from util import graph_creation

g = graph_creation.create_directed_smallWorld(2000, 40)
votetrust.vote_assignment(g, [0,500,1000])
d = 1-3/(len(g.nodes()))
def runVoteAssignment():
	votetrust.vote_propagation(g,d)
print(timeit.Timer(runVoteAssignment).timeit(number=1))
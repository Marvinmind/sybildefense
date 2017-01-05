from sybil import integro, votetrust, sybilframe
from scipy import stats
import numpy as np
from evaluations import benchmarks
import time


def eval_system(g, system=None, paras=None):
	seeds = []
	for i in g.nodes_iter():
		if g.node[i]['seed'] == 1:
			seeds.append(i)

	if system == 'integro':
		ranks = integro.run_integro(g, seeds=seeds)

	elif system == 'votetrust':
		votetrust.vote_assignment(g, seeds)
		ranks = votetrust.vote_combined(g, paras.d)

	elif system == 'sybilframe':
		t = time.clock()
		sybilframe.inferPosteriorsEdgeImproveNew(g)
		ranks = sybilframe.getRanks(g)
		print(time.clock()-t)
		print(ranks)
		sybilframe.inferPosteriorsEdgeImprove(g)
		ranks = sybilframe.getRanks(g)
		print(ranks)

	real = [g.node[i]['label'] for i in g.nodes_iter()]
	b = benchmarks.Benchmarks(real, ranks)

	return b
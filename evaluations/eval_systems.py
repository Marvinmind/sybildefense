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
		t = time.clock()
		ranks = integro.run_integro(g, seeds=seeds)
		print('eval time total integro {}'.format(time.clock() - t))

	elif system == 'votetrust':
		t = time.clock()
		votetrust.vote_assignment(g, seeds)
		ranks = votetrust.vote_combined(g, paras.d)
		print('eval time total votetrust {}'.format(time.clock()-t))

	elif system == 'sybilframe':
		t = time.clock()
		sybilframe.inferPosteriorsEdgeImproveNew(g)
		ranks = sybilframe.getRanks(g)
		print('eval time total sybilframe {}'.format(time.clock()-t))


	real = [g.node[i]['label'] for i in range(len(g.nodes()))]
	b = benchmarks.Benchmarks(real, ranks)

	return b
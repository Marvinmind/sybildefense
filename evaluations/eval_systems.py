from sybil import integro, votetrust, sybilframe
from scipy import stats
from evaluations import benchmarks


def eval_system(g, system=None):
	seeds = []
	for i in g.nodes_iter():
		if g.node[i]['seed'] == 1:
			seeds.append(i)

	if system == 'integro':
		g_temp = g.copy()
		integro.set_weights_and_start_seed(g_temp, seeds=seeds, trust=len(g.nodes()))
		ranks = integro.get_ranks(g_temp)

	elif system == 'votetrust':
		votetrust.vote_assignment(g, seeds)
		votetrust.vote_propagation_mat(g, d=0.99)
		votetrust.vote_aggregation(g)
		ranks = votetrust.getRanks(g)

	elif system == 'sybilframe':
		sybilframe.inferPosteriorsEdgeImprove(g)
		ranks = sybilframe.getRanks(g)

	real = [g.node[i]['label'] for i in g.nodes_iter()]
	b = benchmarks.Benchmarks(real, ranks)
	g_stripped = g.copy()

	for n in g_stripped.nodes_iter():
		attr = tuple(g_stripped.node[n].keys())
		for k in attr:
			if k not in ('label', 'sublabel'):
				del g_stripped.node[n][k]

	for x, y in g_stripped.edges_iter():
		attr = tuple(g_stripped[x][y].keys())
		for k in attr:
			del g_stripped[x][y][k]

	#b.graph = g_stripped
	return b
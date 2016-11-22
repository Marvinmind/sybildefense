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
		print(sum([g_temp[x][y]['weight'] for (x,y) in g_temp.edges_iter() if g_temp.node[x]['label']!=g_temp.node[y]['label']])/len([x for (x,y) in g_temp.edges_iter() if g_temp.node[x]['label']!=g_temp.node[y]['label']]))
		print(sum([g_temp[x][y]['weight'] for (x,y) in g_temp.edges_iter() if g_temp.node[x]['label']==g_temp.node[y]['label']])/len([x for (x,y) in g_temp.edges_iter() if g_temp.node[x]['label']==g_temp.node[y]['label']]))

		ranks = integro.get_ranks(g_temp)

	elif system == 'votetrust':
		votetrust.vote_assignment(g, seeds)
		votetrust.vote_propagation_mat(g, d=0.99)
		votetrust.vote_aggregation(g)
		ranks = votetrust.getRanks(g)

	elif system == 'sybilframe':
		sybilframe.inferPosteriorsParallel(g)
		ranks = sybilframe.getRanks(g)

	real = [g.node[i]['label'] for i in g.nodes_iter()]
	return benchmarks.Benchmarks(real, ranks)


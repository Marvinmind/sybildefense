from evaluations import parameters
from evaluations.run_experiment import run_experiment

#warnings.filterwarnings('error')


"""
	Experiment:
	Determine the Influence of the Sybil Edge Classifier on Sybilframe

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	FP: 0.1,
	FN: 0.1, 0.3, 0.5, 0.6


"""

graph = 'facebook'
for i in (0.1, 0.3, 0.6, 0.81):
	for j in (0.1, 0.32, 0.6, 0.8):
		paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=False, evalAt=(50,), numRepeats=3)
		paras.edgeProbSybil = 1-i
		paras.edgeProbNonSybil = 0.1

		paras.nodeProbSybil = 1-j
		paras.nodeProbNonSybil = 0.1
		paras.numSeeds = 100
		run_experiment(paras, saveAs='./sybilEdgeProb/sybilEdgeProb{}PTar{}_node{}_edge{}.p'.format(i, graph, paras.nodeProbSybil, paras.edgeProbSybil), systems=('sybilframe',))
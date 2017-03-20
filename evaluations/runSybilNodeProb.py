from evaluations import parameters
from evaluations.run_experiment import run_experiment
"""
	Experiment:
	Determine the Influence of the Sybil Node Classifier on Sybilframe

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	FN = FP: 0.1, 0.2, 0.4

	Yes, large node priors indicate BENIGN labels

"""

evalIntervals = (1,5,10,15,20,25,30,35,40,45,50)
graph = 'slashdot'

for i in (0.1, 0.3, 0.6, 0.8):
	paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=False, evalAt=evalIntervals, numRepeats=1)
	paras.nodeProbSybil = 1-i
	paras.nodeProbNonSybil = 0.1
	paras.edgeProbSybil = 0.8
	paras.edgeProbNonSybil = 0.2

	paras.numSeeds = 100

	run_experiment(paras, saveAs='./sybilNodeProb/sybilNodeProb{}PTar{}.p'.format(i, graph), systems=('sybilframe',))
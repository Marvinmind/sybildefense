from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the Influence of the Sybil Edge Classifier on Sybilframe

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	FP: 0.1,
	FN: 0.1, 0.3, 0.5, 0.6


"""


for i in (0.1, 0.3, 0.5, 0.6):
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=(50,), numRepeats=3)
	paras.edgeProbSybil = 1-i
	paras.edgeProbNonSybil = i
	paras.numSeeds = 100
	run_experiment(paras, saveAs='./sybilEdgeProb/sybilEdgeProb{}PRand.p'.format(i), systems=('sybilframe',))
from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the Influence of the Sybil Edge Classifier on Sybilframe

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	FN = FP: 0.1, 0.2, 0.4


"""


for i in (0.1, 0.2, 0.4):
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='random', boosted=True, evalAt=(50,), numRepeats=3)
	paras.edgeProbSybil = 1-i
	paras.edgeProbNonSybil = i
	paras.numSeeds = 100
	run_experiment(paras, saveAs='./sybilEdgeProb/sybilEdgeProb{}PRand.p'.format(i), systems=('sybilframe',))
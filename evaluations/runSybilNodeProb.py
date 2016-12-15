from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the Influence of the Sybil Node Classifier on Sybilframe

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	FN = FP: 0.1, 0.2, 0.4


"""


for i in (0.1, 0.2, 0.4):
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='random', boosted=True, evalAt=(50,), maxRequests=51, numRepeats=3)
	paras.nodeProbSybil = 1-i
	paras.nodeProbNonSybil = i
	paras.numSeeds = 100
	run_experiment(paras, saveAs='./sybilNodeProb/sybilNodeProb{}PRand.p'.format(i), systems=('sybilframe',))
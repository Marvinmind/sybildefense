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


for i in (0.1,):
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=(50,), numRepeats=3)
	paras.nodeProbSybil = 1-i
	paras.nodeProbNonSybil = 0.1
	paras.numSeeds = 100
	"Not usual setting"
	paras.edgeProbSybil = 0.6
	run_experiment(paras, saveAs='./sybilNodeProb/sybilNodeProb{}PTar{}.p'.format(i,paras.edgeProbSybil), systems=('sybilframe',))
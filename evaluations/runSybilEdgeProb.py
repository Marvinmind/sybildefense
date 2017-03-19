from evaluations import parameters
from evaluations.run_experiment import run_experiment
import warnings

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
for i in (0.1, 0.3, 0.6, 0.82):
	print(i)
	paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=False, evalAt=(50,), numRepeats=5)
	paras.edgeProbSybil = 1-i
	paras.edgeProbNonSybil = 0.1
	paras.numSeeds = 100
	run_experiment(paras, saveAs='./sybilEdgeProb/sybilEdgeProb{}PTar{}.p'.format(i, graph), systems=('sybilframe',))
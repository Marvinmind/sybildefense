from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the Influence of the D parameter on the performance of Votetrust

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	d=0.8, 0.9, 0.95,  0.99, 0.999
"""


boosttype = 'random'
graph ='facebook'

for i in (0.8, 0.99, 0.999):
	paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=boosttype, evalAt=(50,), numRepeats=3)
	paras.d = i
	paras.numSeeds = 100
	run_experiment(paras, saveAs='./d/d{}PTar_{}_{}.p'.format(i, boosttype, graph), systems=('votetrust',))
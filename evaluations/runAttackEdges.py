from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the success rate influences the performance

	Variations:
	Success Rate:
		0.2 - 0.8
		0.1 - 0.5

	Systems:
	All Systems, all scenarios

"""

graph = 'facebook'
evalIntervals = (5,10,20,30,40,50,60,70,80,90,100)

"""
paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=True, evalAt=evalIntervals, numRepeats=3)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPTar.p')

paras = parameters.ParameterSettingsP(graph=graph, strategy='random', boosted=False, evalAt=evalIntervals, numRepeats=3)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPRand.p')

paras = parameters.ParameterSettingsSR(graph=graph, evalAt=evalIntervals, numRepeats=3)
run_experiment(paras, saveAs='./attackEdges/attackEdgesSRRand.p')

"""
paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=False, evalAt=evalIntervals, numRepeats=3)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPTarNoboost.p')

paras = parameters.ParameterSettingsP(graph=graph, strategy='twoPhase', boosted=False, evalAt=evalIntervals, numRepeats=3)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPTwoPhase.p')


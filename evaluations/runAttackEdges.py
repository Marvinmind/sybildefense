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

graph = 'slashdot'
num_repeats = 3
evalIntervals = (5,10,20,30,40,50,60,70,80,90,100)

#paras = parameters.ParameterSettingsSR(graph=graph, strategy='breadthFirst', evalAt=evalIntervals, numRepeats=num_repeats)
#run_experiment(paras, saveAs='./attackEdges/attackEdgesSRTar{}.p'.format(graph))

paras = parameters.ParameterSettingsSR(graph=graph, evalAt=evalIntervals, numRepeats=num_repeats)
run_experiment(paras, saveAs='./attackEdges/attackEdgesSRRand{}.p'.format(graph))
"""
paras = parameters.ParameterSettingsP(graph=graph, strategy='random', boosted=False, evalAt=evalIntervals, numRepeats=num_repeats)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPRand{}.p'.format(graph))

paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted=False, evalAt=evalIntervals, numRepeats=num_repeats)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPTarNoboost{}.p'.format(graph))

paras = parameters.ParameterSettingsP(graph=graph, strategy='breadthFirst', boosted='random', evalAt=evalIntervals, numRepeats=num_repeats)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPTar{}.p'.format(graph))

paras = parameters.ParameterSettingsP(graph=graph, strategy='twoPhase', boosted='random', evalAt=evalIntervals, numRepeats=num_repeats)
run_experiment(paras, saveAs='./attackEdges/attackEdgesPTwoPhase{}.p'.format(graph))
"""
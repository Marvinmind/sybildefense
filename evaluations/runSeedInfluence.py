from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine how the number of seeds influences the performance

	Variations:
	Number of seeds: 1, 3, 10, 100, 1000

	Systems:
	All Systems, all scenarios

"""
for i in (1, 3, 10, 100, 1000):
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=True, evalAt=(50,), maxRequests=51, numRepeats=3)
	paras.numSeeds = i
	run_experiment(paras, saveAs='seeds{}PTar.p'.format(i))

	paras = parameters.ParameterSettingsP(graph='facebook', strategy='random', boosted=False, evalAt=(50,), maxRequests=51, numRepeats=3)
	paras.numSeeds = i
	run_experiment(paras, saveAs='seeds{}PRand.p'.format(i))

	paras = parameters.ParameterSettingsSR(graph='facebook', evalAt=(50,), maxRequests=51, numRepeats=3)
	paras.numSeeds = i
	run_experiment(paras, saveAs='seeds{}SRRand.p'.format(i))



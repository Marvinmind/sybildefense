from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the Influence of the Victim Classifier's performance on the performance of Integro

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	d=0.8, 0.9, 0.95,  0.99, 0.999


"""

for i in (0.1, 0.2, 0.4):
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='random', boosted=True, evalAt=(50,), maxRequests=51, numRepeats=3)
	paras.nodeProbNonVictim = 1-i
	paras.nodeProbVictim = i
	paras.numSeeds = 100
	run_experiment(paras, saveAs='./victimProb/victimProb{}PRand.p'.format(i), systems=('integro',))
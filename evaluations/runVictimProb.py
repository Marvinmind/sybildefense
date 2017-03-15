from evaluations import parameters
from evaluations.run_experiment import run_experiment

"""
	Experiment:
	Determine the Influence of the Victim Classifier's performance on the performance of Integro

	System:
	Votetrust Targeted Breadth First

	Set of variations:
	d=0.8, 0.9, 0.95,  0.99, 0.99

"""

numRepeats = 1
evalInt = (1, 20, 50)

for i in (0.1, 0.2, 0.4):
	paras = parameters.ParameterSettingsSR(graph='facebook', strategy='breadthFirst', evalAt=evalInt, numRepeats=numRepeats)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}SRTar.p'.format(i), systems=('integro',))

	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=evalInt, numRepeats=numRepeats)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}PTar.p'.format(i), systems=('integro',))


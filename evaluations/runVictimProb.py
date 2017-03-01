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

numRepeats =5

for i in (0.1, 0.2, 0.4):
	for evalAt in (50, 20, 1):
		paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=(evalAt,), numRepeats=numRepeats)
		paras.nodeProbNonVictim = 0.9
		paras.nodeProbVictim = i
		run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}PTar.p'.format(i, evalAt), systems=('integro',))

		paras = parameters.ParameterSettingsSR(graph='facebook', strategy='breadthFirst', evalAt=(evalAt,), numRepeats=numRepeats)
		paras.nodeProbNonVictim = 0.9
		paras.nodeProbVictim = i
		run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}SRTar.p'.format(i, evalAt), systems=('integro',))

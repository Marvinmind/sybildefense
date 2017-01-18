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

for i in (0.1, 0.2, 0.4):

	evalAt = 50
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=(evalAt,), numRepeats=3)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}PTar.p'.format(i, evalAt), systems=('integro',))

	paras = parameters.ParameterSettingsSR(graph='facebook', evalAt=(evalAt,), numRepeats=3)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}SRRand.p'.format(i, evalAt), systems=('integro',))


	evalAt = 20
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=(evalAt,), numRepeats=3)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}PTar.p'.format(i, evalAt), systems=('integro',))

	paras = parameters.ParameterSettingsSR(graph='facebook', evalAt=(evalAt,), numRepeats=3)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}SRRand.p'.format(i,evalAt), systems=('integro',))

	evalAt = 1
	paras = parameters.ParameterSettingsP(graph='facebook', strategy='breadthFirst', boosted=False, evalAt=(evalAt,),numRepeats=3)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}PTar.p'.format(i, evalAt), systems=('integro',))

	paras = parameters.ParameterSettingsSR(graph='facebook', evalAt=(evalAt,), numRepeats=3)
	paras.nodeProbNonVictim = 0.9
	paras.nodeProbVictim = i
	run_experiment(paras, saveAs='./victimProb/victimProb{}eval{}SRRand.p'.format(i, evalAt), systems=('integro',))


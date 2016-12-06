__author__ = 'Martin'
import json

class ParameterSettingRealistic():
	def __init__(self, d=0.99, beta=2,acceptance=(0.2,0.8), nodeProbVictim=0.2, nodeProbNonVictim=0.8, nodeProbSybil=0.8, nodeProbNonSybil=0.2, edgeProbSybil=0.8, edgeProbNonSybil=0.2, sizeSmallWorld=4000, sizeSybilRegion=100, edgesSmallWorld=40, numSybils= 10, numRepeats=15, seeds=(0,1000, 1500,2000), maxRequests=51, evalInterval=2, graph='smallWorld'):
		self.d=d
		self.beta=beta
		self.acceptance=acceptance
		self.nodeProbVictim=nodeProbVictim
		self.nodeProbNonVictim=nodeProbNonVictim
		self.nodeProbSybil=nodeProbSybil
		self.nodeProbNonSybil=nodeProbNonSybil
		self.edgeProbSybil=edgeProbSybil
		self.edgeProbNonSybil=edgeProbNonSybil
		self.sizeSmallWorld=sizeSmallWorld
		self.sizeSybilRegion=sizeSybilRegion
		self.edgesSmallWorld=edgesSmallWorld
		self.numSybils= numSybils
		self.numRepeats=numRepeats
		self.seeds=seeds
		self.maxRequests = maxRequests
		self.evalInterval = evalInterval
		self.graph = graph

class ParameterSettings():
	def __init__(self):
		base = json.load(open('baseparameters.json', 'r'))

		self.d = base['d']
		self.beta = base['beta']
		self.acceptanceRatioLimits = base['acceptanceRatioLimits']
		self.nodeProbVictim = base['nodeProbVictim']
		self.nodeProbNonVictim = base['nodeProbNonVictim']
		self.nodeProbSybil = base['nodeProbSybil']
		self.nodeProbNonSybil = base['nodeProbNonSybil']
		self.edgeProbSybil = base['edgeProbSybil']
		self.edgeProbNonSybil = base['edgeProbNonSybil']
		self.seedsList = base['seedsList']
		self.seedStrategy = base['seedStrategy']

class ParameterSettingsSR(ParameterSettings):
	def __init__(self, maxRequests = 501, numIter=5, evalInterval=20, evalAt=False, graph='facebook', sizeSybilRegion = 100):
		super(ParameterSettingsSR, self).__init__()

		self.scenario = 'SR'
		self.sizeSybilRegion = sizeSybilRegion
		self.maxRequests = maxRequests
		self.numIter = numIter
		self.evalInterval = evalInterval
		self.evalAt = evalAt
		self.graph = graph


class ParameterSettingsP(ParameterSettings):
	def __init__(self, maxRequests=51, numIter=5, evalInterval=2, evalAt=False, graph='facebook', strategy='random', boosted='False'):
		super(ParameterSettingsSR, self).__init__()

		paras = json.load(open('srparameters.json', 'r'))
		self.scenario = 'SR'
		self.sizeSybilRegion = paras['sizeSybilRegion']
		self.maxRequests = maxRequests
		self.numIter = numIter
		self.evalInterval = evalInterval
		self.evalAt = evalAt
		self.graph = graph
		self.strategy = strategy
		self.boosted = boosted


p = json.load(open('parameters.json'))
print(type(p))
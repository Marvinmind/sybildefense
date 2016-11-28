__author__ = 'Martin'
class ParameterSettingRealistic():
	def __init__(self, d=0.99, beta=2,acceptance=(0.2,0.8), nodeProbVictim=0.2, nodeProbNonVictim=0.8, nodeProbSybil=0.69, nodeProbNonSybil=0.08, edgeProbSybil=0.18, edgeProbNonSybil=0.1, sizeSmallWorld=4000, sizeSybilRegion=100, edgesSmallWorld=40, numSybils= 10, numRepeats=15, seeds=(0,1000, 1500,2000), maxRequests=51, evalInterval=2, graph='smallWorld'):
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
import unittest
from util import calc
from sklearn import metrics
import numpy as np

class ProbTests(unittest.TestCase):
	def test_nodeProb(self):
		func = calc.getNodeProbClosure(0.25)
		res = []
		for i in range(100000):
			res.append(func())

		res = [round(x) for x in res]
		print(sum(res))

	def test_acceptance_closure(self):
		func = calc.getAcceptanceClosure(0.2,0.8)
		res = []
		for i in range(10000):
			res.append(func(4))
		print(sum(res))

	def test_auc(self):
		real = [0]*20
		real.extend([1]*20)
		pred = [0.999999]*20
		pred.extend([1]*20)
		print(metrics.roc_auc_score(real, pred))

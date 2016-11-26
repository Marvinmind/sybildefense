__author__ = 'Martin'
from util import calc
from sklearn import metrics
import numpy as np

class Benchmarks():
	def __init__(self, real, predValues):
		"""invert ranks.
		ranks are expected to have high values for benign node and low for sybils.
		ROC AUC expects the opposite. 1 - predValue inverses the order
		"""

		self.real = real
		self.ranks = predValues
		predValues = 1 - predValues
		self.auc = metrics.roc_auc_score(np.array(real), predValues)
		predLabels = [round(x) for x in predValues]
		mat =  metrics.confusion_matrix(real, predLabels)
		self.FN = mat[1,0]
		self.FP = mat[0,1]
import pickle
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
from util.calc import get_cdf, getMergedRanks, getMergedAuc
import numpy as np


graph = 'facebook'
sys = 'sybilframe'

for enu, i in enumerate((0.1, 0.3, 0.4, 0.6)):
	perTarAll = pickle.load(open('../pickles/sybilNodeProb/sybilNodeProb{}PTar.p'.format(i, graph), 'rb'))
	perTar = perTarAll[0]
	paras = perTarAll[1]
	perTarAuc = getMergedAuc(perTar)
	print(list(perTarAuc['sybilframe'].values()))
	ranksPerTar = getMergedRanks(perTar)

	""" plot random per"""

	x_h = sorted(ranksPerTar[sys][0][:-(paras.numSybils)])
	x_s = sorted(ranksPerTar[sys][0][-(paras.numSybils):])

	print(x_h)
	plt.boxplot(x_h)
	plt.show()
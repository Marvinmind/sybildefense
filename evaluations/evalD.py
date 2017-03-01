import pickle
from collections import defaultdict
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
import numpy as np
from util import setMatplotlib
from util.calc import get_cdf, getMergedRanks
from baseparameters import paras as pathParas

graph = 'facebook'
boosttype = 'seed'

for sys in ('votetrust', ):
	f, axarr = plt.subplots(1, 3, figsize = (6,2))
	f.suptitle('Influence of \'d\' Factor on Votetrust - {} Boosted Scenario'.format(boosttype.capitalize()), weight='bold')

	for enu, i in enumerate((0.8, 0.99, 0.999)):
		perTarAll = pickle.load(open('../pickles/d/d{}PTar_{}_{}.p'.format(i, boosttype, graph), 'rb'))
		perTar = perTarAll[0]
		paras = perTarAll[1]

		ranksPerTar = getMergedRanks(perTar)

		print(paras.numSybils)

		""" plot random per"""

		x_h = sorted(ranksPerTar[sys][0][:-(paras.numSybils)])
		x_s = sorted(ranksPerTar[sys][0][-(paras.numSybils):])

		scaler = prep.MinMaxScaler()
		scaler.fit(sorted(ranksPerTar[sys][0]))

		x_h = scaler.transform(x_h)
		x_s = scaler.transform(x_s)


		y_h = get_cdf(x_h)
		y_s = get_cdf(x_s)


		axarr[enu].set_ylim((0, 1.1))
		axarr[enu].set_xlim((-0.1, 1.1))
		axarr[enu].set_title('d='+str(i))


		axarr[enu].plot(x_s, y_s, 'r--', label='Sybil')
		axarr[enu].plot(x_h, y_h, 'b--', label='Honest')
axarr[2].legend(bbox_to_anchor=(0,1), loc='upper left')

plt.tight_layout()

plt.subplots_adjust(top=0.8)
plt.savefig((pathParas['figuresPath']+'/d_{}_{}_{}.pdf').format(boosttype, graph, paras.numSeeds), type='pdf')
#plt.show()
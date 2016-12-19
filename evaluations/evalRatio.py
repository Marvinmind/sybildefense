import pickle
from collections import defaultdict
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
import numpy as np
from util.calc import get_cdf, getMergedRanks
from util import setMatplotlib
graph = 'facebook'


for sys in ('integro', 'votetrust', 'sybilframe'):
	f, axarr = plt.subplots(2, 2)
	f.suptitle('Influence of Acceptance Ratio: '+sys, weight='bold')
	for enu, i in enumerate(((0.2,0.7),(0.1, 0.5))):
		perTar = pickle.load(open('../pickles/ratio/ratio{}PTar.p'.format(i),'rb'))[0]
		perRand = pickle.load(open('../pickles/ratio/ratio{}PRand.p'.format(i),'rb'))[0]
		sr = pickle.load(open('../pickles/ratio/ratio{}SRRand.p'.format(i),'rb'))[0]

		paras = pickle.load(open('../pickles/ratio/ratio{}SRRand.p'.format(i),'rb'))[1]

		ranksPerTar = getMergedRanks(perTar)
		ranksPerRand = getMergedRanks(perRand)
		ranksSR = getMergedRanks(sr)

		print(paras.numSybils)
		print(ranksPerTar[sys])
		"plot tar boosted"
		x_h = sorted(ranksPerTar[sys][0][:-(paras.numSybils)+3])
		x_s = sorted(ranksPerTar[sys][0][-(paras.numSybils)+3:])

		scaler = prep.MinMaxScaler()
		scaler.fit(sorted(ranksPerTar[sys][0]))
		x_h = scaler.transform(x_h)
		x_s = scaler.transform(x_s)

		y_h = get_cdf(x_h)
		y_s = get_cdf(x_s)

		axarr[0,enu].set_ylim((0,1.1))
		axarr[0,enu].set_xlim((-0.1,1.1))

		axarr[0,enu].plot(x_s, y_s, 'r--', label='Sybil Nodes')
		axarr[0,enu].plot(x_h, y_h, 'b--', label='Honest Nodes')


		""" plot random per"""

		x_h = sorted(ranksPerRand[sys][0][:-(paras.numSybils)])
		x_s = sorted(ranksPerRand[sys][0][-(paras.numSybils):])

		scaler = prep.MinMaxScaler()
		scaler.fit(sorted(ranksPerRand[sys][0]))

		x_h = scaler.transform(x_h)
		x_s = scaler.transform(x_s)


		y_h = get_cdf(x_h)
		y_s = get_cdf(x_s)


		axarr[1,enu].set_ylim((0, 1.1))
		axarr[1,enu].set_xlim((-0.1, 1.1))


		axarr[1,enu].plot(x_s, y_s, 'r--')
		axarr[1,enu].plot(x_h, y_h, 'b--')

		""" plot SR"""
		"""
		x_h = sorted(ranksSR[sys][0][:-(paras.numSybils)])
		x_s = sorted(ranksSR[sys][0][-(paras.numSybils):])


		scaler = prep.MinMaxScaler()
		scaler.fit(sorted(ranksSR[sys][0]))

		x_h = scaler.transform(x_h)
		x_s = scaler.transform(x_s)

		y_h = get_cdf(x_h)
		y_s = get_cdf(x_s)

		axarr[2, enu].set_ylim((0,1.1))
		axarr[2, enu].set_xlim((-0.1,1.1))


		axarr[2, enu].plot(x_s, y_s, 'r--', label='sybil')
		axarr[2, enu].plot(x_h, y_h, 'b--', label='honest')
		"""
		axarr[0, enu].set_title('Ratio Limits: '+str(i))

	pad = 3
	rows = ['Peripheral\nTargeted', 'Peripheral\nRandom', 'Sybil Region\nRandom']
	for ax, row in zip(axarr[:,0], rows):
		ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0), xycoords=ax.yaxis.label, textcoords='offset points', size='x-large', ha='right', va='center')

	axarr[0, 0].legend(loc=(0.05, 0.8))
plt.show()
import pickle
from collections import defaultdict
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
import numpy as np
from util.calc import get_cdf, getMergedRanks
from util import setMatplotlib
graph = 'facebook'

f, axarr = plt.subplots(3, 2, sharey=True, sharex=True, figsize=(3.5, 5))
f.suptitle('Influence of Acceptance Ratio', weight='bold')

for j, sys in enumerate(('integro', 'votetrust', 'sybilframe')):
	for enu, i in enumerate(((0.2,0.7),(0.1, 0.5))):
		perTar = pickle.load(open('../pickles/ratio/ratio{}PTar.p'.format(i),'rb'))[0]
		paras = pickle.load(open('../pickles/ratio/ratio{}SRRand.p'.format(i),'rb'))[1]
		ranksPerTar = getMergedRanks(perTar)
		print(paras.numSybils)
		print(ranksPerTar[sys])

		"plot tar"
		x_h = sorted(ranksPerTar[sys][0][:-(paras.numSybils)+3])
		x_s = sorted(ranksPerTar[sys][0][-(paras.numSybils)+3:])

		scaler = prep.MinMaxScaler()
		scaler.fit(sorted(ranksPerTar[sys][0]))
		x_h = scaler.transform(x_h)
		x_s = scaler.transform(x_s)

		y_h = get_cdf(x_h)
		y_s = get_cdf(x_s)

		axarr[j, enu].set_ylim((0,1.1))
		axarr[j, enu].set_xlim((-0.1,1.1))

		axarr[j, enu].plot(x_s, y_s, 'r--', label='Sybil Nodes')
		axarr[j, enu].plot(x_h, y_h, 'b--', label='Honest Nodes')

		axarr[0, enu].set_title('Ratio Limits: ' + str(i))

	axarr[j, 0].set_ylabel(sys)
	"""
	pad = 3
	rows = ['Peripheral\nTargeted', 'Peripheral\nRandom', 'Sybil Region\nRandom']
	ax = axarr[j,0]
	ax.annotate(sys, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0), xycoords=ax.yaxis.label, textcoords='offset points', ha='right', va='center')
	"""
#plt.tight_layout()
axarr[2, 0].legend(loc=(0.05, 0.7), borderpad=0.2)
plt.savefig('/home/martin/Dropbox/MasterGöttingen/Masterarbeit/figures/AcceptanceRatio.png', format='png')
import pickle
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
from util.calc import get_cdf, getMergedRanks
from util import setMatplotlib

graph = 'facebook'
sys = 'sybilframe'

f, axarr = plt.subplots(4, 1, figsize=(3.5, 6), sharex=True)
f.suptitle('Sybilframe Edge Prior Influence', weight='bold')

for enu, i in enumerate((0.1, 0.3, 0.5, 0.6)):
	perTarAll = pickle.load(open('../pickles/sybilEdgeProb/sybilEdgeProb{}PTar.p'.format(i), 'rb'))
	perTar = perTarAll[0]
	paras = perTarAll[1]

	ranksPerTar = getMergedRanks(perTar)

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
	axarr[enu].set_ylabel('FN='+str(i))

	axarr[enu].plot(x_h, y_h, 'b--', label='Honest')
	axarr[enu].plot(x_s, y_s, 'r--', label='Sybil')

axarr[3].legend(loc='upper left')
plt.tight_layout()
plt.subplots_adjust(top=0.94)
plt.savefig('/home/martin/Dropbox/MasterGöttingen/Masterarbeit/figures/EdgeProb.png', format='png', dpi=900)
#plt.show()
import pickle
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
from util.calc import get_cdf, getMergedRanks
from util import setMatplotlib

graph = 'facebook'
sys = 'sybilframe'

f, axarr = plt.subplots(2, 2, figsize=(3.5, 3.5), sharex=True, sharey=True)
f.suptitle('Sybilframe Edge Prior Influence')

for enu, i in enumerate((0.1, 0.3, 0.5, 0.6)):
	perTarAll = pickle.load(open('../pickles/sybilEdgeProb/sybilEdgeProb{}PTar{}.p'.format(i, graph), 'rb'))
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

	ind_row = lambda enu: 0 if enu in (0,1) else 1
	ind_col = lambda enu: 0 if enu in (0, 2) else 1

	axis = axarr[ind_row(enu)][ind_col(enu)]
	axis.set_ylim((0, 1.1))
	axis.set_xlim((-0.1, 1.1))
	axis.set_ylabel('FN='+str(i))

	axis.plot(x_h, y_h, 'b--', label='Honest')
	axis.plot(x_s, y_s, 'r--', label='Sybil')

axis.legend(loc='upper left')
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig('/home/martin/Dropbox/MasterGöttingen/Masterarbeit/figures/EdgeProb{}.pdf'.format(graph), format='pdf')
#plt.show()
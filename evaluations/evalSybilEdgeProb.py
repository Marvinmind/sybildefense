import pickle
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
from util.calc import get_cdf, getMergedRanks

graph = 'facebook'


for sys in ('sybilframe', ):
	f, axarr = plt.subplots(1, 3)
	f.suptitle('Sybilframe Edge Prior Influence - - Peripheral Random', fontsize=14, weight='bold')

	for enu, i in enumerate((0.1, 0.2, 0.4)):
		perTarAll = pickle.load(open('../pickles/sybilEdgeProb/sybilEdgeProb{}PRand.p'.format(i), 'rb'))
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
		axarr[enu].set_title('FN=FP='+str(i))


		axarr[enu].plot(x_s, y_s, 'r--')
		axarr[enu].plot(x_h, y_h, 'b--')


plt.show()
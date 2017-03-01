import pickle
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
from util.calc import get_cdf, getMergedRanks, getMergedAuc

graph = 'facebook'


for sys in ('integro', ):
	f, axarr = plt.subplots(1, 3)
	f.suptitle('Integro Victim Prior Influence - Peripheral Random', fontsize=14, weight='bold')

	for enu, i in enumerate((0.1, 0.2, 0.4)):
		print(" ### FP is {} ###".format(i))
		SRall = pickle.load(open('../pickles/victimProb/victimProb{}eval50SRTar.p'.format(i), 'rb'))
		Pall = pickle.load(open('../pickles/victimProb/victimProb{}eval50PTar.p'.format(i), 'rb'))

		pRes = Pall[0]
		pResAUC = getMergedAuc(pRes)
		print('auc peripheral 50')
		print(list(pResAUC['integro'].values()))
		parasP = Pall[1]

		SrRes = SRall[0]
		SrResAUC = getMergedAuc(SrRes)
		print('auc SR 50')
		print(list(SrResAUC['integro'].values()))
		parasSR = SRall[1]

		SRall20 = pickle.load(open('../pickles/victimProb/victimProb{}eval20SRTar.p'.format(i), 'rb'))
		Pall20 = pickle.load(open('../pickles/victimProb/victimProb{}eval20PTar.p'.format(i), 'rb'))

		pRes = Pall20[0]
		pResAUC = getMergedAuc(pRes)
		print('auc peripheral 20')
		print(list(pResAUC['integro'].values()))
		parasP = Pall[1]

		SrRes = SRall20[0]
		SrResAUC = getMergedAuc(SrRes)
		print('auc SR 20')
		print(list(SrResAUC['integro'].values()))
		parasSR = SRall20[1]

"""

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


#plt.show()
"""
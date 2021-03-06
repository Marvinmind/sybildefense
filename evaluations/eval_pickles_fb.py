__author__ = 'Martin'
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

def getMergedAuc(b):
	d = {'integro': defaultdict(lambda: 0), 'votetrust': defaultdict(lambda: 0), 'sybilframe':  defaultdict(lambda: 0)}
	for e in b:
		for i, x in enumerate(e['integro']):
			d['integro'][i] += x.auc/len(b)
		for i, x in enumerate(e['votetrust']):
			d['votetrust'][i] += x.auc/len(b)
		for i, x in enumerate(e['sybilframe']):
			d['sybilframe'][i] += x.auc/len(b)

	return d

peripheral_tar_boosted_fb = pickle.load(open('../pickles/results_targeted_boosted_P_fb.p','rb'))[0]
peripheral_tar_boosted_sm = pickle.load(open('../pickles/results_targeted_boosted_P_sm.p','rb'))[0]
peripheral_tar_boosted_da = pickle.load(open('../pickles/results_targeted_boosted_P_da.p','rb'))[0]

peripheral_random_noboost_fb = pickle.load(open('../pickles/results_random_noboost_P_fb.p','rb'))[0]
peripheral_random_noboost_sm = pickle.load(open('../pickles/results_random_noboost_P_sm.p','rb'))[0]
peripheral_random_noboost_da = pickle.load(open('../pickles/results_random_noboost_P_da.p','rb'))[0]

sr_fb = pickle.load(open('../pickles/results_random_noboost_SR_fb.p','rb'))[0]
sr_sm = pickle.load(open('../pickles/results_random_noboost_SR_sm.p','rb'))[0]
sr_da = pickle.load(open('../pickles/results_random_noboost_SR_da.p','rb'))[0]


bench = pickle.load(open('../pickles/results_random_noboost_SR_fb.p','rb'))[1]
print(bench.numRepeats)
mergeAuc_peripheral_tar_boosted_fb = getMergedAuc(peripheral_tar_boosted_fb)
mergeAuc_peripheral_tar_boosted_sm = getMergedAuc(peripheral_tar_boosted_sm)
mergeAuc_peripheral_tar_boosted_da = getMergedAuc(peripheral_tar_boosted_da)

mergeAuc_peripheral_random_noboost_fb = getMergedAuc(peripheral_random_noboost_fb)
mergeAuc_peripheral_random_noboost_sm = getMergedAuc(peripheral_random_noboost_sm)
mergeAuc_peripheral_random_noboost_da = getMergedAuc(peripheral_random_noboost_da)

mergeAuc_sr_fb = getMergedAuc(sr_fb)
mergeAuc_sr_sm = getMergedAuc(sr_sm)
mergeAuc_sr_da = getMergedAuc(sr_da)

f, axarr = plt.subplots(3,3)

x_per = [x*2 for x in range(26)]
x_sr = [x*25 for x in range(21)]


axarr[0,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_fb['integro'].values()), 'r--')
axarr[0,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_fb['votetrust'].values()),'b--')
axarr[0,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_fb['sybilframe'].values()),'k--')

axarr[0,0].set_ylim((0,1.1))
axarr[0,0].set_title('Peripheral Targeted Boosted')

axarr[0,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_fb['integro'].values()), 'r--')
axarr[0,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_fb['votetrust'].values()),'b--')
axarr[0,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_fb['sybilframe'].values()),'k--')

axarr[0,1].set_ylim((0,1.1))
axarr[0,1].set_title('Peripheral Random')


axarr[0,2].plot(x_sr, list(mergeAuc_sr_fb['integro'].values()), 'r--')
axarr[0,2].plot(x_sr, list(mergeAuc_sr_fb['votetrust'].values()),'b--')
axarr[0,2].plot(x_sr, list(mergeAuc_sr_fb['sybilframe'].values()),'k--')

axarr[0,2].set_ylim((0,1.1))
axarr[0,2].set_title('Sybil Region')


axarr[1,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_sm['integro'].values()), 'r--')
axarr[1,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_sm['votetrust'].values()),'b--')
axarr[1,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_sm['sybilframe'].values()),'k--')

axarr[1,0].set_ylim((0,1.1))

axarr[1,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_sm['integro'].values()), 'r--')
axarr[1,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_sm['votetrust'].values()),'b--')
axarr[1,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_sm['sybilframe'].values()),'k--')

axarr[1,1].set_ylim((0,1.1))


axarr[1,2].plot(x_sr, list(mergeAuc_sr_sm['integro'].values()), 'r--')
axarr[1,2].plot(x_sr, list(mergeAuc_sr_sm['votetrust'].values()),'b--')
axarr[1,2].plot(x_sr, list(mergeAuc_sr_sm['sybilframe'].values()),'k--')

axarr[1,2].set_ylim((0,1.1))

axarr[2,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_da['integro'].values()), 'r--')
axarr[2,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_da['votetrust'].values()),'b--')
axarr[2,0].plot(x_per, list(mergeAuc_peripheral_tar_boosted_da['sybilframe'].values()),'k--')

axarr[2,0].set_ylim((0,1.1))

axarr[2,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_da['integro'].values()), 'r--')
axarr[2,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_da['votetrust'].values()),'b--')
axarr[2,1].plot(x_per, list(mergeAuc_peripheral_random_noboost_da['sybilframe'].values()),'k--')

axarr[2,1].set_ylim((0,1.1))


axarr[2,2].plot(x_sr, list(mergeAuc_sr_da['integro'].values()), 'r--')
axarr[2,2].plot(x_sr, list(mergeAuc_sr_da['votetrust'].values()),'b--')
axarr[2,2].plot(x_sr, list(mergeAuc_sr_da['sybilframe'].values()),'k--')

axarr[2,2].set_ylim((0,1.1))

plt.show()


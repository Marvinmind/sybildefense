__author__ = 'Martin'
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

peripheral_tar = pickle.load(open('../pickles/results_targeted_noboost_P.p','rb'))[0]
peripheral_rand = pickle.load(open('../pickles/results_random_noboost_P_fb.p','rb'))[0]
sr_rand = pickle.load(open('../pickles/results_random_noboost_SR.p','rb'))[0]
peripheral_tar_boosted = pickle.load(open('../pickles/results_targeted_boosted_P.p','rb'))[0]


mergeAuc_integro_peripheral_tar = defaultdict(lambda: 0)
for e in peripheral_tar:
	for i, x in enumerate(e['integro']):
		mergeAuc_integro_peripheral_tar[i] += x.auc/len(peripheral_tar)

mergeAuc_integro_peripheral_rand = defaultdict(lambda: 0)
for e in peripheral_rand:
	for i, x in enumerate(e['integro']):
		mergeAuc_integro_peripheral_rand[i] += x.auc/len(peripheral_rand)

mergeAuc_votetrust_peripheral_tar = defaultdict(lambda: 0)
for e in peripheral_tar:
	for i, x in enumerate(e['votetrust']):
		mergeAuc_votetrust_peripheral_tar[i] += x.auc/len(peripheral_tar)

mergeAuc_votetrust_peripheral_rand = defaultdict(lambda: 0)
for e in peripheral_rand:
	for i, x in enumerate(e['votetrust']):
		mergeAuc_votetrust_peripheral_rand[i] += x.auc/len(peripheral_rand)

mergeAuc_votetrust_sr_rand = defaultdict(lambda: 0)
for e in sr_rand:
	for i, x in enumerate(e['votetrust']):
		mergeAuc_votetrust_sr_rand[i] += x.auc/len(sr_rand)

mergeAuc_integro_sr_rand = defaultdict(lambda: 0)
for e in sr_rand:
	for i, x in enumerate(e['integro']):
		mergeAuc_integro_sr_rand[i] += x.auc/len(sr_rand)

mergeAuc_votetrust_peripheral_tar_boost = defaultdict(lambda: 0)
for e in peripheral_tar_boosted:
	for i, x in enumerate(e['votetrust']):
		mergeAuc_votetrust_peripheral_tar_boost[i] += x.auc/len(peripheral_tar_boosted)

mergeAuc_integro_peripheral_tar_boost = defaultdict(lambda: 0)
for e in peripheral_tar_boosted:
	for i, x in enumerate(e['integro']):
		mergeAuc_integro_peripheral_tar_boost[i] += x.auc/len(peripheral_tar_boosted)

x = [x*5 for x in range(21)]
print(mergeAuc_integro_peripheral_tar)
print(mergeAuc_votetrust_peripheral_rand)
print(mergeAuc_votetrust_peripheral_tar)
print(mergeAuc_integro_peripheral_rand)
print(mergeAuc_integro_sr_rand)
print(mergeAuc_votetrust_sr_rand)
print(mergeAuc_votetrust_peripheral_tar_boost)
print(mergeAuc_integro_peripheral_tar_boost)


" peripheral plot"
plt.plot(x, list(mergeAuc_integro_peripheral_rand.values()),'ro', label='Integro Random')
plt.plot(x, list(mergeAuc_integro_peripheral_tar.values()),'r:',  label='Integro Targeted')
plt.plot(x, list(mergeAuc_integro_peripheral_tar_boost.values()),'r-.',  label='Integro Targeted Boosted')
plt.plot(x, list(mergeAuc_votetrust_peripheral_rand.values()),'bo', label='Votetrust Random')
plt.plot(x, list(mergeAuc_votetrust_peripheral_tar.values()),'b:',  label='Votetrust Targeted')
plt.plot(x, list(mergeAuc_votetrust_peripheral_tar_boost.values()),'b-.',  label='Votetrust Targeted Boosted')


plt.xlabel('Number of requests')
plt.ylabel('Mean AUC')
plt.title('Peripheral Scenario')

plt.ylim((0,1.1))
plt.legend(bbox_to_anchor=(0,0.25), loc='upper left', prop={'size':12})
plt.show()


"sr plot"
x = [x*25 for x in range(21)]
plt.plot(x, list(mergeAuc_integro_sr_rand.values()), 'r--', label='Integro')
plt.plot(x, list(mergeAuc_votetrust_sr_rand.values()), 'b:',label='Votetrust')

plt.xlabel('Number of requests')
plt.ylabel('Mean AUC')
plt.ylim((0,1.1))
plt.title('Sybil Region Scenario')
plt.legend(bbox_to_anchor=(0,0.25), loc='upper left', prop={'size':12})
plt.show()
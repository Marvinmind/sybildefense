__author__ = 'Martin'
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

peripheral_tar = pickle.load(open('../pickles/results_targeted_noboost_P.p','rb'))[0]
peripheral_rand = pickle.load(open('../pickles/results_random_noboost_P.p','rb'))[0]

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

x = [x*5 for x in range(21)]
print(mergeAuc_integro_peripheral_tar)
print(mergeAuc_votetrust_peripheral_rand)
print(mergeAuc_votetrust_peripheral_tar)
print(mergeAuc_integro_peripheral_rand)

plt.plot(x, list(mergeAuc_integro_peripheral_rand.values()),'r--')
plt.plot(x, list(mergeAuc_integro_peripheral_tar.values()),'r')
plt.plot(x, list(mergeAuc_votetrust_peripheral_rand.values()),'b--')
plt.plot(x, list(mergeAuc_votetrust_peripheral_tar.values()),'b')

plt.ylim((0,1.1))
plt.show()

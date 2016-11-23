__author__ = 'Martin'
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt

sybil_region = pickle.load(open('../pickles/resultsSybilRegion.p','rb'))
peripheral = pickle.load(open('../pickles/results_targeted_noboost_P.p','rb'))

mergeAuc_integro_SR = defaultdict(lambda: 0)
for e in sybil_region:
	for i, x in enumerate(e['integro']):
		mergeAuc_integro_SR[i] += x.auc/len(sybil_region)

mergeAuc_integro_P = defaultdict(lambda: 0)
for e in peripheral:
	for i, x in enumerate(e['integro']):
		mergeAuc_integro_P[i] += x.auc/len(peripheral)

mergeAuc_votetrust_SR = defaultdict(lambda: 0)
for e in sybil_region:
	for i, x in enumerate(e['votetrust']):
		mergeAuc_votetrust_SR[i] += x.auc/len(sybil_region)

mergeAuc_votetrust_P = defaultdict(lambda: 0)
for e in peripheral:
	for i, x in enumerate(e['votetrust']):
		mergeAuc_votetrust_P[i] += x.auc/len(peripheral)

print(mergeAuc_integro_SR)
print(mergeAuc_votetrust_SR)
print(mergeAuc_integro_P)
print(mergeAuc_votetrust_P)


import pickle
from collections import defaultdict
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
import numpy as np

graph = 'facebook'
def get_cdf(v):
	l = len(v)
	v_new = np.array(v, dtype=np.float)
	currEl = v[0]
	currCount = 0

	for i, e in enumerate(v):
		if e == currEl:
			currCount += 1

		else:
			v_new[i-currCount:i] = i/l
			currCount = 1
			currEl = e

	v_new[l-currCount:] = 1.0

	return list(v_new)


def getMergedRanks(b):
	d = {'integro': defaultdict(lambda: 0), 'votetrust': defaultdict(lambda: 0), 'sybilframe':  defaultdict(lambda: 0)}
	for e in b:
		for i, x in enumerate(e['integro']):
			d['integro'][i] += x.ranks/len(b)
		for i, x in enumerate(e['votetrust']):
			d['votetrust'][i] += x.ranks/len(b)
		for i, x in enumerate(e['sybilframe']):
			d['sybilframe'][i] += x.ranks/len(b)

	return d



peripheral_tar_boosted_no = pickle.load(open('../pickles/res_breadthFirst_boosted_{}_P.p'.format(graph),'rb'))[0]
peripheral_random_noboost_no = pickle.load(open('../pickles/res_random_noboost_{}_P.p'.format(graph),'rb'))[0]
sr_no = pickle.load(open('../pickles/res_random_noboost_{}_SR.p'.format(graph),'rb'))[0]

ranks_peripheral_tar_boosted_no = getMergedRanks(peripheral_tar_boosted_no)
ranks_peripheral_random_noboost_no = getMergedRanks(peripheral_random_noboost_no)
ranks_sr_no = getMergedRanks(sr_no)

print(pickle.load(open('../pickles/res_random_noboost_{}_SR.p'.format(graph),'rb'))[1].nodeProbSybil)
print(len(ranks_peripheral_tar_boosted_no['integro'][0]))
print(np.median(ranks_peripheral_tar_boosted_no['integro'][0]))
print(np.max(ranks_peripheral_tar_boosted_no['integro'][0]))


f, axarr = plt.subplots(3,3)

""" Targeted Peripheral Integro"""


x_h = sorted(ranks_peripheral_tar_boosted_no['integro'][0][:-23])[:-15]
x_s = sorted(ranks_peripheral_tar_boosted_no['integro'][0][-23:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_peripheral_tar_boosted_no['integro'][0]))
x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[0,0].set_ylim((0,1.1))
axarr[0,0].set_xlim((-0.1,1.1))


axarr[0,0].plot(x_s, y_s, 'r--')
axarr[0,0].plot(x_h, y_h, 'b--')

""" Targeted Peripheral Votetrust"""

x_h = sorted(ranks_peripheral_tar_boosted_no['votetrust'][0][:-23])
x_s = sorted(ranks_peripheral_tar_boosted_no['votetrust'][0][-23:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_peripheral_tar_boosted_no['votetrust'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)


y_h = get_cdf(x_h)
y_s = get_cdf(x_s)


axarr[1,0].set_ylim((0, 1.1))
axarr[1,0].set_xlim((-0.1, 1.1))


axarr[1,0].plot(x_s, y_s, 'r--')
axarr[1,0].plot(x_h, y_h, 'b--')

""" Targeted Peripheral Sybilframe"""

x_h = sorted(ranks_peripheral_tar_boosted_no['sybilframe'][0][:-23])
x_s = sorted(ranks_peripheral_tar_boosted_no['sybilframe'][0][-23:])


scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_peripheral_tar_boosted_no['sybilframe'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[2,0].set_ylim((0,1.1))
axarr[2,0].set_xlim((-0.1,1.1))



sybil, = axarr[2,0].plot(x_s, y_s, 'r--', label='sybil')
honest, = axarr[2,0].plot(x_h, y_h, 'b--', label='honest')


""" Random Peripheral Integro"""

x_h = sorted(ranks_peripheral_random_noboost_no['integro'][0][:-20])
x_s = sorted(ranks_peripheral_random_noboost_no['integro'][0][-20:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_peripheral_random_noboost_no['integro'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[0,1].set_ylim((0,1.1))
axarr[0,1].set_xlim((-0.1,1.1))

axarr[0,1].plot(x_s, y_s, 'r--')
axarr[0,1].plot(x_h, y_h, 'b--')


""" Random Peripheral Votetrust"""

x_h = sorted(ranks_peripheral_random_noboost_no['votetrust'][0][:-20])
x_s = sorted(ranks_peripheral_random_noboost_no['votetrust'][0][-20:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_peripheral_random_noboost_no['votetrust'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)


y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[1,1].set_ylim((0,1.1))
axarr[1,1].set_xlim((-0.1,1.1))

axarr[1,1].plot(x_s, y_s, 'rs')
axarr[1,1].plot(x_h, y_h, 'b--')

""" Random Peripheral Sybilframe"""

x_h = sorted(ranks_peripheral_random_noboost_no['sybilframe'][0][:-20])
x_s = sorted(ranks_peripheral_random_noboost_no['sybilframe'][0][-20:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_peripheral_random_noboost_no['sybilframe'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[2,1].set_ylim((0,1.1))
axarr[2,1].set_xlim((-0.1,1.1))

axarr[2,1].plot(x_s, y_s, 'r--')
axarr[2,1].plot(x_h, y_h, 'b--')

""" SR Integro"""

x_h = sorted(ranks_sr_no['integro'][0][:-100])
x_s = sorted(ranks_sr_no['integro'][0][-100:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_sr_no['integro'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[0,2].set_ylim((0,1.1))
axarr[0,2].set_xlim((-0.1,1.1))

axarr[0,2].plot(x_s, y_s, 'r--')
axarr[0,2].plot(x_h, y_h, 'b--')


""" SR Votetrust"""

x_h = sorted(ranks_sr_no['votetrust'][0][:-100])
x_s = sorted(ranks_sr_no['votetrust'][0][-100:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_sr_no['votetrust'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[1,2].set_ylim((0,1.1))
axarr[1,2].set_xlim((-0.1,1.1))

axarr[1,2].plot(x_s, y_s, 'rs')
axarr[1,2].plot(x_h, y_h, 'b--')

""" SR Sybilframe"""
x_h = sorted(ranks_sr_no['sybilframe'][0][:-100])
x_s = sorted(ranks_sr_no['sybilframe'][0][-100:])

scaler = prep.MinMaxScaler()
scaler.fit(sorted(ranks_sr_no['sybilframe'][0]))

x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[2,2].set_ylim((0,1.1))
axarr[2,2].set_xlim((-0.1,1.1))

axarr[2,2].plot(x_s, y_s, 'r--')
axarr[2,2].plot(x_h, y_h, 'b--')


axarr[0,0].set_title('Targeted Peripheral Boosted')
axarr[0,1].set_title('Random Peripheral Noboost')
axarr[0,2].set_title('Sybil Region')


plt.figlegend((honest, sybil), ('honest', 'sybil'),  'upper left')
plt.show()
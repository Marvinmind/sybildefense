from util.calc import get_cdf, getMergedRanks
from matplotlib import pyplot as plt
from sklearn import preprocessing as prep
import pickle
import json

paras = json.load(open('baseparameters.json','r'))

graph = 'facebook'

res_boost = pickle.load(open('../pickles/res_breadthFirst_boosted_{}_P.p'.format(graph),'rb'))
boost = getMergedRanks(res_boost[0])
paras_b = res_boost[1]

res_nob = pickle.load(open('../pickles/res_breadthFirst_noboost_{}_P.p'.format(graph),'rb'))
print(res_nob)
noboost = getMergedRanks(res_nob[0])
paras_n = res_nob[1]

f, axarr = plt.subplots(1,2)
print(noboost['votetrust'][0])
"plot boosted"
x_h = sorted(boost['votetrust'][0][:-(paras_b.numSybils+3)])
x_s = sorted(boost['votetrust'][0][-(paras_b.numSybils+3):])
print(x_h)

scaler = prep.MinMaxScaler()
scaler.fit(sorted(boost['votetrust'][0]))
x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[0].set_ylim((0,1.1))
axarr[0].set_xlim((-0.1,1.1))

axarr[0].plot(x_s, y_s, 'r--')
axarr[0].plot(x_h, y_h, 'b--')


"plot noboost"
x_h = sorted(noboost['votetrust'][0][:-paras_n.numSybils])
x_s = sorted(noboost['votetrust'][0][-paras_n.numSybils:])
print(len(x_h))

scaler = prep.MinMaxScaler()
scaler.fit(sorted(noboost['votetrust'][0]))
x_h = scaler.transform(x_h)
x_s = scaler.transform(x_s)

y_h = get_cdf(x_h)
y_s = get_cdf(x_s)

axarr[1].set_ylim((0,1.1))
axarr[1].set_xlim((-0.1,1.1))

axarr[1].plot(x_s, y_s, 'r--')
axarr[1].plot(x_h, y_h, 'b--')

plt.show()



import pickle
from matplotlib import pyplot as plt
import sklearn.preprocessing as prep
from util.calc import get_cdf, getMergedRanks, getMergedAuc
import numpy as np
from util import setMatplotlibPaper


graph = 'slashdot'
colors = ['r-', 'b--.', 'k-.', 'g:']
sys = 'sybilframe'

plt.figure(figsize=(3.5, 2.3))
plt.ylim(0,1.1)
plt.suptitle('Sybilframe Edge Prior Influence - '  +str.upper(str(graph)[0])+str(graph)[1:], weight='bold')

for enu, i in enumerate((0.1, 0.3, 0.6, 0.82)):
	perTarAll = pickle.load(open('../pickles/sybilEdgeProb/sybilEdgeProb{}PTar{}.p'.format(i, graph), 'rb'))
	perTar = perTarAll[0]
	perTarAUC = getMergedAuc(perTar)
	print(perTarAUC)
	paras = perTarAll[1]

	x = [x for x in (1,5,10,15,20,25,30,35,40,45,50)]
	print(x)
	print(list(perTarAUC['sybilframe'].values()))
	plt.plot(x, list(perTarAUC['sybilframe'].values()), colors[enu], label='FN = '+str(i))

if graph=='facebook':
	plt.legend(loc='lower right')

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig('/home/martin/Dropbox/MasterGöttingen/Masterarbeit/figures/EdgeProb{}.pdf'.format(graph), format='pdf')
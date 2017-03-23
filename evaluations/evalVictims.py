import pickle
from util.calc import get_cdf, getMergedRanks, getMergedAuc

graph = 'facebook'
for i in (0.1, 0.2, 0.4):
	resSR = pickle.load(open('../pickles/victimProb/victimProb{}{}SRTar.p'.format(i, graph), 'rb'))[0]
	resP = pickle.load(open('../pickles/victimProb/victimProb{}{}PTar.p'.format(i, graph),'rb'))[0]

	SRAuc = getMergedAuc(resSR)
	PAuc = getMergedAuc(resP)

	print(SRAuc['integro'])
	print(PAuc['integro'])
	print('')

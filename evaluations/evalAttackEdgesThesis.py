from util.calc import getMergedAuc
import pickle
from matplotlib import pyplot as plt
from util import setMatplotlibPaper
from baseparameters import paras as pathParas
graph = 'slashdot'

PRandAll = pickle.load(open('../pickles/attackEdges/attackEdgesPRand{}.p'.format(graph),'rb'))
PRandRes = PRandAll[0]
PRandAUC = getMergedAuc(PRandRes)
PRandParas = PRandAll[1]


PTarAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTar{}.p'.format(graph),'rb'))
PTarRes = PTarAll[0]
PTarAUC = getMergedAuc(PTarRes)
PTarParas = PTarAll[1]

SRRandAll = pickle.load(open("../pickles/attackEdges/attackEdgesSRRand{}.p".format(graph), 'rb'))
SRRandRes = SRRandAll[0]
SRRandAUC = getMergedAuc(SRRandRes)
SRRandParas = SRRandAll[1]

SRTarAll = pickle.load(open('../pickles/attackEdges/attackEdgesSRTar{}.p'.format(graph),'rb'))
SRTarRes = SRTarAll[0]
SRTarAUC = getMergedAuc(SRTarRes)
SRTarParas = SRTarAll[1]

PTarTwoPhaseAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTwoPhase{}.p'.format(graph),'rb'))
PTarTwoPhaseRes = PTarTwoPhaseAll[0]
PTarTwoPhaseAUC = getMergedAuc(PTarTwoPhaseRes)
PTarTwoPhaseParas = PTarTwoPhaseAll[1]

PTarNoboostAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTarNoboost{}.p'.format(graph),'rb'))
PTarNoboostRes = PTarNoboostAll[0]
PTarNoboostAUC = getMergedAuc(PTarNoboostRes)
PTarNoboostParas = PTarNoboostAll[1]

f, axarr = plt.subplots(2, 3, figsize=(5.8, 5), sharey=True)

x = [x for x in PRandParas.evalAt]
f.suptitle('Systems Performance by Number of Requests - '+str.upper(str(graph)[0])+str(graph)[1:], weight='bold')

"SR Random"
axarr[0,0].plot(x, list(SRRandAUC['integro'].values()), 'r-', label='Integro')
axarr[0,0].plot(x, list(SRRandAUC['votetrust'].values()),'b--', label='Votetrust')
axarr[0,0].plot(x, list(SRRandAUC['sybilframe'].values()),'k-.', label='SybilFrame')
axarr[0,0].set_ylabel('Area Under ROC')

axarr[0,0].set_ylim((0,1.1))
axarr[0,0].set_title('Sybil Region Random', loc='center')

"P Random"
axarr[0,1].plot(x, list(PRandAUC['integro'].values()), 'r-')
axarr[0,1].plot(x, list(PRandAUC['votetrust'].values()),'b--')
axarr[0,1].plot(x, list(PRandAUC['sybilframe'].values()),'k-.')

axarr[0,1].set_ylim((0, 1.1))
axarr[0,1].set_title('Peri. Random', loc='center')
axarr[1,1].set_xlabel('Number of Requests')


"P Targeted Noboost"
axarr[0,2].plot(x, list(PTarNoboostAUC['integro'].values()), 'r-')
axarr[0,2].plot(x, list(PTarNoboostAUC['votetrust'].values()),'b--')
axarr[0,2].plot(x, list(PTarNoboostAUC['sybilframe'].values()),'k-.')

axarr[0,2].set_ylim((0, 1.1))
axarr[0,2].set_title('Peri. Targeted', loc='center')

"P Targeted Boost"
axarr[1,0].plot(x, list(PTarAUC['integro'].values()), 'r-')
axarr[1,0].plot(x, list(PTarAUC['votetrust'].values()),'b--')
axarr[1,0].plot(x, list(PTarAUC['sybilframe'].values()),'k-.')

axarr[1,0].set_title('Peri. Targeted Boosted', loc='center')
axarr[1,0].set_ylim((0, 1.1))
axarr[1,0].set_ylabel('Area Under ROC')


"P Two Phase Boost"
axarr[1,1].plot(x, list(PTarTwoPhaseAUC['integro'].values()), 'r-')
axarr[1,1].plot(x, list(PTarTwoPhaseAUC['votetrust'].values()),'b--')
axarr[1,1].plot(x, list(PTarTwoPhaseAUC['sybilframe'].values()),'k-.')

axarr[1,1].set_ylim((0, 1.1))
axarr[1,1].set_title('Peri. Two Phase Boosted', loc='center')

"SR Tar"
axarr[1,2].plot(x, list(SRTarAUC['integro'].values()), 'r-')
axarr[1,2].plot(x, list(SRTarAUC['votetrust'].values()),'b--')
axarr[1,2].plot(x, list(SRTarAUC['sybilframe'].values()),'k-.')

axarr[1,2].set_ylim((0, 1.1))
axarr[1,2].set_title('Sybil Region Targeted', loc='center')
axarr[1,0].legend(bbox_to_anchor=(0,0.52), loc='upper left')

for i in range(2):
	for j in range(1,3):
		axarr[i,j].xaxis.get_major_ticks()[0].label1.set_visible(False)


plt.tight_layout()
plt.subplots_adjust(top=0.78, bottom=0.1)
f.subplots_adjust(wspace=0.1)
plt.savefig(pathParas['figuresPath']+'/AttackEdges{}.pdf'.format(graph), format='pdf')


from util.calc import getMergedAuc
import pickle
from matplotlib import pyplot as plt

PRandAll = pickle.load(open('../pickles/attackEdges/attackEdgesPRand.p','rb'))
PRandRes = PRandAll[0]
PRandAUC = getMergedAuc(PRandRes)
PRandParas = PRandAll[1]


PTarAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTar.p','rb'))
PTarRes = PTarAll[0]
PTarAUC = getMergedAuc(PTarRes)
PTarParas = PTarAll[1]

SRRandAll = pickle.load(open('../pickles/attackEdges/attackEdgesSRRand.p','rb'))
SRRandRes = SRRandAll[0]
SRRandAUC = getMergedAuc(SRRandRes)
SRRandParas = SRRandAll[1]

PTarTwoPhaseAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTwoPhase.p','rb'))
PTarTwoPhaseRes = PTarTwoPhaseAll[0]
PTarTwoPhaseAUC = getMergedAuc(PTarTwoPhaseRes)
PTarTwoPhaseParas = PTarTwoPhaseAll[1]

PTarNoboostAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTarNoboost.p','rb'))
PTarNoboostRes = PTarNoboostAll[0]
PTarNoboostAUC = getMergedAuc(PTarNoboostRes)
PTarNoboostParas = PTarNoboostAll[1]


f, axarr = plt.subplots(1,5)

f.suptitle('Systems Performance by Number of Attack Edges', fontsize=14, weight='bold')

x = [x for x in PRandParas.evalAt]


axarr[0].plot(x, list(PTarAUC['integro'].values()), 'r-', label='Integro')
axarr[0].plot(x, list(PTarAUC['votetrust'].values()),'b--', label='Votetrust')
axarr[0].plot(x, list(PTarAUC['sybilframe'].values()),'k-.', label='SybilFrame')
axarr[0].set_ylabel('Area Under ROC')

axarr[0].set_ylim((0,1.1))
axarr[0].set_title('Peripheral Targeted')

axarr[1].plot(x, list(PRandAUC['integro'].values()), 'r-')
axarr[1].plot(x, list(PRandAUC['votetrust'].values()),'b--')
axarr[1].plot(x, list(PRandAUC['sybilframe'].values()),'k-.')

axarr[1].set_ylim((0,1.1))
axarr[1].set_title('Peripheral Random')


axarr[2].plot(x, list(SRRandAUC['integro'].values()), 'r-')
axarr[2].plot(x, list(SRRandAUC['votetrust'].values()),'b--')
axarr[2].plot(x, list(SRRandAUC['sybilframe'].values()),'k-.')

axarr[2].set_ylim((0,1.1))
axarr[2].set_title('Sybil Region Random', loc='left')
axarr[2].set_xlabel('Number of Attack Edges')

axarr[3].plot(x, list(PTarNoboostAUC['integro'].values()), 'r-')
axarr[3].plot(x, list(PTarNoboostAUC['votetrust'].values()),'b--')
axarr[3].plot(x, list(PTarNoboostAUC['sybilframe'].values()),'k-.')

axarr[3].set_ylim((0,1.1))
axarr[3].set_title('Peripheral Targeted Noboost', loc='left')

axarr[4].plot(x, list(PTarTwoPhaseAUC['integro'].values()), 'r-')
axarr[4].plot(x, list(PTarTwoPhaseAUC['votetrust'].values()),'b--')
axarr[4].plot(x, list(PTarTwoPhaseAUC['sybilframe'].values()),'k-.')

axarr[4].set_ylim((0,1.1))
axarr[4].set_title('Peripheral Two Phase Boosted', loc='left')



axarr[0].legend(bbox_to_anchor=(0,0.38), loc='upper left', prop={'size':12})


plt.show()


from util.calc import getMergedAuc
import pickle
from matplotlib import pyplot as plt
from util import setMatplotlibPaper

graph = 'slashdot'

PRandAll = pickle.load(open('../pickles/attackEdges/attackEdgesPRand{}.p'.format(graph),'rb'))
PRandRes = PRandAll[0]
PRandAUC = getMergedAuc(PRandRes)
PRandParas = PRandAll[1]


PTarAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTar{}.p'.format(graph),'rb'))
PTarRes = PTarAll[0]
PTarAUC = getMergedAuc(PTarRes)
PTarParas = PTarAll[1]

SRRandAll = pickle.load(open('../pickles/attackEdges/attackEdgesSRRand{}.p'.format(graph),'rb'))
SRRandRes = SRRandAll[0]
SRRandAUC = getMergedAuc(SRRandRes)
SRRandParas = SRRandAll[1]

PTarTwoPhaseAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTwoPhase{}.p'.format(graph),'rb'))
PTarTwoPhaseRes = PTarTwoPhaseAll[0]
PTarTwoPhaseAUC = getMergedAuc(PTarTwoPhaseRes)
PTarTwoPhaseParas = PTarTwoPhaseAll[1]

PTarNoboostAll = pickle.load(open('../pickles/attackEdges/attackEdgesPTarNoboost{}.p'.format(graph),'rb'))
PTarNoboostRes = PTarNoboostAll[0]
PTarNoboostAUC = getMergedAuc(PTarNoboostRes)
PTarNoboostParas = PTarNoboostAll[1]

f, axarr = plt.subplots(1, 4, figsize=(7.5, 2.3), sharey=True)
supt = f.suptitle('Systems Performance by Number of Requests')

x = [x for x in PRandParas.evalAt]

"SR Random"
axarr[0].plot(x, list(SRRandAUC['integro'].values()), 'r-', label='Integro')
axarr[0].plot(x, list(SRRandAUC['votetrust'].values()),'b--', label='Votetrust')
axarr[0].plot(x, list(SRRandAUC['sybilframe'].values()),'k-.', label='SybilFrame')
axarr[0].set_ylabel('Area Under ROC')

axarr[0].set_ylim((0,1.1))
axarr[0].set_title('Sybil Region Random', loc='center')

"P Random"
axarr[1].plot(x, list(PRandAUC['integro'].values()), 'r-')
axarr[1].plot(x, list(PRandAUC['votetrust'].values()),'b--')
axarr[1].plot(x, list(PRandAUC['sybilframe'].values()),'k-.')

axarr[1].set_ylim((0, 1.1))
axarr[1].set_title('Peri. Random', loc='center')


"P Targeted Noboost"
axarr[2].plot(x, list(PTarNoboostAUC['integro'].values()), 'r-')
axarr[2].plot(x, list(PTarNoboostAUC['votetrust'].values()),'b--')
axarr[2].plot(x, list(PTarNoboostAUC['sybilframe'].values()),'k-.')

axarr[2].set_ylim((0, 1.1))
axarr[2].set_title('Peri. Targeted', loc='center')

"P Targeted Boost"
axarr[3].plot(x, list(PTarAUC['integro'].values()), 'r-')
axarr[3].plot(x, list(PTarAUC['votetrust'].values()),'b--')
axarr[3].plot(x, list(PTarAUC['sybilframe'].values()),'k-.')

axarr[3].set_title('Peri. Targeted Boosted', loc='center')
axarr[3].set_ylim((0, 1.1))


axarr[0].legend(bbox_to_anchor=(0,0.35), loc='upper left')

axarr[1].xaxis.get_major_ticks()[0].label1.set_visible(False)
axarr[2].xaxis.get_major_ticks()[0].label1.set_visible(False)
axarr[3].xaxis.get_major_ticks()[0].label1.set_visible(False)



plt.tight_layout()
plt.subplots_adjust(top=0.9)
f.subplots_adjust(wspace=0.1)
caption = f.text(0.525, 0, 'Number of Requests', ha='center', fontsize=8)

plt.savefig('/home/martin/Dropbox/MasterGöttingen/Masterarbeit/figures/AttackEdgesPaper{}.pdf'.format(graph), format='pdf', bbox_extra_artists=(caption, supt), bbox_inches='tight')


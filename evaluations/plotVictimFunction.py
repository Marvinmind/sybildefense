from sybil.integro import getValues
from matplotlib import pyplot as plt
from matplotlib import rcParams
from math import ceil
import numpy as np
from baseparameters import paras
from util import setMatplotlib

n = 200
auc = 0.3
xvalues = list(np.linspace(0,1,n))
yvalues = getValues(len(xvalues), auc)
yvalues[-1] = 0
rcParams['figure.titlesize'] = 9
plt.figure(figsize=(2.9, 2.9))
plt.plot(xvalues, yvalues, 'b--')
half_index = ceil(len(xvalues)/2)
plt.fill(xvalues[0:half_index]+[xvalues[half_index-1]], yvalues[0:half_index]+[0], facecolor='blue', alpha=0.3)

plt.fill([xvalues[half_index-1]] + xvalues[half_index-1:], [0]+yvalues[half_index-1:], facecolor='red', alpha=0.5)

lyposition = np.mean((np.max(yvalues[:half_index]),0))-0.2
ryposition = np.mean((np.max(yvalues[half_index:]),0))-0.2
plt.text(0.22,lyposition, 'a={}'.format(auc))
plt.text(0.55,ryposition, 'a={}'.format(round(1-auc,2)))

plt.xlabel('Victim Probability')
plt.suptitle('Victim Probability Density Function')
plt.subplots_adjust(bottom=0.2, top=0.90)

plt.savefig(paras['figuresPath']+'/VictimProbFunction{}.pdf'.format(str(0)+str(auc)[2]), type='pdf')
plt.tight_layout()

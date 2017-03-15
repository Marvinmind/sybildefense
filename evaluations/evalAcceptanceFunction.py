import matplotlib.pyplot as plt
from util.calc import getSuccessProb
from util import setMatplotlibPaper
import matplotlib as mpl
from baseparameters import paras


plt.figure(figsize=(2.8, 2.5))

"Plot success distribution"
plt.suptitle('Success Probability Function')
x = list(range(10))

y_low = [getSuccessProb(z, start=0.1, max=0.5) for z in x]
y_high = [getSuccessProb(z, start=0.2, max=0.7) for z in x]

plt.plot(x,y_low, 'b--', label='low=0.1, high=0.5')
plt.plot(x,y_high, 'r-.', label='low=0.2, high=0.7')

plt.ylabel('Success Probability')
plt.xlabel('Number of Common Friends')
plt.legend(loc='lower right')


plt.tight_layout(pad=0.1)
plt.subplots_adjust(top=0.85, bottom=0.2)

plt.savefig(paras['figuresPath']+'/funcAcceptance.pdf', type='pdf')

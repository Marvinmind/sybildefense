import matplotlib.pyplot as plt
from util.calc import getSuccessProb
from util import setMatplotlib
plt.figure(figsize=(3.5, 2.5))

"Plot success distribution"
x = list(range(10))

y_low = [getSuccessProb(z, start=0.1, max=0.5) for z in x]
y_high = [getSuccessProb(z, start=0.2, max=0.7) for z in x]

plt.plot(x,y_low, 'b--', label='low=0.1, high=0.5')
plt.plot(x,y_high, 'r-.', label='low=0.2, high=0.7')
plt.legend()

plt.ylabel('Success Probability')
plt.xlabel('Number of Common Friends')
plt.suptitle('Success Probability Function')
plt.ylim(0,1)
plt.tight_layout()
plt.savefig('/home/martin/Dropbox/MasterGöttingen/Masterarbeit/figures/funcAcceptance.pdf', type='pdf')
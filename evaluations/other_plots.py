import matplotlib.pyplot as plt
from util.calc import getSuccessProb

"Plot success distribution"
x = list(range(10))

y_low = [getSuccessProb(z, start=0.1, max=0.5) for z in x]
y_high = [getSuccessProb(z, start=0.2, max=0.7) for z in x]

plt.plot(x,y_low, 'b--', label='low=0.1, high=0.5')
plt.plot(x,y_high, 'r-.', label='low=0.2, high=0.7')
plt.legend()

plt.ylabel('Success Probability')
plt.xlabel('Number of Common Friends')
plt.title('Success Probability Function')
plt.ylim(0,1)
plt.show()
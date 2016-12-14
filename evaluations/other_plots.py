import matplotlib.pyplot as plt
from util.calc import getSuccessProb

"Plot success distribution"
x = list(range(10))

y = [getSuccessProb(z, max=0.8) for z in x]

print(y)
plt.plot(x,y, 'b--')
plt.ylabel('Success Probability')
plt.xlabel('Number of Common Friends')
plt.title('Success Probability Function')
plt.show()
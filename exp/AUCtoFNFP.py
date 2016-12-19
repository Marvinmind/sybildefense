from sklearn.metrics import roc_auc_score
import random

FPN = 0.75

n_pos = 10000
n_neg = 10000000

real = [1]*n_pos+[0]*n_neg
res= []

for i in range(n_pos):
	r = random.random()
	if r < FPN:
		res.append(1)
	else:
		res.append(0)

for i in range(n_neg):
	r = random.random()
	if r < FPN:
		res.append(0)
	else:
		res.append(1)

print(roc_auc_score(real, res))
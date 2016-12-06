import random
import scipy.stats as stats
import numpy as np
from math import exp
from sybil.integro import getValues


def wilsonScore(p, n, alpha=0.05):
	return (p + (1/(2*n))*pow(stats.norm.ppf(1-alpha/2),2))/(1+(1/n)*pow(stats.norm.ppf(1-alpha/2),2))


def getSuccessByFriends(f, k=0.3, start=0.2, max=1):
	prob = max-(max-start)*exp(-1*k*f)
	r = random.random()
	if r < prob:
		return True
	else:
		return False
def getSuccessByProb(prob):
	r = random.random()
	if r < prob:
		return True
	else:
		return False

def getSuccessProb(f, k=0.3, start=0.2, max=1):
	prob = max-(max-start)*exp(-1*k*f)
	return prob


def getNodeProbClosure(middle):
	prec = 10000
	val = np.array(getValues(prec, middle))
	val = val / sum(val)
	y = np.cumsum(val)
	x = np.array(range(prec)) / prec

	def retFunc():
		rand = random.random()
		return np.interp(rand, y, x)

	return retFunc

def getAcceptanceClosure(min, max):
	def retFunc(f):
		return getSuccessByFriends(f, start=min, max=max)
	return retFunc

import random
import scipy.stats as stats
import numpy as np
from math import exp
from sybil.integro import getValues
from collections import defaultdict


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

def get_cdf(v):
	l = len(v)
	v_new = np.array(v, dtype=np.float)
	currEl = v[0]
	currCount = 0

	for i, e in enumerate(v):
		if e == currEl:
			currCount += 1

		else:
			v_new[i-currCount:i] = i/l
			currCount = 1
			currEl = e

	v_new[l-currCount:] = 1.0

	return list(v_new)

def getMergedRanks(b):
	d = {'integro': defaultdict(lambda: 0), 'votetrust': defaultdict(lambda: 0), 'sybilframe':  defaultdict(lambda: 0)}
	for e in b:
		for i, x in enumerate(e['integro']):
			d['integro'][i] += x.ranks/len(b)
		for i, x in enumerate(e['votetrust']):
			d['votetrust'][i] += x.ranks/len(b)
		for i, x in enumerate(e['sybilframe']):
			d['sybilframe'][i] += x.ranks/len(b)

	return d

def getMergedAuc(b):
	d = {'integro': defaultdict(lambda: 0), 'votetrust': defaultdict(lambda: 0), 'sybilframe':  defaultdict(lambda: 0)}
	for e in b:
		for i, x in enumerate(e['integro']):
			d['integro'][i] += x.auc/len(b)
		for i, x in enumerate(e['votetrust']):
			d['votetrust'][i] += x.auc/len(b)
		for i, x in enumerate(e['sybilframe']):
			d['sybilframe'][i] += x.auc/len(b)

	return d
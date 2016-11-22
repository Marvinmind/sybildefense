__author__ = 'Martin'
from multiprocessing import Process, Queue
import random
from math import floor
import numpy as np

def getHighestPrime(l,q):

	results = []
	for n in l:
		prime = True
		for i in range(2,floor(n**0.5)):
			if n%i==0:
				prime = False
		if prime == True:
			results.append(n)
	q.put(max(results))
	return

if __name__ == '__main__':
	print('go')
	vectors = []
	procs = []
	res_queue = Queue()
	for i in range(4):
		vectors.append(tuple([random.randint(0,100000) for x in range(10000)]))

	for v in vectors:
		p = Process(target=getHighestPrime, args=(v,res_queue))
		procs.append(p)
		p.start()

	res_list = []
	for p in procs :
		res_list.append(res_queue.get())

	for p in procs:
		p.join()

	print(max(res_list))


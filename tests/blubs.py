import  networkx as nx
import numpy as np

"""

with open('../datasets/FINAL_BA_RND_0.3.txt','r') as f:
    with open('../datasets/davidGraph.txt', 'w+') as g:
        for l in f:
            a = l.split(' ')
            if a[2][0] == 'R':
                g.write('{} {} {{\'type\': \'{}\' }}'.format(a[0],a[1],a[2][0])+'\n')


g = nx.watts_strogatz_graph(1000,80,0.4)

d = list(g.degree(range(len(g.nodes()))).values())

print(sorted(d))
print(np.mean(d))


with open('../datasets/facebook-links.txt.anon','r') as f:
	with open('../datasets/newOrleans.txt','w+') as n:
		for l in f.readlines():
			s = l.split('\t')
			n.write('{} {}\n'.format(s[0],s[1]))
"""

def getcdfs(v):
	l = len(v)
	v_new = np.array(v, dtype=np.float)
	print(v_new)
	currEl = v[0]
	currCount = 0

	for i, e in enumerate(v):
		if e == currEl:
			currCount += 1

		else:
			print(i/l)
			v_new[i-currCount:i] = i/l
			currCount = 1
			currEl = e


	v_new[l-currCount:] = 1.0

	return v_new



v = [1,1,1,2,2,3,4,4]
print(getcdfs(v))

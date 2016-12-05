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
"""

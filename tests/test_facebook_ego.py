import networkx as nx
import pickle

"""
g = nx.read_adjlist('/home/martin/Downloads/facebook_combined.txt')

partition = community.best_partition(g)
print(partition)
X

g = nx.Graph()

g.add_node(0)

g.node[0]['att'] = lambda x:x*2
g.node[0]['label'] = 0
g.add_edge(0,1)
g[0][1]['jo'] = lambda x:x+5

for n in g.nodes_iter():
	attr = tuple(g.node[n].keys())
	print(attr)
	for k in attr:
		if k not in ('label', 'sublabel'):
			del g.node[n][k]

for x, y in g.edges_iter():
	attr = tuple(g[x][y].keys())
	for k in attr:
		del g[x][y][k]

print('pickle')
pickle.dump(g, open('../pickles/lambdaTest.p','wb+'))


g = nx.read_edgelist('../datasets/FINAL_BA_RND_0.3.txt')
print(len(g.nodes()))
print(sorted(g.nodes()))
"""

with open('../datasets/FINAL_BA_RND_0.3.txt','r') as f:
	with open('../datasets/FINAL_BA_RND_0.3.txt', 'w+') as g:
		for l in f.readline():
			g.write('h')
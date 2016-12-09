import networkx as nx
"""
with open('../datasets/facebook-links.txt.anon','r') as f:
	with open('../datasets/newOrleans.txt','w+') as n:
		for l in f.readlines():
			s = l.split('\t')
			n.write('{} {}\n'.format(s[0],s[1]))

g = nx.read_adjlist('../datasets/newOrleans.txt')
l = list(nx.connected_component_subgraphs(g))

nx.write_edgelist(l[0],'../datasets/newOrleansCon')
"""
with open('../datasets/newOrleansCon','r') as f:
	with open('../datasets/newOrleansConA', 'w+') as h:
		for l in f.readlines():
			s = l.split(' ')
			h.write('{} {}\n'.format(s[0],s[1]))
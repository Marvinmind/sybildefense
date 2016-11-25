import networkx as nx

g = nx.read_adjlist('/home/martin/Downloads/facebook_combined.txt')

partition = community.best_partition(g)
print(partition)

import networkx as nx
import matplotlib.pyplot as plt

g = nx.read_edgelist('../datasets/davidGraph.txt','r', nodetype=int, create_using = nx.DiGraph())
d = sorted(g.out_degree(list(range(len(g.nodes())))).values())
d_in = sorted(g.in_degree(list(range(len(g.nodes())))).values())

print(d)
print(d_in)

plt.plot(d)
plt.show()
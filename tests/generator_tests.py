import networkx as nx
import matplotlib.pyplot as plt

g = nx.barabasi_albert_graph(1000,15)

deg = g.degree(list(range(1000)))
print(deg)

deg = sorted(deg.values())
plt.plot(deg)
plt.show()

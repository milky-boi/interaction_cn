import networkx as nx
from random import seed
from random import randint
import matplotlib.pyplot as plt
#seed(1)

G=nx.Graph()

G.add_nodes_from([0,120])
for i in range(1120):
    
    start = randint(0, 1120)
    end = randint(0, 1120)
    G.add_edge(start, end)


nx.draw(G)
#nx.draw_circular(G)


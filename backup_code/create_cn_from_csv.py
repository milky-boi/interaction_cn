# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:57:43 2020

@author: icecream boi
"""
import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('distances_between_all_flies.csv', index_col=0)
df = df.T

indexes = []
weights = []
for i in range(len(df)):
    counter = 0
    row = df.iloc[i]
    for value in row:
        if value <= 10:
            counter +=1
        else:
            if counter >= 15:
                indexes.append(i)
                weights.append(float(counter/15))
                
            counter = 0
            
node_pairs = df.iloc[indexes].index.values.tolist()

dictionary = dict(zip(node_pairs, weights))

G=nx.Graph()
how_much_nodes = 17
nodes_list = list(range(1,how_much_nodes+1))

G.add_nodes_from(nodes_list)

print(G.nodes)

for pair in dictionary:
    start, end = pair.split(' ')
    start, end = int(start), int(end)
    weight_ = dictionary.get(pair)
    G.add_edge(start, end, weight=weight_)

#nx.draw(G)
nx.draw_circular(G,with_labels=True)
plt.savefig("graph.png")
plt.show()

number_of_nodes = len(G)
#number of edges
print(G.nodes)
nx.write_edgelist(G, "test.edgelist", data=False)
"""
pos = nx.spring_layout(G)
for weight in weights:
    #4 d. Form a filtered list with just the weight you want to draw
    weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
    width = weight
    nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width)

"""
    
    
    
    
    
    
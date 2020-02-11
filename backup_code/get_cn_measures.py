#loads undirected weighted edgelist
import networkx as nx
import matplotlib.pyplot as plt
import collections

def draw_bar(D, label):
    D = collections.OrderedDict(sorted(D.items()))
    plt.bar(range(len(D)),  list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys())) #[x+1 for x in 
    plt.title(label)
    name = label + '.png'
    plt.savefig(name)
    plt.show()
    
G=nx.read_adjlist("test.edgelist")
G = nx.convert_node_labels_to_integers(G)

#number of nodes
number_of_nodes = len(G)
#number of edges
print(number_of_nodes)
print(G.nodes())
nx.draw_circular(G, with_labels=True)
plt.show()
"""measures of prominence"""
#Degree centrality 
degree_centrality = nx.degree_centrality(G)
draw_bar(degree_centrality, 'degree_centrality')
    
#Degree centralization

#eigenvalue centrality.
eigenvector_centrality = nx.eigenvector_centrality(G)
draw_bar(eigenvector_centrality, 'eigenvector_centrality')

#Closeness centrality
closeness_centrality = nx.closeness_centrality(G)
draw_bar(closeness_centrality, 'closeness_centrality')

#Closeness centralization

#Betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)
draw_bar(betweenness_centrality, 'betweenness_centrality')

#Betweenness centralization

#Information centrality

#Page rank
page_rank = nx.pagerank(G, alpha=0.9)
draw_bar(page_rank, 'page rank')
#A weighted version of betweenness centrality
"""measures of range"""
#reach
#Number of edges separating the focal node from other nodes of interest
reach = nx.global_reaching_centrality(G, weight=None, normalized=True)
#diameter
diameter = nx.diameter(G, e=None)

"""measures of cohesion"""
#density
density = nx.density(G)

#reciprocity
reciprocity = nx.reciprocity(G, nodes=None)
#clustering coefficient 
clustering_coeff = nx.clustering(G)
#fragmentation
#fragmentation = 
#assortativity
#Compute degree assortativity of graph.
assortativity_degree = nx.degree_assortativity_coefficient(G)

#Compute degree assortativity of graph.	
assortativity_graph = nx.degree_pearson_correlation_coefficient(G)

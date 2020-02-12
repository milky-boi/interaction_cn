# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:31:53 2020

@author: icecream boi
"""
def draw_sorted_bar(D, label):
    #CHANGE TO LINE GRAPH
    sorted_d = dict(sorted(D.items(), key=operator.itemgetter(1), reverse=True))
    plt.bar(range(len(sorted_d)), list(sorted(D.values(), reverse=True)), align='center')
    plt.xticks(range(len(sorted_d)), list(sorted_d.keys()), rotation=60)  # [x+1 for x in

    name = label + '_sorted'
    name_png = 'results/' + label + '_sorted.png'
    plt.title(name)
    plt.savefig(name_png)
    #plt.clf()

def load_experiments:
    """takes path as input and return list of graphs from experiments and 
    names of experiments"""
    pass
    

def compare_experiments():
    """returns dataframe of numeric network values and 
    images of graphs created from sorted cn measures"""
    pass

def measures(G, exp_name):
    #Degree centrality
    degree_centrality = nx.degree_centrality(G)
    draw_sorted_bar(degree_centrality, 'Degree centrality')
    # Degree centralization MISSING

    # eigenvalue centrality.
    eigenvector_centrality = nx.eigenvector_centrality(G)
    draw_sorted_bar(eigenvector_centrality, 'Eigenvector centrality')

    # Closeness centrality
    closeness_centrality = nx.closeness_centrality(G)
    draw_sorted_bar(closeness_centrality, 'Closeness centrality')

    # Closeness centralization MISSING

    # Betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(G, weight=None)
    draw_sorted_bar(betweenness_centrality, 'Betweenness centrality')

    # Betweenness centrality WEIGHTED
    betweenness_centrality = nx.betweenness_centrality(G, weight=G.edges(data=True))
    draw_sorted_bar(betweenness_centrality, 'Betweenness centrality')
    # Betweenness centralization MISSING

    # Information centrality
    information_centrality = nx.information_centrality(G)
    draw_sorted_bar(information_centrality, 'Information centrality')

    # Page rank
    page_rank = nx.pagerank(G, alpha=0.9)
    draw_sorted_bar(page_rank, 'Page rank')

    #Clustering coeff
    clustering_coeff = nx.clustering(G)
    draw_sorted_bar(clustering_coeff, 'Clustering coeff')


def main():
    #load folder with .csv data for each flie
    path = ''
    load_experiments(path)
    experiments_edges = []
    experiments_names = []

    measures(G, experiments_names)

    compare_experiments(experiments_edges, experiments_names)

    
    
if __name__ == '__main__':
    main()
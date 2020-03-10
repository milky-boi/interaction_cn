# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:31:53 2020

@author: icecream boi
"""

import os
import community
import networkx as nx
import matplotlib.pyplot as plt

def draw_box_plot(d, title):
    # or backwards compatable    
    labels, data = [*zip(*d.items())]
    labels = [label[4:] for label in labels]
    data = [list(d.values()) for d in data]
          
    average_bsl = mean([mean(e) for e in data[0:5]])
    average_coc = mean([mean(e) for e in data[5:]])
    
    plt.axhline(y=average_bsl, color='blue', label='Mean BSL')
    plt.axhline(y=average_coc, color='red', label='Mean COC')
    
    plt.boxplot(data, labels)
    plt.title(title)
    plt.xticks(range(0, len(labels)+1), labels, rotation=60)
    plt.axvspan(5.5, 11.5, alpha=0.05, color='red', label='COC pop')
    plt.legend()
    plt.show()
    plt.cla()
    plt.clf()
    plt.close()

def compare_measures(experiments_dict):
    """

    :param g:
    :param exp_name:
    :return:
    """
    # Degree centrality
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path)    
        degree_centrality = nx.degree_centrality(g)
        d.update({exp_name[0:-4] : degree_centrality})
    draw_box_plot(d, 'degree_centrality')

    # eigenvalue centrality.
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path)    
        eigenvector_centrality = nx.eigenvector_centrality(g)
        d.update({exp_name[0:-4] : eigenvector_centrality})
    draw_box_plot(d, 'eigenvector_centrality')

    # Closeness centrality
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path) 
        closeness_centrality = nx.closeness_centrality(g)
        d.update({exp_name[0:-4] : closeness_centrality})
    draw_box_plot(d, 'closeness_centrality')

    # Betweenness centrality
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path) 
        betweenness_centrality = nx.betweenness_centrality(g, weight=None)
        d.update({exp_name[0:-4] : betweenness_centrality})
    draw_box_plot(d, 'betweenness_centrality')

    # Betweenness centrality WEIGHTED
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path) 
        betweenness_centrality_w = nx.betweenness_centrality(g, weight=g.edges(data=True))
        d.update({exp_name[0:-4] : betweenness_centrality_w})
    draw_box_plot(d, 'betweenness_centrality_weighted')
    

    # Information centrality
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path)
        gc = max(nx.connected_component_subgraphs(g), key=len)
        information_centrality = nx.information_centrality(gc)
        d.update({exp_name[0:-4] : information_centrality})
    draw_box_plot(d, 'information_centrality')

    # Page rank
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path)
        page_rank = nx.pagerank(g, alpha=0.9)
        d.update({exp_name[0:-4] : page_rank})
    draw_box_plot(d, 'page_rank')
    
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path)
        clustering_coeff_w = nx.clustering(g, weight='weight')
        d.update({exp_name[0:-4] : clustering_coeff_w})
    draw_box_plot(d, 'clustering coeff w')

def distances_box_plot(d):
    d = {}  
    for exp_name, path in experiments_dict.items():         
        g = nx.read_gml(path)    
        degree_centrality = nx.degree_centrality(g)
        d.update({exp_name[0:-4] : degree_centrality})
    draw_box_plot(d, 'degree_centrality')
    

def main():
    path = r'H:\0_theory\interaction_c_n\results\graphs'
    
    experiments_dicts = {}
    for r, d, f in os.walk(path):
        # f = natural_sort(f)
        for file in f:
            if '.gml' in file:
                experiments_dicts.update({file : os.path.join(r, file)})
    
    compare_measures(experiments_dicts)

        
    


if __name__ == '__main__':
    main()
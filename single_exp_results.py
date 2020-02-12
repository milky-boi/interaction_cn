import operator
import collections

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#import plotly.figure_factory as ff

from natsort import natsorted, ns
from statistics import mean

from networkx.algorithms.community import greedy_modularity_communities


def draw_bar(D, label):
    D = collections.OrderedDict(D.items())
    sortiranje = list(D.keys())
    nsorted = natsorted(sortiranje, key=lambda y: y.lower())

    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), nsorted, rotation=60)
    plt.title(label)

    name = 'results/' + label + '.png'
    plt.savefig(name)
    plt.clf()


def draw_sorted_bar(D, label):

    sorted_d = dict(sorted(D.items(), key=operator.itemgetter(1), reverse=True))
    plt.bar(range(len(sorted_d)), list(sorted(D.values(), reverse=True)), align='center')
    plt.xticks(range(len(sorted_d)), list(sorted_d.keys()), rotation=60)  # [x+1 for x in

    name = label + '_sorted'
    name_png = 'results/' + label + '_sorted.png'
    plt.title(name)
    plt.savefig(name_png)
    plt.clf()


def and_results(G, exp_name):

    total_nodes = len(G.nodes())
    total_edges = float(G.number_of_edges())
    average_degree = 2 * total_edges / total_nodes
    network_density = nx.density(G)

    # https://royalsocietypublishing.org/doi/full/10.1098/rsos.160757
    degree_heterogeneity = 'MISSING'
    degree_assortativity = nx.degree_assortativity_coefficient(G)

    betweenness_centrality = nx.betweenness_centrality(G)
    average_betw_cent_unweighted = mean(betweenness_centrality[k] for k in betweenness_centrality)

    betweenness_centrality_w = nx.betweenness_centrality(G)
    average_betw_cent_weighted = mean(betweenness_centrality_w[k] for k in betweenness_centrality)

    clustering_coeff = nx.clustering(G)
    average_cl_coeff_unweighted = mean(clustering_coeff[k] for k in clustering_coeff)

    clustering_coeff_w = nx.clustering(G)
    average_cl_coeff_weighted = mean(clustering_coeff_w[k] for k in clustering_coeff)
    # Find communities in graph using Clauset-Newman-Moore greedy modularity maximization.
    # This method currently supports the Graph class and does not consider edge weights.

    Newman_modularity = 'ERROR' #'#greedy_modularity_communities(G)
    maximum_modularity = 'ERROR'  # nx.modularity_matrix(G)
    relative_modularity = 'MISSING'

    group_cohesion = 'MISSING'
    network_diameter = nx.diameter(G, e=None)

    d = {'total_nodes': total_nodes, 'total_edges': total_edges, 'network_density': network_density,
         'average_degree': average_degree, 'degree_heterogeneity': degree_heterogeneity,
         'degree_assortativity': degree_assortativity,
         'average_betw_cent_unweighted': average_betw_cent_unweighted,
         'average_betw_cent_weighted': average_betw_cent_weighted,
         'average_cl_coeff_unweighted': average_cl_coeff_unweighted,
         'average_cl_coeff_weighted': average_cl_coeff_weighted, 'Newman_modularity': Newman_modularity,
         'maximum_modularity': maximum_modularity, 'relative_modularity': relative_modularity,
         'group_cohesion': group_cohesion, 'network_diameter': network_diameter}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/and_res_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())

    print('-----------------------ANIMAL-NETWORKS-DATASET-MEASURES-----------------------------')
    print(df.head)
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/and_res_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())

def dendogram(G):
    print(list(G.edges(data=True)))
    G_ = nx.to_numpy_matrix(G)
    fig = ff.create_dendrogram(G_)
    fig.update_layout(width=1000, height=500)
    fig.show()

def main_measures(G, exp_name):
    # average number of edges
    total_nodes = len(G.nodes())
    total_edges = float(G.number_of_edges())

    edges_ave = total_edges / total_nodes

    # Number of components
    ncc = nx.number_connected_components(G)
    # Biggest component size
    bcs = 'MISSING'

    # Global efficiency
    ge = nx.global_efficiency(G)

    # Global grouping coeff
    ggc = 'MISSING'
    # Ave grouping coeff
    agc = nx.average_clustering(G)

    degree_centrality = nx.degree_centrality(G)
    ave_val = mean(degree_centrality[k] for k in degree_centrality)

    betweenness_centrality = nx.betweenness_centrality(G, weight=None)
    ave_b_c = mean(betweenness_centrality[k] for k in betweenness_centrality)

    d = {'total_nodes': total_nodes, 'total_edges': total_edges, 'edges_ave': edges_ave,
         'number_of_components': ncc, 'bigges_component_size': bcs, 'Global efficiency': ge,
         'Global grouping coeff':ggc, 'Ave grouping coeff': agc, 'ave_degree_centrality': ave_val,
         'average betweenness centrality':ave_b_c}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/main_measures_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())
    print('-----------------------MAIN-MEASURES------------------------------------------------')
    print(df.head)
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/main_measures_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())


def measures_of_prominence(G, exp_name):
    #Degree centrality
    degree_centrality = nx.degree_centrality(G)
    draw_bar(degree_centrality, 'Degree centrality')
    draw_sorted_bar(degree_centrality, 'Degree centrality')
    # Degree centralization MISSING

    # eigenvalue centrality.
    eigenvector_centrality = nx.eigenvector_centrality(G)
    draw_bar(eigenvector_centrality, 'Eigenvector centrality')
    draw_sorted_bar(eigenvector_centrality, 'Eigenvector centrality')

    # Closeness centrality
    closeness_centrality = nx.closeness_centrality(G)
    draw_bar(closeness_centrality, 'Closeness centrality')
    draw_sorted_bar(closeness_centrality, 'Closeness centrality')

    # Closeness centralization MISSING

    # Betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(G, weight=None)
    draw_bar(betweenness_centrality, 'Betweenness centrality')
    draw_sorted_bar(betweenness_centrality, 'Betweenness centrality')

    # Betweenness centrality WEIGHTED
    betweenness_centrality = nx.betweenness_centrality(G, weight=G.edges(data=True))
    draw_bar(betweenness_centrality, 'Betweenness centrality')
    draw_sorted_bar(betweenness_centrality, 'Betweenness centrality')
    # Betweenness centralization MISSING

    # Information centrality
    information_centrality = nx.information_centrality(G)
    draw_bar(information_centrality, 'Information centrality')
    draw_sorted_bar(information_centrality, 'Information centrality')

    # Page rank
    page_rank = nx.pagerank(G, alpha=0.9)
    draw_bar(page_rank, 'Page rank')

def measures_of_range(G, exp_name):
    # Measures of range
    # reach
    # Number of edges separating the focal node from other nodes of interest
    reach = nx.global_reaching_centrality(G, weight=None, normalized=True)

    # diameter
    diameter = nx.diameter(G, e=None)

    # shortest path length,  eccentricity
    spl = 'MISSING'
    ecc = 'MISSING'

    d = {'reach': reach, 'diameter': diameter, 'shortest path length': spl,
         'eccentricity': ecc}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/measures_of_range_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())
    print('-----------------------MEASURES-OF-RANGE--------------------------------------------')
    print(df.head)
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/measures_of_range_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())

def measures_of_cohesion(G, exp_name):
    # Measures of cohesion
    # density
    density = nx.density(G)

    # reciprocity
    reciprocity = nx.reciprocity(G)

    # clustering coefficient
    clustering_coeff = nx.clustering(G)

    draw_bar(clustering_coeff, 'Clustering coeff')
    draw_sorted_bar(clustering_coeff, 'Clustering coeff')
    # fragmentation
    fragmentation = 'MISSING'

    # assortativity
    # Compute degree assortativity of graph.
    assortativity_degree = nx.degree_assortativity_coefficient(G)

    # Compute degree assortativity of graph.
    assortativity_graph = nx.degree_pearson_correlation_coefficient(G)

    d = {'density': density, 'reciprocity': reciprocity, 'fragmentation': fragmentation,
         'assortativity_degree': assortativity_degree, 'assortativity_graph': assortativity_graph}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/measures_of_cohesion_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())

    print('-----------------------MEASUERS-OF-COHESION-----------------------------------------')
    print(df.head)
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/measures_of_cohesion_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())

def main():
    exp_name = 'Exp1_16_01_2020_video_5'
    print('----------------------RESULTS FOR ->' + exp_name + '-------------------------')
    print('------------------------------------------------------------------------------------')
    path = r'/home/firestarter/interaction_cn/net.gml'
    G = nx.read_gml(path)

    and_results(G, exp_name)
    #dendogram(G)
    main_measures(G, exp_name)
    measures_of_prominence(G, exp_name)
    measures_of_range(G, exp_name)
    measures_of_cohesion(G, exp_name)

if __name__ == '__main__':
    main()
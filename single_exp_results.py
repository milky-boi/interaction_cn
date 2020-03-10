import os
import operator
import collections
import community
import pandas as pd
import networkx as nx

import matplotlib.pyplot as plt
# import plotly.figure_factory as ff

from natsort import natsorted  # ,ns
from statistics import mean, stdev


def draw_bar(d, label):
    """

    :param d:
    :param label:
    :return:
    """
    d = collections.OrderedDict(d.items())
    sortiranje = list(d.keys())
    nsorted = natsorted(sortiranje, key=lambda y: y.lower())

    plt.bar(range(len(d)), list(d.values()), align='center')
    plt.xticks(range(len(d)), nsorted, rotation=60)
    plt.title(label)

    name = 'results/' + label + '.png'
    plt.savefig(name, dpi=150)
    plt.clf()


def draw_sorted_bar(d, label):
    """

    :param d:
    :param label:
    :return:
    """
    axes = plt.gca()
    # axes.set_xlim([0,1])
    ymin = 0
    ymax = 0.4
    axes.set_ylim([ymin, ymax])
    sorted_d = dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))
    plt.bar(range(len(sorted_d)), list(sorted(d.values(), reverse=True)), align='center')
    plt.xticks(range(len(sorted_d)), list(sorted_d.keys()), rotation=60)  # [x+1 for x in

    name = label + '_sorted'
    name_png = 'results/img/' + label + '_sorted.png'
    plt.title(name)

    plt.savefig(name_png, dpi=150)
    plt.clf()


def and_results(g, exp_name):
    """

    :param g:
    :param exp_name:
    :return:
    """

    total_nodes = len(g.nodes())
    total_edges = float(g.number_of_edges())

    average_degree = 2 * total_edges / total_nodes

    network_density = nx.density(g)

    degree_distribution = dict(g.degree(weight='weight'))
    standard_deviation_degree = stdev(degree_distribution.values())
    degree_heterogeneity = standard_deviation_degree / average_degree

    degree_assortativity = nx.degree_assortativity_coefficient(g)

    betweenness_centrality = nx.betweenness_centrality(g)
    average_betw_cent_unweighted = mean(betweenness_centrality[k] for k in betweenness_centrality)

    betweenness_centrality_w = nx.betweenness_centrality(g, weight='weight')
    average_betw_cent_weighted = mean(betweenness_centrality_w[k] for k in betweenness_centrality)

    clustering_coeff = nx.clustering(g)
    average_cl_coeff_unweighted = mean(clustering_coeff[k] for k in clustering_coeff)

    clustering_coeff_w = nx.clustering(g, weight='weight')

    average_cl_coeff_weighted = mean(clustering_coeff_w[k] for k in clustering_coeff)

    part = community.best_partition(g)
    newman_modularity = community.modularity(part, g, weight='weight')
    maximum_modularity = 0  # nx.modularity_matrix(G)
    relative_modularity = 0  # newman_modularity / maximum_modularity

    group_cohesion = 'SS'

    gc = max(nx.connected_component_subgraphs(g), key=len)
    network_diameter = nx.diameter(gc, e=None)

    d = {'total_nodes': total_nodes, 'total_edges': total_edges, 'network_density': network_density,
         'average_degree': average_degree, 'degree_heterogeneity': degree_heterogeneity,
         'degree_assortativity': degree_assortativity,
         'average_betw_cent_unweighted': average_betw_cent_unweighted,
         'average_betw_cent_weighted': average_betw_cent_weighted,
         'average_cl_coeff_unweighted': average_cl_coeff_unweighted,
         'average_cl_coeff_weighted': average_cl_coeff_weighted, 'Newman_modularity': newman_modularity,
         'maximum_modularity': maximum_modularity, 'relative_modularity': relative_modularity,
         'group_cohesion': group_cohesion, 'network_diameter': network_diameter}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/csv_results/and_res_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())

    print('-----------------------ANIMAL-NETWORKS-DATASET-MEASURES-----------------------------')
    print(df.head)
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/tables/and_res_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())


def dendogram(g):
    """

    :param g:
    :return:
    """

    print(list(g.edges(data=True)))
    # g_ = nx.to_numpy_matrix(g)
    # fig = ff.create_dendrogram(g_)
    # fig.update_layout(width=1000, height=500)
    # fig.show()


def main_measures(g, exp_name):
    """

    :param g:
    :param exp_name:
    :return:
    """
    # average number of edges
    total_nodes = len(g.nodes())
    total_edges = float(g.number_of_edges())

    edges_ave = total_edges / total_nodes

    # Number of components
    ncc = nx.number_connected_components(g)
    # bggest component size
    gcc = sorted(nx.connected_components(g), key=len, reverse=True)
    bcs = len(g.subgraph(gcc[0]))
    # +max(nx.connected_component_subgraphs(g), key=len)

    # Global efficiency
    ge = nx.global_efficiency(g)

    # Global grouping coeff
    ggc = 'SSSSSS'
    # Ave grouping coeff
    agc = nx.average_clustering(g)

    degree_centrality = nx.degree_centrality(g)
    ave_val = mean(degree_centrality[k] for k in degree_centrality)

    betweenness_centrality = nx.betweenness_centrality(g, weight=None)
    ave_b_c = mean(betweenness_centrality[k] for k in betweenness_centrality)

    d = {'total_nodes': total_nodes, 'total_edges': total_edges, 'edges_ave': edges_ave,
         'number_of_components': ncc, 'biggest_component_size': bcs, 'Global efficiency': ge,
         'Global grouping coeff': ggc, 'Ave grouping coeff': agc, 'ave_degree_centrality': ave_val,
         'average betweenness centrality': ave_b_c}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/csv_results/main_measures_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())
    print('-----------------------MAIN-MEASURES------------------------------------------------')
    print(df.head)
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/tables/main_measures_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())


def measures_of_prominence(g, exp_name):
    """

    :param g:
    :param exp_name:
    :return:
    """
    # Degree centrality
    degree_centrality = nx.degree_centrality(g)
    # draw_bar(degree_centrality, 'Degree centrality')
    draw_sorted_bar(degree_centrality, 'degree_centrality' + exp_name)
    # Degree centralization MISSING

    # eigenvalue centrality.
    eigenvector_centrality = nx.eigenvector_centrality(g)
    # draw_bar(eigenvector_centrality, 'Eigenvector centrality')
    draw_sorted_bar(eigenvector_centrality, 'eigenvector_centrality' + exp_name)

    # Closeness centrality
    closeness_centrality = nx.closeness_centrality(g)
    # draw_bar(closeness_centrality, 'Closeness centrality')
    draw_sorted_bar(closeness_centrality, 'closeness_centrality' + exp_name)

    # Closeness centralization MISSING

    # Betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(g, weight=None)
    # draw_bar(betweenness_centrality, 'Betweenness centrality')
    draw_sorted_bar(betweenness_centrality, 'betweenness_centrality' + exp_name)

    # Betweenness centrality WEIGHTED
    betweenness_centrality = nx.betweenness_centrality(g, weight=g.edges(data=True))
    # draw_bar(betweenness_centrality, 'Betweenness centrality')
    draw_sorted_bar(betweenness_centrality, 'betweenness_centrality_weighted' + exp_name)
    # Betweenness centralization MISSING

    # Information centrality
    gc = max(nx.connected_component_subgraphs(g), key=len)
    information_centrality = nx.information_centrality(gc)
    # draw_bar(information_centrality, 'Information centrality')
    draw_sorted_bar(information_centrality, 'information_centrality' + exp_name)

    # Page rank
    page_rank = nx.pagerank(g, alpha=0.9)
    # draw_bar(page_rank, 'Page rank')
    draw_sorted_bar(page_rank, 'page_rank' + exp_name)


def measures_of_range(g, exp_name):
    """

    :param g:
    :param exp_name:
    :return:
    """
    # Measures of range
    # reach
    # Number of edges separating the focal node from other nodes of interest
    reach = nx.global_reaching_centrality(g, weight=None, normalized=True)

    # diameter
    gc = max(nx.connected_component_subgraphs(g), key=len)
    diameter = nx.diameter(gc, e=None)

    # shortest path length,  eccentricity
    spl = nx.average_shortest_path_length(gc)

    ecc = nx.eccentricity(gc)

    draw_sorted_bar(ecc, 'eccentricity')

    d = {'reach': reach, 'diameter': diameter, 'shortest path length': spl}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/measures_of_range_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())
    print('-----------------------MEASURES-OF-RANGE--------------------------------------------')
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/tables/measures_of_range_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())


def measures_of_cohesion(g, exp_name):
    """

    :param g:
    :param exp_name:
    :return:
    """
    # Measures of cohesion
    # density
    density = nx.density(g)

    # reciprocity
    reciprocity = nx.reciprocity(g)

    # clustering coefficient
    clustering_coeff = nx.clustering(g)

    # draw_bar(clustering_coeff, 'Clustering coeff')
    draw_sorted_bar(clustering_coeff, 'clustering_coeff' + exp_name)
    # fragmentation
    fragmentation = 'SSSSS'  # nx.dispersion(g)
    # print(fragmentation)
    # draw_sorted_bar(fragmentation, 'fragmentation')

    # assortativity
    # Compute degree assortativity of graph.
    assortativity_degree = nx.degree_assortativity_coefficient(g)

    # Compute degree assortativity of graph.
    assortativity_graph = nx.degree_pearson_correlation_coefficient(g)

    d = {'density': density, 'reciprocity': reciprocity, 'fragmentation': fragmentation,
         'assortativity_degree': assortativity_degree, 'assortativity_graph': assortativity_graph}

    df = pd.DataFrame(d, index=[exp_name])
    df = df.T

    name = 'results/csv_results/measures_of_cohesion_' + exp_name + '.csv'
    with open(name, 'w') as tf:
        tf.write(df.to_csv())

    print('-----------------------MEASUERS-OF-COHESION-----------------------------------------')
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/tables/measures_of_cohesion_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())


def main():
    
    ##first create folders to save results 
    os.mkdir('results/distances_traveled')
    os.mkdir('results/tables')
    os.mkdir('results/csv_results')
    os.mkdir('results/img')
    os.mkdir('results/graph_images')
    
    
    path = r'H:\0_theory\interaction_c_n\results\graphs'

    files = []
    exp_names = []
    for r, d, f in os.walk(path):
        # f = natural_sort(f)
        for file in f:
            if '.gml' in file:
                exp_names.append(file)
                files.append(os.path.join(r, file))
    print(exp_names)

    for i in range(0, len(files)):
        file = files[i]
        exp_name = exp_names[i]
        print('----------------------RESULTS FOR ->' + exp_name + '-------------------------')
        print('------------------------------------------------------------------------------------')
        g = nx.read_gml(file)

        nx.draw(g)  # networkx draw()
        plt.draw()
        plt.title(exp_name)
        plt.savefig('graph_images/' + exp_name + '.png')
        # plt.show()

        and_results(g, exp_name)
        # dendogram(g)
        main_measures(g, exp_name)
        measures_of_prominence(g, exp_name)
        measures_of_range(g, exp_name)
        measures_of_cohesion(g, exp_name)


if __name__ == '__main__':
    main()

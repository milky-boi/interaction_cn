import operator
import collections
#import community
from networkx import community
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#import plotly.figure_factory as ff

#from natsort import natsorted, ns
from statistics import mean, stdev

from networkx.algorithms.community import greedy_modularity_communities


def draw_bar(D, label):
    D = collections.OrderedDict(D.items())
    sortiranje = list(D.keys())
    #nsorted = natsorted(sortiranje, key=lambda y: y.lower())

    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), sortiranje, rotation=60)
    plt.title(label)

    name = 'results/' + label + '.png'
    plt.savefig(name, dpi=150)
    plt.clf()


def draw_sorted_bar(D, label):
    axes = plt.gca()
    #axes.set_xlim([0,1])
    ymin = 0 
    ymax = 0.4
    axes.set_ylim([ymin,ymax])
    sorted_d = dict(sorted(D.items(), key=operator.itemgetter(1), reverse=True))
    plt.bar(range(len(sorted_d)), list(sorted(D.values(), reverse=True)), align='center')
    plt.xticks(range(len(sorted_d)), list(sorted_d.keys()), rotation=60)  # [x+1 for x in

    name = label + '_sorted'
    name_png = 'results/img/' + label + '_sorted.png'
    plt.title(name)
    
    plt.savefig(name_png, dpi=150)
    plt.clf()


def and_results(G, exp_name):

    total_nodes = len(G.nodes())
    total_edges = float(G.number_of_edges())
    average_degree = 2 * total_edges / total_nodes
    network_density = nx.density(G)

    # https://royalsocietypublishing.org/doi/full/10.1098/rsos.160757

    degree_distribution = dict(G.degree())
    standard_deviation_degree = stdev(degree_distribution.values())
    degree_heterogeneity = standard_deviation_degree / average_degree
    
    degree_assortativity = nx.degree_assortativity_coefficient(G)

    betweenness_centrality = nx.betweenness_centrality(G)
    average_betw_cent_unweighted = mean(betweenness_centrality[k] for k in betweenness_centrality)

    betweenness_centrality_w = nx.betweenness_centrality(G)
    average_betw_cent_weighted = mean(betweenness_centrality_w[k] for k in betweenness_centrality)

    clustering_coeff = nx.clustering(G)
    average_cl_coeff_unweighted = mean(clustering_coeff[k] for k in clustering_coeff)

    clustering_coeff_w = nx.clustering(G)
    
    average_cl_coeff_weighted = mean(clustering_coeff_w[k] for k in clustering_coeff)

    from networkx.algorithms.community.quality import modularity
    
    Gc = nx.algorithms.community.modularity_max.greedy_modularity_communities(G, weight=None)
    
    Newman_modularity = 0
    
    maximum_modularity = 0 #nx.algorithms.community.modularity_max(G, Gc, weight='weight')
    relative_modularity = 0 # Newman_modularity / maximum_modularity

    group_cohesion = 'SS'
    
    Gc = max(nx.connected_component_subgraphs(G), key=len)
    network_diameter = nx.diameter(Gc, e=None)

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
    name = 'results/tables/and_res_' + exp_name + '.tex'
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
    bcs = 0 #max(nx.connected_component_subgraphs(G), key=len)

    # Global efficiency
    ge = nx.global_efficiency(G)

    # Global grouping coeff
    ggc = 'SSSSSS'
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
    name = 'results/tables/main_measures_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())

def measures_of_prominence(G, exp_name):
    #Degree centrality
    degree_centrality = nx.degree_centrality(G)
    #draw_bar(degree_centrality, 'Degree centrality')
    draw_sorted_bar(degree_centrality, 'degree_centrality'+exp_name)
    # Degree centralization MISSING

    # eigenvalue centrality.
    eigenvector_centrality = nx.eigenvector_centrality(G)
    #draw_bar(eigenvector_centrality, 'Eigenvector centrality')
    draw_sorted_bar(eigenvector_centrality, 'eigenvector_centrality' + exp_name)

    # Closeness centrality
    closeness_centrality = nx.closeness_centrality(G)
    #draw_bar(closeness_centrality, 'Closeness centrality')
    draw_sorted_bar(closeness_centrality, 'closeness_centrality' + exp_name)

    # Closeness centralization MISSING

    # Betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(G, weight=None)
    #draw_bar(betweenness_centrality, 'Betweenness centrality')
    draw_sorted_bar(betweenness_centrality, 'betweenness_centrality' + exp_name)

    # Betweenness centrality WEIGHTED
    betweenness_centrality = nx.betweenness_centrality(G, weight=G.edges(data=True))
    #draw_bar(betweenness_centrality, 'Betweenness centrality')
    draw_sorted_bar(betweenness_centrality, 'betweenness_centrality_weighted' + exp_name)
    # Betweenness centralization MISSING

    # Information centrality
    Gc = max(nx.connected_component_subgraphs(G), key=len)
    information_centrality = nx.information_centrality(Gc)
    #draw_bar(information_centrality, 'Information centrality')
    draw_sorted_bar(information_centrality, 'information_centrality' + exp_name)

    # Page rank
    page_rank = nx.pagerank(G, alpha=0.9)
    #draw_bar(page_rank, 'Page rank')
    draw_sorted_bar(page_rank, 'page_rank' + exp_name)

def measures_of_range(G, exp_name):
    # Measures of range
    # reach
    # Number of edges separating the focal node from other nodes of interest
    reach = nx.global_reaching_centrality(G, weight=None, normalized=True)

    # diameter
    Gc = max(nx.connected_component_subgraphs(G), key=len)
    diameter = nx.diameter(Gc, e=None)

    # shortest path length,  eccentricity
    spl = nx.average_shortest_path_length(Gc)
    
    ecc = nx.eccentricity(Gc)

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

def measures_of_cohesion(G, exp_name):
    # Measures of cohesion
    # density
    density = nx.density(G)

    # reciprocity
    reciprocity = nx.reciprocity(G)

    # clustering coefficient
    clustering_coeff = nx.clustering(G)

    #draw_bar(clustering_coeff, 'Clustering coeff')
    draw_sorted_bar(clustering_coeff, 'clustering_coeff' + exp_name)
    # fragmentation
    fragmentation = 'SSSSS'#nx.dispersion(G)
    #print(fragmentation)
    #draw_sorted_bar(fragmentation, 'fragmentation')

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
    print('------------------------------------------------------------------------------------')

    # SAVE TABLE TO TEX
    name = 'results/tables/measures_of_cohesion_' + exp_name + '.tex'
    with open(name, 'w') as tf:
        tf.write(df.to_latex())

def main():
    #path = path = r'H:\0_theory\interaction_c_n\results\18_02_12_04.gml'
    #exp_name = '18_02_12_04' 
    #print('----------------------RESULTS FOR ->' + exp_name + '-------------------------')
    #print('------------------------------------------------------------------------------------')
    
    
    path = path = r'H:\0_theory\interaction_c_n\graphs'

    files = []
    exp_names = []
    for r, d, f in os.walk(path):
        f = natural_sort(f)
        for file in f:
            if '.gml' in file:
                exp_names.append(file)
                files.append(os.path.join(r, file))   
    print(exp_names)
    
    for i in range(0,len(files)):
        file = files[i]
        exp_name = exp_names[i]
        print('----------------------RESULTS FOR ->' + exp_name + '-------------------------')
        print('------------------------------------------------------------------------------------')
        G = nx.read_gml(file)
        nx.draw(G)  # networkx draw()
        plt.draw()  
        plt.title(exp_name)
        plt.show()
        
        and_results(G, exp_name)
        #dendogram(G)
        main_measures(G, exp_name)
        measures_of_prominence(G, exp_name)
        measures_of_range(G, exp_name)
        measures_of_cohesion(G, exp_name)

if __name__ == '__main__':
    main()
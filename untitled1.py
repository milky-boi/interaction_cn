# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 02:41:45 2020

@author: icecream boi
"""
from statistics import mean 

path = r'H:\0_theory\interaction_c_n\results\graphs'

experiments_dicts = {}
for r, d, f in os.walk(path):
    # f = natural_sort(f)
    for file in f:
        if '.gml' in file:
            experiments_dicts.update({file : os.path.join(r, file)})
            
experiments_dicts

d = {}  
for exp_name, path in experiments_dicts.items():         
    g = nx.read_gml(path)    
    degree_centrality = nx.degree_centrality(g)
    d.update({exp_name[0:-4] : degree_centrality})

labels, data = [*zip(*d.items())]
labels = [label[4:] for label in labels]
data = [list(d.values()) for d in data]

averages = [sum(e)/len(e) for e in data]
average_bsl = mean([mean(e) for e in data[0:5]])
average_coc = mean([mean(e) for e in data[5:]])





# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 22:51:11 2020

@author: icecream boi
"""
import os
import pandas as pd

path = r'H:\0_theory\interaction_c_n\results\csv_results'
#path1 = r'H:\0_theory\interaction_c_n\results_e1_v5\csv_results'

files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))
            
frames = [pd.read_csv(file, index_col=0) for file in files]

df = pd.concat(frames)

df1 = df.drop(['total_edges', 'total_nodes', 'degree_heterogeneity', 'Newman_modularity', 'maximum_modularity', 'relative_modularity',
              'group_cohesion', 'bigges_component_size', 'Global grouping coeff',
              'fragmentation', 'shortest path length', 'eccentricity'])
    
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

df1['Exp1_16_01_2020_video_3'] = df1['Exp1_16_01_2020_video_3'].astype(float)









sn.set(font_scale=1.4) # for label size
sn.heatmap(df1, annot=True, annot_kws={"size": 16}) # font size

plt.show()

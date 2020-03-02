# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 23:52:21 2020

@author: icecream boi
"""
import os
import math
import pandas as pd  

import matplotlib.pyplot as plt
import numpy as np

def distances(x): 
    return math.sqrt((x['pos x2'] - x['pos x1'])**2 + (x['pos y2'] - x['pos y1'])**2)  


path = r'H:\0_theory\interaction_c_n\raw_data\18_02_12_04'
exp_name = '16_01_11_25'
#path1 = r'H:\0_theory\interaction_c_n\results_e1_v5\csv_results'

files = []
all_distances = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))
            
for file in files:         
    df = pd.read_csv(file)
    df1 = df[['pos x', 'pos y']]
    print(file)
    
    df2 = df[['pos x', 'pos y']]
    
    df1.drop(df.tail(1).index,inplace=True) # drop last n rows
    df1.reset_index(drop=True, inplace=True)
    df2.drop(df.head(1).index,inplace=True)
    df2.reset_index(drop=True, inplace=True)
    
    x1 = df1['pos x']-600 
    y1 = df1['pos y']
    x2 = df2['pos x']-600 
    y2 = df2['pos y']  
         
    df = pd.concat([x1, y1, x2, y2], axis=1)
    df.columns = ['pos x1', 'pos y1', 'pos x2', 'pos y2']
    lines = df.plot.line(x='pos x1', y='pos y1')
    res_apply = df.apply(distances, axis=1)
    res_apply = list(res_apply)    
    res_apply = [x for x in res_apply if (math.isnan(x) == False)]
    res_apply = sum(res_apply)
    all_distances.append(res_apply)    

num_l = [x for x in range(1,int(len(all_distances)+1))]
all_distances = sorted(all_distances, reverse=True)

plt.bar(num_l, all_distances)
plt.ylabel('Distance', fontsize=12)
plt.xlabel('No of flies', fontsize=12)
plt.xticks(num_l,fontsize=12)
plt.title(exp_name)
plt.show()

name = 'results/img/' + exp_name + '.png'
plt.savefig(name, dpi=150)






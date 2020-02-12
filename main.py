# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:26:47 2020

@author: icecream boi
"""
import os
import pandas as pd 
import math 
import time 
import numpy as np
import re

import networkx as nx
import matplotlib.pyplot as plt
import collections

def distances_f(df1, df2):
    distances = []
    for i in range(len(df1)):
        x1 = df1.iloc[i]['pos x']
        y1 = df1.iloc[i]['pos y']        
        x2 = df2.iloc[i]['pos x']
        y2 = df2.iloc[i]['pos y']
        
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distances.append(dist)
        
    return distances

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key)] 
    
    return sorted(l, key = alphanum_key)

def distances_to_csv(path, exp_name):
    
    start_time = time.time()
    
    files = []

    for r, d, f in os.walk(path):
        f = natural_sort(f)
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file))   

    all_distances = []
    all_pairs = []
    
    for i in range(len(files)):
        start_time = time.time()

        df1 = pd.read_csv(files[i])   
        next_flie = i + 1
        
        if next_flie <= len(files):     
            for j in range(next_flie, len(files)):
                df2 = pd.read_csv(files[j])         
                all_distances.append(distances_f(df1, df2))
                all_pairs.append(str(i) + ' ' + str(j))
        
        clean_time = time.time()-start_time      
        print('flie ' + files[i][-9:-4] + " calc in: %.2f" % clean_time + " seconds")
        
    df = pd.DataFrame.from_records(all_distances)
    df.replace(r'^\s*$', np.nan, regex=True)
    df= df.fillna(999)
    df= df.T
    df.columns = all_pairs
    
    name = 'results/' + exp_name + '_distances_between_all_flies.csv'
    df.to_csv(name)
    
    clean_time = time.time()-start_time
    print("Distances calculated in %.2f" % clean_time + " seconds")
    print('distances between all flies saved to .csv')
    print(df.head())
    return df
    
def cn_from_csv(df, distance, duration, exp_name):
    """Takes df, distance, duration_of_touch, exp_name as input and returns
    edgelist calculated between flies for given distance and time"""
    
    start_time = time.time()
    print(df.head())
    
    df = df.T
    
    indexes = []
    weights = []
    for i in range(len(df)):
        counter = 0
        row = df.iloc[i]
        for value in row:
            if value <= distance:
                counter +=1
            else:
                if counter >= duration:
                    indexes.append(i)
                    weights.append(float(counter/duration))                  
                counter = 0
                
    node_pairs = df.iloc[indexes].index.values.tolist()   
    dictionary = dict(zip(node_pairs, weights))
    
    G=nx.Graph()   
    print(G.nodes)
    
    for pair in dictionary:
        start, end = pair.split(' ')
        start, end = int(start), int(end)
        weight_ = dictionary.get(pair)
        G.add_edge(start, end, weight=weight_)
    
    print(G.nodes)
    
    name = 'results/' + exp_name + '.edgelist'
    
    nx.write_edgelist(G, name, data=False)
    
    clean_time = time.time()-start_time
    print("Distances calculated in %.2f" % clean_time + " seconds")
    print('Interaction edgelist created and saved in .edgelist')
    
    return G


def main():
    #load folder with .csv data for each flie
    path = r'H:\0_theory\interaction_c_n\data'
    exp_name = 'test_1'
    
    df = distances_to_csv(path, exp_name)
    
    distance = 10
    duration = 15
    cn_from_csv(df, distance, duration, exp_name)
    
    #cn_results_script(edgelist)
    
    
    

    #CREATE log file track program execution time and memory usage
    
if __name__ == '__main__':
    main()
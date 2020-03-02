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

def distances(x): 
    return math.sqrt((x['pos x2'] - x['pos x1'])**2 + (x['pos y2'] - x['pos y1'])**2)  

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key)] 
    
    return sorted(l, key = alphanum_key)

def distances_to_csv(path, exp_name):
    """ Loads files with flies positions in each frame, and returns distances between flies inf 
    that frame.
    Function returns .csv file, number of rows in the table corresponds to the number of frames in the video,
    Number of columns is equal to the formula (n-1)*n / 2 where is n, number of flies.
    """
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
        df1 = pd.read_csv(files[i])
        x1 = df1['pos x']
        y1 = df1['pos y'] 
        next_flie = i + 1
        if next_flie <= len(files):     
            for j in range(next_flie, len(files)):         
                df2 = pd.read_csv(files[j])   
                x2 = df2['pos x']
                y2 = df2['pos y']
                
                df = pd.concat([x1, y1, x2, y2], axis=1)
                df.columns = ['pos x1', 'pos y1', 'pos x2', 'pos y2']
                
                res_apply = df.apply(distances, axis=1)
                res_apply = list(res_apply)
                
                all_distances.append(res_apply)                
                all_pairs.append(str(i) + ' ' + str(j))
        
    df = pd.DataFrame.from_records(all_distances)
    """
    df.replace(r'^\s*$', np.nan, regex=True)
    df= df.fillna(999)
    """
    df= df.T
    df.columns = all_pairs
    
    name = 'results/all_distances/' + exp_name + '_distances_between_all_flies.csv'
    df.to_csv(name)
    
    
    
    clean_time = time.time()-start_time
    
    f= open("log_file.txt","a+")
    f.write('exp_name:' + exp_name + ' files:' + str(len(files)) + 
            ' rows:' + str(len(df1)) + " distances_proc_time(s): %.2f" % clean_time + " seconds\n")
    
    f.close() 
    
    print(exp_name + ' distances between all flies saved to .csv')
    print(df.head())
    
    
    return df
    
def cn_from_csv(df, distance, duration_sec, fps, exp_name):
    """Takes df, distance, duration_of_touch, exp_name as input and returns
    edgelist calculated between flies for given distance and time"""   
    start_time = time.time()
    print(df.head())
    #df = df.T
    duration = int(duration_sec*fps)
    G=nx.Graph()  
    
    res = (" ".join(["".join(pair) for pair in list(df.columns)])).split(' ')
    mylist = list(dict.fromkeys(res))
    G.add_nodes_from(mylist)
    
    for column in df.columns:
        df1 = df[column]  
        mask = df1 < 80
        
        df_r = df1[mask]
    
        counter = 0
        for i in range(len(df_r)):           
            value = df_r.iloc[i]   
            if value <= distance:               
                counter +=1
            else:
                if counter > duration:
                    start, end = column.split(' ')
                    weight_ = float(fps/counter)                    
                    G.add_edge(start, end, weight=weight_)                      
                counter = 0
                
    nx.draw(G)
    
    name = 'results/graphs/' + exp_name + '.edgelist'    
    nx.write_edgelist(G, name, data=True)
    
    name = 'results/graphs/' + exp_name + '.gml'    
    nx.write_gml(G, name)
    
    clean_time = time.time()-start_time
    
    f= open("log_file.txt","a+")
    f.write("network_creation_time:%.2f" % clean_time + " seconds \Nn)
    f.close
    print(exp_name + 'Interaction edgelist created and saved in .gml and .edgelist')
    
    #return G


def main():
    """
    The program takes a folder containing a .csv record of measures that quantify
    the behavior of each individual over a period of time. 
    Using the distances_to_csv () function, it compares individuals relationships
    over time (for example, distance between units in time) and returns .csv file.
    The cn_from_csv () function takes a previously created .csv file and 
    reutrns a weighted network based on the given parameters.
    """
    
    path = r'H:\0_theory\interaction_c_n\raw_data'
    
    experiments = {}
    
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for folder in d:
            experiments.update({folder : os.path.join(r, folder)})
    
    
    #load folder with .csv data for each flie
 
    
    for exp_name, path in experiments.items():
    #create cv of distacnes between flies 
        df = distances_to_csv(path, exp_name)
        
        #interaction criteria for network creation
        distance = 20 #px distance, arena is 120mm wide, 1000x1000 on x,y axis
        duration_sec = 0.6
        
        #video fps
        fps = 24
        
        #create net
        cn_from_csv(df, distance, duration_sec, fps, exp_name)


    #CREATE log file track program execution time and memory usage
    
if __name__ == '__main__':
    main()
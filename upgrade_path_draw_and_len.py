# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 23:52:21 2020

@author: icecream boi
"""
import os
import csv
import math
import operator 
import pandas as pd  

import matplotlib.pyplot as plt
import numpy as np

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
    
    
def distances(x): 
    return math.sqrt((x['pos x2'] - x['pos x1'])**2 + (x['pos y2'] - x['pos y1'])**2)  

def distance_traveled(path, exp_name):
    flies = {}
    
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                flies.update({file : os.path.join(r, file)})
    
    fly_distances = {}   
     
    for fly, path in flies.items():   
        fly = fly[0:-4]      
        df = pd.read_csv(path)
        df1 = df[['pos x', 'pos y']]
        #print(fly)
        
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
        res_apply = list(df.apply(distances, axis=1))
        res_apply = sum([x for x in res_apply if (math.isnan(x) == False)])
        fly_distances.update({fly : res_apply})  
        
    
    with open('results/distances_traveled/' + exp_name + '_traveled_distance.csv', 'w') as f:
        for key in fly_distances.keys():
            f.write("%s,%s\n"%(key,fly_distances[key]))
    
    return fly_distances



def main():
    """
    """
    
    path = r'H:\0_theory\interaction_c_n\raw_data'
    
    experiments = {}
    
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for folder in d:
            experiments.update({folder : os.path.join(r, folder)})
    
    #load folder with .csv data for each flie
    all_distances_traveled = {}
    
    for exp_name, path in experiments.items():
    #create cv of distacnes between flies 
        d = distance_traveled(path, exp_name)
        all_distances_traveled.update({exp_name : d})
    
    draw_box_plot(all_distances_traveled, 'distances traveled')    
    
if __name__ == '__main__':
    main()








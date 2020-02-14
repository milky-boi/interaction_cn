# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:57:24 2020

@author: icecream boi
"""

import pandas as pd 
import networkx as nx
import time 

start_time = time.time()

df = pd.read_csv('test.csv', index_col=0)
#df = df['fly1 fly3']
#print(type(df[1]))

distance = 250
duration = 15
indexes = []
weights = []
G=nx.Graph()  

for column in df.columns:
    df1 = df[column]  
    mask = df1 < 500
    
    df_r = df1[mask]
    #print(len(df_r))
    counter = 0
    for i in range(len(df_r)):
        
        value = df_r.iloc[i]

        if value <= distance:
            
            counter +=1
        else:
            if counter > 15:
                start, end = column.split(' ')
                weight_ = float(counter/duration)
                
                G.add_edge(start, end, weight=weight_)
                
                 
            counter = 0
            

print(G.nodes)

clean_time = time.time()-start_time
print("Distances calculated in %.2f" % clean_time + " seconds")
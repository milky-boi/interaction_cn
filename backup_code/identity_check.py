#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:45:01 2020

@author: firestarter
"""
import os 
import re
import matplotlib.pyplot as plt
import pandas as pd 

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    
    return sorted(l, key = alphanum_key)


path = r'/home/firestarter/interaction_c_n/data'
files = []
for r, d, f in os.walk(path):
    f = natural_sort(f)
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))  
            
sorted_ = natural_sort(f)

def draw_graph(df):
    df.plot.line()

for file in files:
    df = pd.read_csv(file)
    
    df = df[['pos x', 'pos y']]
    df.set_index('pos x', inplace=True)
    
    df.plot(legend=True)

    plt.show()
    
    
    #x1.plot.line()
    #y1.plot.line()      
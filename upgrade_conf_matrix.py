# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 22:51:11 2020

@author: icecream boi
"""
import os
import pandas as pd

path = r'H:\0_theory\interaction_c_n\raw_data\21_02_v1'
#path1 = r'H:\0_theory\interaction_c_n\results_e1_v5\csv_results'

files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))            
# frames = [pd.read_csv(file, index_col=0) for file in files]
# df = pd.concat(frames)

# import the required packages
from scipy import stats, integrate
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

frames = [pd.read_csv(file, index_col=0) for file in files]
df = pd.concat(frames)

df = df.round(0)
# load the coordinates file

x = df['pos x']
y = df['pos y']

# call the kernel density estimator function
fig, ax = plt.subplots()
fig.set_size_inches(14,4)

sns.kdeplot(x, y, shade="True", n_levels=40)

plt.show()


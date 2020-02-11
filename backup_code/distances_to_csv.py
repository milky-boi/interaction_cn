"""
this part of script loads .csv tracking files of each flie. 
Every row are values taken from each frame by Flytrack software
"""
import os
import pandas as pd 
import math 
import time 
import numpy as np
import re

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

#def distances_flies():

start_time = time.time()

path = r'/home/firestarter/interaction_c_n/data'
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
    next_flie = i + 1
    
    if next_flie <= len(files):     
        for j in range(next_flie, len(files)):
            df2 = pd.read_csv(files[j])         
            all_distances.append(distances_f(df1, df2))
            all_pairs.append(str(i) + ' ' + str(j))
               
df = pd.DataFrame.from_records(all_distances)
df.replace(r'^\s*$', np.nan, regex=True)
df= df.fillna(999)
df= df.T
df.columns = all_pairs

df.to_csv('distances_between_all_flies.csv')

clean_time = time.time()-start_time
print("Distances calculated in %.2f" % clean_time + " seconds")
print('distances between all flies saved to .csv')

"""
def main():
    distances_flies()
    
if __name__ == '__main__':
    main()
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:16:15 2020

@author: icecream boi
"""

import pandas as pd 

experiments = {}

for r, d, f in os.walk(path):
    for file in f:
        if '.xls' in file:
            experiments.update({file:os.path.join(r, file)})  


for exp_name, xlsx_file in experiments.items():
    xls = pd.ExcelFile(xlsx_file)
    

    print(len(xls.sheet_names))
    
    names = ['fly'+str(n) for n in range(1, len(xls.sheet_names))]
    
    
    df = [pd.read_excel(xls, fly) for fly in names]
     	
    os.mkdir(exp_name)
    names = [exp_name+'/'+name+'.csv' for name in names]
    
    for i in range (0,len(df)) :
        name = names[i]
        df_s = df[i]
        df_s = df_s[['pos x', 'pos y']]
        df_s.to_csv(name, index=True)



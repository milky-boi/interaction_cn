# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:31:53 2020

@author: icecream boi
"""
def load_experiments:
    """takes path as input and return list of graphs from experiments and 
    names of experiments"""
    pass
    

def compare_experiments():
    """returns dataframe of numeric network values and 
    images of graphs created from sorted cn measures"""
    pass

def main():
    #load folder with .csv data for each flie
    path = ''
    load_experiments(path)
    experiments_edges = []
    experiments_names = []
    
    compare_experiments(experiments_edges, experiments_names)

    
    
if __name__ == '__main__':
    main()
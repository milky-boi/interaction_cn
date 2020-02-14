def distances(x): 
    return math.sqrt((x['pos x2'] - x['pos x1'])**2 + (x['pos y2'] - x['pos y1'])**2)  

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
    
    name = 'results/' + exp_name + '_distances_between_all_flies.csv'
    df.to_csv(name)
    
    clean_time = time.time()-start_time
    print("Distances calculated in %.2f" % clean_time + " seconds")
    print('distances between all flies saved to .csv')
    print(df.head())
    return df
import numpy as np
import pandas as pd

def to_df(dinnerfood):
    dates = list(dinnerfood.keys())
    feats = np.empty((0,2))
    others = list(dinnerfood.values())
    for tuple in dates:
        feat = np.asarray(tuple)
        feats = np.vstack((feats,feat))

    data = pd.DataFrame(data=feats, columns = ['Date','Day'])

    for x in data.index:
        for item in others[x]:
            data[item] = 0
            data.loc[x,item] = 1
    
    return data
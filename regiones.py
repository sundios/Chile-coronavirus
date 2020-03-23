#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 00:21:43 2020

@author: konradburchardt
"""
### Regiones Day by day
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob


#Files that we want to run to get totals
files = sorted(glob.glob('*-coronavirus-chile.csv'))

#opening all files
li = []
for f in files:
    df = pd.read_csv(f,index_col=False)
    print(df)
    li.append(df)

#concatenating all Dataframes into one
df = pd.concat(li)

#Getting list of regions
regiones = df['Region']

#deduplicate
regiones = list(dict.fromkeys(regiones))

#sort by region and Date
df = df.sort_values(by=['Region','Dates'])

#grouping regiones together by date
r=[]
for j in range(1):
    print(j)
    for i in regiones:
        print(i)
        r.append(df.loc[df['Region'] == i])


#Groupping Regions by totals
        
group_region = df.groupby(['Region']).sum()





        
        
        



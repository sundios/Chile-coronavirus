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
from corona import daily


#Files that we want to run to get totals
files = sorted(glob.glob('/usr/local/airflow/dags/*-coronavirus-chile.csv'))

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

df = df[['Region','Nuevos Casos','Casos Totales','Fallecidos','Recuperados','Dates']]

df["Dates"] = pd.to_datetime(df["Dates"]).dt.strftime("%Y-%m-%d")

daily = daily.sort_values(by=['Fecha'])

#grouping regiones together by date
r=[]
for j in range(1):
    print(j)
    for i in regiones:
        print(i)
        r.append(df.loc[df['Region'] == i])


#Groupping Regions by totals
        
group_region = df.groupby(['Region']).sum()


import datetime
import pygsheets

#***** CONNECTION TO GOOGLE SHEETS *****

gc = pygsheets.authorize(service_file='/usr/local/airflow/dags/corona-271822-557422d15ba0.json')

#open the google spreadsheet 
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FeE8dWfdFJi8lgi_sVg2Qn5xHM9wvP8eB7tB39lm374/edit#gid=0')

                    

#***** PUSHING DATA TO EACH OF THE REGIONES WORKSHEET. THIS IS FOR ALL REGIONES GRAPHS. *****

# Pushing Regiones values to Google Sheets
for j in range(1,18):
    print(j)
    wsheet = sh[j]
    wsheet.set_dataframe(r[j-1],'A1',copy_head=True)
    



        
        
        



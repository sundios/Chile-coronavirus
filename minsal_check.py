#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:46:56 2020

@author: konradburchardt
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import glob


def minsal():
    #URL to scrape data
    url = "https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/"
    page = requests.get(url)
    
    #Parsing HTML
    soup = BeautifulSoup(page.text, 'html.parser')
    print(soup.prettify())
    
    
    #exporting thee table that we want
    rows = []
    for tr in soup.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    
    
    #transforming scraped data(text) into a dataframe with new columns
    df = pd.DataFrame(rows, columns =  ['Region', 'Nuevos Casos', 'Casos Totales','% Casos totales','Fallecidos'])
    
    #Selecting nunmber from todays data to compare
    df = df.iloc[18:19, 2]
    
    #removing . in thousand separator
    df = df.str.replace(".","")
    
    df = int(float(df))
    
    #Files that we want to run to get totals
    #files = sorted(glob.glob('/usr/local/airflow/dags/*-coronavirus-chile.csv'))
    
    #test locally
    files = sorted(glob.glob('*-coronavirus-chile.csv'))
    
    dates=[]
    totals = []
    totals_daily =[]
    recuperados = []
    fallecidos = []
    for f in files:
        df1 = pd.read_csv(f,index_col=False)
        print(f)
        d = df1.iloc[0:1,6]
        d = d.to_string(index=False)
        t = df1.iloc[16:,2]
        t = t.to_string(index=False)
        td = df1.iloc[16:,1]
        td = td.to_string(index=False)
        f = df1.iloc[16:,4]
        f = f.to_string(index=False)
        r = df1.iloc[16:,5]
        r = r.to_string(index=False)
        totals.append(t)
        dates.append(d)
        totals_daily.append(td)
        recuperados.append(r)
        fallecidos.append(f)
        
    
    #zipping 3 new df into one
    daily = pd.DataFrame(list(zip(dates,totals,totals_daily,recuperados,fallecidos)),
                  columns=['Fecha','Casos Totales','Nuevos Casos Diarios','Recuperados','Fallecidos'])
    
    #float numbers
    daily['Casos Totales'] = daily['Casos Totales'].astype(float)
    daily['Nuevos Casos Diarios'] = daily['Nuevos Casos Diarios'].astype(float)
    daily['Recuperados'] = daily['Recuperados'].astype(float)
    daily['Fallecidos'] = daily['Fallecidos'].astype(float)
    
    
    daily["Fecha"] = pd.to_datetime(daily["Fecha"]).dt.strftime("%Y-%m-%d")
    
    daily = daily.sort_values(by=['Fecha'])
    
    
    #Selecting Last row of Daily. (Yesterday data to compare)
    daily = daily.iloc[-1, 1]
    
    #removing . in thousand separator
    daily = int(float(daily))
    
    #Checking if Yesterday total value is same as today. If different we will run our script
    print(daily)
    print(df)
    
    checker(df,daily)



def checker(df,daily):
    import subprocess
    import time
    

    #checking if minsal has uploaded the data
    while df == daily:
        #this means data has not been updated yet
        No = 'did Minsal updated the data? No they havent, they are still sleeping. Data is the same as yesterday'
        #Sleep for 5 minutes and then check again
        time.sleep(5)
        print(No)
        minsal()
       
    else:
        #This means data is not the same so minsal has changed the data
        Yes = 'did Minsal updated the data? Yes! they have. So now we should run all our scripts.'
        print(Yes)
        
minsal()


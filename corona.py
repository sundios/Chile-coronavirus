#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:36:31 2020

@author: konradburchardt
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import glob

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
df = pd.DataFrame(rows, columns =  ['Region', 'Nuevos Casos', 'Casos Totales'])


#creating date column
dates = datetime.date.today().strftime("%d-%m-%Y")

df['Dates'] =  dates

#removing noise and selecting only columns we need
df = df.iloc[2:19]

# Convert everything to float values
df['Nuevos Casos']= df['Nuevos Casos'].astype(float)
df['Casos Totales']= df['Casos Totales'].astype(float)

#creating new DF to plot without total values
df_plot =  df.iloc[2:16]




#plotting New cases and all cases of Chile

img_file = 'Images/' + datetime.date.today().strftime("%d-%m-%Y")
title = 'Corona Virus en Chile ' + datetime.date.today().strftime("%d-%m-%Y")

plt.plot(df_plot['Region'],df_plot['Nuevos Casos'], label = "Nuevos Casos")
plt.plot(df_plot['Region'],df_plot['Casos Totales'], label = "Casos Totales")
plt.ylabel('# Casos')
plt.title(title )
plt.xlabel('Regiones')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(img_file)
plt.show()


#exporting dataframe to CSV with date

#filename with date
filename = datetime.date.today().strftime("%d-%m-%Y")+'-coronavirus-chile.csv'

#here we export it to CSV
df.to_csv(filename,index=False)


#Files that we want to run to get totals
files = sorted(glob.glob('*-coronavirus-chile.csv'))


dates=[]
totals = []
totals_daily =[]
for f in files:
    df1 = pd.read_csv(f,index_col=False)
    print(f)
    d = df1.iloc[0:1,3]
    d = d.to_string(index=False)
    t = df1.iloc[16:,2]
    t = t.to_string(index=False)
    td = df1.iloc[16:,1]
    td = td.to_string(index=False)
    totals.append(t)
    dates.append(d)
    totals_daily.append(td)
    
#xipping 3 new df into one
daily = pd.DataFrame(list(zip(dates, totals,totals_daily)),
              columns=['Fecha','Casos Totales','Nuevos Casos Diarios'])

#float numbers
daily['Casos Totales'] = daily['Casos Totales'].astype(float)
daily['Nuevos Casos Diarios'] = daily['Nuevos Casos Diarios'].astype(float)


#plotting
img_file2 = 'Images/'+ datetime.date.today().strftime("%d-%m-%Y") + 'Totales-Chile'
title2 = 'Corona Virus en Chile Totales ' + datetime.date.today().strftime("%d-%m-%Y")

plt.plot(daily['Fecha'],daily['Casos Totales'], label = "Casos Totales")
plt.plot(daily['Fecha'],daily['Nuevos Casos Diarios'], label = "Nuevos Casos Diarios")
plt.ylabel('# Casos')
plt.xlabel('Fecha')
plt.title(title2)
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(img_file2)
plt.show()



    
        
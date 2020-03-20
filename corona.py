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

#removing noise and selecting only columns we need
df = df.iloc[2:19]

# Convert everything to float values
df['Nuevos Casos']= df['Nuevos Casos'].astype(float)
df['Casos Totales']= df['Casos Totales'].astype(float)

#creating new DF to plot without total values
df_plot =  df.iloc[2:16]


img_file = datetime.date.today().strftime("%d-%m-%Y")


#plotting New cases and all cases of Chile
plt.plot(df_plot['Region'],df_plot['Nuevos Casos'], label = "Nuevos Casos")
plt.plot(df_plot['Region'],df_plot['Casos Totales'], label = "Casos Totales")
plt.ylabel('Casos')
plt.title('Corona Virus En Chile 20-03-2020')
plt.xlabel('Regiones')
plt.xticks(rotation=90)
plt.legend()
plt.savefig(img_file)
plt.show()


#exporting dataframe to CSV with date

filename = datetime.date.today().strftime("%d-%m-%Y")+'-coronavirus-chile.csv'

df.to_csv(filename)


files = sorted(glob.glob('*-coronavirus-chile.csv'))

Dates=[]
rankscore = []
for f in files:
    print(f)
        
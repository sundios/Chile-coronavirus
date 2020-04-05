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

print(df)





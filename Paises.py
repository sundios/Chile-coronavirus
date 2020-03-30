#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:27:16 2020

@author: konradburchardt
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import matplotlib.pyplot as plt



#URL to scrape data
url = "https://www.worldometers.info/coronavirus/#nav-today"
page = requests.get(url)

#Parsing HTML
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.prettify())

soup2 = soup.find("table", attrs={"id": "main_table_countries_today"})

#code for getting Tables
rows = []
for tr in soup2.find_all("tr")[1:]:
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
df = pd.DataFrame(rows, columns =  ['Country', 'Total Cases', 'New Cases','Total Deaths','New Deaths','Total Recovered','Active Cases','Serious,Critical' , 'Total Cases/1M pop','Total Deaths/1M pop', 'Reported 1st Case'])


#slicing DF with only Southamerican Countries

Brazil = df.loc[df['Country'] == 'Brazil']
Argentina = df.loc[df['Country'] == 'Argentina']
Uruguay = df.loc[df['Country'] == 'Uruguay']
Paraguay = df.loc[df['Country'] == 'Paraguay']
Bolivia = df.loc[df['Country'] == 'Bolivia']
Peru = df.loc[df['Country'] == 'Peru']
Ecuador = df.loc[df['Country'] == 'Ecuador'] 
Venezuela = df.loc[df['Country'] == 'Venezuela']
Colombia = df.loc[df['Country'] == 'Colombia'] 
Guyana = df.loc[df['Country'] == 'Guyana']
Suriname = df.loc[df['Country'] == 'Suriname'] 
French_Guiana = df.loc[df['Country'] == 'French Guiana']

df_list = [Brazil,Argentina,Uruguay,Paraguay,Bolivia,Peru,Ecuador,Venezuela,Colombia,Guyana,Suriname,French_Guiana]

Paises =  pd.concat(df_list)

#This is the DF we need to push to Gsheets
Paises = Paises.reset_index(drop=True)



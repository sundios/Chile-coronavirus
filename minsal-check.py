#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:46:56 2020

@author: konradburchardt
"""

from corona import daily
import requests
from bs4 import BeautifulSoup
import pandas as pd



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


#Selecting Last row of Daily. (Yesterday data to compare)
daily = daily.iloc[-1, 1]

#removing . in thousand separator
daily = int(float(daily))

#Checking if Yesterday total value is same as today. If different we will run our script

import subprocess
import time

#checking if minsal has uploaded the data
if df == daily:
    #this means data has not been updated yet
    print('did Minsal updated the data? No they havent, they are still sleeping. Data is the same as yesterday')
else:
    #This means data is not the same so minsal has changed the data
    print('did Minsal updated the data? Yes! they have. So now we should run all our scripts.')
    subprocess.run(['python3', 'corona.py'])
    #8 minutes break
    time.sleep(500)
    subprocess.run(['python3', 'corona.py'])
    



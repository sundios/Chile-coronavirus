#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:49:03 2020

@author: konradburchardt
"""
  
from corona import df,daily
from regiones import r
import datetime
import pygsheets



gc = pygsheets.authorize(service_file='corona-271822-557422d15ba0.json')

#open the google spreadsheet 
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FeE8dWfdFJi8lgi_sVg2Qn5xHM9wvP8eB7tB39lm374/edit#gid=0')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell A1. MAIN GRAPH and SECONDARY GRAPH
wks.set_dataframe(daily,'A1',copy_head=True)


#totales for scorecard in dashboard

totales = df.iloc[16:17,]
#selecting sheet # 20
tot = sh[20]

#Updating Totales for Score card
tot.set_dataframe(totales,'A1',copy_head=True)


#select sheet 19 Regiones
wks = sh[19]

df = df.iloc[0:16]

# with df, starting at cell A1. 
wks.set_dataframe(df,'A1',copy_head=True)


#adding new sheet

#new = sh.add_worksheet(title)

#new.set_dataframe(df,'A1',copy_head=True)

# Pushing Regiones values to Google Sheets
for j in range(1,18):
    print(j)
    wsheet = sh[j]
    wsheet.set_dataframe(r[j-1],'A1',copy_head=True)





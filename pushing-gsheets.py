#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:49:03 2020

@author: konradburchardt
"""
  
from corona import df,daily
from regiones import r
from Paises import Paises
import datetime
import pygsheets

#***** CONNECTION TO GOOGLE SHEETS *****

gc = pygsheets.authorize(service_file='corona-271822-557422d15ba0.json')

#open the google spreadsheet 
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FeE8dWfdFJi8lgi_sVg2Qn5xHM9wvP8eB7tB39lm374/edit#gid=0')

                    
#***** PUSHING DATA TO TOTALS WORKSHEET. THIS IS FOR MAIN GRAPH AND SECONDARY GRAPH *****                  
                    
#select the first sheet TOTALS
wks = sh[0]

#update the first sheet with df, starting at cell A1. MAIN GRAPH and SECONDARY GRAPH
wks.set_dataframe(daily,'A1',copy_head=True)


#***** PUSHING DATA TO TOTALES WORKSHEET. THIS IS FOR SCORECARD *****

#Getting only last row
totales = df.iloc[16:17,]

#selecting sheet #20 TOTALES
tot = sh[20]

#Updating Totales for Scorecard
tot.set_dataframe(totales,'A1',copy_head=True)

#***** PUSHING DATA TO REGIONES WORKSHEET. THIS IS FOR REGIONES TABLE *****

#select sheet 19 Regiones
wks = sh[19]

df = df.iloc[0:16]

#Add to Regiones worksheet
wks.set_dataframe(df,'A1',copy_head=True)


#***** PUSHING DATA TO EACH OF THE REGIONES WORKSHEET. THIS IS FOR ALL REGIONES GRAPHS. *****

# Pushing Regiones values to Google Sheets
for j in range(1,18):
    print(j)
    wsheet = sh[j]
    wsheet.set_dataframe(r[j-1],'A1',copy_head=True)
    
#***** PUSHING DATA TO PAISES WORKSHEET. THIS IS FOR THE SOUTH AMERICA MAPS AND THE GRAPH WITH COUNTRIES . *****

#Selecting worksheet 18 Paises
wks = sh[18]

#Add to Paises worksheet
wks.set_dataframe(Paises,'A1',copy_head=True)

    
###### THIS IS ONLY IF WE WANT TO CREATE A NEW SHEET #####
      
#adding new sheet
#new = sh.add_worksheet(title)
#new.set_dataframe(df,'A1',copy_head=True)





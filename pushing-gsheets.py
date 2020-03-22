#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:49:03 2020

@author: konradburchardt
"""
  
from corona import df,daily,markdown_daily,markdown
import datetime
import pygsheets



gc = pygsheets.authorize(service_file='corona-271822-e18788e4c847.json')

#open the google spreadsheet 
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FeE8dWfdFJi8lgi_sVg2Qn5xHM9wvP8eB7tB39lm374/edit#gid=0')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell A1. 
wks.set_dataframe(daily,'A1',copy_head=True)

title= datetime.date.today().strftime("%d-%m-%Y")
 
#adding new worksheet
wks.add_worksheet(title, rows=100, cols=26, src_tuple=None, src_worksheet=None, index=None)
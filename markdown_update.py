#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 10:53:23 2020

@author: konradburchardt
"""

# Git File Generator
from corona import df,daily, img_file
import datetime


markdown = daily.to_markdown()
markdown_daily = df.to_markdown()

print(markdown)
print(markdown_daily)


date= datetime.date.today().strftime("%d-%m-%Y")

print("\n"+ '###' + date + "\n" + '<img src="https://github.com/sundios/Chile-coronavirus/blob/master/' + img_file + '.png" width="60%" height="100%">'+"\n" + markdown_daily, file=open("readme.md", "a"))



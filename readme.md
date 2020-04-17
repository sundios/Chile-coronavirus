# Corona Virus in Chile

Daily Chile Corona virus data pipeline. Data is scraped daily from misal.cl 


## Live Dashboard

All the data gathered is pushed to a live dashoboard that you can find [here](https://datastudio.google.com/reporting/f97733c1-17e1-4bd6-8841-9dd2d45ac9b4)


## Daily Chile cases 

<img src="https://github.com/sundios/Chile-coronavirus/blob/master/Images/Totales-Chile.png" width="60%" height="100%">

### Requirements.txt

```
pygsheets==2.0.3.1
matplotlib==3.2.1
beautifulsoup4==4.9.0
pandas==1.0.3
numpy==1.18.2

```

## Sources 

* [Worldometers Corona Virus Data](https://www.worldometers.info/coronavirus/#countries)
* [Minsal Chile Corona Virus Data](https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/)

## PipeLine

To scrape the minsal and the worldometers data I built a pipline using airflow that consists in 5 tasks that run 3 different scripts. Each of the script pushes data to a Google spreadsheet. I wanted to use google spreadhseet since the data is not that heavy and its easy to connect google sheets. with data studio.

The pipline is set to run every day at 11:05AM CLT. Since airflow uses Directed acyclic graphs I cant re run a task, so I created a while loop as the first task that keeps runing until the condition is true.

The task are:

1. **Minsal_check:** scrapes the site and compares the current data with a while loop with yesterday's data. If data is the same than yesterday then the while loops keeps running until the data has been updated and we can proceed with out pipeline.
2. **Continue_task:** echo a message that tell us that data has been change.
3. **Scraping Data**
   1. **Scrape_Minsal_data:** Scrape new minsal data,clean the data, Create daily csv and push it to g oogle sheets
   2. **Scrape_Regiones_Data:** We open all files from the minsal data we scraped and concatenate all of them in one file, then we do some cleaning and output all different regions by totals. We push these into different worksheets in google sheets.
   3. **Scrape_Paises_data:** Scrape new data from Worldometer and then only select southamerican countries and push it to google sheets.
4. **finish_task:** echo task is finished

 ![Graph View](/Images/gv.png)









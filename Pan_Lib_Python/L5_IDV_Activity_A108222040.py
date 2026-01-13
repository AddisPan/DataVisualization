# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 14:56:43 2022

@date:2022/06/10
@author: A108222040
@subject:Stock
"""
##Enviroment
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

##Packages
from pandas_datareader import data
import pandas_datareader.data as pdData
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

import altair as alt
from vega_datasets import data

###Data Process
def l5_dataset(dataset=InputPath + "/microsoft_stock.csv", index='Date'):
    df = pd.read_csv(dataset)
    print("Columns info. --> \n", df.info(), sep="")
    print("\nNumerical Data info. --> \n", df.describe(), sep="")
    print("\nCategorical Data info. --> \n", df.describe(include=object), sep="")
    print("\ndata --> \n", df.head(5), sep="")
    return df

###Lesson5: Time interval + dash example dataset - multiple stocks
def getStocks():
    #-- get data
    startDate = "2020-1-1"
    endDate = "2022-6-6"
    source = "yahoo"
    #-- get data
    appleStock = pdData.DataReader("AAPL", start=startDate, end=endDate, data_source=source
                               ).reset_index()[["Date", "Close", "High"]]
    ibmStock = pdData.DataReader("IBM", start=startDate, end=endDate, data_source=source
                               ).reset_index()[["Date", "Close", "High"]]
    googleStock = pdData.DataReader("GOOG", start=startDate, end=endDate, data_source=source
                               ).reset_index()[["Date", "Close", "High"]]
    microsoftStock = pdData.DataReader("IBM", start=startDate, end=endDate, data_source=source
                               ).reset_index()[["Date", "Close", "High"]]
    
    #--save data
    appleStock.to_csv(InputPath + "/AppleStock_20200101_20220606.csv")
    ibmStock.to_csv(InputPath + "/IbmStock_20200101_20220606.csv")
    googleStock.to_csv(InputPath + "/GoogleStock_20200101_20220606.csv")
    microsoftStock.to_csv(InputPath + "/MicrosfotStock_20200101_20220606.csv")
    
    #--process data
    appleStock["Stock"] = "Apple"
    ibmStock["Stock"] = "Ibm"
    googleStock["Stock"] = "Google"
    microsoftStock["Stock"] = "Microsoft"
    
    stocks = pd.concat([appleStock, ibmStock, googleStock, microsoftStock])
    stocks["Month"] = stocks.Date.dt.month
    stocks["Year"] = stocks.Date.dt.year
    stocks["Day"] = stocks.Date.dt.day
    stocks.to_csv(InputPath + "/stocks_20200101_20220606.csv")
    
    return stocks

def IDV_Altair_Stocks(stocks):
    stockSelection1 = alt.selection_single(fields=["Stock"], bind="legend")
    
    #--rightChart
    rightChart = alt.Chart(stocks).mark_line().encode(
                       x="Date", y="Close", color="Stock",
                       opacity=alt.condition(stockSelection1, alt.value(1), alt.value(0.1)),
                       tooltip=["Date", "Close"] #hover
        ).properties(height=300, width=500
        ).configure_title(color="green", fontSize=24
        ).configure_axis(labelFontSize=14,
                         labelColor="brown",
                         titleFontSize=20,
                         titleColor="purple"
        ).add_selection(stockSelection1
        ).interactive()
                       
    rightChart.show()
    
    
    #-- left chart
    stockSelection1 = alt.selection_single(fields=["Stock"], bind="legend")
    
    rightChart = alt.Chart(stocks).mark_line().encode(
                       x="Date", y="Close", color="Stock",
                       opacity=alt.condition(stockSelection1, alt.value(1), alt.value(0.1)),
                       tooltip=["Date", "Close"] #hover
        ).properties(height=300, width=500
        ).add_selection(stockSelection1
        ).interactive()
                                   
    upper = rightChart.encode(alt.X('Date:T', scale=alt.Scale(domain=stockSelection1)))
    
    lower = rightChart.properties(height=60).add_selection(stockSelection1)
    
    leftChart = upper & lower 
    leftChart.show()
    
    #-- left chart
    brush = alt.selection(type='interval', encodings=['x'])
    
    base = alt.Chart(stocks.loc[stocks["Stock"] == "Microsoft"]
                ).mark_line().encode(x = 'Date:T', y = 'Close:Q'
                ).properties(width=600, height=200)
                                   
    upper = base.encode(alt.X('Date:T', scale=alt.Scale(domain=brush)))
    
    lower = base.properties(height=60).add_selection(brush)
    
    leftChart = upper & lower 
    leftChart.show()

if (__name__ == "__main__"):
    stocks = getStocks()
    IDV_Altair_Stocks(stocks)
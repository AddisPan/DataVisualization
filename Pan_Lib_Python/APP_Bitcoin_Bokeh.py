# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
@date:2022/04/09
@author: A108222040
@subject:
"""
###enviroment
import os, time, sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

###import packages
import numpy as np     #linear algebra
import pandas as pd    #data processing, CSV file I/O

from matplotlib import pyplot as plt
import bokeh.sampledata
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.layouts import column, row, gridplot

from bokeh.models import BoxSelectTool, TapTool, CustomJS
from bokeh.events import Tap

###Global
#--- Retrieve datasets
df_bitcoin = pd.read_csv(InputPath + "/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv")
df_bitcoin.Timestamp = pd.to_datetime(df_bitcoin.Timestamp, unit='s')
dailyDate = np.array(df_bitcoin.index, dtype=np.datetime64)
dailyOpen = np.array(df_bitcoin.Open)
dailyHigh = np.array(df_bitcoin.High)
dailyLow = np.array(df_bitcoin.Low)
dailyClose = np.array(df_bitcoin.Close)
dailyWeightedPrice = np.array(df_bitcoin.Weighted_Price)

print("bit coin -->\n", df_bitcoin.describe(include='all'), sep="") #inclue = 
print("\nbit ocin -->")
print(df_bitcoin.info())

###-- Preprocessing
df_bitcoin.index = df_bitcoin.Timestamp
dfDay   = df_bitcoin.resample('D').mean()      #Resampling to  daily frequency
dfMonth = df_bitcoin.resample('M').mean()    #Resampling to monthly frequency
dfYear  = df_bitcoin.resample('A-DEC').mean() #Resampling to annual frequency
dfQ     = df_bitcoin.resample('Q-DEC').mean()  #Resampling to quarterly frequency
print("Daily -->/n",     dfDay.head(5), sep="")
print("Month -->/n",     dfMonth.head(5), sep="")
print("Yearly -->/n",    dfYear.head(5), sep="")
print("Quarterly -->/n", dfQ.head(5), sep="")

###Method
def testCase():
    dd = {'xValues': [1,2,3,4,5], 'yValues': [6,7,2,3,6]}
    source =ColumnDataSource(data=dd)
    pp=figure()
    pp.circle(x="xValue", y="yValue", source=source)
    
###Bitcoin dataset
#---- Plot 1 
def bitcoinYMQD():
    #PLOTS
    fig = plt.figure(figsize=[15, 7])
    plt.suptitle('Bitcoin exchanges, mean USD', fontsize=22)
    
    plt.subplot(221)
    plt.plot(dfDay.Weighted_Price, '-', label='By Days')
    plt.legend()
    
    plt.subplot(222)
    plt.plot(dfMonth.Weighted_Price, '-', label='By Months')
    plt.legend()
    
    plt.subplot(223)
    plt.plot(dfQ.Weighted_Price, '-', label='By Quarters')
    plt.legend()
    
    plt.subplot(222)
    plt.plot(dfYear.Weighted_Price, '-', label='By Years')
    plt.legend()
    
    plt.show()
    
def bitcoinD():
    dfCut = df_bitcoin[4700000:]
    print("shape of dfCut -->", np.shape(dfCut))
    dailyOpen = np.array(dfCut.Open)
    dailyHigh = np.array(dfCut.High)
    dailyLow = np.array(dfCut.Low)
    dailyClose = np.array(dfCut.Close)
    dailyWeightedPrice = np.array(dfCut.Weighted_Price)
    dailyDates = np.array(dfCut.index, dtype=np.datetime64)
    
    #figure1
    p1 = figure(plot_width=800, plot_height=350, x_axis_type="datetime")
    
    #add renderers
    p1.circle(dailyDates, dailyOpen, size=6, color='grey', alpha=0.5, legend_label = 'open')
    p1.square(dailyDates, dailyClose, size=6, color='grey', alpha=0.5, legend_label = 'close')
    p1.triangle(dailyDates, dailyHigh, size=6, color='grey', alpha=0.5, legend_label = 'high')
    p1.asterisk(dailyDates, dailyLow, size=6, color='grey', alpha=0.5, legend_label = 'low')
    p1.line(dailyDates, dailyWeightedPrice, color='navy', legend_label = 'weighted')
    
    # NEW: customize by setting attributes
    p1.title.text = "Bitcoin daily"
    p1.legend.location = "top_left"
    p1.grid.grid_line_alpha = 0
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    p1.ygrid.band_fill_color = "olive"
    p1.ygrid.band_fill_alpha = 0.1
    
    output_file(outputPath + "/bitcoinDaily.html")
    output_notebook()
    
    show(p1)
    
    ##figure 2
    sourceOpen = ColumnDataSource(pd.DataFrame({'index': dailyDates, 'open': dailyOpen}))
    sourceHigh = ColumnDataSource(pd.DataFrame({'index': dailyDates, 'high': dailyHigh}))
    sourceLow = ColumnDataSource(pd.DataFrame({'index': dailyDates, 'low': dailyLow}))
    sourceClose = ColumnDataSource(pd.DataFrame({'index': dailyDates, 'close': dailyClose}))
    sourceWeightedPrice = ColumnDataSource(pd.DataFrame({'index': dailyDates, 'open': dailyWeightedPrice}))
    
    p2 = figure(plot_width=800, plot_height=350, x_axis_type="datetime")
    
    #add renders
    p2.circle(x='index', y='open', source=sourceOpen, size=6, color='grey', alpha=0.5, legend_label= 'open')
    p2.square(x='index', y='close', source=sourceClose, size=6, color='grey', alpha=0.5, legend_label= 'close')
    p2.triangle(x='index', y='high', source=sourceHigh, size=6, color='grey', alpha=0.5, legend_label= 'high')
    p2.asterisk(x='index', y='low', source=sourceLow, size=6, color='grey', alpha=0.5, legend_label= 'low')
    p2.line(x='index', y='Weighted_Price', source=sourceWeightedPrice, color='navy', legend_label= 'open')
    
    #New: customize by setting attributes
    p2.title.text = "Bitcoin daily"
    p2.legend.location = "top_left"
    p2.grid.grid_line_alpha = 0
    p2.xaxis.axis_label = 'Date'
    p2.yaxis.axis_label = 'Price'
    p2.ygrid.band_fill_color = "olive"
    p2.ygrid.band_fill_alpha = 0.1
    
    output_notebook()
    show(p2)
    
    #-- 5 plots
    # create five plots
    s1 = figure(plot_width=800, plot_height=350, background_fill_color="#fafafa", x_axis_type="datetime")
    s1.circle(x='index', y='open', source=sourceOpen, size=6, color='#bf831c', alpha=0.5, legend_label= 'open')
    s2 = figure(plot_width=800, plot_height=350, background_fill_color="#fafafa", x_axis_type="datetime")
    s2.square(x='index', y='close', source=sourceClose, size=6, color='#6f091b', alpha=0.5, legend_label= 'close')
    s3 = figure(plot_width=800, plot_height=350, background_fill_color="#fafafa", x_axis_type="datetime")
    s3.triangle(x='index', y='high', source=sourceHigh, size=6, color='#658950', alpha=0.5, legend_label= 'high')
    s4 = figure(plot_width=800, plot_height=350, background_fill_color="#fafafa", x_axis_type="datetime")
    s4.asterisk(x='index', y='low', source=sourceLow, size=6, color='#309c9c', alpha=0.5, legend_label= 'low')
    s5 = figure(plot_width=800, plot_height=350, background_fill_color="#fafafa", x_axis_type="datetime")
    s5.line(x='index', y='Weighted_Price', source=sourceWeightedPrice, color='#494574', legend_label= 'open')
    #put the results in a column and show
    show(column(s1, s2, s3, s4, s5))
    #put the results in a row and show
    show(row(s1, s2, s3, s4, s5))
    #make a grid
    grid = gridplot([[s1, s2, s3], [s4, s5]], plot_width=250, plot_height=250)
    
    #-- interactive
    s1 = figure(plot_width=800, plot_height=350, background_fill_color="#fafafa", x_axis_type="datetime")
    s1.circle(x='index', y='open', source=sourceOpen, size=6, color='grey', alpha=0.5, legend_label= 'open')
    # configure so that no drag tools are active
    s1.toolbar.active_drag = None
    #configure so that Bokeh chooses what (if any) scroll tool is active
    s1.add_tools(BoxSelectTool(dimensions="width"))
    s1.add_tools(TapTool())
    taptool = p1.select(type=TapTool)
    # hover = HoverTool(tooltips=[("count", "@count")])
    
    callback = CustomJS(args=dict(source=sourceOpen), code="""
        var selectedIndex = source.selected.indices;
        for (var i = 0; i < selectedIndex.length; i++){
            console.log("Index:", selectedIndex[i])
            console.log("x:", source.data['index'][selectedIndex[i]])
            console.log("y:", source.data['open'][selectedIndex[i]])
        }
    """)
    taptool = s1.select(type=TapTool)
    sourceOpen.selected.js_on_change('indices', callback)
    
    show(s1)

if (__name__ == "__main__"):
    bitcoinD()
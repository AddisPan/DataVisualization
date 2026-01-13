# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 13:32:42 2022

@author: Addis
"""
##Enviroment
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

##Packages
import pandas as pd
from vega_datasets import data  #data.weather.url

#--altair--#
import altair as alt


##--Load
#weatherURL='https://vega.github.io/vega-datasets/data/weather.csv'
def loadData(dataset=InputPath + "/weather.csv"):
    df  = pd.read_csv(dataset)
    print("Columns info. -->\n", df.info(), sep="")
    print("\nNumerical Data info. -->\n", df.describe(), sep="")
    print("\nCategorical Data info. -->\n", df.describe(include=object), sep="")
    print("\ndata -->\n", df.head(5), sep="")
    return df
    
##---Case1
def case1_transformC(df):
    #-- left chart
    tempMinMax = alt.Chart(df).mark_area(opacity=0.3).encode(
                     alt.X('month(date):T', title=None, axis=alt.Axis(format='%b')),
                     alt.Y('average(temp_max):Q', title='Avg. Max/Min Temperature °C'),
                     alt.Y2('average(temp_min):Q'),
                     alt.Color('location:N'))
    
    #--right chart
    tempMid = alt.Chart(df).mark_line().transform_calculate(
                   temp_mid='(+datum.temp_min + +datum.temp_max)/2' 
                 ).encode(alt.X('month(date):T'),
                          alt.Y('average(temp_mid):Q'),
                          alt.Color('location:N'))
                          
    #-- tempMinMax + tempMid
    chart = alt.layer(tempMinMax, tempMid)
    charts = alt.hconcat(tempMinMax, tempMid, spacing=50, title="Weather", center=True,
              ).configure_title(color='green', fontSize=24, anchor="middle", align="right",
              ).configure_axis(labelFontSize=14,
                               labelColor="red",
                               titleFontSize=20,
                               titleColor="blue",
                               )
    chart.show()
    
def case2_transformF(df):
    #--method 1
    precip = alt.Chart(df).transform_filter('datum.location == "Seattle"'
               ).mark_line(interpolate='monotone', stroke='grey'
               ).encode(alt.X('month(date):T', title=None, axis=alt.Axis(format='%b')),
                        alt.Y('average(precipitation):Q', title='Precipitation'))
                        
    tempMinMax = alt.Chart(df).transform_filter('datum.location == "Seattle"'
               ).mark_area(opacity=0.3).encode(
                        alt.X('month(date):T', title=None, axis=alt.Axis(format='%b')),
                        alt.Y('average(temp_max):Q', title='Avg. Max/Min Temperature °C'),
                        alt.Y2('average(temp_min):Q'))
    
    chart = alt.layer(tempMinMax, precip, title="Weather in Seattle").resolve_scale(y='independent')
    chart.show()
    
    #--method 2
    precip = alt.Chart(df).mark_line(interpolate='monotone', stroke='grey'
               ).encode(alt.X('month(date):T', title=None),
                        alt.Y('average(precipitation):Q', title='Precipitation'))
                        
    tempMinMax = alt.Chart().mark_area(opacity=0.3).encode(
                        alt.X('month(date):T', title=None, axis=alt.Axis(format='%b')),
                        alt.Y('average(temp_max):Q', title='Avg. Max/Min Temperature °C'),
                        alt.Y2('average(temp_min):Q'))
    
    chart = alt.layer(tempMinMax, precip, data=df, title="Weather in Seattle"
                     ).transform_filter('datum.location == "Seattle"'
                     ).resolve_scale(y='independent')
    chart.show()

def case3_facet(df):
    colors = alt.Scale()
    
#Q1
def case6_composition(df):
    #-- method 1
    basic1 = alt.Chart(df).transform_filter('datum.location == "Seattle"'
               ).mark_bar(
               ).encode(alt.X('month(date):O'), alt.Y('average(temp_max):Q'))
    basic2 = alt.Chart(df).transform_filter('datum.location == "Seattle"'
               ).mark_rule(stroke='firebrick'
               ).encode(alt.Y('average(temp_max):Q'))
                           
    chart = alt.layer(basic1, basic2)
    chart.show()
    
    #--method 2
    chart = alt.layer(alt.Chart().mark_bar().encode(
                          alt.X('month(date):O', title='Month'),
                          alt.Y(alt.repeat('column'), aggregate='average', type='quantitative')),
                      alt.Chart().mark_rule(stroke='firebrick').encode(
                          alt.Y(alt.repeat('column'), aggregate='average', type='quantitative'))
                         ).properties(width=200, height=150
                         ).repeat(data=df, column=['temp_max', 'precipitation', 'wind']
                         ).transform_filter('datum.location == "Seattle"')
    chart.show()
    
    #--method 3
    splom = alt.Chart().mark_point(filled=True, size=15, opacity=0.5
              ).encode(alt.X(alt.repeat('column'), type='quantitative'),
                       alt.Y(alt.repeat('row'), type='quantitative')
              ).properties(width=125, height=125
              ).repeat(row=['temp_max', 'precipitation', 'wind'],
                       column=['wind', 'precipitation', 'temp_max']
              )
                       
    dateHist = alt.layer(alt.Chart(df).mark_bar().encode(
                             alt.X('month(date):O', title='Month'),
                             alt.Y(alt.repeat('row'), aggregate='average', type='quantitative')),
                             #alt.Color('month(date):O', scale = alt.Scale(range=['#aec7e8', 'c7c7c7', '#1f77b4', '#9467bd', '#e7ba52']))),
                         alt.Chart().mark_rule(stroke='firebrick').encode(
                             alt.Y(alt.repeat('row'), aggregate='average', type='quantitative'))
                            ).properties(width=175, height=125
                            ).repeat(row=['temp_max', 'precipitation', 'wind'])
                                         
    tempHist =  alt.Chart(df).mark_bar(
                  ).encode(alt.X('temp_max:Q', bin=True, title='Temperature (°C)'),
                           alt.Y('count():Q'),
                           alt.Color('weather:N', scale=alt.Scale(
                                     domain=['drizzle', 'fog', 'rain', 'snow', 'sun'],
                                     range=['blue', 'black', 'yellow', 'pink', 'red']))
                  ).properties(width=115, height=100
                  ).facet(column="weather:N")
                               
    chart = alt.vconcat(alt.hconcat(splom, dateHist),
                        tempHist, data=df, title='Seattle Weather Dashboard', center=True
              ).transform_filter('datum.location == "Seattle"'
              ).resolve_legend(color='independent'
              ).configure_axis(
                               labelAngle=0,
                               labelFontSize=10,
                               labelColor="orange",
                               titleFontSize=16,
                               titleColor="green",)
    chart.show()

if (__name__ == "__main__"):
    df = loadData()
    #case1_transformC(df)
    #case2_transformF(df)
    case6_composition(df)
    
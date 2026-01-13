# -*- coding: utf-8 -*-
"""
Created on Tue May 24 21:37:00 2022

@date:2022/05/24
@author: A108222040
@subject:
"""
##Enviroment
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

##Packages
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

import altair as alt
from vega_datasets import data

###Data Process
def l4_dataset(dataset=InputPath + "/hpi_data_countries.tsv", show=True):
    df  = pd.read_csv(dataset, sep='\t')
    if show:
        print("Columns info. -->\n", df.info(), sep="")
        print("\nNumerical Data info. -->\n", df.describe(), sep="")
        print("\nCategorical Data info. -->\n", df.describe(include=object), sep="")
        print("\ndata -->\n", df.head(5), sep="")
    return df

#change實心
def ex27_SDV_Zoom(df):
    chart = alt.Chart(df, title="Wellbeing vs. HPI").mark_circle().encode(
        x = ('Wellbeing (0-10):Q'),
        y = ('Happy Planet Index:Q'),
        color='Region:N',
        tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
        ).interactive( #zoom in/out
        ).properties(width=400, height=300
        ).configure_title(color='green', fontSize=24
        ).configure_axis(labelFontSize=14,
                         labelColor="red",
                         titleFontSize=20,
                         titleColor="blue",
        )
    chart.show()

def ex28_SDV_Zoom_Hover(df):
   chart = alt.Chart(df, title="Wellbeing vs. HPI").mark_point().encode(
        x = 'Wellbeing (0-10):Q',
        y = 'Happy Planet Index:Q',
        color='Region:N',
        tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).interactive( #zoom in/out
    ).properties(width=400, height=300
    ).configure_title(color='green', fontSize=24
    ).configure_axis(labelFontSize=14,
                     labelColor="red",
                     titleFontSize=20,
                     titleColor="blue",
        )
   chart.show()

def ex29_SelectedArea(df):
    selected_area = alt.selection_interval()

    chart = alt.Chart(df, title="Wellbeing vs. HPI").mark_point().encode(
        x='Wellbeing (0-10):Q',
        y='Happy Planet Index:Q',
        color=alt.condition(selected_area, 'Region:N', alt.value('lightgray')),
        tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).add_selection(selected_area
    ).properties(width=400, height=300
    ).configure_title(color='green', fontSize=24
    ).configure_axis(labelFontSize=14,
                     labelColor="red",
                     titleFontSize=20,
                     titleColor="blue",
    )
    chart.show()
    
def ex30_SelectedArea_Zoom_Hover(df):
    selected_area = alt.selection_interval()

    chart = alt.Chart(df, title="Wellbeing vs. HPI").mark_point().encode(
        x='Wellbeing (0-10):Q',
        y='Happy Planet Index:Q',
        color=alt.condition(selected_area, 'Region:N', alt.value('lightgray')),
        tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).interactive(
    ).add_selection(selected_area
    ).properties(width=400, height=300
    ).configure_title(color='green', fontSize=24
    ).configure_axis(labelFontSize=14,
                     labelColor="red",
                     titleFontSize=20,
                     titleColor="blue",
    )
    chart.show()

def ex31_MultiplePlot(df):
    selectedArea = alt.selection_interval()

    chart = alt.Chart(df, title="HPI").mark_point().encode(
    x='Wellbeing (0-10):Q',
    y='Happy Planet Index:Q',
    color='Region:N',
    tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).interactive(
    ).add_selection(selectedArea
    ).properties(width=400, height=300)
    # .configure_title(color='green', fontSize=24
    # ).configure_axis(labelFontSize=14,
    #                  labelColor="red",
    #                  titleFontSize=20,
    #                  titleColor="blue",
    # )
    chart1 = chart.encode(x='Wellbeing (0-10)').properties(title="Wellbeing vs. HPI")
    chart2 = chart.encode(x='Life Expectancy (years)').properties(title="Life Expectancy vs. HPI")
    chart = alt.hconcat(chart1, chart2
               ).configure_title(color='green', fontSize=24
               ).configure_axis(labelFontSize=14,
                                labelColor="red",
                                titleFontSize=20,
                                titleColor="blue",
               )
    chart.show()

def ex31_Slecetion(df):
    selectedArea = alt.selection_interval()

    chart = alt.Chart(df, title="HPI").mark_point().encode(
    #x='Wellbeing (0-10):Q',
    y='Happy Planet Index:Q',
    color=alt.condition(selectedArea, 'Region', alt.value('lightgray')),
    tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    #),interactive()
    ).add_selection(selectedArea
    ).properties(width=400, height=300)
    # .configure_title(color='green', fontSize=24
    # ).configure_axis(labelFontSize=14,
    #                  labelColor="red",
    #                  titleFontSize=20,
    #                  titleColor="blue",
    # )
    chart1 = chart.encode(x='Wellbeing (0-10)').properties(title="Wellbeing vs. HPI")
    chart2 = chart.encode(x='Life Expectancy (years)').properties(title="Life Expectancy vs. HPI")
    charts = alt.hconcat(chart1, chart2
               ).configure_title(color='green', fontSize=24
               ).configure_axis(labelFontSize=14,
                                labelColor="red",
                                titleFontSize=20,
                                titleColor="blue",
               )
    charts.show()

def ex32_Selection_FeatureValue_MP(df):
    #input_dropdown = alt.binding_select(options=list(r))
    input_dropdown = alt.binding_select(
    options=[None] + list(df.Region.unique()), labels = ['All'] + list(df.Region.unique()))
    selected_points = alt.selection_single(fields=['Region'], 
                                           bind=input_dropdown, name='Select')
    
    #chart
    chart = alt.Chart(df, title="Wellbeing vs. HPI").mark_point().encode(
    x='Wellbeing (0-10):Q',
    y='Happy Planet Index:Q',
    color=alt.condition(selected_points, alt.Color("Region:N"), alt.value("lightgray")),
    tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).interactive(
    ).add_selection(selected_points
    ).properties(width=600, height=300)
    
    chart1 = chart.encode(x='Wellbeing (0-10)').properties(title="Wellbeing vs. HPI")
    chart2 = chart.encode(x='Life Expectancy (years)').properties(title="Life Expectancy vs. HPI")
    charts = alt.hconcat(chart1, chart2, spacing=50
               ).configure_title(color='green', fontSize=24
               ).configure_axis(labelFontSize=14,
                                labelColor="red",
                                titleFontSize=20,
                                titleColor="blue",
               )
    charts.show()

def testAltair_MP_weather():
    #---Load Data
    weather = 'https://vega.github.io/vega-datasets/data/weather.csv'
    df = pd.read_csv(weather)
    
    #--plot
    splom = alt.Chart().mark_point(filled=True, size=15, opacity=0.5
              ).encode(alt.X(alt.repeat('column'), type='quantitative'),
                       alt.Y(alt.repeat('row'), type='quantitative')
              ).properties(width=125, height=125
              ).repeat(row=['temp_max', 'precipitation', 'wind'],
                       column=['wind', 'precipitation', 'temp_max'])
    
    dateHist = alt.layer(alt.Chart().mark_bar().encode(
                            alt.X('month(date):O', title='Month'),
                            alt.Y(alt.repeat('row'), aggregate='average', type='quantitative')),
                            alt.Chart().mark_rule(stroke='firebrick').encode(
                            alt.Y(alt.repeat('row'), aggregate='average', type='quantitative'))
              ).properties(width=175, height=125
              ).repeat(row=['temp_max', 'precipitation', 'wind'])
                           
    tempHist = alt.Chart(weather).mark_bar().encode(
                            alt.X('temp_max:Q', bin=True, title='Temperature (°C)'),
                            alt.Y('count():Q'),
                            alt.Color('weather:N', scale=alt.Scale(
                            domain=['drizzle', 'fog', 'rain', 'snow', 'sun'],
                            range=['#aec7e8', '#c7c7c7', '#1f77b4', '#9467bd', '#e7ba52']))
              ).properties(width=115, height=100
              ).facet(column='weather:N')
                           
    chart = alt.vconcat(alt.hconcat(splom, dateHist), tempHist, data=weather, title='Seattle Weather Dashb'
                       ).transform_filter('datum.location == "Seattle"'
                       ).resolve_legend(color='independent'
                       ).configure_axis(labelAngle=0)
                                        
    chart.show()
    
def ex33_Bar(df):
    columns = df.columns
    xData = columns[2] + ":N"
    yData = "mean(" + columns[7] + "):Q"
    bars = alt.Chart(df, title="Happy Planet Index").mark_bar().encode(
        x=xData, # x=alt.X('x', axis=alt.Axis(format='%', title='Wellbeing'))
        y=yData, # y=alt.Y('y', axis=alt.Axis(labels=False))
        #color='Region:N',
        #color=alt.condition(selectedArea, "Region:N", alt.value("lightgray")),
        #tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).properties(width=300, height=200)
    #).interactive()
    #).add_selection(selected_points
    
    line = alt.Chart(df).mark_rule(color='firebrick').encode(
        y=yData,
        size=alt.SizeValue(3))
    
    #-- Concate 1: horizontal two figures
    #charts = alt.hconcat(chart1, chart2, spacing=50
    #           ).configure_title(color='green', fontSize=24
    #           ).configure_axis(labelFontSize=14,
    #                            labelColor="red",
    #                            titleFontSize=20,
    #                            titleColor="blue",
    #           )
    
    #--Concate 2 : overlap
    chart = alt.layer(bars, line, data=df).interactive()
    chart.show()
    
def ex34_Bar_Selection(df):
    selectedBars = alt.selection(type="interval", encodings=["x"])
    
    columns = df.columns
    xData = columns[2] + ":N"
    yData = "mean(" + columns[7] + "):Q"
    bars = alt.Chart(df, title="Happy Planet Index").mark_bar().encode(
        x=xData, # x=alt.X('x', axis=alt.Axis(format='%', title='Wellbeing'))
        y=yData, # y=alt.Y('y', axis=alt.Axis(labels=False))
        opacity=alt.condition(selectedBars, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        color='Region:N',
        #color=alt.condition(selectedArea, "Region:N", alt.value("lightgray")),
        #tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).properties(width=300, height=200
    ).add_selection(selectedBars
    ).interactive()
    
    
    line = alt.Chart(df).mark_rule(color='firebrick').encode(
        y=yData,
        size=alt.SizeValue(3)
    ).transform_filter(selectedBars)
    
    chart = alt.layer(bars, line, data=df)
    chart.show()
    
def ex35_Heatmap(df):
    columns = df.columns
    xData = columns[7] + ":Q"
    yData = columns[4] + ":Q"
    chart = alt.Chart(df, title="Happy Planet Index vs. Well Being").mark_rect().encode(
        x=alt.X(xData, title="HPI", bin=True),
        y=alt.Y(yData, bin=True),
        color=alt.Color('count()', scale=alt.Scale(scheme="greenblue"),
                                   legend=alt.Legend(title="Total Countries")),
        #color=alt.condition(selectedArea, "Region:N", alt.value("lightgray")),
        #tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).properties(width=400, height=300
    ).interactive()
    
    chart.show()

def ex35_Heatmap_Circle(df):
    #-- chart 1
    columns = df.columns
    xData = columns[7] + ":Q"
    yData = columns[4] + ":Q"
    heatmap = alt.Chart(df, title="Happy Planet Index vs. Well Being").mark_rect().encode(
        x=alt.X(xData, title="HPI", bin=True),
        y=alt.Y(yData, bin=True),
        color=alt.Color('count()', scale=alt.Scale(scheme="greenblue")),
        #color=alt.condition(selectedArea, "Region:N", alt.value("lightgray")),
        #tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).properties(width=400, height=300)
    
    #-- chart2
    circles = heatmap.mark_point().encode(
        alt.ColorValue("red"),
        alt.Size("count()", legend=alt.Legend(title="Records in Selection"))
        ).interactive()
    
    #--overlap
    chart = alt.layer(heatmap, circles)
    chart.show()

def ex36_Bar_Heatmap(df):
    #-- chart 1 
    bars = alt.Chart(df, title="Happy Planet Index vs. Countries").mark_bar().encode(
        x="Region:N",
        y="count():Q",
        color=alt.ColorValue("red")
    ).properties(width=350, height=300).interactive()
    
    #-- chart2
    columns = df.columns
    xData = columns[4] + ":Q"
    yData = columns[3] + ":Q"
    heatmap = alt.Chart(df, title="Well Being vs. Lefe Expectancy").mark_rect().encode(
        x=alt.X(xData, bin=True),
        y=alt.Y(yData, bin=True),
        color=alt.Color('count()', scale=alt.Scale(scheme="greenblue"),
                        legend=alt.Legend(title="Total Countries")),
        #color=alt.condition(selectedArea, "Region:N", alt.value("lightgray")),
        #tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).properties(width=350, height=300).interactive()
    
    #-- overlap
    chart = alt.hconcat(bars, heatmap, spacing=50, title="",
              ).configure_title(color='green', fontSize=24, align="center", anchor="middle"
              ).configure_axis(labelFontSize=14,
                               labelColor="red",
                               titleFontSize=20,
                               titleColor="blue",
                               )
    chart.show()

def ex37_Bar_Link_Heatmap(df):
    selectedRegion = alt.selection(type="interval", encodings=["x"])
    
    #-- chart 1
    bars = alt.Chart(df, title="Regions vs. Countries").mark_bar().encode(
        x="Region:N",
        y="count():Q",
        color=alt.condition(selectedRegion,
                            alt.ColorValue("steelblue"), alt.ColorValue("grey"))
    ).properties(width=350, height=300
    ).add_selection(selectedRegion
    ).interactive()
                    
    #-- chart 2
    columns = df.columns
    xData = columns[4] + ":Q"
    yData = columns[3] + ":Q"
    heatmap = alt.Chart(df, title="Well Being vs. Lefe Expectancy").mark_rect().encode(
        x=alt.X(xData, bin=True),
        y=alt.Y(yData, bin=True),
        color=alt.Color('count()', scale=alt.Scale(scheme="greenblue"),
                        legend=alt.Legend(title="Total Countries")),
        #color=alt.condition(selectedArea, "Region:N", alt.value("lightgray")),
        #tooltip=["Country", "Region", "Wellbeing(0~10):Q", "Happy Planet Index", "Life Expectancy(years):Q"]
    ).properties(width=350, height=300)
    
    circles = heatmap.mark_point().encode(
        alt.ColorValue('magenta'),
        alt.Size("count()", legend=alt.Legend(title="Records in Selection"))
        ).interactive()
    
    heatmapCircle = alt.layer(heatmap, circles)
    
    #--overlap
    chart = alt.hconcat(heatmapCircle, bars, spacing=50, title="",
              ).configure_title(color='green', fontSize=24, align="center", anchor="middle"
              ).configure_axis(labelFontSize=14,
                               labelColor="red",
                               titleFontSize=20,
                               titleColor="blue",
                               )
    chart.show()
    
if (__name__ == "__main__"):
    df = l4_dataset(show=False)
    #ex27_SDV_Zoom(df)
    #ex28_SDV_Zoom_Hover(df)
    #ex29_SelectedArea(df)
    #ex30_SelectedArea_Zoom_Hover(df)
    #ex31_MultiplePlot(df)
    #ex31_Slecetion(df)
    #ex32_Selection_FeatureValue_MP(df)
    #testAltair_MP_weather()
    
    #ex33_Bar(df)
    #ex34_Bar_Selection(df)
    #ex35_Heatmap(df)
    #ex35_Heatmap_Circle(df)
    #ex36_Bar_Heatmap(df)
    ex37_Bar_Link_Heatmap(df)
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:56:13 2022

@date:2022/05/31
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
def l4_dataset(dataset=InputPath + "/googleplaystore.csv"):
    df = pd.read_csv(dataset)
    print("Columns info. --> \n", df.info(), sep="")
    print("\nNumerical Data info. --> \n", df.describe(), sep="")
    print("\nCategorical Data info. --> \n", df.describe(include=object), sep="")
    print("\ndata --> \n", df.head(5), sep="")
    return df

if (__name__ == "__main__"):
    df = l4_dataset(InputPath + "/googleplaystore.csv")
    
    gps_apps_df = df.dropna()
    
    selectedCategory = alt.selection(type="single", encodings=['x'])
    
    alt.data_transformers.enable('default', max_rows=None)
    bars = alt.Chart(gps_apps_df, title="Content Rating").mark_bar().encode(
        x='Content Rating:N',
        y='count():Q',
        color=alt.condition(selectedCategory, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
    ).properties(width=100, height=100
    ).add_selection(selectedCategory)
                 
    #-- Heatmap indicating number of apps across app Category and Rating ranges.
    heatmap = alt.Chart(gps_apps_df, title="Rating of Category").mark_rect().encode(
        alt.X('Category:N'),
        alt.Y('Rating:Q', bin=True),
        alt.Color('count()',
            scale=alt.Scale(scheme='greenblue'),
            legend=alt.Legend(title='Total Apps')
        )
    ).properties(width=400, height=100)
    
    #-- Circle stick on heatmap
    circles = heatmap.mark_point().encode(
        alt.ColorValue('magenta'),
        alt.Size('count()', scale=alt.Scale(domain=(1, 600), range=(1, 200)),
                            legend=alt.Legend(title='Apps in Selection'))
    ).transform_filter(selectedCategory)
    
    heatmapCircles = alt.layer(heatmap, circles)
    
    chart = alt.hconcat(heatmapCircles, bars, spacing=50, title="Google Play Store Apps Rating"
                ).configure_title(color='green', fontSize=22, align="center", anchor="middle"
                ).configure_axis(labelFontSize=14,
                                 labelColor="red",
                                 titleFontSize=20,
                                 titleColor="blue",
                                 )
    chart.show()
    
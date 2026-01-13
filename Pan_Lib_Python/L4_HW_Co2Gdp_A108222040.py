# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 16:43:44 2022

@date:2022/06/03
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
def l4_dataset(dataset=InputPath + "/new_co2_gdp.csv"):
    df = pd.read_csv(dataset)
    print("Columns info. --> \n", df.info(), sep="")
    print("\nNumerical Data info. --> \n", df.describe(), sep="")
    print("\nCategorical Data info. --> \n", df.describe(include=object), sep="")
    print("\ndata --> \n", df.head(5), sep="")
    return df

if (__name__ == "__main__"):
    df = l4_dataset(InputPath + "/new_co2_gdp.csv")
    
    gdp_aco2_df = df.dropna()
    
    selectedRegion = alt.selection(type="single", encodings=['x'])
    
    alt.data_transformers.enable('default', max_rows=None)
    bars = alt.Chart(gdp_aco2_df, title="Region").mark_bar().encode(
        x='region:N',
        y='count():Q',
        color=alt.condition(selectedRegion, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
    ).properties(width=200
    ).add_selection(selectedRegion)
                 
    #-- Heatmap indicating number of apps across app Category and Rating ranges.
    heatmap = alt.Chart(gdp_aco2_df, title="Co2 & GDP of Region").mark_rect().encode(
        alt.X('co2', bin=True),
        alt.Y('gdp', bin=True),
        alt.Color('count()',
            scale=alt.Scale(scheme='greenblue'),
            legend=alt.Legend(title='Region Count')
        )
    ).properties(width=400, height=200)
    
    #-- Circle stick on heatmap
    circles = heatmap.mark_point().encode(
        alt.ColorValue('magenta'),
        alt.Size('count()', scale=alt.Scale(domain=(1, 2000), range=(1, 200)),
                            legend=alt.Legend(title='Total GDP & CO2'))
    ).transform_filter(selectedRegion)
    
    heatmapCircles = alt.layer(heatmap, circles)
    
    chart = alt.hconcat(heatmapCircles, bars, spacing=50, title="CO2 & GDP relationship"
                ).configure_title(color='green', fontSize=22, align="center", anchor="middle"
                ).configure_axis(labelFontSize=14,
                                 labelColor="red",
                                 titleFontSize=20,
                                 titleColor="blue",
                                 )
    chart.show()
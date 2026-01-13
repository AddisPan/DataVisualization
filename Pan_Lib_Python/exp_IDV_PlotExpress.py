# -*- coding: utf-8 -*-
"""
Created on Tue May 10 13:32:54 2022

@date:2022/05/10
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

import plotly.express as px
import plotly.io as pio


#Method
#scatter1
def ex1():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    fig.show()

#line
def ex2():
    df = px.data.gapminder()
    df.describe()
    df.info()
    fig = px.line()
    fig.show()

#bar
def ex7():
    
    
def ex11():
    data = dict(
        number=[39, 27.4, 20.6, 11, 2],
        stage=["Website visit", "Downloads", "Potential customers", "Requested price", "Invoice sent"])
    fig = px.funnel(data, x='number', y='stage')
    fig.show()    


if (__name__ == "__main__"):
    ex1()
    ex2()
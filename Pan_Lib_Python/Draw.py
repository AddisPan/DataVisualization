# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:18:42 2022

@date:2022/03/22
@author: A108222040
@subject:
"""
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

###Program Code 
###Import packages
import pandas as pd
import numpy as np

###Data
data = [100, 110, 150 ,170, 190, 200, 220]
weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
"""
dists = {"name":["Banqiao", "Beitun", "Sanmin", "Yonghe", "Cianjhen", "Xinyi"],
         "population":[550000, 200000, 350000, 200000, 350000, 300000]}
dists = {"name":["Banqiao", "Beitun", "Sanmin", "Yonghe", "Cianjhen", "Xinyi"],
         "population":[550000, 200000, 350000, 200000, 350000, 300000],
         "area":[50000, 70000, 100000, 20000, 35000, 30000]}
"""

datab = [100, 110, 150, 170, 190, 200, 220]
usage = {"os": ["Windows","Mac OS", "Linux", "Chrome OS", "BSD"],
         "precentage": [88.78, 8.21, 2.32, 0.34, 0.02]}

fruits = ["Apple", "Pears", "Bananas", "Orange"]
precentage = [30, 10, 40, 20]
###Draw Method
def Plot_Line1():
    s = pd.Series(data)
    s.plot()
    
def Plot_Line2():
    s = pd.Series(data, index=weekday)
    s.plot()
"""
def Plot_Line3():
    df = pd.DataFrame(dists, columns=["population"], index=dists["name"])
    print(df)
    df.plot(xticks=range(len(df.index)), use_index=True)                    #kind 預設是line
    df.plot(xticks=range(len(df.index)), use_index=True, rot=90)
   

def Plot_Line4():
    df = pd.DataFrame(dists, columns=["population", "area"], index=dists["name"])
    print(df)
    df["area"] *= 1000
    df.plot(xticks=range(len(df.index)), use_index=True, rot=90)
"""    

def Plot_Bar1():
    s = pd.Series(datab)
    s.plot(kind="bar", rot=0)
    
def Plot_Bar2():
    df = pd.DataFrame(usage, columns=["precentage"], index=usage["os"])
    print(df)
    df.plot(kind="bar")
    
def Plot_Pie1():
    s = pd.Series(precentage, index=fruits, name="Fruits")
    print(s)
    s.plot(kind="pie")
    
def Plot_Pie2():
    s = pd.Series(precentage, index=fruits, name="Fruits")
    print(s)
    explode = [0.1, 0.3, 0.1, 0.3]
    s.plot(kind="pie", figsize=(6, 6), explode=explode)                 #浮突的 pie chart
    
def Plot_Scatter():
    x = np.linspace(0, 2*np.pi, 50)
    y = np.sin(x)
    df = pd.DataFrame({"x":x, "y":y})
    df.plot(kind="scatter", x="x", y="y", title="Sin(x)")

"""    
def BoxPlot():
    iris = pd.read_csv(InputPath + "/iris.csv")
    iris.boxplot(column="sepal_length", by="target", figsize=(6,5))
"""  
    
if (__name__ == "__main__"):
    #Plot_Line1()
    #Plot_Line2()
    #Plot_Line3()
    #Plot_Line4()
    #Plot_Bar1()
    #Plot_Bar2()
    #Plot_Pie1()
    #Plot_Pie2()
    Plot_Scatter()
    #BoxPlot()
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:47:58 2022

@date:2022/04/26
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
from matplotlib import pyplot as plt

##bokeh
from bokeh.io import curdoc, output_notebook, save
from bokeh.plotting import figure, show, output_file, output_notebook

# interactive tool/method for mapping data from pandas DF to data 
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.models import HoverTool, Slider 
from bokeh.models import CustomJS
from bokeh.palettes import Spectral6    # pallette for the plot
from bokeh.layouts import row, column, gridplot

#---- Plotly ----#
import plotly.express as px

###Codes
def l3_dataset(dataset=InputPath + "/co2.csv"):
    df = pd.read_csv(dataset)
    print("Columns info. -->\n", df.info(), sep="")
    print("\nNumerical Data info. -->\n", df.describe(), sep="")
    print("\nCategorical Data info. -->\n", df.describe(include=object), sep="")
    print("\ndata -->\n", df.head(5), sep="")
    return df

def e22_dataset():
    #-- load data
    co2 = pd.read_csv(InputPath + "/co2.csv")
    gdp = pd.read_csv(InputPath + "/gapminder.csv")
    
    #-- preproceesing data
    c_gdp = gdp[["Country","region"]].drop_duplicates()
    
    #--- inner join gdp(Country) and co2(country), 這樣co2才能有 region的資料 (co2 的)
    co2_gdp = pd.merge(c_gdp, co2, left_on="Country", right_on="country", how="inner")
    co2_gdp = co2_gdp.drop("Country", axis="columns") # Country/country 在 gdp 是 Country
    
    #-- change the format of a Dataframe with specified identifier
    # 保留 country and region 兩個特徵屬性, 其他的特徵屬性就依這兩個屬性質變成 muti-value 的 repeating group
    # 然後設定好 year 的 data type 為 int64, 依country and year 作排序
    #最後產生 carbon dioxide emissions per year per country
    columns = ["country", "region", "year", "co2"]
    new_co2 = pd.melt(co2_gdp, id_vars=["country", "region"])
    new_co2.columns = columns
    
    new_co2 = new_co2[new_co2["year"].astype("int64")>1963]
    new_co2 = new_co2.sort_values(by=["country","year"])
    new_co2["year"] = new_co2["year"].astype("int64")
    
    print("Columns info. -->\n", new_co2.info(), sep="")
    print("\ndata -->\n", new_co2.head(5), sep="")
    
    # 產生 GDP per year per country
    new_gdp = gdp[["Country", "Year", "gdp"]]
    new_gdp.columns = ["country", "year", "gdp"] # columns 全變成小寫 , 跟co2
    
    print("Columns info. -->\n", new_gdp.info(), sep="")
    print("\ndata -->\n", new_gdp.head(5), sep="")
    
    #-- merge co2 and gdp with columns["country", "year"] using left join co
    # co2 資料較多 left join 可保留 gdp中, 對應不到的 co2
    new_co2_gdp = pd.merge(new_co2, new_gdp, on=["country", "year"], how="left")
    new_co2_gdp = new_co2_gdp.dropna()
    
    print("Columns info. -->\n", new_co2_gdp.info(), sep="")
    print("\ndata -->\n", new_co2_gdp.head(5), sep="")
    
    #-- show correlation of co2 and gdp
    np_co2 = np.array(new_co2_gdp["co2"])
    np_gdp = np.array(new_co2_gdp["gdp"])
    relation_co2_gdp = np.corrcoef(np_co2, np_gdp)
    print("relation of co2 and gdp -->\n", relation_co2_gdp, sep="")
    
    return new_co2_gdp

#Q4 circle and scatter difference
#Q5 HoverTool: color of text in tooltip
def ex23_25_SDVtoIDV(dataSource):
    #initial seeting
    regionsList = dataSource.region.unique().tolist() #get regioin name
    colorMapper = CategoricalColorMapper(factors=regionsList, palette=Spectral6)  #assign color to different
    
    #set data source: x: gdp, y: co2
    sourceAll = ColumnDataSource(data={'x': dataSource.gdp,
                                       'y': dataSource.co2,
                                       'country': dataSource.country,
                                       'region': dataSource.region})
    curYear = 2000
    source = ColumnDataSource(data={'x': dataSource.gdp[dataSource['year'] == curYear],
                                    'y': dataSource.co2[dataSource['year'] == curYear],
                                    'country': dataSource.country[dataSource['year'] == curYear],
                                    'region': dataSource.region[dataSource['year'] == curYear]})
    #save the minimum and maximum values of the gdp/co2 column: x/y min/max
    xmin, xmax = min(dataSource.gdp), max(dataSource.gdp)
    ymin, ymax = min(dataSource.co2), max(dataSource.co2)
    
    #create the empty figure: plot
    dvPlot = figure(title="CO2 Emissions vs GDP in {}".format(curYear),
                    x_range=(xmin, xmax),
                    y_range=(ymin, ymax))

    #static DV
    # dvPlot.circle(x='x', y='y',  fill_alpha=0.8,
    #               source=source, legend='region',
    #               color=dict(field='region', transform=colorMapper),
    #               size=7)
    dvPlot.scatter(x='x', y='y',  fill_alpha=0.8,
                    source=source, legend='region',
                    color=dict(field='region', transform=colorMapper),
                    size=7)
    
    #set the legend.location attribute of the plot
    dvPlot.legend.location = 'top_right'
    
    #set the x/y-axis label
    dvPlot.xaxis.axis_label = 'Income Per Person'
    dvPlot.yaxis.axis_label = 'CO2 Emisssions (tons per person)'
    #show(dvPlot)
    
    #ex25
    hover = HoverTool(tooltips="""
    <div style ="border-style: solid;border-width: 15px;background-color:black;">         
        <div>
            <span style="font-size: 12px; color: white;font-family:century gothic;">Country @country</span><br>
            <span style="font-size: 12px; color: yellow;font-family:century gothic;">GDP @x</span><br>
            <span style="font-size: 12px; color: orange;font-family:century gothic;">CO2 Emission @y</span>
        </div>
    </div>""")
    dvPlot.add_tools(hover)
    
    #ex24
    yearSlider = Slider(start=min(dataSource.year),
                        end=max(dataSource.year),
                        step=1,
                        value=curYear, # min(dataSource.year),
                        title="Year", width=800)

    def callBK(attr, old, new):
        # set data for interactive DV: add slider to plot
        yr = yearSlider.value
        newData = {'x': dataSource.gdp[dataSource['year'] == yr],
                   'y': dataSource.co2[dataSource['year'] == yr],
                   'country': dataSource.country[dataSource['year'] == yr],
                   'region': dataSource.region[dataSource['year'] == yr], }
        source.data = newData
        dvPlot.title.text = "'Co2 Emissions vs GDP in %d' % yr"
                   
    # set slider event
    # yearSlider.js_on_change("value", callBK) # for CustomJS callback
    yearSlider.on_change('value', callBK)
    
    # output the plot result
    resultLayout = column(dvPlot, yearSlider)
    # curdoc().add_root(layout)
    
    # save 之前先建立 output_file 物件，才會保存成功
    fileName = outputPath + "/co2_gdp_SDV.csv"
    output_file(fileName)
    output_notebook()
    show(resultLayout)
    show(resultLayout)
    
if (__name__ == "__main__"):
    l3_dataset(InputPath + "/co2.csv")
    l3_dataset(InputPath + "/co2.csv")
    co2_gdp = e22_dataset()

    #bokeh
    ex23_25_SDVtoIDV(co2_gdp)    
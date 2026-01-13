# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:57:48 2022

@date:2022/04/09
@author: A108222040
@subject:Static DV with Global Patterns
"""
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

###import packages
import pandas as pd
import seaborn as sns
import numpy as np
import math
from matplotlib import pyplot as plt

#---Lesson 2: mpg dataset description
"""
def 12_mpgDataset():
    mpg_df = sns.load_dataset("mpg")
    print("Columns info. -->\n", mpg_df.info(), sep="")
    print("Numerical Data info. -->\n", mpg_df.describe(), sep="")
    print("Categorical Data info. -->\n", mpg_df.describe(include=object), sep="")
"""

"""
def 12_flightsDataset():
    flights_df = =pd.read_csv(inPath + "/flights.csv")
    print("Columns info. -->\n", flights_df.info(), sep="")
    print("Numerical Data info. -->\n", flights_df.describe(), sep="")
    print("Categorical Data info. -->\n", flights_df.describe(include=object), sep="")
"""

def ex13_scatter():
    #hue要改, 改顏色(截兩張圖)
    mpg_df = sns.load_dataset("mpg")
    plt.figure(figsize=(4,4))   #width, height
    #點有改顏色
    
    #ax = sns.scatterplot(x="weight", y="mpg", data=mpg_df, color='red')
    
    #hue 變成 displacement size有大有小
    ax = sns.scatterplot(x="weight", y="mpg", data=mpg_df, hue="displacement", size="displacement", sizes=(20, 200))
    
    ax.set_title("Mile Per Gallon", size=24)
    #plt.savefig(outputPath, "/ex_13scatter.jpg")
    plt.show()   

def ex14_hexagonBin():
    #能不會重疊 標題位置改動
    mpg_df = sns.load_dataset("mpg")
    """
    ax = sns.jointplot(x="weight", y="mpg", data=mpg_df,
                       height=4, kind="hex", color="#ff0000")
    """
    ax = sns.jointplot(x="weight", y="mpg", data=mpg_df,
                       height=4, kind="hist", color="#ff0000")
    
    ax.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    ax.fig.suptitle("Mile Per Gallon", size=24)
    
    
    plt.show()
    
def ex15_contour():
    #cybar位置改變(右邊那個) 顏色變調色盤 hue要加
    mpg_df = sns.load_dataset("mpg")
    
    sns.set_style("white")
    #contour plot
    mpg_df = sns.load_dataset("mpg")
    plt.figure(figsize=(4,4))
    ax = sns.kdeplot(x=mpg_df.weight, y=mpg_df.mpg, data=mpg_df, hue='origin',
                     shade=True, bw=1, cbar=True, cmap="mako",
                     cbar_kws = {'location':'bottom', 'aspect':80, 'pad':0.05, 'anchor':(0.5, -1.0)})
    ax.set_title("Mile Per Gallon", size=24)
    plt.show()    
    #hue無
    #重疊
    
def ex17_multipleLine():
    #tick畫出來 迴圈 圖例
    flights_df = sns.load_dataset("flights")
   
    plt.figure(figsize=(5,4))
    
    monthList = flights_df["month"].unique()
    colors = ['#FF00FF', '#28FF28', '#0080FF', '#9F4D95', '#FFFF37', '#842B00',
              '#3C3C3C', '#02C874', '#743A3A', '#616130', '#000000', '#460046']
    sns.set_style("ticks")
    for ii,mm in zip(range(len(monthList)), monthList):
        ax = sns.lineplot(x="year", y="passengers",
                          data=flights_df[flights_df['month']==mm],
                          color=colors[ii])
    
    ax.set_title("Flights", size=24)
    plt.subplots_adjust(right=0.8)
    ax.legend(labels = monthList,loc = 2, bbox_to_anchor = (1,1))
    
    plt.show()
    #迴圈方式會造成month很多 改顏色
    """
    ax = sns.lineplot(data=flights_df, x="year", y="passengers", hue="month", style="month")
    ax.set_title("Flights", size=24)
    """

def ex18_heatmap():
    #change example to mpg  model_year, weight, mpg
    """
    flights_df = sns.load_dataset("flights")
    df_pivoted = flights_df.pivot("month", "year", "passengers") 
    
    #heatmap
    sns.set_style("white")  
    plt.figure(figsize=(4,4))
    #heatmap method 2
    ax = sns.heatmap(flights_df.pivot_table(index="month", columns="year", values="passengers"),
                     cmap="copper", cbar_kws={'label': "passengers"})
    ax.set_title("Flight", size=24, fontweight='hold', y=1)
    """
    
    mpg_df = sns.load_dataset("mpg")
    df_pivoted = mpg_df.pivot_table("model_year", "weight", "mpg")
    
    #heatmap
    sns.set_style("white")
    plt.figure(figsize=(4,4))
    #heatmap method 2
    ax = sns.heatmap(df_pivoted, cmap="copper", cbar_kws={'label': "mpg"})
    ax.set_title("Mpg", size=24)


def ex18_clustermap():
    #cbar改變位置 title y的位置
    flights_df = sns.load_dataset("flights")
    df_pivoted = flights_df.pivot("month", "year", "passengers") #parameters: row, column, cell
    
    #heatmap
    #cluster by row
    ax = sns.clustermap(df_pivoted, col_cluster=False, row_cluster=False,
                        metric="correlation", #default is enculiden
                        cmap="copper", cbar_kws={'label': "passengers"},
                        cbar_pos=(1, 0.8, 0.05, 0.18), figsize=(4, 4))   #cbar_pos(left, bottom, width, height)
    ax.fig.suptitle("Flight - month", size=24) #clustermap has no attribute set_title
    plt.show()
    # cluster by column
    ax = sns.clustermap(df_pivoted, col_cluster=False, row_cluster=False,
                        cmap="coolwarm", cbar_kws={'label': "passengers"},
                        cbar_pos=(1, 0.8, 0.05, 0.18), figsize=(4, 4))
    ax.fig.suptitle("Flight - year", size=24) #clustermap has no attribute set_title
    plt.show()
    # cluster by both
    ax = sns.clustermap(df_pivoted, #col_cluster=False, row_cluster=False,  #預設兩軸是True
                        cmap="vlag", cbar_kws={'label': "passengers", 'orientation':'horizontal'},
                        metric="correlation", #mean, std, correlation, complete, average, single...
                        cbar_pos=(1, 0.8, 0.2, 0.18), figsize=(4, 4))
    #ax.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    ax.fig.suptitle("Flight - month+year", size=24, fontweight='bold', y=1.1) #clustermap has no attribute set_title  
    plt.show()

def ex19_clustermap_linkage():
    flights_df = sns.load_dataset("flights")
    df_pivoted = flights_df.pivot("month", "year", "passengers") #parameters: row, column, cell
    
    # cluster with average linkage - average of all pairs
    ax = sns.clustermap(df_pivoted, col_cluster=False, #row_cluster=False,  #預設兩軸是True               
                        metric="correlation", method='average',
                        cmap="vlag", cbar_kws={'label': "passengers"},
                        cbar_pos=(1, 0.8, 0.18, 0.18), figsize=(4, 4))
    #ax.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    ax.fig.suptitle("Flight - Average", size=16, fontweight='bold', y=1.02) #clustermap has no attribute set_title
    plt.show()
    # cluster with average linkage - average of all pairs
    ax = sns.clustermap(df_pivoted, col_cluster=False, #row_cluster=False,  #預設兩軸是True               
                        metric="correlation", method='complete',
                        cmap="vlag", cbar_kws={'label': "passengers"},
                        cbar_pos=(1, 0.8, 0.18, 0.18), figsize=(4, 4))
    #ax.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    ax.fig.suptitle("Flight - Complete", size=16, fontweight='bold', y=1.02) #clustermap has no attribute set_title
    plt.show()
    # cluster with average linkage - average of all pairs
    ax = sns.clustermap(df_pivoted, col_cluster=False, #row_cluster=False,  #預設兩軸是True               
                        metric="correlation", method='single',
                        cmap="vlag", cbar_kws={'label': "passengers"},
                        cbar_pos=(1, 0.8, 0.18, 0.18), figsize=(4, 4))
    #ax.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    ax.fig.suptitle("Flight - Single", size=16, fontweight='bold', y=1.02) #clustermap has no attribute set_title
    plt.show()

def ex20_box():
    mpg_df = sns.load_dataset("mpg")
    
    plt.figure(figsize=(4,4))
    sns.boxplot(x='model_year', y='mpg', data=mpg_df, palette="Set3")
    plt.title("MPG vs Model_Year", size=16)
    plt.show()
    
    
    #create new feature
    mpg_df['model_decade'] = np.floor(mpg_df.model_year/10)*10
    mpg_df['model_decade'] = mpg_df['model_decade'].astype(int)
    
    #a boxplot with multiple classes - ten years
    plt.figure(figsize=(4,4))
    sns.boxplot(x='model_decade', y='mpg', data=mpg_df, palette="Set3")
    plt.title("MPG vs Model_Year(Decade)", size=16)
    plt.show()
    
    #boxplot
    plt.figure(figsize=(4,4))
    sns.boxplot(x='model_decade', y='mpg', data=mpg_df, hue="origin", palette="Set3")
    plt.title("MPG vs Model_Year(Decade)  With Origin", size=16)
    plt.ylim(5, 50)
    plt.show()
    
def ex21_violin():
    mpg_df = sns.load_dataset("mpg")  
    
    mpg_df['model_decade'] = np.floor(mpg_df.model_year/10)*10
    mpg_df['model_decade'] = mpg_df['model_decade'].astype(int)
    
    #code for violinplots
    #parameter hue is used to group by a specific feature , in this cas 'origin'
    plt.figure(figsize=(4,4))
    sns.violinplot(x='model_decade', y='mpg', data=mpg_df, hue='origin', palette="light:#5A9")
    plt.title("MPG vs Model_Year(Decade)  With Origin", size=16)
    plt.ylim(5, 50)
    plt.show()
    
def ex_pairplot():
    sns.set_theme(style="ticks")
    penguins_df = sns.load_dataset("penguins")
    print("penguins -->" , penguins_df.info(), sep="")
    sns.pairplot(penguins_df, hue="species", markers=["o", "s", "D"])
    
def ex_displot():
    penguins_df = sns.load_dataset("penguins")
    
    #-- one feature with categories: hist, kde, line
    sns.displot(data=penguins_df, x="flipper_length_mm", hue="species", multiple="stack", palette="Set3")
    plt.title("Penguins-Species With Stack", size=12)
    sns.displot(data=penguins_df, x="flipper_length_mm", hue="species", multiple="stack", kind="kde", palette="light:#5A9")
    plt.title("Penguins-Species With kde", size=16)
    sns.displot(data=penguins_df, x="flipper_length_mm", hue="species", col="species", palette="ch:s=.25,rot=-.25")
    sns.displot(data=penguins_df, x="flipper_length_mm", hue="species", col="sex", kind="kde", palette="pastel")
       
    sns.displot(penguins_df, x="bill_length_mm", color='g', kde=True, palette="husl")
    plt.title("Penguins-Species With Stack & kde", size=16)
     
    sns.displot(penguins_df, x="bill_length_mm", y="bill_depth_mm", hue="species", kind="kde", palette="Set2", rug=True)
    plt.title("Penguins-Species With kde", size=16)
    sns.displot(penguins_df, x="bill_length_mm",  y="bill_depth_mm", binwidth=(2, .5), cbar=True, palette="Set1")
    plt.title("Penguins-Species With bivariate plot", size=16)

def ex_rugplot():
    tips_df = sns.load_dataset("tips")
    
    sns.scatterplot(data=tips_df, x="total_bill", y="tip", hue="time")
    sns.rugplot(data=tips_df, x="total_bill", y="tip", hue="time", height=-0.02, clip_on=False)
    plt.show()
    
if (__name__ == "__main__"):
    #ex13_scatter()
    #ex14_hexagonBin()
    #ex15_contour()
    #ex17_multipleLine()
    #ex18_heatmap()
    #ex18_clustermap()
    #ex19_clustermap_linkage()
    #ex20_box()
    #ex21_violin()
    #ex_pairplot()
    #ex_displot()
    #ex_rugplot()
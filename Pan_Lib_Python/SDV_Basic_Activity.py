# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 00:59:23 2022

@date:2022/04/09
@author: A108222040
@subject:
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

###Codes
olympics_df = pd.read_csv(InputPath + "/athlete_events.csv")

#preview dataframe
print("Olympic history data shape -->", olympics_df.shape)
print("Olympic history data info -->", olympics_df.info())
print("Olympic history data numerical data -->", olympics_df.describe())
print("Olympic history data categorical data -->", olympics_df.describe(include=object))

# filter the dataframe to contain medal winners only (for non-winners, the Medal feature is NaN)
# note use of the inplace parameter
olympics_winners = olympics_df.dropna(subset=['Medal'])
print("Olpymic winners shape -->", olympics_winners.shape)

#print records for each value of the feature 'Sport'
olympics_winners_2016 = olympics_winners[(olympics_winners.Year == 2016)]
olympics_winners_2016_sportCount = olympics_winners_2016.Sport.value_counts()
print("Olympics winners 2016 sport value count -->\n",
      olympics_winners_2016_sportCount, sep="")

#list the top 5 sports
#top_sports = ['Atheletics', 'Swimming', 'Rowing', 'Football', 'Hockey']
top_sports = olympics_winners_2016_sportCount[0:5].index

print(top_sports)
#subset the dataframe to include data from the top sports
olympics_top_sports_winners_2016 = olympics_winners_2016[(olympics_winners_2016.Sport.isin(top_sports))]
print("top sports winners in 2016 -->\n",
      olympics_top_sports_winners_2016.shape, sep="")
"""
# generate bar plot indicating count of medals awarded in each of the top sports
g = sns.catplot('Sport', data=olympics_top_sports_winners_2016,
                kind="count", aspect=1.5, size=5, margin_titles=True)
plt.title("Top 5 Sport Winner by Team in 2016", size=20)
plt.show()

g = sns.distplot(olympics_top_sports_winners_2016.Age,
                 kde=False)
g.set_title("Top 5 Sport Winner by Team in 2016 - Age", size=20)
plt.show()

g = sns.catplot('Team', data=olympics_top_sports_winners_2016,
                kind="count", aspect=3, size=5)
g.set_xticklabels(rotation=90)
plt.title("Top 5 Sport Winner by Team in 2016", size=20)
plt.show()

sns.set(style="whitegrid")
g = sns.barplot(x="Sport", y="Weight",
                hue="Sex",
                data=olympics_top_sports_winners_2016)
plt.title("Top 5 Sport Winner by Team in 2016-Sex", size=20)
plt.show()
"""
#Lesson2
"""
#scatter
plt.figure(figsize=(4, 4))
ax = sns.scatterplot(x="Height", y="Weight", data=olympics_top_sports_winners_2016)
plt.title("Top 5 Sport Winner in 2016", size=16)
plt.show()

#hexagonl
ax = sns.jointplot(olympics_top_sports_winners_2016.Height, 
                   olympics_top_sports_winners_2016.Weight,
                   kind="hex", color="#ff0000", height=4)
ax.fig.tight_layout(rect=[0, 0.03, 1, 0.95])
ax.fig.suptitle("Top 5 Sport Winner in 2016", size=24, ha="center")
plt.show()
"""
#Sex vs Weight
#stack
sns.displot(data=olympics_top_sports_winners_2016, x='Sex', hue='Medal', 
            multiple="stack", palette=["Brown", "Silver", "Gold"])
plt.title("Top 5 Sport Winner in 2016 - Sex vs Weight", size=16)
plt.show()

#boxplot
plt.figure(figsize=(4,4))
sns.boxplot(data=olympics_top_sports_winners_2016, x='Sex', y='Weight', hue='Medal', 
            palette=["Brown", "Silver", "Gold"])
plt.title("Top 5 Sport Winner in 2016 - Sex vs Weight", size=16)
plt.show()

#volin
plt.figure(figsize=(4,4))
sns.set_style('white')
ax1 = sns.violinplot(x='Sex', y='Weight', data=olympics_top_sports_winners_2016, hue='Medal',
                     palette=["Brown", "Silver", "Gold"])
plt.title("Top 5 Sport Winner in 2016 - Sex vs Weight", size=16)
plt.show()

#kde
sns.set_theme(style="ticks")
sns.displot(data=olympics_top_sports_winners_2016, x='Sex', hue='Medal', kde=True,
            multiple="stack", rug=True, palette=["Brown", "Silver", "Gold"])
plt.title("Top 5 Sport Winner in 2016 - Sex vs Weight", size=16)
plt.show()

#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

import plotly.express as px


# In[7]:


#--data describing insurance_America
df = pd.read_csv(InputPath + "/Final/US_youtube_trending_data_process.csv", encoding='latin1')
print("Original data -----> ")
df.info()
df.describe(include="all")


# In[9]:


plt.figure(figsize=(6,6))   #width, height

ax = sns.scatterplot(data=df, x="view_count", y="likes")
    
ax.set_title("Medical Cost Personal(Smoker)", size=12)
#plt.savefig(outputPath, "/ex_13scatter.jpg")
plt.show()   
#可以看到說有抽菸的不管在哪個年齡層都花災醫療的費用較高


# In[ ]:





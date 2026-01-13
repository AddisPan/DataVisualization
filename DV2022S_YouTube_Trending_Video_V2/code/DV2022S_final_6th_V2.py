#!/usr/bin/env python
# coding: utf-8

# In[4]:


#https://www.kaggle.com/code/skalskip/youtube-data-exploration-and-plotly-visualization
#https://www.kaggle.com/code/quannguyen135/what-is-trending-on-youtube-eda-with-python
#https://www.kaggle.com/code/yanpapadakis/trending-youtube-video-metadata-analysis
#https://www.kaggle.com/code/jyotishranjan/analysis-on-trending-youtube-videos
##Enviroment(自己的環境) __ input, output, image
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

##Packages(安裝套件)
###Data process #pip install
import pandas as pd
###Draw
import numpy as np
import seaborn as sns
import math
import matplotlib.pyplot as plt
from matplotlib import cm

import plotly.express as px

import altair as alt
from vega_datasets import data

#process language
import re
import nltk


#------- Dataset
###Dataset all load
#USA
us_yt = pd.read_csv(InputPath + "/US_youtube_trending_data_process.csv", encoding='latin1') 
print("Process US data -----> ")
us_yt.info()

#Canada
ca_yt = pd.read_csv(InputPath + "/CA_youtube_trending_data_process.csv", encoding='latin1') 
print("Process Canda data -----> ")
ca_yt.info()

#Germany
de_yt = pd.read_csv(InputPath + "/DE_youtube_trending_data_process.csv", encoding='latin1') 
print("Process Germany data -----> ")
de_yt.info()

#France
fr_yt = pd.read_csv(InputPath + "/FR_youtube_trending_data_process.csv", encoding='latin1')
print("Process Germany data -----> ")
de_yt.info()

#United Kingdom (Great Brittain)
gb_yt = pd.read_csv(InputPath + "/GB_youtube_trending_data_process.csv", encoding='latin1') 
print("Process United Kingdom data -----> ")
gb_yt.info()

#India
in_yt = pd.read_csv(InputPath + "/IN_youtube_trending_data_process.csv", encoding='latin1')
print("Process India data -----> ")
in_yt.info()

#Japan
jp_yt = pd.read_csv(InputPath + "/JP_youtube_trending_data_process.csv", encoding='latin1') 
print("Process Japan data -----> ")
jp_yt.info()

#South Korea
kr_yt = pd.read_csv(InputPath + "/KR_youtube_trending_data_process.csv", encoding='latin1') 
print("Process South Korea data -----> ")
kr_yt.info()

#Mexico
mx_yt = pd.read_csv(InputPath + "/MX_youtube_trending_data_process.csv", encoding='latin1') 
print("Process Mexico data -----> ")
mx_yt.info()

#Russia
ru_yt = pd.read_csv(InputPath + "/RU_youtube_trending_data_process.csv", encoding='latin1') 
print("Process Russia data -----> ")
ru_yt.info()



#-----統一入口 web->
# 引入 tkinter 模組，始用別名 tk 代表 tkinter，可以少打字
import tkinter as tk

# 建立主視窗，建立 Tk 物件實例
window = tk.Tk()

# 設定視窗標題
window.title('Hello World')
# 設定視窗大小寬x高 800x600
window.geometry('800x600')
# 設定背景顏色為白色
window.configure(background='white')

def one():
    #Q1 : 各個影片類型的數量
    us_yt = pd.read_csv(InputPath + "/US_youtube_trending_data_process.csv", encoding='latin1')  #read csv
    plt.figure(figsize=(150,100))   #width, height
        #ax = sns.countplot(data=us_yt, y="category_title")   #draw y軸為影片類型 
        #ax.set_title("America video type count", size=200)   #設置標題
        #ax.set_xlabel("count",fontsize=150)                  #xlabel的大小
        #ax.set_ylabel("category_title",fontsize=150)         #ylabel的大小
        #ax.tick_params(labelsize=150)
    category = us_yt["category_title"].unique()
    
    fig = px.histogram(us_yt, x="category_title", color="category_title",
                         title="America video type count")
    
    buttons = []
    for i in category:
        buttons.append(dict(label=i,
                method = 'update',
                args=[{'visible' : [True if j==i else False for j in category]}, 
                     {'showlegend' : True}]))
    buttons.append(dict(label='All',
                       method='update',
                       args=[{'visible' : [True for j in category]},
                             {'showlegand' : True}]))
    fig.update_layout(
        updatemenus=[
            dict(
                direction='down',
                active=0,x=0.5,y=1.5,
                buttons = buttons
            )
        ]
    )

    fig.show()

def two():
    #Q2-- 各類型影片觀看人數
    #x軸是觀看數 y軸是影片類型 hover_data中有影片標題 喜歡數 不喜歡數 留言數 trending日期
    fig = px.scatter(us_yt, x="view_count", y="category_title", 
                     color="category_title", hover_data=['title','likes','dislikes','comment_count','trending_date'],
                     title="America Category_title with view_count")

    fig.write_image(outputPath + "/America_video_watch.jpg")
    fig.show()
    
def three():
    ##Q3:美國前20產出最多影片地頻道 資料前處理
    #前20個產出最多影片頻道的名稱
    l=us_yt.channelTitle.value_counts()[:20].index
    #去抓出前20個產出最多影片頻道的影片數量
    video_count = pd.DataFrame({'channel_title':l,'no_of_videos':us_yt.channelTitle.value_counts()[:20]})
    video_count.index=[i for i in range(1,21)]
    print(video_count)
    
    ##Q3:前20部熱門影片
    plt.figure(figsize=(9,9))
    #x軸是影片的數量 y軸是頻道的名稱
    fig = sns.barplot(y="channel_title",x="no_of_videos",data = video_count)
    fig.set_title("Top 20 Popular Videos", size=20) # 設置標題

    #用前20部熱門影片 各影片的占比
    fig = px.pie(video_count, values='no_of_videos', names='channel_title', title='Top 20 Popular Videos')
    fig.show()

    fig1 = px.sunburst(video_count, values='no_of_videos', names='channel_title', title='Top 20 Popular Videos', 
                      path=['channel_title', 'no_of_videos'], width=700, height=700)
    fig1.show()
    
def four():
    #資料前處理
    us_yt = pd.read_csv(InputPath + "/US_youtube_trending_data_process.csv", encoding='latin1') #read csv
    us_yt["trending_year"]=pd.DatetimeIndex(us_yt['trending_date']).year  #抓取year

    m=list(us_yt["trending_year"].value_counts())
    plt.figure(figsize=(9,9))
    sns.barplot(x=list(us_yt["trending_year"].unique()),y=m)   #各年份影片trending數量

    us_yt["trendingDate"]=pd.DatetimeIndex(us_yt['trending_date']).date  #抓取date

    print(us_yt["trendingDate"][:5]) #前五筆date
    us_yt["trendingDate"]=pd.to_datetime(us_yt["trendingDate"],format = "%Y.%m.%d")
    #us["trending_date"]=pd.to_datetime(us["trending_date]"]).dt.date
    us_yt["publish_date"]=pd.to_datetime(us_yt["publishedAt"]).dt.date  #抓取date
    print(us_yt["publish_date"])
    us_yt["publish_clock"]=pd.to_datetime(us_yt["publishedAt"]).dt.hour #抓取hour
    print(us_yt["publish_clock"][:24]) #前五個時間(0~4點)
    us_yt["publish_date"]=pd.to_datetime(us_yt["publish_date"],format = "%Y/%m/%d")
    l=[]
    for i in us_yt["publish_date"]:
        l.append(i.day_name())
    us_yt["publish_day"]= l
    
    ##draw
    ##Q4Week 
    x=us_yt["publish_day"].value_counts()  #各天影片數量
    print(x.index)
    h=pd.DataFrame({"publish_day":x.index,"no_of_videos":x})
    h.index=[i for i in range(0,7)]  #七天
    plt.figure(figsize=(9,9))
    fig = px.histogram(h, x="publish_day",y="no_of_videos", color="publish_day",
                       title="Number of videos posted in a week") #x軸為(一~日<依據每天數量多寡>) y軸是影片數量
    fig.show()
    
def five():
    #Q6
    #分析觀看數 喜歡數 不喜歡數 留言數
    keep_columns = ['view_count', 'likes', 'dislikes', 'comment_count']
    corr_matrix = us_yt[keep_columns].corr()
    corr_matrix

    def visualize_statistics(us_yt, id_list): # 獲取ID列表
        target_df = us_yt.loc[id_list]

        ax = target_df[['view_count', 'likes', 'dislikes', 'comment_count']].plot.bar() #用bar去呈現

        labels = []
        for item in target_df['title']:
            labels.append(item[:10] + '...') #透過上述影片id 抓前十名的影片名稱
        ax.set_xticklabels(labels, rotation=45, fontsize=10) #影片標題較長 旋轉45度
        ax.set_title("Top 10 video", size=20)
        plt.show()

    sample_id_list = us_yt.sample(n=10, random_state=4).index
    sample_id_list

    visualize_statistics(us_yt, sample_id_list)
    
def six():
    ###Q7
    us_yt = pd.read_csv(InputPath + "/US_youtube_trending_data_process.csv", encoding='latin1') 
    s=pd.Series(us_yt["title"])  #抓影片標題
    l=[]
    for i in range(0,len(s)):
        #主要處理標題中的字 Regular Expression 可以去匹配標題中任何字
        s[i]= re.sub('[^a-zA-Z]', ' ',s[i])
        s[i]= re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",s[i])
        s[i]= re.sub("(\\d|\\W)+"," ",s[i])
        l.append(len(s[i]))
    us_yt["filter_title"]=s
    us_yt["title_length"]=pd.Series(l)


    plt.figure(figsize=(12,12))
    ax = px.scatter(us_yt, x="title_length",y="view_count", color="category_title",
                   title="Length & view_count")
    ax.show()
    
def seven():
    ###8
    ##把國家串成list
    df_list = [us_yt, ca_yt, de_yt, fr_yt, gb_yt, in_yt, jp_yt, kr_yt, mx_yt, ru_yt]
    df_name_list = ['United States', 'Canada', 'Germany', 'France', 'Great Brittain', 'India',
                    'Japan', 'South Korea', 'Mexico', 'Russia']
    #for a in df_list:
    def wordcld(a,j):
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        title_words = list(a["title"].apply(lambda x: x.split()))
        title_words = [x for y in title_words for x in y] # title文字
        #print(df_name_list[j])
        wc = WordCloud(width=1200, height=500, 
                                    collocations=False, background_color="black", 
                                    colormap="tab20b").generate(" ".join(title_words)) #背景為黑色 有colormap
        plt.figure(figsize=(15,10))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title(df_name_list[j], fontsize=30)
        plt.ylabel(df_name_list[j])
    #迴圈跑十個國家
    j=0
    while j<len(df_list):
        #print(df_name_list[j])
        wordcld(df_list[j],j)
        j=j+1

def eight():
    #Q9
    us_yt = pd.read_csv(InputPath + "/US_youtube_trending_data_process.csv", encoding='latin1')
    category = us_yt["category_title"].unique()

    buttons = [] #下拉式選單

    labels = {'view_count': 'View Count (Millions)', 'trending_date': 'Trending Date'}
    fig = px.area(us_yt, x='trending_date', y='view_count', color="category_title", title='View Count Time Series for category(USA)'
                , labels=labels, height=800) #y軸是觀看數 x軸是日期 
    #buttons
    for i in category:
        buttons.append(dict(label=i,
                    method = 'update',
                    args=[{'visible' : [True if j==i else False for j in category]},
                         {'showlegend':True}]))
    buttons.append(dict(label='All',
                        method='update',
                        args=[{'visible': [True for j in category]},
                               {'showlegend': True}]))
    fig.update_layout(
        updatemenus=[
            dict(
                direction='down',
                active=0,x=0.5,y=1.5,
                buttons = buttons
            )
        ]

    )

    fig.update_xaxes(rangeslider_visible=True) #rangeslider

    fig.show()
    
def nine():
    df_list = [us_yt, ca_yt, de_yt, fr_yt, gb_yt, in_yt, jp_yt, kr_yt, mx_yt, ru_yt]
    df_name_list = ['United States', 'Canada', 'Germany', 'France', 'Great Brittain', 'India',
                    'Japan', 'South Korea', 'Mexico', 'Russia']
    
    #資料前處理
    Allcountry_df = pd.DataFrame(columns=['view_count', 'likes', 'dislikes', 'comment_count', 'country'])
    display(Allcountry_df)

    #去抓到10個國家的資料 merge進DataFrame
    count = 0
    entries = 0
    while count != 10:
        current_df = df_list[count]
        entries = entries + len(current_df)
        country_name = df_name_list[count]
        current_df['country'] = country_name
        Allcountry_df = pd.merge(Allcountry_df, current_df, how='outer')
        count += 1
    print(entries)
    
    #Draw
    #Q10: 喜歡 留言數比較
    plt.figure(figsize=(6,6))   #width, height
    #x軸為留言數 y軸為喜歡數 color用國家
    ax = px.scatter(df_list, x=Allcountry_df["comment_count"], y=Allcountry_df["likes"], color=Allcountry_df["country"],
                    title="All Country like(y) vs count(x)")
    ax.write_image(outputPath + "/AllCountry_likes_commentcount.jpg")   

    ax.show()
    
def ten():
    us_yt = pd.read_csv(InputPath + "/US_youtube_trending_data_process.csv", encoding='latin1')
    
    keep_columns = ['view_count', 'likes', 'dislikes', 'comment_count'] # only looking at correlations between these variables
    corr_matrix = us_yt[keep_columns].corr()
    corr_matrix

    fig, ax = plt.subplots()
    heatmap = ax.imshow(corr_matrix, interpolation='nearest', cmap=cm.coolwarm)

    # making the colorbar on the side
    cbar_min = corr_matrix.min().min()
    cbar_max = corr_matrix.max().max()
    cbar = fig.colorbar(heatmap, ticks=[cbar_min, cbar_max])

    # making the labels
    labels = ['']
    for column in keep_columns:
        labels.append(column)
        labels.append('')
    ax.set_yticklabels(labels, minor=False)
    ax.set_xticklabels(labels, minor=False)

    plt.show()
        
    
def One():
    # 一
    one()
def Two():
    # 二
    two()
def Three():
    # 三
    three()
def Four():
    # 四
    four()
def Five():
    # 五
    five()
def Six():
    # 六
    six()
def Seven():
    # 七
    seven()
def Eight():
    # 八
    eight()
def Nine():
    # 九
    nine()
def Ten():
    # 十
    ten()
    
# Pic 1建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button1 = tk.Button(window, text='pic1', command=One)
# 渲染按鈕元件
button1.pack()

# Pic 2建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button2 = tk.Button(window, text='pic2', command=Two)
# 渲染按鈕元件
button2.pack()

# Pic 3建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button3 = tk.Button(window, text='pic3', command=Three)
# 渲染按鈕元件
button3.pack()

# Pic 4建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button4 = tk.Button(window, text='pic4', command=Four)
# 渲染按鈕元件
button4.pack()

# Pic 5建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button5 = tk.Button(window, text='pic5', command=Five)
# 渲染按鈕元件
button5.pack()

# Pic 6建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button6 = tk.Button(window, text='pic6', command=Six)
# 渲染按鈕元件
button6.pack()

# Pic 7建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button7 = tk.Button(window, text='pic7', command=Seven)
# 渲染按鈕元件
button7.pack()

# Pic 8建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button8 = tk.Button(window, text='pic8', command=Eight)
# 渲染按鈕元件
button8.pack()

# Pic 9建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button9 = tk.Button(window, text='pic9', command=Nine)
# 渲染按鈕元件
button9.pack()

# Pic 10建立按鈕元件（第一個參數放入 window 代表要顯示在哪個區塊），顯示文字為 click me，command 是當點擊會觸發處理的函式
button10 = tk.Button(window, text='pic10', command=Ten)
# 渲染按鈕元件
button10.pack()

# 運行主程式，最後一定要運行 window.mainloop()，讓 window 不斷地重新整理
# 這部份可以想成是電影或是動畫，事實上是不斷翻頁，所以就是一個 while 迴圈的感覺 
window.mainloop()


# In[ ]:





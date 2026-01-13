# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 15:25:06 2022

@author: A108222040
"""
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
#imagePath = os.path.join("..","..","Image")
imagePath = os.path.join("..","Image")

import requests
from urllib.request import urlretrieve
import json

from bs4 import BeautifulSoup

import pandas as pd

import sqlalchemy

#----Constant
BASE_URL="https://en.wikipedia.org"
HEADERS={"User-Agent": "Mozilla/5.0"}

nobel_winners = [{"Category":   "Physics",
                  "Name":       "Albert Einstein",
                  "Nationality":"Swiss",
                  "Sex":        "Male",
                  "Year":       1921},
                 {"Category":   "Physics",
                  "Name":       "Paul Dirac",
                  "Nationality":"British",
                  "Sex":        "Male",
                  "Year":       1933},
                 {"Category":   "Chemistry",
                  "Name":       "Marie Curie",
                  "Nationality":"Polish",
                  "Sex":        "Female",
                  "Year":       1911}
                 ]


def getWebNobelPrize(url=BASE_URL+"/wiki/List_of_Nobel_laureates", header=HEADERS):
    try:
        resData=requests.get(url, headers=header)
        soupObj = BeautifulSoup(resData.content, "html.parser")
        dd = soupObj.select_one('table',{'class': 'wikitable sortable'})
        getNobelWinners(dd)
    except Exception as errMessage:
        print("Get Web Page Fail:", errMessage)

def getNobelWinners(table):
    cols = getColumnTitles(table)
    winners = []
    for row in table.select('tr')[1:-1]:
        year = int(row.select_one('td').text[0:4])
        for i, td in enumerate(row.select('td')[1:]):
            for winner in td.select('a'):
                href = winner.attrs['href']
                if not href.startswith("#endnote"):
                    winners.append({'year': year,
                                    'category': cols[i]['name'],
                                    'name': winner.text,
                                    'link': winner.attrs['href']})
    print("Winner ----", len(winners))
    print(winners)
    fileName = outputPath+"/nobelWinnerInProcessingByBs4.json"
    with open(fileName, "w") as fptr:
        json.dump(winners,fptr)

    return winners

def getColumnTitles(table):
    cols=[]
    for th in table.select_one('tr').select('th')[1:]:
        link = th.select_one('a')
        if link:
            cols.append({'name': link.text, 'href':link.attrs['href']})
        else:
            cols.append({'name': th.text, 'href':None})
    return cols

#Wee4
def getWebGreenMap():
    htmlSavePath = imagePath + "/onegreen"
    os.makedirs(htmlSavePath, exist_ok=True)
    
    #Get Web content
    url = 'http://www.onegreen.net/maps/List/List_933.html'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    imgURL = soup.find_all('img')
    print(len(imgURL), "-----\n", imgURL)
    
    #Save img inside web page
    for uu in imgURL:
        urlSrc = uu['src']
        img = 'http://www.onegreen.net/' + urlSrc
        print(img)
        urlretrieve(img, htmlSavePath+"/%s" % urlSrc.split('/')[-1])
        
def getWebSHU():
    #Save path
    htmlSavePath = imagePath + "/shu"
    os.makedirs(htmlSavePath, exist_ok=True)
    
    #find image
    url = 'http://www.shu.edu.tw/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    imgURL = soup.find_all('img')
    print(len(imgURL), "-----\n", imgURL)
    
    for uu in imgURL:
        urlSrc = uu['src']
        if ("http" in urlSrc):
            img = urlSrc
        else:
            img = "http://www.shu.edu.tw/" + urlSrc
        print(img)
        try:
            urlretrieve(img, htmlSavePath+"/%s" % urlSrc.split('/')[-1])
        except Exception as errMessage:
            print("urlretrieve error-----", errMessage)
            
def getWebImage(urlSource="http://www.onegreen.net/maps/List/List_933.html",
                urlImage = "http://www.onegreen.net/",
                htmlSavePath = imagePath + "/temp"):
     os.makedirs(htmlSavePath, exist_ok=True)
     
     url = urlSource
     html = requests.get(url).text
     soup = BeautifulSoup(html, "html.parser")
     imgURL = soup.find_all('img')
     print(len(imgURL), "-----\n", imgURL)
    
     for uu in imgURL:
        urlSrc = uu['src']
        if ("http" in urlSrc):
            img = urlSrc
        else:
            img = urlImage + urlSrc
        print(img)
        try:
            urlretrieve(img, htmlSavePath+"/%s" % urlSrc.split('/')[-1])
        except Exception as errMessage:
            print("urlretrieve error-----", errMessage)
            
def testPandasRW():
    #--csv,html,json
    dataJson = outputPath + "/nobelWinnerInProcessingByBs4.json"
    dataCsv = outputPath + "/nobelWinnerInProcessingByBs4.csv"
    dataHtml = outputPath + "/nobelWinnerInProcessingByBs4.html"
    
    """
    df = pd.read_json(dataJson)
    print("Info -->", df.info())
    print("Data -->", df.head(3), sep="")
    #df = df.reset_index()
    df.set_index("category", )把左邊0~....去掉
    df.to_csv(dataCsv)
    df.to_html(dataHtml)
    """
    
    """
    #--Csv
    df = pd.read_csv(dataCsv)
    print("Columns -->\n", df.columns)
    print("Index -->\n", df.index)
    
    #row
    df = df.set_index("name")
    print("\n\nFind data via specified index -->\n", df.loc["Albert Einstein"])
    df = df.reset_index()
    print("\n\nFind data via index -->\n", df.iloc[2])
    
    #column
    genderCol = df["category"]
    print("\n\nfirst five item in genderCol -->\n", genderCol.head() + "\n")
    
    #groupby
    groupCategory = df.groupby("category")
    groupPhysics =  groupCategory.get_group("Physics")
    print("\n\ngroupCategory --> \n",groupCategory.groups.keys())
    print("\n\nPhysics group -->\n", groupPhysics.head())
    
    #dictionary
    df = pd.DataFrame.from_dict(nobel_winners)
    df.set_index("Name", inplace=True)
    print("Dict head --> \n", df.head())
    df.to_csv(outputPath + "/nobelWinner20220315.csv")
    df.to_json(outputPath + "/nobelWinner20220315.json", orient="records")
    df.to_html(outputPath + "/nobelWinner20220315.html")
    """
    
    #MySQL
    try:
        engine = sqlalchemy.create_engine("mysql://root:@localhost:3306/nobelPrizeWinner?charset=utf8mb4&binary_prefix=true",
                                          isolation_level="READ UNCOMMITTED")
        df = pd.read_sql("winner", engine)
        print("\n\nPanda read from mysql --> \n", df.columns)
        print("Data is --> \n", df.head())
        
        df = pd.read_json(outputPath+"/nobelWinner20220315.json")
        df.to_sql("winner2", engine)
    except Exception as errMessage:
        print("DB Connect fail!")
    

if (__name__ == "__main__"):
    #getWebNobelPrize()
    #getWebGreenMap()
    #getWebSHU()
    #getWebImage("http://www.onegreen.net/maps/List/List_933.html",
    #            "http://www.onegreen.net/", imagePath + "/temp")
    testPandasRW()
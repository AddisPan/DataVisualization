# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 13:32:59 2022

@author: s303
"""

import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

###Read/Write data
import csv
import json
import pandas as pd
import sqlite3


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

### Create db and table
def createDBTable(dbName="A108222040nobelWinner.sqlite",
                  dbTable="CREATE TABLE winner(Category, Name, Nationality, Sex, Year)"):
    try:
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute(dbTable)
        conn.commit()
        conn.close()
    except Exception as mess:
        print("SQLite error, processing abort!!\n", mess)
    
def writeSQLite(dbPath="nobelWinner.sqlite"):
    try:
        data1 = "Peace, Maria Angelita Ressa, USA, Female, 2021"
        fields = data1.split(',')
        sqlString = "INSERT INTO winner (Category, Name, Nationality, Sex, Year) " +\
                    "VALUES ('{0}','{1}','{2}','{3}','{4}')"
        sql1 = sqlString.format(fields[0].strip(), fields[1].strip(),
                                fields[2].strip(), fields[3].strip(),
                                fields[4].strip())

        data2 = nobel_winners[0]
        sql2 = sqlString.format(data2['Category'], data2['Name'], data2['Nationality'],
                                data2['Sex'], data2['Year'])     
        
        df = pd.DataFrame(nobel_winners)
        df = pd.read_json(InputPath + "/Nobel_winner_2021.json")
        
        #connect db and insert data
        conn = sqlite3.connect(dbPath)  #connect DB
        result1 = conn.execute(sql1)    #execute sql
        result2 = conn.execute(sql2)    #execute sql
        result3 = df.to_sql("winner", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()
        print("data1 row count -->", result1.rowcount)
        print("data2 row count -->", result2.rowcount)
        print("data3 row count -->", result3)
    except Exception as mess:
        print("SQLite error, processing abort!!\n", mess)
        
#### Read data from SQLite
def readSQLite(dbPath="nobelWinner.sqlite"):
    try:
         conn = sqlite3.connect(dbPath) # connect DB
         result = conn.execute("SELECT * FROM winner")  #DB query
         resultDF = pd.read_sql("SELECT * FROM winner WHERE Sex like '%Male%'", conn)
         print("\n=====Using sql execute to read from SQLite -->")
         for row in result: #data type of row is tuple
             print(row)     #data type is tuple
             #print("\t".join(row))# 必須 row record 中將每個屬性皆為字串
         print("\n=====Using pandas to read from SQLite -->\n", resultDF, sep="")
         conn.close()
    except Exception as mess:
         print("SQLite error, processing aboty!!\n", mess)
        
        
if (__name__ == "__main__"):
    createDBTable() #Case 1: create db and table
    writeSQLite()   #Case 2: insert data and into DB
    readSQLite()    #Case 3: read data from DB
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:49:06 2022
@date:2022/03/22
@author: A108222040
"""
###Enviroment Setting
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")

###Program Code 
###Import packages
import pymysql
import mysql.connector
import sqlalchemy
import pandas as pd

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


##Methods
## Check db server
def checkDBserver(myHost="localhost", account="root", pw=""):
    try:
        #-- connect db server
        serverConn = mysql.connector.connect(host=myHost,
                                             user=account, password=pw)
        #--list db
        myCur = serverConn.cursor()
        myCur.execute("SHOW DATABASES") #s remeber
        for db in myCur: print(db)
        
        #--end or return conn
        serverConn.close()
    except Exception as err:
        print("Connection DB server fail -->", err, sep="")
        
## Connect DB server
def connectDBserver(myHost="localhost", account="root", pw=""):
    try:
        ##-- connect db server
        serverConn = mysql.connector.connect(host=myHost,
                                             user=account, password=pw)
        
        return serverConn
    except Exception as mess:
        print("Connection DB Server Fail -->\n", mess, sep="")
        
        
#有無連接成功
def connectDB(myHost="localhost", account="root", pw="", dbName="a108222040nobelWinner"):
    try:
        #method 2
        dbConn = mysql.connector.connect(
            host=myHost,
            user=account,
            password=pw,
            database = dbName)
        return dbConn
    except Exception as err:
        print("Connection DB fail -->", err)
        
###Create DB    
def createDB(myHost="localhost", account="root", pw="", dbName="a108222040nobelWinner", sqlStr=""):
    try:
        if (sqlStr == ""):
            sqlStr = "CREATE DATABASE " + dbName;
        conn = connectDBserver(myHost=myHost, account=account, pw=pw)
        myCur = conn.cursor()
        result = myCur.execute(sqlStr)
        conn.close()
        print("Create database result -->", result)
    except Exception as err:
        print("Create DB Fail -->", err)       
        
###Create DB table
def createTable(dbConn="", dbName="a108222040nobelWinner", tableName="winnerAllyears",
                sqlStr="",
                columnDT="Category VARCHAR(30), Name VARCHAR(100), " + \
                         "Nationality VARCHAR(100), Sex VARCHAR(50), Year INT(4)"):
    try:
        if sqlStr == "": sqlStr ="CREATE TABLE " + tableName + "(" + columnDT + ")"
        if dbConn != "":
            myCur = dbConn.cursor()
            result = myCur.execute(sqlStr)
            print("Create table result -->", result)
        else:
            dbConn = connectDB(dbName=dbName)
            myCur = dbConn.cursor()
            result = myCur.execute(sqlStr)
            dbConn.close()
    except Exception as err:
        print("Create DB Fail -->", err)
            
### Drop DB table
def dropTable(dbConn, dbName="testdb", tableName="winnerAllyears", sqlStr="", condition=""):
    try:
        if sqlStr == "": sqlStr = "DROP TABLE " + tableName + " " + condition
        if dbConn!="":
            myCur = dbConn.cursor()
            myCur.execute(sqlStr)
        else:
            dbConn = connectDB(dbName=dbName)
            myCur = dbConn.cursor()
            result = myCur.execute(sqlStr)
            dbConn.close()
    except Exception as err:
        print("Drop DB Table Fail -->", err)
    
def insertData(dbConn="", dbName="a108222040nobelWinner", tableName="winner",
                sqlStr="",
                columnValue="Category, Name, Nationality, Sex, Year",
                value=('test', 'test', 'test', 'test', 2022)):
    try:
        if dbConn!="":
            myCur = dbConn.cursor()
            if sqlStr == "":
                sqlStr = "INSERT INTO " + tableName + "(" + columnValue + \
                         ") VALUES(%s, %s, %s, %s, %s)"
                myCur.execute(sqlStr, value)
            else:
                myCur.execute(sqlStr)
            dbConn.commit()
            print("=====", myCur.rowcount, "records(s) inserted")
        else:
            print("DB connection error, processing abort!!")
    except Exception as err:
        print("Insert Data Table Fail -->", err) 


def deleteData(dbName="testdb", sqlStr="DELETE FROM test WHERE account='test'"):
    dbConn = connectDB(dbName)
    myCur = dbConn.cursor()
    myCur.execute(sqlStr)
    dbConn.commit()
    dbConn.close()
    print("====", myCur.rowcount, "records(s) deleted")
    
def updateData(dbName="testdb", sqlStr="UPDATE test SET password='test' WHERE account='test'"):
    dbConn = connectDB(dbName)
    myCur = dbConn.cursor()
    myCur.execute(sqlStr)
    dbConn.commit()
    dbConn.close()
    print("====", myCur.rowcount, "records(s) affected")
    
if (__name__ == "__main__"):
    #checkDBserver(myHost="localhost", account="root", pw="")
    #createDB(sqlStr="CREATE DATABASE a108222040nobelWinner")
    #createDB(myHost="localhost", account="root", pw="",  dbName="nobelWinner1")
    dbConn=connectDB(myHost="localhost", account="root", pw="", dbName="a108222040nobelWinner")
    #print("dbConn -->", dbConn)
    #sqlS = "CREATE TABLE  a108222040nobelWinner(Category VARCHAR(30), Name VARCHAR(100), Nationality VARCHAR(100), Sex VARCHAR(50), Year INT(4))"
    # createTable(dbConn="", dbName="a108222040nobelWinner", tableName="winnerAllyears",
    #             sqlStr="",
    #             columnDT="Category VARCHAR(30), Name VARCHAR(100), " + \
    #                      "Nationality VARCHAR(100), Sex VARCHAR(50), Year INT(4)")
    #dropTable(dbConn, dbName="a108222040nobelWinner", tableName="winnerAllyears", sqlStr="", condition="")
    insertData(dbConn, dbName="a108222040nobelWinner", tableName="winner",
               sqlStr="",
               columnValue="Category, Name, Nationality, Sex, Year",
               value=('test', 'test', 'test', 'test', 2022))
    dbConn.close()
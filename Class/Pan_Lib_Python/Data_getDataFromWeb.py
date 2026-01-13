# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:05:54 2022

@author: Addis
"""
import os,sys
outputPath = os.path.join("..","Output")
InputPath = os.path.join("..","Input")
imagePath = os.path.join("..","Image")
LibPath = os.path.join("Python")
import requests #!pip install requests
from urllib.request import urlretrieve
#---- Package for get google spreadsheet via Web API

#from oauth2client.service_account import SignedJWAssertionCredentials
import gspread 
from oauth2client.service_account import ServiceAccountCredentials

import json

"""
#Case1
resData = requests.get("https://data.taipei/api/getDatasetInfo/downloadResource?id=2e1e7eca-deed-48c2-8c56-5a8b91f36538&rid=7230b654-64e4-4f6f-a159-583f44c0a068")
print(dir(resData))
print("\nThe result of web request (200 means ok) ---", resData.encoding)
#print("\nWeb header ----\n", resData.headers)
print("\nWeb header ----\n", resData.text)
#print("\nWeb header ----\n", resData.content)
"""

#Case2
#print("\npython default encoding -----\n", sys.getdefaultencoding())
#csvURL = "	https://data.taipei/api/getDatasetInfo/downloadResource?id=2e1e7eca-deed-48c2-8c56-5a8b91f36538&rid=7230b654-64e4-4f6f-a159-583f44c0a068"

"""
#Method 1 
csvURL = "https://data.taipei/api/getDatasetInfo/downloadResource?id=2e1e7eca-deed-48c2-8c56-5a8b91f36538&rid=7230b654-64e4-4f6f-a159-583f44c0a068"
resData = requests.get(csvURL)
if (resData.status_code==200):
    print("\ncsv encoding original -----\n", resData.encoding)
    
    print("\ncsv -----\n", resData.text)
    with open(outputPath+ "/20220214.csv", "wb") as fptr:
        fptr.write(resData.content)
else: print("URL not correct!!")
"""


#JSON
jsonURL = "https://sports.tms.gov.tw/opendata/sports_tms.json"

resData = requests.get(jsonURL)
print("\nThe result of web request (200 means ok) ---", resData.status_code)
data = resData.json()
print("\nKeys in json ----\n", data.headers)
#print("\nKeys in json ----\n", data.keys())
#print("\nWeb header ----\n", resData.text)
#print("\nWeb header ----\n", resData.content)

filename = outputPath + "/Animal.json"
urlretrieve(jsonURL, filename)

    

#Google sheet
#Declare Data
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

def getSpreadSheetFromGoogleServiceAPI():
    authJsonPath = InputPath+"/dva108222040-81db778ac098.json"
    gssScopes = ['https://spreadsheets.google.com/feeds']
    
    #Connect service
    credentials = ServiceAccountCredentials.from_json_keyfile_name(authJsonPath,gssScopes)
    gssClient = gspread.authorize(credentials)
    
    #Open google spreadsheet
    spreadsheetKey = "1QXfPNUrR_O1lsoXdUiMa8zhUXDZmG2aHytHd2lEb1RQ"
    sheet = gssClient.open_by_key(spreadsheetKey).sheet1
    
    #Access spread sheet
    try:
        print(sheet.get_all_records())  #dictionary
        print("\n=======")
        print(sheet.get_all_values())   #list
        #Insert data into book
        sheet.clear()
        sheet.append_row(list(nobel_winners[0].keys()))#column name
        for dd in nobel_winners:
            sheet.append_row(list(dd.values()))
            
        #row index start1
        #sheet.delete_row(2)
        #cell start 1,1
        sheet.update_cell(row=2, col=5, value="2023")
            
    except Exception as errMessage:
        print("No data!". errMessage)

if (__name__ == "__main__"):
    getSpreadSheetFromGoogleServiceAPI()
        
        
        
        
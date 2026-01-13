# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:05:54 2022

@author: Addis
"""
import os,sys
outputPath = os.path.join(".","Output")
import requests #!pip install requests
from urllib.request import urlretrieve

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
#print("\nKeys in json ----\n", data.keys())
#print("\nWeb header ----\n", resData.text)
#print("\nWeb header ----\n", resData.content)

#filename = outputPath + "/Animal.json"
#urlretrieve(jsonURL, filename())
    
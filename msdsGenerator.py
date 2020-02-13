import requests
from bs4 import BeautifulSoup
import re
import pymongo


# Set up the MongoDB for connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# check if the db or col existed already
dblist = myclient.list_database_names()
if "my_MSDS" not in dblist:
    mydb = myclient["my_MSDS"]
collist = mydb.list_collection_names()
if "GHS_Classification" not in collist:
    GHS = mydb["GHS_Classification"]
if "Precautions_and_Storages" not in collist:
    Precaution = mydb["Precautions_and_Storages"]
if "EU_Precautions" not in collist:
    Precaution = mydb["EU_Precautions"]

# Set up for webpage connection
url = "https://pubchem.ncbi.nlm.nih.gov/ghs/#_pict"
headers = {'user-agent': 'Mozilla/5.0'}
res = requests.get(url, headers=headers)
# decorate the program as a browser
res.encoding = "GB2312"
soup = BeautifulSoup(res.text,"html.parser")

# 1. hazardous classes 
# get the pictogramTable as a reference for hazardous classes
# look through the webpage
pictogramTable = soup.find_all(id="pic")
picts = pictogramTable[0].find_all("td")
for pict in picts:
    # get the address of the image
    img = pict.find_all("img")
    imgSrc = img[0]["src"]
    # get the name of the clasee
    pictStr = pict.decode_contents()
    search = re.search("<br/>(.*?)<br/>", pictStr)
    if search:
        classH = re.split("<br/>", pictStr)[1].replace("<br/>","")
    else:
        classH = re.search(">(.*?)<br/>", pictStr)[0].replace("<br/>","").replace(">","")
    # add to the database for further reference
    if GHS.find({classH : imgSrc}).count() == 0:
        GHS.insert_one({classH : imgSrc})

# 2.a Handling Procedures and Storage Methods


HCodeTable = soup.find_all(id="hcode")
columnName = HCodeTable[0].find_all("th")
columnNameList = []
# Code
# Hazard Statements
# Hazard Class
# Category
# Pictogram
# Signal Word
# Precautionary Statements P-Codes contains
    # Prevention
    # Response
    # Storage
    # Disposal
# collect the columnName for each category
for column in columnName:
    columnStr = column.decode()
    column = re.search(">(.*?)</th>",columnStr)[0].replace("</th>","").replace(">","").strip()
    print(column)
    if column != "Precautionary Statements P-Codes contains":
        columnNameList.append(column)
# the actual content start at the third row
content = HCodeTable[0].find_all("tr")
row = 2
while row < len(content):
    contentRow = content[row].find_all("td")
    index = 0
    chemical = {}
    while index < len(contentRow):
        item = contentRow[index].decode().replace("<td>","").replace("</td>","")
        # print("the added content is:")
        # print({columnNameList[index]:item})
        # print("\n")
        chemical[columnNameList[index]] = item
        index += 1
    if Precaution.find(chemical).count() == 0: # no replicate data captured
        Precaution.insert_one(chemical)
    row += 1


# 2.b EU code procedures

EUCodeTable = soup.find_all(id="eucode")
columnName = EUCodeTable[0].find_all("th")
columnNameList = ["Code","Hazard"]





### help functions
def getContent(table, row):
    columnName = table[0].find_all("th")
    columnNameList = []
    # collect the columnName for each category
    for column in columnName:
        columnStr = column.decode()
        column = re.search(">(.*?)</th>",columnStr)[0].replace("</th>","").replace(">","").strip()
        print(column)
        if column != "Precautionary Statements P-Codes contains":
            columnNameList.append(column)
    # the actual content start at row(th) row
    content = HCodeTable[0].find_all("tr")
    while row < len(content):
        contentRow = content[row].find_all("td")
        index = 0
        chemical = {}
        while index < len(contentRow):
            item = contentRow[index].decode().replace("<td>","").replace("</td>","")
            # print("the added content is:")
            # print({columnNameList[index]:item})
            # print("\n")
            chemical[columnNameList[index]] = item
            index += 1
        if Precaution.find(chemical).count() == 0: # no replicate data captured
            Precaution.insert_one(chemical)
        row += 1

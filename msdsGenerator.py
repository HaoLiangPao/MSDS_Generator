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
if "HazardStatement" not in collist:
    HazardStatement = mydb["HazardStatement"]
if "EU_Precautions" not in collist:
    EU_Precaution = mydb["EU_Precautions"]
if "AUS_Precautions" not in collist:
    AUS_Precaution = mydb["AUS_Precautions"]
if "Precaution_Procedure" not in collist:
    Precaution_Procedure = mydb["Precaution_Procedure"]

# Set up for webpage connection
url = "https://pubchem.ncbi.nlm.nih.gov/ghs/#_pict"
headers = {'user-agent': 'Mozilla/5.0'}
res = requests.get(url, headers=headers)
# decorate the program as a browser
res.encoding = "GB2312"
soup = BeautifulSoup(res.text,"html.parser")

### help functions
def code_Procedure(table,columnNameList,collection,row):
    content = table[0].find_all("tr")
    while row < len(content):
        contentRow = content[row].find_all("td")
        index = 0
        prep = {}
        while index < len(contentRow):
            item = contentRow[index].decode().replace("<td>","").replace("</td>","")
            prep[columnNameList[index]] = item
            index += 1
        if collection.find(prep).count() == 0: # no replicate data captured
            collection.insert_one(prep)
        row += 1

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
# collect the columnName for each category
for column in columnName:
    columnStr = column.decode()
    column = re.search(">(.*?)</th>",columnStr)[0].replace("</th>","").replace(">","").strip()
    print(column)
    if column != "Precautionary Statements P-Codes contains":
        columnNameList.append(column)
# the actual content start at the third row
code_Procedure(HCodeTable, columnNameList, HazardStatement, 2)


# 2.b EU code procedures
EUCodeTable = soup.find_all(id="eucode")
columnNameList = ["Code","Hazard"]
code_Procedure(EUCodeTable, columnNameList, EU_Precaution, 0)

# 2.c AUS code procedures
AUSCodeTable = soup.find_all(id="aucode")
columnNameList = ["Code","Hazard"]
code_Procedure(AUSCodeTable, columnNameList, AUS_Precaution, 0)

# 3. Precaution Processes
PreTable = soup.find_all(id="pcode")
columnNameList = ["Code","Precaution"]
code_Procedure(PreTable, columnNameList, Precaution_Procedure, 0)


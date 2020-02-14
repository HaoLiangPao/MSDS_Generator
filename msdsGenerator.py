import requests
from bs4 import BeautifulSoup
import re
import pymongo

# Set up the MongoDB for connection
myClient = pymongo.MongoClient("mongodb://localhost:27017/")

# check if the db or col existed already
dbList = myClient.list_database_names()
if "my_MSDS" not in dbList:
    myDb = myClient["my_MSDS"]
colList = myDb.list_collection_names()
if "GHS_Classification" not in colList:
    GHS = myDb["GHS_Classification"]
if "HazardStatement" not in colList:
    HazardStatement = myDb["HazardStatement"]
if "EU_Precautions" not in colList:
    EU_Precaution = myDb["EU_Precautions"]
if "AUS_Precautions" not in colList:
    AUS_Precaution = myDb["AUS_Precautions"]
if "Precaution_Procedure" not in colList:
    Precaution_Procedure = myDb["Precaution_Procedure"]

# Set up for webpage connection
url = "https://pubchem.ncbi.nlm.nih.gov/ghs/#_pict"
headers = {'user-agent': 'Mozilla/5.0'}
res = requests.get(url, headers=headers)
# decorate the program as a browser
res.encoding = "GB2312"
soup = BeautifulSoup(res.text, "html.parser")


# help functions
def code_procedure(table, column_name_list, collection, row):
    content = table[0].find_all("tr")
    while row < len(content):
        content_row = content[row].find_all("td")
        index = 0
        prep = {}
        while index < len(content_row):
            item = content_row[index].decode().replace("<td>", "").replace("</td>", "")
            prep[column_name_list[index]] = item
            index += 1
        if collection.find(prep).count() == 0:  # no replicate data captured
            collection.insert_one(prep)
        row += 1


# 1. hazardous classes
# get the pictogramTable as a reference for hazardous classes
# look through the web page
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
        classH = re.split("<br/>", pictStr)[1].replace("<br/>", "")
    else:
        classH = re.search(">(.*?)<br/>", pictStr)[0].replace("<br/>", "").replace(">", "")
    # add to the database for further reference
    if GHS.find({classH: imgSrc}).count() == 0:
        GHS.insert_one({classH: imgSrc})

# 2.a Handling Procedures and Storage Methods
HCodeTable = soup.find_all(id="hcode")
columnName = HCodeTable[0].find_all("th")
columnNameList = []
# collect the columnName for each category
for column in columnName:
    columnStr = column.decode()
    column = re.search(">(.*?)</th>", columnStr)[0].replace("</th>", "").replace(">", "").strip()
    print(column)
    if column != "Precautionary Statements P-Codes contains":
        columnNameList.append(column)
# the actual content start at the third row
code_procedure(HCodeTable, columnNameList, HazardStatement, 2)

# 2.b EU code procedures
EUCodeTable = soup.find_all(id="eucode")
columnNameList = ["Code", "Hazard"]
code_procedure(EUCodeTable, columnNameList, EU_Precaution, 0)

# 2.c AUS code procedures
AUSCodeTable = soup.find_all(id="aucode")
columnNameList = ["Code", "Hazard"]
code_procedure(AUSCodeTable, columnNameList, AUS_Precaution, 0)

# 3. Precaution Processes
PreTable = soup.find_all(id="pcode")
columnNameList = ["Code", "Precaution"]
code_procedure(PreTable, columnNameList, Precaution_Procedure, 0)

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests


# Set up for webpage connection
chemBase = "https://pubchem.ncbi.nlm.nih.gov/#query="
chemical = "Polycyclic Aromatic Hydrocarbons"
headers = {'user-agent': 'Mozilla/5.0'}
print(chemBase+chemical.replace(" ", "%20"))
res = requests.get(chemBase+chemical.replace(" ", "%20"), headers=headers)
print(res)
# decorate the program as a browser
res.encoding = "GB2312"
soup = BeautifulSoup(res.text, "html.parser")
print(soup)
# find all relevant results on the page
searchResult = soup.find_all(id="js-rendered-content")[0].find_all("a", href=True)
print(searchResult)
for chemicalFound in searchResult:
    chemicalURL = chemicalFound['href']
    print(chemicalURL)


# pubChem search, which will open a chrome browser,
# enter chemical identifiers into the search bar and click search
def searchPubChem(identifier, chrome, chemical):
    chrome.set_page_load_timeout(10)
    # PubChem URL
    chrome.get("https://pubchem.ncbi.nlm.nih.gov/")
    search_xpath = "//input[starts-with(@id,'search')]"
    button_xpath = "//button[@class='button width-2em height-2em lh-1']"
    # find the input searching bar, enter the chemical name to be searched
    chrome.find_element_by_xpath(search_xpath).send_keys(chemical)
    print("Chemical entered")
    # find the search button, click and go to the detailed page
    chrome.find_element_by_xpath(button_xpath).click()
    print("button clicked")
    time.sleep(4)
    chrome.quit()

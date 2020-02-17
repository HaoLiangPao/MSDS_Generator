from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4
import time
import requests


# # Set up for webpage connection
# chemBase = "https://pubchem.ncbi.nlm.nih.gov/#query="
# chemical = "Polycyclic Aromatic Hydrocarbons"
# headers = {'user-agent': 'Mozilla/5.0'}
# print(chemBase+chemical.replace(" ", "%20"))
# res = requests.get(chemBase+chemical.replace(" ", "%20"), headers=headers)
# print(res)
# # decorate the program as a browser
# res.encoding = "GB2312"
# soup = BeautifulSoup(res.text, "html.parser")
# print(soup)
# # find all relevant results on the page
# searchResult = soup.find_all(id="js-rendered-content")[0].find_all("a", href=True)
# print(searchResult)
# for chemicalFound in searchResult:
#     chemicalURL = chemicalFound['href']
#     print(chemicalURL)


def xpath_search(driver, url, xpath):
    driver.get(url)
    # some webpage elements may not shown at the time it loads.
    # we will wait until it loaded up to 10 seconds
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return element
    except:
        return None


def get_attributes(browser, url, xpath):
    element = xpath_search(browser, url, xpath)[0]
    if element.text.find("\n"):
        attribute = element.text[:element.text.find("\n")]
    else:
        attribute = element.text
    return attribute


def chemicalList(identifier, chrome):
    chrome = webdriver.Chrome("../Drivers/chromedriver")
    urlBase = "https://pubchem.ncbi.nlm.nih.gov/#query="
    chrome.get(urlBase + identifier.replace(" ", "%20"))
    # these are absolute Xpath, may need to change if the layout of the website changes
    suggestedXpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[" \
                     "2]/div[1]/a[1]/span[1]/span[1] "
    firstXpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/ul[" \
                 "1]/li[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/span[1] "
    element = xpath_search(chrome, urlFinal, suggestedXpath)
    # if given identifier does not have a suggested compound by PubChem
    if element is None:
        element = xpath_search(chrome, urlFinal, firstXpath)
    soup = bs4(chrome.page_source, 'html.parser')
    href = soup.findAll('a', {'class': 'capitalized'})[0]['href']
    return href


def getCompound(chrome, href, database):
    chrome.get(href)

    soup = bs4(chrome.page_source, "html.parser")  # get the html file from the chemical page
    MW = soup.find('th', )  # molecular weight
    syno = ""  # synonyms
    MF = ""  # molecular formula


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


chrome = webdriver.Chrome("../Drivers/chromedriver")
identifier = "HCL"
urlBase = "https://pubchem.ncbi.nlm.nih.gov/#query="
# 1. get the url for the specific compound
# handel the space between the words in the identifier
urlFinal = urlBase + identifier.replace(" ", "%20")
suggestedXpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[" \
                 "2]/div[1]/a[1]/span[1]/span[1] "
firstXpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/ul[" \
             "1]/li[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/span[1] "
element = xpath_search(chrome, urlFinal, suggestedXpath)
# if given identifier does not have a suggested compound by PubChem
if element is None:
    element = xpath_search(chrome, urlFinal, firstXpath)
soup = bs4(chrome.page_source, 'html.parser')
# directly go to Laboratory safety data sheet page
href = soup.findAll('a', {'class': 'capitalized'})[0]['href'] + "#datasheet=LCSS"
# 2. get the corresponding information and store them into the database
MW_xpath = "//p[contains(text(),'g/mol')]"
MW = get_attributes(chrome, href, MW_xpath)  # Molecular Weight
ordor_xpath = "//section[@id='Odor']//div[@class='section-content-item']"
ordor = get_attributes(chrome, href, ordor_xpath)  # Ordor
BP_xpath = "//section[@id='Boiling-Point']//div[@class='section-content']//div[2]"
BP = get_attributes(chrome, href, BP_xpath)  # boiling point
MP_xpath = "//section[@id='Melting-Point']//div[@class='section-content']//div[2]"
MP = get_attributes(chrome, href, MP_xpath)  # melting point
solu_xpath = "//section[@id='Solubility']//div[@class='section-content']//div[2]"
solu = get_attributes(chrome, href, solu_xpath)  # solubility
dens_xpath = "//section[@id='Density']//div[@class='section-content']//div[2]"
dens = get_attributes(dens_xpath)  # density

print(ordor)
print(BP)




# # put all the information together
# # physical properties
# color = ""
# ordor = ""
# BP = 0  # boiling point
# MP = 0  # melting point
# solu = 0  # solubility
# dens = 0  # density
# physical = ", ".join((color, ordor, BP, MP, solu, dens))
#
# # Potential Hazards
# NFPA_pig = "link"  # the pigment of NFPA hazards
# health = ""  # NFPA health rating
# fire = ""  # NFPA fire rating
# instability = ""  # NFPA instability rating
# NFPA = "health:" + health + "\n" + "fire:" + fire + "\n" + "instability:" + instability
#
# # First Aids
# inhal = ""  # inhalation aids
# skin = ""  # skin first aids
# eye = ""  # eye first aids
# inje = ""  # ingestion first aids
# firstAids = "inhalation:" + inhal + "\n" + "skin:" + skin + "\n" + "eye:" + eye + "\n" + "injection:" + inhal

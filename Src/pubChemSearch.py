import logging
import re
import traceback
import time

import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4


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
        element = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return element
    except Exception as e:
        logging.error(traceback.format_exc())


def get_attributes_GHS(browser, url, xpath, pigment):
    try:
        pigments = []
        attributes = []
        element = xpath_search(browser, url, xpath)[0]
        # get src for the pigment picture
        if pigment is True:
            pigments.append(element.get_attribute("src"))
            attributes.append(element.get_attribute("alt"))
            try:
                xpath = xpath[:-10] + "2" + xpath[-10 + 1:]
            except Exception as e:
                logging.error(traceback.format_exc())
                print("No more pigments are available", xpath)
                return None
        return attributes
    except Exception as e:
        logging.error(traceback.format_exc())
        print("The attribute corresponding to this xpath does not existed.", xpath)
        return None

def get_attributes(browser, url, xpath):
    try:
        element = xpath_search(browser, url, xpath)[0]
        # check if the attribute is an image
        if element.get_attribute("src"):
            attribute = element.get_attribute("src")
        # normal case: check if the element is text
        else:
            # print(element.text)
            if element.text.find("\n") != -1:
                attribute = element.text[:element.text.find("\n")]
            else:
                attribute = element.text
            # print(attribute)
        return attribute
    except Exception as e:
        logging.error(traceback.format_exc())
        print("The attribute corresponding to this xpath does not existed.", xpath)
        return None


def get_physical_prop(browser, url, xpath):
    result = get_attributes(browser, url, xpath)
    print("physical property is:", xpath)
    print(result)
    # if no information available at all, return null
    if result is not None:
        # if this compound has multiple info sources, choose the first one
        if re.search("(.*)[Ss]howing(.*)of(.*)", result):
            xpath = xpath[:-2] + "2" + xpath[-2 + 1:]
            result = get_attributes(browser, url, xpath)
    return result


def chemical_list(browser, url):
    # these are absolute Xpath, may need to change if the layout of the website changes
    suggested_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[" \
                      "2]/div[1]/a[1]/span[1]/span[1] "
    first_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/ul[" \
                  "1]/li[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/span[1] "
    web_element = xpath_search(browser, url, suggested_xpath)
    # if given identifier does not have a suggested compound by PubChem
    if web_element is None:
        web_element = xpath_search(browser, url, first_xpath)
    soup = bs4(browser.page_source, 'html.parser')
    chemical_url = soup.findAll('a', {'class': 'capitalized'})[0]['href'] + "#datasheet=LCSS"
    return chemical_url


# pubChem search, which will open a chrome browser,
# enter chemical identifiers into the search bar and click search
def searchPubChem(browser, chemical):
    browser.set_page_load_timeout(10)
    # PubChem URL
    browser.get("https://pubchem.ncbi.nlm.nih.gov/")
    search_xpath = "//input[starts-with(@id,'search')]"
    button_xpath = "//button[@class='button width-2em height-2em lh-1']"
    # find the input searching bar, enter the chemical name to be searched
    browser.find_element_by_xpath(search_xpath).send_keys(chemical)
    print("Chemical entered")
    # find the search button, click and go to the detailed page
    browser.find_element_by_xpath(button_xpath).click()
    print("button clicked")
    time.sleep(4)
    browser.quit()


def generate_chemical_profile(identifier):
    # 1. get the url for the specific compound
    # handel the space between the words in the identifier
    chemical = {}
    chrome = webdriver.Chrome("../Drivers/chromedriver")
    chemical["identifier"] = identifier
    urlBase = "https://pubchem.ncbi.nlm.nih.gov/#query="
    urlFinal = urlBase + identifier.replace(" ", "%20")
    href = chemical_list(chrome, urlFinal)  # get the webpage which contains the information about given chemical
    # 2. get the corresponding information and store them into the database
    # 2.1 get physical properties
    Name_xpath = "//h1[@class='m-zero p-zero']"
    chemical["Name"] = get_attributes(chrome, href, Name_xpath)  # Common name
    MW_xpath = "//p[contains(text(),'g/mol')]"
    chemical["MW"] = get_attributes(chrome, href, MW_xpath)  # Molecular Weight
    ordor_xpath = "//section[@id='Odor']//div[@class='section-content-item']"
    chemical["ordor"] = get_attributes(chrome, href, ordor_xpath)  # Ordor
    BP_xpath = "//section[@id='Boiling-Point']//div[@class='section-content']//div[1]"
    chemical["BP"] = get_physical_prop(chrome, href, BP_xpath)  # boiling point
    MP_xpath = "//section[@id='Melting-Point']//div[@class='section-content']//div[1]"
    chemical["MP"] = get_physical_prop(chrome, href, MP_xpath)  # melting point
    solu_xpath = "//section[@id='Solubility']//div[@class='section-content']//div[1]"
    chemical["solubility"] = get_physical_prop(chrome, href, solu_xpath)  # solubility
    dens_xpath = "//section[@id='Density']//div[@class='section-content']//div[1]"
    chemical["density"] = get_physical_prop(chrome, href, dens_xpath)  # density
    # physical properties summary (optional data source)
    description_xpath = "//section[@id='Physical-Description']//div[@class='section-content']//div[1]"
    chemical["description"] = get_physical_prop(chrome, href, description_xpath)
    physical_combine = ""
    physical_combine_list = [("ordor: ", chemical["ordor"]),
                            ("Boiling Point: ", chemical["BP"]),
                            ("Melting Point: ", chemical["MP"]),
                            ("solubility: ", chemical["solubility"]),
                            ("Density: ", chemical["density"])]
    for value in physical_combine_list:
        if value[1] is not None:
            physical_combine += value[0] + value[1] + ";\n"
    chemical["description_combine"] = physical_combine

    # 2.2 get hazards properties
    # NFPA
    NFPA_pig_xpath = "//section[@id='NFPA-Hazard-Classification']//img[@class='icon']"
    chemical["NFPA_pig"] = get_attributes(chrome, href, NFPA_pig_xpath)  # the src for the image of NFPA pigment
    health_xpath = "//section[@id='Flammability-and-Explosivity']//tr[2]"
    chemical["health_hazards"] = get_attributes(chrome, href, health_xpath)
    fire_xpath = "//section[@id='Flammability-and-Explosivity']//tr[3]"
    chemical["fire_hazards"] = get_attributes(chrome, href, fire_xpath)
    inst_xpath = "//section[@id='Flammability-and-Explosivity']//tr[4]"
    chemical["instability_hazards"] = get_attributes(chrome, href, inst_xpath)
    hazards_xpath = "//section[@id='Toxicity-Summary']//div[@class='section-content-item']"
    chemical["hazards"] = get_attributes(chrome, href, hazards_xpath)
    hazards_combine = ""
    hazards_combine_list = [("health_hazards: ", chemical["health_hazards"]),
                              ("fire_hazards: ", chemical["fire_hazards"]),
                              ("instability_hazards: ", chemical["instability_hazards"])]
    for hazard in hazards_combine_list:
        if hazard[1] is not None:
            hazards_combine += hazard[1] + "\n"
    chemical["hazards_combine"] = hazards_combine
    # GHS
    GHS_pigment_xpath = "//div[@class='section-content-item']//div[2]//img[1]"
    chemical["GHS_pigment"] = get_attributes_GHS(chrome, href, GHS_pigment_xpath, True)

    # 2.3 get first aids properties
    inhal_xpath = "//section[@id='Inhalation-First-Aid']//div[@class='section-content-item']"
    chemical["inhalation_first_aid"] = get_attributes(chrome, href, inhal_xpath)
    skin_xpath = "//section[@id='Skin-First-Aid']//div[@class='section-content-item']"
    chemical["skin_first_aid"] = get_attributes(chrome, href, skin_xpath)
    eye_xpath = "//section[@id='Eye-First-Aid']//div[@class='section-content-item']"
    chemical["eye_first_aid"] = get_attributes(chrome, href, eye_xpath)
    inges_xpath = "//section[@id='Ingestion-First-Aid']//div[@class='section-content-item']"
    chemical["ingestion_first_aid"] = get_attributes(chrome, href, inges_xpath)
    first_aid_xpath = "//body[@class='lcss']/div[@id='js-rendered-content']/div[@class='relative " \
                      "flex-container-vertical']/main[@id='main-content']/div[@class='main-width']/div[" \
                      "@class='table-grid full-width fixed-layout align-top']/div[@class='p-l-top p-l-right " \
                      "p-xl-bottom']/div[@id='section-container']/section[@id='First-Aid']/div[" \
                      "@class='section-content']/div[1] "
    first_aid = get_attributes(chrome, href, first_aid_xpath)
    if first_aid is not None:
        chemical["first_aid"] = re.sub("<.*>", "", first_aid)
    else:
        chemical["first_aid"] = first_aid
    # set first_aid_combine
    first_aid_combine = ""
    first_aid_combine_list = [("inhalation: ", chemical["inhalation_first_aid"]),
                              ("skin: ", chemical["skin_first_aid"]),
                              ("eye: ", chemical["eye_first_aid"]),
                              ("ingestion: ", chemical["ingestion_first_aid"])]
    for item in first_aid_combine_list:
        if item[1] is not None:
            first_aid_combine += item[0] + item[1] + "\n"
    chemical["first_aid_combine"] = first_aid_combine
    print(chemical)

    # 3. store the dictionary into the MongoDB
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    myDb = myClient["my_MSDS"]
    Chemicals = myDb["Chemicals"]
    print("\n")
    print(Chemicals.find(chemical).count())
    if Chemicals.find(chemical).count() == 0:  # no replicate data captured
        Chemicals.insert_one(chemical)
    chrome.quit()  # terminate the browser as the search ends


if __name__ == "__main__":
    identifier = input("Please enter the chemicals you are looking for: ")
    generate_chemical_profile(identifier)

# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# import pandas as pd


# specify the url
urlpage = 'https://groceries.asda.com/search/yogurt'
print(urlpage)
# run chrome webdriver from the environment set alone with this project
driver = webdriver.Chrome(executable_path='../Drivers/chromedriver')
# get web page
driver.get(urlpage)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                      "lenOfPage;")
# sleep for 30s
time.sleep(30)
# driver.quit()
# find elements by xpath
# updated Nov 2019:
results = driver.find_elements_by_xpath("//*[@class=' co-product-list__main-cntr']//*[@class=' co-item ']//*["
                                        "@class='co-product']//*[@class='co-item__title-container']//*["
                                        "@class='co-product__title']")
print('Number of results', len(results))
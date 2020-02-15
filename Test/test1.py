from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/Users/lianghao/Desktop/MSDS_Generator_py/Drivers/chromedriver")
# driver = webdriver.Firefox()
# driver = webdriver.Ie()

driver.set_page_load_timeout(10)
driver.get("http://google.com")
driver.find_element_by_name("q").send_keys("Automation Step by Step")
driver.find_element_by_name("btnk").send_keys(Keys.Enter)
time.sleep(4)
driver.quit()

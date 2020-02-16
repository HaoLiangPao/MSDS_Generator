from selenium import webdriver
import unittest
import HtmlTestRunner


class GoogleSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome("../Drivers/chromedriver")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_search_automationstepbystep(self):
        self.driver.get("http://google.com")
        self.driver.find_element_by_name("q").send_keys("MSDS Data")
        self.driver.find_element_by_name("btnK").click()

    def test_search_pubChem(self):
        self.driver.get("http://google.com")
        self.driver.find_element_by_name("q").send_keys("PubChem")
        self.driver.find_element_by_name("btnK").click()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.close()
        cls.driver.quit()
        print("test completed")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="../Reports"))

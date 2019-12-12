from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import urllib.request
import time
import pandas as pd

#Setup
#Webpage to Crawl
urlpage = 'https://www.bidfta.com/'
zipCode = 45236

#Driver and driver options
driverOptions = Options()
driverOptions.headless = True
#Uncomment for full browser
driver = webdriver.Firefox()
#Uncomment for headless browswer
#driver = webdriver.Firefox(options=driverOptions)
driver.implicitly_wait(15)

#Wait action Timeout explicit when needed
wait = WebDriverWait(driver, 10)

#Crawling actions
driver.get(urlpage)
results = driver.find_elements_by_xpath("//*[@class='col-xs-12 col-sm-6 col-md-4 col-lg-3 product-list padd-0 slick-slide slick-active']")

for eachAuction in results:
	print(eachAuction.text)

zipCodeField = driver.find_element_by_id("zip")
zipCodeField.send_keys(zipCode)
#zipCodeField.submit()
milesRadius = Select(driver.find_element_by_id("miles"))
milesRadius.select_by_value('50')
#milesRadius.click()
filterButton = driver.find_element_by_class_name("filterAuction")
filterButton.click()

loadingOverlay = driver.find_element_by_class_name("overlay")
wait.until(EC.invisibility_of_element_located(loadingOverlay));
time.sleep(2)
results = driver.find_elements_by_xpath("//*[@class='col-xs-12 col-sm-6 col-md-4 col-lg-3 product-list padd-0 slick-slide slick-active']")
print("==========================================================================")
for eachAuction in results:
	print(eachAuction.text)

#Cleanup
driver.quit()

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

#Define
bid_fta_homepage = 'https://www.bidfta.com/'
bid_fta_all_auctions = 'https://www.bidfta.com/home'
zip_code = 45236
city = 'Cincinnati'

#Driver Options
browser = "FIREFOX" #FIREFOX or CHROME
headless = False #Open the browser in headless mode = True
implicitly_wait = 15 #Seconds to wait implicitly if not explicitly set

def setup_driver (headless,browser,implicitly_wait):
	if headless:
		driver_options = Options()
		driver_options.headless = True
		driver = webdriver.Firefox(options=driver_options)
	else:
		driver = webdriver.Firefox()
	
	actions = ActionChains(driver)
	driver.implicitly_wait(15)
	return driver,actions

def filter_auctions_by_zip(driver,bid_fta_homepage,zip_code):
	#Wait action Timeout explicit when needed
	wait = WebDriverWait(driver, 10)

	driver.get(bid_fta_homepage)

	#Fill out zipcode and search radius(miles)
	zip_code_field = driver.find_element_by_id("zip")
	zip_code_field.send_keys(zip_code)
	milesRadius = Select(driver.find_element_by_id("miles"))
	milesRadius.select_by_value('50')
	#Click button to apply filter
	filterButton = driver.find_element_by_class_name("filterAuction")
	filterButton.click()

	#Wait for loading overlay
	loadingOverlay = driver.find_element_by_class_name("overlay")
	wait.until(EC.invisibility_of_element_located(loadingOverlay))
	time.sleep(2)




def filter_all_auctions_page_by_warehouses_in_city(driver,bid_fta_all_auctions,city):
	wait = WebDriverWait(driver, 10)

	#Open the Webpage
	driver.get(bid_fta_all_auctions)

	#Expand the warehouse location dropdown
	clickable_warehouse_dropdown = driver.find_element_by_xpath("//*[@class='multiselect dropdown-toggle btn btn-default']")
	clickable_warehouse_dropdown.click()

	#Find all the dropdown options
	warehouse_dropdown = driver.find_element_by_xpath("//*[@class='multiselect-container dropdown-menu']")
	warehouses = warehouse_dropdown.find_elements_by_tag_name("li")

	#Loop through the warehouse locations for any containing the city of interest and select them
	for warehouse in warehouses:
		warehouse_location = warehouse.find_element_by_class_name("checkbox")
		warehouse_location_name = warehouse_location.get_attribute("title")
		if city in warehouse_location_name:
			#Checks that the warehouse location isnt already selected since we dont want it to de-select it
			warehouse_location_classes = warehouse.get_attribute("class")
			if "active" not in warehouse_location_classes:
				warehouse.click()
	
	#Click the filter button
	filter_button = driver.find_element_by_xpath("//*[@class='btn btn-lg btn-style filter-btn']")
	filter_button.click()

	#Wait for loading overlay
	loadingOverlay = driver.find_element_by_class_name("overlay")
	wait.until(EC.invisibility_of_element_located(loadingOverlay))
	time.sleep(2)

def get_all_auctions_on_page (driver):
	wait = WebDriverWait(driver, 10)
	#Print all auction results on page bidfta.com/home
	all_auctions = driver.find_elements_by_xpath("//div[starts-with(@id,'auctionContainer')]")
	for each_auction in all_auctions:
		print(each_auction.text)

	#This gets auctions on the bidfta.com when filtering by zipcode... doesnt current work right.
	'''
	results = driver.find_elements_by_xpath("//div[contains(@class,'product-list padd-0 slick-slide')]") #product-list padd-0 slick-slide
	
	print(results)
	print("==========================================================================")
	for eachAuction in results:
		print(eachAuction.get_attribute("aria-describedby"))
		print(eachAuction.text)
	'''

def clean_up ():
	driver.quit()

#Run it
driver,actions = setup_driver (headless,browser,implicitly_wait)
filter_all_auctions_page_by_warehouses_in_city(driver,bid_fta_all_auctions,city)
#filter_auctions_by_zip(driver,bid_fta_homepage,zip_code)
get_all_auctions_on_page(driver)
#clean_up()
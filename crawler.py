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
browser = "FIREFOX" #FIREFOX or CHROME. Havent tested with Chrome yet
headless = False #Open the browser in headless mode = True/False
implicitly_wait = 15 #Seconds to wait implicitly if not explicitly set

def change_page (driver,wait,page_num):
	page_input = driver.find_element_by_id("pageInput")
	page_input.send_keys(page_num)
	
	#Click Go button
	go_button = driver.find_element_by_id("pagebtn")
	go_button.click()

	#Wait for loading overlay
	loadingOverlay = driver.find_element_by_class_name("overlay")
	wait.until(EC.invisibility_of_element_located(loadingOverlay))
	time.sleep(2)

def clean_up ():
	driver.quit()

def filter_auctions_by_zip(driver,wait,bid_fta_homepage,zip_code):
	#Probably wont use this function. Will use the all auctions page instead
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

def filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city):
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

def get_all_auctions_on_page (driver,wait):
	#Print all auction results on page bidfta.com/home
	page_of_auction_details = []
	all_auctions = driver.find_elements_by_xpath("//div[starts-with(@id,'auctionContainer')]")
	#Record details for each auction
	for each_auction in all_auctions:
		auction_id = each_auction.find_element_by_xpath(".//p[starts-with(text(),'Auction:')]").text
		auction_end = each_auction.find_element_by_xpath(".//div[contains(@class,'endTime')]").text
		auction_time_remaining = each_auction.find_element_by_xpath(".//span[starts-with(@id,'time')]").text
		auction_link = each_auction.find_element_by_xpath(".//a[starts-with(@href,'/auctionDetails')]").get_attribute("href")
		individual_auction_details = [auction_id,auction_end,auction_time_remaining,auction_link]
		#print(auction_id)
		#print(auction_end)
		#print(auction_time_remaining)
		#print(auction_link)
		page_of_auction_details.append(individual_auction_details)
	
	return page_of_auction_details
	
	#This gets auctions on the bidfta.com when filtering by zipcode... doesnt currently work, probably wont use this.
	'''
	results = driver.find_elements_by_xpath("//div[contains(@class,'product-list padd-0 slick-slide')]") #product-list padd-0 slick-slide
	
	print(results)
	print("==========================================================================")
	for eachAuction in results:
		print(eachAuction.get_attribute("aria-describedby"))
		print(eachAuction.text)
	'''

def get_total_pages (driver):
	total_pages = driver.find_element_by_xpath("//span[@class='total total_page']")
	print(total_pages.text)

	return int(total_pages.text)

def find_all_auctions_by_city(driver):
	all_pages_of_auction_details = []
	filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city)
	#Get the number of result pages
	total_result_pages = get_total_pages (driver)
	#Scan all pages and pull auction info
	for i in range(2, total_result_pages+1):
		one_page_of_auctions = get_all_auctions_on_page(driver,wait)
		change_page(driver,wait,i)
		all_pages_of_auction_details.append(one_page_of_auctions)
	#Get final page
	one_page_of_auctions = get_all_auctions_on_page(driver,wait)
	all_pages_of_auction_details.append(one_page_of_auctions)

	return all_pages_of_auction_details

def setup_driver (headless,browser,implicitly_wait):
	if headless:
		driver_options = Options()
		driver_options.headless = True
		driver = webdriver.Firefox(options=driver_options)
	else:
		driver = webdriver.Firefox()
	
	actions = ActionChains(driver)
	#Wait time when using explicit wait
	wait = WebDriverWait(driver, 10)
	driver.implicitly_wait(15)
	return driver,actions,wait

#Run it
driver,actions,wait = setup_driver (headless,browser,implicitly_wait)
filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city)
one_page_of_auctions = get_all_auctions_on_page (driver,wait)
print(one_page_of_auctions)
#all_auctions = find_all_auctions_by_city(driver)
#clean_up()


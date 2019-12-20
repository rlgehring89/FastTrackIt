import crawler
import database

##### Define options #####
zip_code = 45236
city = 'Cincinnati'
browser = "FIREFOX" #FIREFOX or CHROME. Havent tested with Chrome yet
headless = False #Open the browser in headless mode = True/False
implicitly_wait = 15 #Seconds to wait implicitly if not explicitly set

###### Web Scraping ######
#Driver setup
driver,actions,wait = crawler.setup_driver(headless,browser,implicitly_wait)

#Get all auctions
all_auctions = crawler.find_all_auctions_by_city(driver,wait,city)

#Statically set auction_id for this test
auction_id = list(all_auctions.keys())[0]

#Pull items for one auction
#auction_dictionary_with_items = crawler.add_all_items_to_auction(driver,wait,auction_id,all_auctions)
all_items_for_auction = crawler.get_all_items_by_auction_id(driver,wait,auction_id,all_auctions)

#### Add auction details from dict to database #####
def add_auction_details_to_database(all_auctions,cursor):
    for key,value in all_auctions.items():
        auction_id_value = key
        auction_end_value = value[0]
        auction_time_remaining_value = value[1]
        auction_link_value = value[2]
        in_statement = """
                    INSERT INTO auctions (auction_id, auction_end, auction_time_remaining, auction_link) 
                    VALUES (?,?,?,?);
                    """
        cursor.execute(in_statement, (auction_id_value,auction_end_value,auction_time_remaining_value,auction_link_value))

#### Add items from auction dict #####
def add_items_to_database(all_items_for_auction,auction_id,cursor):
    for key,value in all_items_for_auction.items():
        item_lot_id_value = key
        item_description_value = value[0]
        item_status_value = value[1]
        item_current_bid_value = value[2]
        item_msrp_value = value[3]
        auction_id_value = auction_id
        in_statement = """
                    INSERT INTO auction_items (item_lot_id, item_description, item_status, item_current_bid, item_msrp, auction_id) 
                    VALUES (?,?,?,?,?,?);
                    """
        cursor.execute(in_statement, (item_lot_id_value,item_description_value,item_status_value,item_current_bid_value,item_msrp_value,auction_id_value))

#Create empty database with auction and auction_items table
database.setup_database()
conn = database.create_connection('pythonsqlite.db')
cursor = conn.cursor()

#cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
#result = cursor.fetchall()
#print(result)

#Add auction details to database
add_auction_details_to_database(all_auctions,cursor)

#Add auction items to database
add_items_to_database(all_items_for_auction,auction_id,cursor)

conn.commit()
cursor.close()
conn.close()

'''
print(auction_dictionary_with_items[auction_id])
try:
	print(type(auction_dictionary_with_items[auction_id][3]))
except:
	print()
try:
	print(auction_dictionary_with_items[auction_id]['GRN0290953'])
except:
	print()
'''

'''
#Get one page of auctions for cincinnati
#filter_auctions_by_warehouse_city(driver,wait,bid_fta_all_auctions,city)
#one_page_of_auctions = get_all_auctions_on_page (driver,wait)
#print(one_page_of_auctions)

#Get all pages of auctions for cincinnati
#all_auctions = find_all_auctions_by_city(driver)
#print(all_auctions.keys())

#Get one page of items from auction
#page_of_items = get_all_items_on_page_by_auction_id(driver,list(all_auctions.keys())[0],all_auctions)
#print(len(page_of_items))

#clean_up()
'''
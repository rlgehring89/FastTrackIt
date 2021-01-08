import crawler
import database

#Debug
import time
total_time = time.time()

def main():
    #############################
    #####   Define options  #####
    #############################
    city = 'Cincinnati'
    state = 'Ohio'
    browser = 'FIREFOX' #FIREFOX or CHROME. Havent tested with Chrome yet
    headless = False #Open the browser in headless mode = True/False
    implicitly_wait = 20 #Seconds to wait implicitly if not explicitly set
    database_file = r'data/pythonsqlite.db'

    #############################
    #####   Database Setup   ####
    #############################
    #Create empty database with auction and auction_items table
    database.setup_database(database_file)
    connection = database.create_connection(database_file)

    #############################
    ######   Web Scraping  ######
    #############################
    #Driver setup
    driver,wait5,wait_halfsec = crawler.setup_driver(headless,browser,implicitly_wait)

    #Get all auctions
    all_auctions = crawler.find_all_auctions_by_city(driver,wait5,city,state)

    #Add items to all auctions
    crawler.add_items_to_all_auctions(driver,wait5,wait_halfsec,all_auctions,connection)

    #############################
    #####      Cleanup      #####
    #############################
    connection.close()
    crawler.clean_up(driver)

    #Debug
    print("--- %s seconds ---" % (time.time() - total_time))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("Failed to complete the crawl, auctions and items will remain in the DB until cleared")
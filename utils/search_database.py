import sqlite3
from sqlite3 import Error
import argparse
import sys

##############################################################
#                                                            #
#    Basic utility script for searching database items       #
#                                                            #
##############################################################

def main():
    database = r"../data/pythonsqlite.db"
    conn = create_connection(database)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--search', help='Keyword to search for within auction items', metavar='')
    parser.add_argument('-p','--print_all', help='Print all auctions and items', action='store_true')
    args = parser.parse_args()
    
    if args.search is not None:
        results = search_for_items(conn,args.search)
        print(results)
    elif args.print_all == True:
        print_auctions_and_items(conn)
    else:
        print ("View help menu using -h for proper usage")
    conn.close()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

def print_auctions_table(conn):
    sql_select_all_from_auctions = """
    SELECT * FROM auctions
    """

    try:
        c = conn.cursor()
        c.execute(sql_select_all_from_auctions)
        results = c.fetchall()
        print(results)
    except Error as e:
        print(e)
    conn.commit()
    return len(results)

def print_auction_items_table(conn):
    sql_select_all_from_auctions = """
    SELECT * FROM auction_items
    """

    try:
        c = conn.cursor()
        c.execute(sql_select_all_from_auctions)
        results = c.fetchall()
        for each_item in results:
            print(each_item)
    except Error as e:
        print(e)
    conn.commit()
    return len(results)
  
def print_auctions_and_items (conn):
    auction_len = print_auctions_table(conn)
    items_len = print_auction_items_table(conn)
    print("Total Auctions: " + str(auction_len))
    print("Total Items: " + str(items_len))

def search_for_items (conn,search_keyword):
    sql_select_matching_items = """
    SELECT * FROM auction_items
    WHERE item_description LIKE '%{}%'
    """.format(search_keyword)
    
    try:
        c = conn.cursor()
        c.execute(sql_select_matching_items)
        results = c.fetchall()
        for each_item in results:
            print(each_item)
    except Error as e:
        print(e)
    conn.commit()
    return results
 

if __name__== "__main__":
    try:
        main()
        sys.exit()
    except SystemExit as ext:
        if ext.code:
            print ("Error")
        raise SystemExit(ext.code)
    except:
        print("Oops!", sys.exc_info(), "occurred. Exiting")
        exit()
    

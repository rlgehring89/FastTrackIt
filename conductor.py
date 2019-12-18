import crawler
import database

mydatabase = database.setup_database
conn = database.create_connection(mydatabase)
cursor = conn.cursor()

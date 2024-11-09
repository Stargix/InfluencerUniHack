print("Module 'database' imported successfully.\n")

import sqlite3
import os
from datetime import datetime
import bcrypt

def create_table(name, fields):
    """Attempt to create a table from the input name and fields"""
    con = sqlite3.connect("jobOffers.db")
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE {}{}".format(name, fields))
    except sqlite3.OperationalError as err:
        print("Table already created!\n")
        print(err)
    con.commit()
    con.close()

def insert_values(name, values):
    """Insert the input values into the given table"""
    con = sqlite3.connect("jobOffers.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON") # ensures there are foreign key constraints
    cur.execute("INSERT INTO {} VALUES {}".format(name, values))
    con.commit()
    con.close()


def generate_database():
    """Set up an exemplar database with static data"""
    # lists to store the example data
    tables = "business_prop"
    # the assumption is made that every measurement is in kg, cm or km, minutes
    fields = """(user_id INTEGER PRIMARY KEY,
                  ig_account_name VARCHAR(255) NOT NULL,
                  offer VARCHAR(225) NULL,
                  message VARCHAR(225) NOT NULL)"""
                  
    # generate database if not already created
    if os.path.isfile("lightr.db"):
        print("Database found. No data generated.\n")
    else:
        print("Database not found. Generating now.\n")
        create_table(tables, fields)
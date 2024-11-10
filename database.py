print("Module 'database' imported successfully.\n")

import sqlite3
import os
from datetime import datetime
import time
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

def insert_message(user_id, message_text):
    """Insert a new message with a unique message_id"""
    print("error here")
    for attempt in range(5):  # Retry up to 5 times for locked database
        try:
            con = sqlite3.connect("jobOffers.db")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO business_prop (user_id, message) VALUES (?, ?)",
                (user_id, message_text)
            )
            con.commit()
            break  # Break loop if successful
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                time.sleep(0.1)  # Wait briefly before retrying
            else:
                raise
        finally:
            con.close()


def generate_database():
    """Set up an exemplar database with static data"""
    table_name = "business_prop"
    fields = """(
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,  
        user_id INTEGER NOT NULL,                      
        message VARCHAR(225) NOT NULL
    )"""
    
    if os.path.isfile("jobOffers.db"):
        print("Database found. No data generated.\n")
    else:
        print("Database not found. Generating now.\n")
        create_table(table_name, fields)


def print_database_contents():
    """Print all records from the 'business_prop' table in the jobOffers.db database."""
    try:
        con = sqlite3.connect("jobOffers.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM business_prop")
        rows = cur.fetchall()
        
        if not rows:
            print("No records found in the 'business_prop' table.\n")
        else:
            print("Contents of 'business_prop' table:\n")
            for row in rows:
                message_id, user_id, message = row  # Updated unpacking
                print(f"Message ID: {message_id}, User ID: {user_id}, Message: {message}")
            print("")  # Add a newline at the end
    except sqlite3.Error as e:
        print(f"An error occurred while accessing the database: {e}")
    finally:
        con.close()

def get_all_messages():
    """Retrieve all messages from the 'business_prop' table in SQLite."""
    try:
        con = sqlite3.connect("jobOffers.db")
        cur = con.cursor()
        cur.execute("SELECT message_id, user_id, message FROM business_prop")
        rows = cur.fetchall()
        return [{"message_id": row[0], "user_id": row[1], "message": row[2]} for row in rows]
    finally:
        con.close()
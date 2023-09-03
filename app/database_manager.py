# database_manager.py
# This module contains the 'DatabaseManager' class responsible for managing the SQLite database connection
# and executing SQL queries.

import sqlite3
import logging_utils

logging_utils.setup_logging()

class DatabaseManager():
    def __init__(self, database_name):
        self.database_name = database_name
 
    def connect(self):
        try:
            # Establish a connection to the database
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
        
        except sqlite3.Error as e:
            print("An error occurred while connecting:", e)
            logging_utils.log_error(f"An error occurred: {e}")

    def disconnect(self):
        try:
            if self.connection:
                # Close the database connection
                self.connection.close()
        
        except sqlite3.Error as e:
            print("An error occurred while disconnecting:", e)
            logging_utils.log_error(f"An error occurred: {e}")
    
    def execute_query(self, query, params=None):
        try:
            self.connect()
            if params:
                # Execute a query with optional parameters
                self.cursor.execute(query, params)
            else:
                # Execute a query without parameters
                self.cursor.execute(query)
        
            # Commit the changes to the database
            self.connection.commit()
        
        except sqlite3.Error as e:
            print("An error occurred while executing a query:", e)
            logging_utils.log_error(f"An error occurred: {e}")
    
    def fetch_all(self, query, values=None):
        try:
            self.connect()
            if values:
                # Execute a query with optional values
                self.cursor.execute(query, values)
            
            else:
                # Execute a query without values
                self.cursor.execute(query)
        
            # Fetch and return all results
            result = self.cursor.fetchall()
            return result
        
        except sqlite3.Error as e:
            print("An error occurred while fetching data:", e)
            logging_utils.log_error(f"An error occurred: {e}")
    
    def commit(self):
        # Commit any pending changes to the database
        self.connection.commit()

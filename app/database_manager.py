import sqlite3

class DatabaseManager():
    def __init__(self, database_name):
        self.database_name = database_name
 
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
        
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        
        except sqlite3.Error as e:
            print("An error occurred:", e)
    
    def execute_query(self, query, params=None):
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        
            self.connection.commit()
        
        except sqlite3.Error as e:
            print("An error occurred:", e)
    
    def fetch_all(self, query, values=None):
        try:
            self.connect()
            if values:
                self.cursor.execute(query, values)
            
            else:
                self.cursor.execute(query)
        
            result = self.cursor.fetchall()
            return result
        
        except sqlite3.Error as e:
            print("An error occurred:", e)
    
    def commit(self):
        self.connection.commit()
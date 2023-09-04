# test_db_create.py
import sqlite3

# Connect to the SQLite database 'test.db'
conn = sqlite3.connect("test.db")

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table named 'my_table' if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_table (
        column1 TEXT,
        column2 TEXT
    )
""")

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

# Reconnect to the SQLite database 'test.db'
import sqlite3
conn = sqlite3.connect("test.db")
c = conn.cursor()

# Select all records from the 'my_table' table
c.execute("SELECT * FROM my_table")

# Fetch all records from the 'my_table' table
menus = c.fetchall()

# Print the records from the 'my_table' table
for menu in menus:
    print(menu)

print("=" * 50)  # Separator

# Close the database connection
conn.close()

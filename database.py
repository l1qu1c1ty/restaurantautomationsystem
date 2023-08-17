#  database.py
import sqlite3

# Create a connection object
conn = sqlite3.connect("restaurant.db")

# Create a cursor object
c = conn.cursor()

# Create a table for login
c.execute("""
CREATE TABLE IF NOT EXISTS login (
    username TEXT,
    password TEXT
)
""")

# # Create a table for menu
# c.execute("""
# CREATE TABLE IF NOT EXISTS menu (
#     name TEXT,
#     price TEXT
# )
# """)

# Insert some sample data into login
login_data = [
    ("Micheal", "1Sw0rd!2023"),
    ("Melih",   "MCD200123"),
]

c.executemany("""
INSERT INTO login (username, password)
VALUES (?, ?)
""", login_data)

# # Insert some sample data into menu
# menu_data = [
#     ("Cheeseburger", "24.99"),
#     ("Sandwich", "19.99"),
#     ("Fries", "16.99"),
#     ("Coffee", "12.99"),
#     ("Soda", "10.99")
# ]

# c.executemany("""
# INSERT INTO menu (name, price)
# VALUES (?, ?)
# """, menu_data)

# Save the changes
conn.commit()

# Close the connection
conn.close()
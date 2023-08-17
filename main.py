import sqlite3
conn = sqlite3.connect("restaurant.db")
c = conn.cursor()
c.execute("SELECT * FROM menu")

d = conn.cursor()
d.execute("SELECT * FROM login")

menus = c.fetchall()

for menu in menus:
    print(menu)

print("="*50)

logins = d.fetchall()

for login in logins:
    print(login)

conn.close()
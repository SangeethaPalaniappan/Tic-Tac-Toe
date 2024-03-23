import sqlite3
con = sqlite3.connect('sqlfile.db')
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
for i in range(4):
    name = input("Name : ")
    age  = int(input("Age : "))
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
con.commit()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

con.close()
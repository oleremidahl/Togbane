import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()
cursor.execute("SELECT * FROM JernbaneStasjon")
p = cursor.fetchall()
print(p)
con.close()

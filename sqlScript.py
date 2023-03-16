import sqlite3
con = sqlite3.connect('jb.db')
cursor = con.cursor()
cursor.execute("SELECT * FROM TogRuteForekomst")
p = cursor.fetchall()
print(p)
con.close()

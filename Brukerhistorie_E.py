import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

cursor.execute("SELECT MAX(kundeNr) FROM Kunde")
max_kundeNr = cursor.fetchone()[0]

if max_kundeNr is None:
    kundeNr = 0
else:
    kundeNr = max_kundeNr + 1

navn = input("Skriv inn navn: ")
epost = input("Skriv inn epost: ")
telefon = input("Skriv inn telefonnummer: ")

cursor.execute("INSERT INTO Kunde VALUES(?,?,?,?)", (kundeNr, navn, epost, telefon))
con.commit()
print("Velkommen ", navn, "! Ditt kundeNr er: ", kundeNr)
cursor.execute("SELECT * FROM Kunde")
p = cursor.fetchall()
print(p)
con.close()
import sqlite3

con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

# Sjekker om epost og telefonnummer allerede eksisterer i databasen
while True:
    navn = input("Skriv inn navn: ")
    email = input("Skriv inn epost: ")
    tlf = input("Skriv inn telefonnummer: ")
    
    cursor.execute("SELECT * FROM Kunde WHERE email = ? OR tlf = ?", (email, tlf))
    eksisterende_kunde = cursor.fetchone()
    
    if eksisterende_kunde is not None:
        print("En kunde med samme epost eller telefonnummer eksisterer allerede i systemet.")
    else:
        break

# Oppretter ny kunde
cursor.execute("SELECT MAX(kundeNr) FROM Kunde")
max_kundeNr = cursor.fetchone()[0]

if max_kundeNr is None:
    kundeNr = 1
else:
    kundeNr = max_kundeNr + 1

cursor.execute("INSERT INTO Kunde VALUES(?,?,?,?)", (kundeNr, navn, email, tlf))
con.commit()
print("Velkommen ", navn, "! Ditt kundeNr er: ", kundeNr)
cursor.execute("SELECT * FROM Kunde")
p = cursor.fetchall()
for rad in p:
    oversikt = "Kundenummer: {}, Navn: {}, Epost: {}, Telefonnummer: {}".format(rad[0], rad[1], rad[2], rad[3])
    print(oversikt)

con.close()

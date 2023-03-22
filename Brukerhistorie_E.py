import sqlite3

con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

# Sjekker om epost og telefonnummer allerede eksisterer i databasen
while True:
    navn = input("Skriv inn navn: ")
    email = input("Skriv inn email: ")
    tlf = input("Skriv inn tlfnummer: ")
    
    cursor.execute("SELECT * FROM Kunde WHERE email = ? OR tlf = ?", (email, tlf))
    eksisterende_kunde = cursor.fetchone()
    
    if eksisterende_kunde is not None:
        print("En kunde med samme email eller tlfnummer eksisterer allerede i databasen.")
    else:
        break

# Oppretter ny kunde
cursor.execute("SELECT MAX(kundeNr) FROM Kunde")
max_kundeNr = cursor.fetchone()[0]

if max_kundeNr is None:
    kundeNr = 0
else:
    kundeNr = max_kundeNr + 1

cursor.execute("INSERT INTO Kunde VALUES(?,?,?,?)", (kundeNr, navn, email, tlf))
con.commit()

# Viser alle kunder i databasen
cursor.execute("SELECT * FROM Kunde")
p = cursor.fetchall()
print(p)

con.close()

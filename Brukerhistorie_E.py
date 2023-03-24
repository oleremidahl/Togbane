import sqlite3

con = sqlite3.connect("jernbane.db")
cursor = con.cursor()

# Sjekker om en kunde allerede eksisterer i databasen basert på epost eller telefonnummer
def sjekk_kunde_eksisterer(email, tlf):
    cursor.execute("SELECT * FROM Kunde WHERE email = ? OR tlf = ?", (email, tlf))
    eksisterende_kunde = cursor.fetchone()
    
    if eksisterende_kunde is not None:
        print("En kunde med samme epost eller telefonnummer eksisterer allerede i systemet.")
        return True
    else:
        return False

# Oppretter en ny kunde i databasen
def opprett_ny_kunde(navn, email, tlf):
    cursor.execute("SELECT MAX(kundeNr) FROM Kunde")
    max_kundeNr = cursor.fetchone()[0]

    if max_kundeNr is None:
        kundeNr = 1
    else:
        kundeNr = max_kundeNr + 1

    cursor.execute("INSERT INTO Kunde VALUES(?,?,?,?)", (kundeNr, navn, email, tlf))
    return kundeNr

# Viser en oversikt over alle kundene i databasen
def vis_kunderegister():
    cursor.execute("SELECT * FROM Kunde")
    kunder = cursor.fetchall()
    print("------ Kunderegister ------")
    for rad in kunder:
        kundenummer = rad[0]
        navn = rad[1]
        epost = rad[2]
        telefonnummer = rad[3]

        print(f"Kundenummer: {kundenummer}")
        print(f"Navn: {navn}")
        print(f"Epost: {epost}")
        print(f"Telefonnummer: {telefonnummer}")
        print("------------------------")

def main():
    navn = input("Skriv inn navn: ")
    while True:
        email = input("Skriv inn epost: ")
        tlf = input("Skriv inn telefonnummer: ")
        
        if sjekk_kunde_eksisterer(email, tlf):
            continue
        else:
            break

    kundeNr = opprett_ny_kunde(navn, email, tlf)
    con.commit()
    print("Velkommen ", navn, "! Ditt kundenummer er: ", kundeNr)

    vis_kunderegister()

    con.close()

main()

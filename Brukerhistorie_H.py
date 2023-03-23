import sqlite3

con = sqlite3.connect("jernbane.db")
cursor = con.cursor()

kundenr = input("Oppgi kundenummeret ditt: ")

# SQL-spørring for å sjekke om en kunde finnes i databasen
sjekk = """
SELECT COUNT(*)
FROM Kunde
WHERE kundeNr = ?
"""

cursor.execute(sjekk, (kundenr,))
antall_rader = cursor.fetchone()[0]

if antall_rader > 0:
  
    # SQL-spørring for å hente informasjon om bestillinger for fremtidige reiser for en gitt kunde
    info = """
    SELECT * FROM Billett b
    JOIN Kundeordre ko ON b.ordreNr = ko.ordreNr
    WHERE ko.kundeNr = ? AND b.dato > date('now')
    """

    # Viser informasjon om bestillinger for fremtidige reiser gitt at kunden eksisterer og har bestilt minst én billett
    cursor.execute(info, (kundenr,))
    resultater = cursor.fetchall()
    if len(resultater) == 0:
        print("Du har ingen bestillinger for fremtidige reiser.")
    else:
        print("Dine bestillinger for fremtidige reiser:")
        for rad in resultater:
            ordrenummer = rad[0]
            dato = rad[1]
            rutenummer = rad[2]
            vognnummer = rad[3]
            setenummer = rad[4]
            startstasjon = rad[5]
            endestasjon = rad[6]
            avgang = rad[7]
            ankomst = rad[8]

            print("Ordrenummer:", ordrenummer)
            print("Dato:", dato)
            print("Rutenummer:", rutenummer)
            print("Vognnummer:", vognnummer)
            print("Setenummer:", setenummer)
            print("Startstasjon:", startstasjon)
            print("Endestasjon:", endestasjon)
            print("Avgang:", avgang)
            print("Ankomst:", ankomst)
            print("--------------------------")
else:
    print("Du er ikke registrert som kunde.")

con.close()

import sqlite3

con = sqlite3.connect("jernbane.db")
cursor = con.cursor()

kundenr = input("Oppgi kundenummeret ditt: ")

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
    SELECT *
    FROM Billett b
    JOIN Kundeordre ko ON b.ordreNr = ko.ordreNr
    WHERE ko.kundeNr = ? AND b.dato > date('now')
    """

    cursor.execute(info, (kundenr,))
    resultater = cursor.fetchall()

    for rad in resultater:
        oversikt = "Ordrenummer: {}, Dato: {}, Rutenummer: {}, Vognnummer: {}, Setenummer: {}, Startstasjon: {}, Endestasjon: {}".format(rad[0], rad[1], rad[2], rad[3], rad[4], rad[5], rad[6])
        print(oversikt)
else:
    print("Du er ikke registrert som kunde.")

con.close()

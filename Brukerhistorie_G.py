import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

variabler
rutenavn, startstasjon, destinasjon, antall_billetter

    # Lage en spørring for å finne rutenr
    query = "SELECT ruteNr FROM Togrute WHERE baneNavn = %s"
    cursor.execute(query, (rutenavn,))
    result = cursor.fetchone()
    ruteNr = result[0]

    # Lage en spørring for å finne stasjonene på ruten
    query = "SELECT stasjonsNavn, ankomstTid, avgangsTid FROM StasjonPaaRute WHERE ruteNr = %s AND (stasjonsNavn = %s OR stasjonsNavn = %s)"
    cursor.execute(query, (ruteNr, startstasjon, destinasjon))
    result = cursor.fetchall()
    stasjoner = [row[0] for row in result]
    ankomsttider = [row[1] for row in result]
    avgangstider = [row[2] for row in result]

    # Lage en spørring for å finne delstrekningene på ruten
    query = "SELECT startStasjon, endeStasjon FROM DelstrekningPaaRute WHERE ruteNr = %s"
    cursor.execute(query, (ruteNr,))
    result = cursor.fetchall()
    delstrekninger = [row for row in result]

    # Lage en spørring for å finne antall seter i hver vogn
    query = "SELECT antSeterPrRad FROM Sittevogn WHERE serieNr IN (SELECT serieNr FROM OppsettPaaRute WHERE ruteNr = %s)"
    cursor.execute(query, (ruteNr,))
    result = cursor.fetchall()
    antall_seter = sum([row[0] for row in result])

    # Lage en spørring for å finne tilgjengelige billetter
    query = "SELECT COUNT(*) FROM Billett WHERE ruteNr = %s AND startStasjon = %s AND endeStasjon = %s AND billetttype = %s"

p = cursor.fetchall()
print(p)
con.close()
import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

start_stasjon = input("Velg en Startstasjon: ")
ende_stasjon = input("Velg en EndeStasjon: ")
dato = input("Velg en dato: ")

cursor.execute('''
        SELECT TogRuteForekomst.ruteNr, ForekomstDato.ukedag, StasjonPaaRute.stasjonsNavn
        FROM ((ForekomstDato 
        INNER JOIN 
        TogRuteForekomst ON ForekomstDato.dato == TogRuteForekomst.dato)
        INNER JOIN 
        StasjonPaaRute ON TogRuteForekomst.ruteNr == StasjonPaaRute.ruteNr)
        WHERE ForekomstDato.ukedag = ? AND StasjonPaaRute.stasjonsNavn = ?
        ''',(ukedag, stasjon))

p = cursor.fetchall()
print(p)
con.close()
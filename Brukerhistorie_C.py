import sqlite3
con = sqlite3.connect('.db')
cursor = con.cursor()

stasjon = input("Velg en stasjon: ")
ukedag = input("Velg en ukedag: ")

cursor.execute('''f'
        SELECT TogRuteForekomst.ruteNr
        FROM ((ForekomstDato 
        INNER JOIN 
        TogRuteForekomst ON ForekomstDato.dato == TogRuteForekomst.dato)
        INNER JOIN 
        StasjonPaaRute ON TogRuteForekomst.ruteNr == StasjonPaaRute.ruteNr)
        WHERE ForekomstDato.ukedag == {ukedag} AND StasjonPaaRute.stasjonsNavn == {stasjon}
        '
        '''
)

p = cursor.fetchall()
print(p)
con.close()

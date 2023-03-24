import sqlite3

con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

# Sjekker etter togavganger som matcher input fra bruker
def sjekk_togavganger(stasjon, ukedag):
    cursor.execute('''
            SELECT TogRuteForekomst.ruteNr, ForekomstDato.ukedag, StasjonPaaRute.stasjonsNavn
            FROM ((ForekomstDato 
            INNER JOIN 
            TogRuteForekomst ON ForekomstDato.dato == TogRuteForekomst.dato)
            INNER JOIN 
            StasjonPaaRute ON TogRuteForekomst.ruteNr == StasjonPaaRute.ruteNr)
            WHERE ForekomstDato.ukedag = ? AND StasjonPaaRute.stasjonsNavn = ?
            ''',(ukedag, stasjon))

    resultater = cursor.fetchall()

    if len(resultater) == 0:
        print("Ingen tog går fra denne stasjonen på denne ukedagen.")
    else:
        print("Tog som går fra", stasjon, "på", ukedag + ":")
        for rad in resultater:
            ruteNr = rad[0]
            ukedag = rad[1]
            stasjonsNavn = rad[2]
            print("Rutenummer:", ruteNr)
            print("Ukedag:", ukedag)
            print("Stasjon:", stasjonsNavn)
            print("--------------------------")

def main():
    stasjon = input("Velg en stasjon: ")
    ukedag = input("Velg en ukedag: ")
    sjekk_togavganger(stasjon, ukedag)
    con.close()

main()
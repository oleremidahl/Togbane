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
        print("\nTog som går fra", stasjon, "på", ukedag + ":")
        print("--------------------------")
        for rad in resultater:
            ruteNr = rad[0]
            ukedag = rad[1]
            stasjonsNavn = rad[2]
            print("Rutenummer:", ruteNr)
            print("Ukedag:", ukedag)
            print("Stasjon:", stasjonsNavn)
            print("--------------------------")

# Sjekker om stasjonen er gyldig
def check_gyldig_stasjon(gyldige_stasjoner):
        stasjon = input("Velg en stasjon: ")
        while (stasjon not in gyldige_stasjoner):
                stasjon = input("Velg en gyldig stasjon: ")
        return stasjon

# Henter ut alle stasjoner
def get_gyldige_stasjoner(): 
        gyldige_stasjoner = []
        cursor.execute('''SELECT * FROM JernbaneStasjon''')
        stasjoner = cursor.fetchall()
        for el in stasjoner:
                gyldige_stasjoner.append(el[0])
        return gyldige_stasjoner

def main():
    gyldige_stasjoner = get_gyldige_stasjoner()
    se_stasjoner = input("Vil du se alle stasjoner? (j/n): ")
    if (se_stasjoner == "j"):
        print(", ".join(str(x) for x in gyldige_stasjoner), end="\n")
    print("Vi aksepterer kun direkte kopi av stasjonsnavnet, Feks 'Trondheim'")
    stasjon = check_gyldig_stasjon(gyldige_stasjoner)
    print("Vi aksepterer kun direkte kopi av Dager, Feks 'Mandag'")
    ukedag = input("Velg en ukedag: ")
    sjekk_togavganger(stasjon, ukedag)
    con.close()

main()
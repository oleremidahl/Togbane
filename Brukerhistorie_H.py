import datetime
import sqlite3

con = sqlite3.connect("jernbane.db")
cursor = con.cursor()

# Sjekker om bruker finnes i databasen
def bruker_eksisterer(kundenr):
    sjekk = """SELECT COUNT(*) FROM Kunde WHERE kundeNr = ?"""
    cursor.execute(sjekk, (kundenr,))
    antall_rader = cursor.fetchone()[0]
    return antall_rader == 0

# Henter kundeinformasjon om bruker eksisterer
def hent_kundeinfo(billettKall):
    kundenr = input("Oppgi kundenummeret ditt: ")
    while (kundenr != "q" and bruker_eksisterer(kundenr)):
        print("Det er ikke en bruker med det kundenummeret.")
        kundenr = input("Oppgi kundenummeret ditt: Skriv 'q' for å avslutte ")
    if (kundenr == "q"):
        return []
    cursor.execute(billettKall, (kundenr,))
    return cursor.fetchall()

# Sjekker om tidspunktet for avgang er i fremtiden
def sjekk_tidspunkt(tidspunkt): # "hh:mm"
    if (int(tidspunkt[0:2]) > int(datetime.datetime.now().strftime("%H"))):
        return False
    elif (int(tidspunkt[0:2]) == int(datetime.datetime.now().strftime("%H"))):
        if (int(tidspunkt[3:5]) > int(datetime.datetime.now().strftime("%M"))):
            return False
    return True

#Prettyprint for biletter
def print_billett(billetter):
    print("\nDine bestillinger for fremtidige reiser:")
    print("---------------------------------------")
    for rad in billetter:
        ordrenummer = rad[0]
        dato = rad[1]
        rutenummer = rad[2]
        vognnummer = rad[3]
        setenummer = rad[4]
        startstasjon = rad[5]
        endestasjon = rad[6]
        avgang = rad[7]
        ankomst = rad[8]
        #Sjekker om dato er idag og om avgangstidspunktet er i fortiden
        if (datetime.datetime.strptime(dato, "%Y-%m-%d").date() == datetime.date.today()):
            if sjekk_tidspunkt(avgang):
                continue
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

billettKall = """
    SELECT * FROM Billett b
    JOIN Kundeordre ko ON b.ordreNr = ko.ordreNr
    WHERE ko.kundeNr = ? AND b.dato >= date('now')
    ORDER BY b.dato ASC
    """

def main():
    billetter = hent_kundeinfo(billettKall)
    print_billett(billetter)
    con.close()
main()
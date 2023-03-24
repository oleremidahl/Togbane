import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

# Henter ut alle togruteforekomster som går på en gitt dato + neste dag etter.
def get_ruter_dato(dato): 
        res = ""
        try: 
                imorgen = dato[:-1] + str(int(dato[-1])+1)
        except:
                print("Datoen må være på formatet yyyy-mm-dd")
                dato = input("Velg en ny dato (yyyy-mm-dd): ")
                imorgen = dato[:-1] + str(int(dato[-1])+1)
        forekomster = get_ruter_dato_sql_kall(dato, imorgen)
        dato_dict = {}
        while (res != "q" and len(forekomster) == 0):
                print("Det går ingen ruter denne datoen")
                dato = input("Velg en ny dato (yyyy-mm-dd): ")
                imorgen = dato[:-1] + str(int(dato[-1])+1)
                forekomster = get_ruter_dato_sql_kall(dato, imorgen)
                if (len(forekomster) == 0):
                        res = input("Du er i en evig løkke, skriv 'q' om du vil hoppe ut: ")
        for el in forekomster:
                dato_dict.setdefault(el[0], []).append(el[1])
        return dato_dict

# SQL kall for å hente ut alle togruteforekomster som går på en gitt dato + neste dag etter.
def get_ruter_dato_sql_kall(dato, dagenetter):
        cursor.execute('''SELECT * FROM TogRuteForekomst WHERE (TogRuteForekomst.dato = ? 
                                OR TogruteForekomst.dato = ?) ORDER BY TogRuteForekomst.dato ''',(dato,dagenetter))
        return cursor.fetchall()

# Henter ut alle stasjoner som er på en rute
def get_stasjoner_paa_rute(forekomster_dict): 
        stasjon_dict = {}
        for key in forekomster_dict:
                cursor.execute('''SELECT * FROM StasjonPaaRute WHERE StasjonPaaRute.ruteNr = ?''',(key,))
                stasjoner = cursor.fetchall()
                i = 0
                for el in stasjoner:
                        stasjon_dict.setdefault(el[1], []).append((el[0],el[3], i))
                        i += 1
        return stasjon_dict

# Henter ut alle stasjoner som finnes i databasen
def get_gyldige_stasjoner(): 
        gyldige_stasjoner = []
        cursor.execute('''SELECT * FROM JernbaneStasjon''')
        stasjoner = cursor.fetchall()
        for el in stasjoner:
                gyldige_stasjoner.append(el[0])
        return gyldige_stasjoner

# Printer ut stasjoner og ruter som går på valgt dato
def pretty_print_station(station_dict, dato_dict): 
        print("Stasjon\t|\tRuteNr\t|\tAvgangstid")
        print("---------------------------------------------------")
        for key in station_dict:
                print("Rute: ",key, " Går dato(ene): " ,dato_dict[key])
                for el in station_dict[key]: # Går gjennom alle stasjonene på en rute
                        print("\t|\t",el[0],"\t|\t",el[1])
                print("---------------------------------------------------")

# Sjekker om stasjonen er gyldig
def check_gyldig_stasjon(str, gyldige_stasjoner):
        stasjon = input("Velg en " + str + "stasjon: ")
        while (stasjon not in gyldige_stasjoner):
                stasjon = input("Velg en gyldig " + str + "stasjon: ")
        return stasjon

# Henter ut alle ruter som går mellom to stasjoner på en gitt dato
def get_valid_rutes(start_stasjon, ende_stasjon, rute_dict, dato_dict): 
        tidspunkt = input("Når på dagen vil du reise (hh:mm): ")
        gyldige_ruter = []
        for key in rute_dict: # Går gjennom alle rutene
                start_nummer, slutt_nummer = start_og_slutt_nummer(rute_dict[key],start_stasjon,ende_stasjon)
                if (start_nummer == -1 or slutt_nummer == -1):
                        continue
                if (start_nummer < slutt_nummer):
                        insert_riktige_ruter(tidspunkt, rute_dict, start_nummer, dato_dict, key, gyldige_ruter) 
        return gyldige_ruter

# Setter inn alle ruter som går mellom to stasjoner på en gitt dato 
def insert_riktige_ruter(tidspunkt, rute_dict, start_nummer, dato_dict, key, gyldige_ruter): 
        index = 0
        for el in dato_dict[key]: 
                if (check_time_earlier(tidspunkt, rute_dict[key][start_nummer][1]) and index < 1):
                        # Legger til -> (rutenr, Stasjonsnavn, avgangstid, dato)
                        gyldige_ruter.append((key, rute_dict[key][start_nummer][0], rute_dict[key][start_nummer][1], el))   
                elif (index >= 1):
                        # Legger til -> (rutenr, Stasjonsnavn, avgangstid, dato)
                        gyldige_ruter.append((key, rute_dict[key][start_nummer][0], rute_dict[key][start_nummer][1],el))
                index += 1
        return gyldige_ruter

# Sjekker om tidspunkt1 er tidligere enn tidspunkt2
def check_time_earlier(tidspunkt1, tidspunkt2):
    time1, minutt1 = map(int, tidspunkt1.split(':'))
    time2, minutt2 = map(int, tidspunkt2.split(':'))
    if time1 < time2: # Returnerer true om tidspunkt1 er tidligere enn tidspuntk2
        return True
    elif time1 == time2 and minutt1 < minutt2:
        return True
    else:
        return False


def start_og_slutt_nummer(list, start_stasjon, ende_stasjon):
        start_nummer = -1
        slutt_nummer = -1
        for el in list: # Går gjennom alle stasjonene i en rute
                if (el[0] == start_stasjon): # Setter så nummeret til å være lik,
                        start_nummer = el[2] # nummeret som er definert i stasjonen.
                if (el[0] == ende_stasjon):
                        slutt_nummer = el[2]
        return start_nummer, slutt_nummer

# Sorterer listen på dato, så på tidspunkt om de går samme dag.
def sorter_paa_dato(lst):
        return sorted(lst, key=lambda x: (x[3], x[2]))

# Pretty print for de gjeldene rutene i søket.
def pretty_print_ruter(gyldige_ruter):
        print("\nRuteNr\t| Stasjonsnavn\t| Avgangstid\t| Dato")
        print("---------------------------------------------------")
        for el in gyldige_ruter:
                print(el[0],"\t| ",el[1],"\t| ",el[2],"\t| ",el[3])
        print("---------------------------------------------------")
 
def main():        
        print("""Siden dette ikke er et ekte eksempel, har vi kun togruteforkomster 
i starten av april. Alle rutene går fra 3 til 7.april.
Ellers går kun rute 2 den 8 og 9.april. Et eksempel på en dato er '2023-04-05'""")
        dato = input("Velg en dato (yyyy-mm-dd): ")

        forekomst_ruter = get_ruter_dato(dato) # Henter ut ruter som går på dato
        stasjon_paa_rute = get_stasjoner_paa_rute(forekomst_ruter) # Henter ut stasjonene på de valgte rutene
        gyldige_stasjoner = get_gyldige_stasjoner() # Henter ut alle databaser
        pretty_print_station(stasjon_paa_rute, forekomst_ruter) # Printer ut info om rutene og stasjonene

        print("Dette er de rutene som går på valgt dato \n")
        print("Vi aksepterer kun direkte kopi av stasjonsnavnet, Feks 'Trondheim'")
        start_stasjon = check_gyldig_stasjon("start", gyldige_stasjoner) # Validerer input fra bruker
        ende_stasjon = check_gyldig_stasjon("ende", gyldige_stasjoner) # Validerer input fra bruker
        gyldige_ruter = get_valid_rutes(start_stasjon, ende_stasjon, stasjon_paa_rute, forekomst_ruter)
        if (gyldige_ruter == []):
                print("Ingen ruter som passer på valgt input")
                con.close()
        else:
                gyldige_ruter = sorter_paa_dato(gyldige_ruter)
                pretty_print_ruter(gyldige_ruter)
                con.close()


main()
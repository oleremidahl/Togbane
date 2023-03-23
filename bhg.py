import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

rute = 0
while rute not in ["1", "2", "3"]:
    rute = input("Hvilken rute vil du ta? 1, 2 eller 3? ")

startstasjon = ""
endestasjon = ""

gyldigStrekning = False
onsketStrekning = []
# Prøver helt til man finner en gyldig strekning
while not gyldigStrekning and endestasjon != "q":
    startstasjon = input("Skriv inn startstasjon: ")
    endestasjon = input('Skriv inn endestasjon: "Skriv q for å avslutte". ')

# Finner ut om startstasjon-endestasjon er en gyldig strekning på ruta
    cursor.execute(f'''SELECT * FROM DelstrekningPaaRute 
                    WHERE ruteNr = {rute} AND (startStasjon = '{startstasjon}' OR endeStasjon = '{endestasjon}')
                    ''')
    onsketStrekning = cursor.fetchall()
    print(onsketStrekning)
    #Sjekker om begge stasjonene er på ruten i riktig retning
    if((onsketStrekning[0][0] != startstasjon or onsketStrekning[0][1] != endestasjon) and len(onsketStrekning) != 2):
    # if len(onsketStrekning) != 2:
        print(f"Startstasjon {startstasjon} eller endestasjon {endestasjon} finnes ikke for rute {rute}.")
    else:
        print(f"Startstasjon {startstasjon} og endestasjon {endestasjon} finnes for rute {rute}.")
        gyldigStrekning = True



    #TODO Finne billetter som overlapper med den oppgitte strekningen og lagre ruteNr, vognNr, og plassNr
    #     Håndtere sengekjøp i kupéer. 

cursor.execute(f'''SELECT DelstrekningPaaRute.startStasjon, DelstrekningPaaRute.endeStasjon
                    FROM DelstrekningPaaRute INNER JOIN Togrute ON DelstrekningPaaRute.ruteNr = Togrute.ruteNr
                    WHERE Togrute.ruteNr = {rute}'''
               )
delStrPaaRute = cursor.fetchall()

#Alle stasjoner på en gitt rute, indeksert
stasjonerPaaRute = {}
for index, stasj in enumerate(delStrPaaRute):
    stasjonerPaaRute[stasj[0]] = index + 1
    if index == len(delStrPaaRute) - 1:
        stasjonerPaaRute[stasj[1]] = index + 2

print(f"Stasjoner på rute {rute}: {stasjonerPaaRute}")


#Alle stasjoner på en gitt strekning, indeksert
def finnStasjonerPaaStrekning(start, slutt):
    stasjonerPaaStrekning = []
    found_startstasjon = False 
    for stasj, nr in stasjonerPaaRute.items():
        if (stasj == start):
            found_startstasjon = True
            stasjonerPaaStrekning.append(nr)
        elif found_startstasjon and (stasj != slutt):
            stasjonerPaaStrekning.append(nr)
        elif (stasj == slutt):
            # stasjonerPaaStrekning.append(nr)
            break
    # print(f"Stasjoner på strekning '{start} - {slutt}': {stasjonerPaaStrekning}")
    return stasjonerPaaStrekning

stasjonerOnsketStrekning = finnStasjonerPaaStrekning(startstasjon, endestasjon)
print(f"Stasjoner på den ønskede strekningen: {stasjonerOnsketStrekning}")

#TODO Finne alle billetter på en rute, finne alle stasjoner på disse strekningene og nummerere dem. 
# Deretter finne ut hvilke som overlapper med ønsket strekning og fjerne disse setene. 
# Med senger må man fjerne hele kupeen uansett om de ikke overlapper. 
# cursor.execute(f'''SELECT dato, ruteNr, vognNr, plassNr, startStasjon, endeStasjon
#                 FROM Billett
#                 WHERE ruteNr = {rute} AND (dato = "2023-04-03" OR dato = "2023-04-04") 
#             ''')
# billetter = cursor.fetchall()

def finn_stasjoner_paa_billetter(billetter):
    stasjonerPaaBilletter = {}
    for billett in billetter:
        stasjPaaBillett = finnStasjonerPaaStrekning(billett[4], billett[5])
                                # vognNr        plassNr         stasjoner
        stasjonerPaaBilletter[f"{billett[2]}.{billett[3]}"] = stasjPaaBillett
    print("Stasjoner på billettene: ", stasjonerPaaBilletter)
    return stasjonerPaaBilletter

def finn_sove_billetter(dato):
    cursor.execute(f'''SELECT Billett.vognNr, plassNr
                        FROM Billett INNER JOIN oppsettPaaRute ON Billett.ruteNr = oppsettPaaRute.ruteNr AND Billett.vognNr = oppsettPaaRute.vognNr
                        INNER JOIN Sovevogn ON Sovevogn.serieNr = oppsettPaaRute.serieNr 
                        WHERE Billett.ruteNr = {rute} AND Billett.dato = "{dato}"
                    ''')
    return cursor.fetchall()

def finn_sittebiletter(dato):
    cursor.execute(f'''SELECT dato, Billett.ruteNr, Billett.vognNr, Billett.plassNr, startStasjon, endeStasjon
                        FROM Billett INNER JOIN oppsettPaaRute  ON Billett.ruteNr = oppsettPaaRute.ruteNr AND Billett.vognNr = oppsettPaaRute.vognNr
                        INNER JOIN Sittevogn ON Sittevogn.serieNr = oppsettPaaRute.serieNr 
                        WHERE Billett.ruteNr = {rute} AND dato = "{dato}"
                    ''')
    return cursor.fetchall()

sove_3_april = finn_sove_billetter("2023-04-03")
# stasj_sov_3 = finn_stasjoner_paa_billetter(sove_3_april)
sitte_3_april = finn_sittebiletter("2023-04-03")
stasj_sitte_3 = finn_stasjoner_paa_billetter(sitte_3_april)

sove_4_april = finn_sove_billetter("2023-04-04")
# stasj_sov_4 = finn_stasjoner_paa_billetter(sove_4_april)
sitte_4_april = finn_sittebiletter("2023-04-04")
stasj_sitte_4 = finn_stasjoner_paa_billetter(sitte_4_april)

def finn_overlappende_billetter(stasj_sitte, sove_billetter):
    overlappende_billetter = []
    onsketRute_set = set(stasjonerOnsketStrekning)
    stasjonerPaaBilletter = stasj_sitte
    #Finner overlappende billetter
    for key, stasj in stasjonerPaaBilletter.items():
        stasj_set = set(stasj)
        if any(x in onsketRute_set for x in stasj_set):
            vognNr, plassNr = key.split(".")
            overlappende_billetter.append((int(vognNr), int(plassNr)))
    
    for b in sove_billetter:
        tup = (b[0],b[1])
        if (tup not in overlappende_billetter):
            overlappende_billetter.append(tup)
    
    return overlappende_billetter

overlappende_billetter_3 = finn_overlappende_billetter(stasj_sitte_3, sove_3_april)
overlappende_billetter_4 = finn_overlappende_billetter(stasj_sitte_4, sove_4_april)


print(f"Følgende billetter overlapper med den ønskede ruten den 3.april: {overlappende_billetter_3}")
print(f"Følgende billetter overlapper med den ønskede ruten den 4.april: {overlappende_billetter_4}")


if (gyldigStrekning):


    #Dictionary med key for hver rute, hver rute har en dictionary med alle plasser
    # {ruteNr: {vognNr: [plassNr]}}
    def finn_alle_seter(dato):
        #Sjekker at det finnes forekomster av ruten 3. og 4. april
        cursor.execute(f'''SELECT Togrute.ruteNr, Sittevogn.antRader, Sittevogn.antSeterPrRad, Sovevogn.antKupeer, Sovevogn.antSengerPrKupe, oppsettPaaRute.vognNr
                        FROM Togrute
                        INNER JOIN TogRuteForekomst ON Togrute.ruteNr = TogRuteForekomst.ruteNr
                        LEFT JOIN oppsettPaaRute ON Togrute.ruteNr = oppsettPaaRute.ruteNr
                        LEFT JOIN Vogn ON oppsettPaaRute.serieNr = Vogn.serieNr
                        LEFT JOIN Sittevogn ON Vogn.serieNr = Sittevogn.serieNr
                        LEFT JOIN Sovevogn ON Vogn.serieNr = Sovevogn.serieNr
                        WHERE Togrute.ruteNr = {rute} AND TogRuteForekomst.dato = "{dato}"
                    ''')
            
        ruteOppsett = cursor.fetchall()
        plassNrPaaRute = {}
        for row in ruteOppsett: 
            plassNr = []
            if (row[1]):
                for i in range(1, row[1]*row[2] + 1):
                    plassNr.append(i)
                if (row[0] not in plassNrPaaRute.keys()):
                    plassNrPaaRute[row[0]] = {}
                    plassNrPaaRute[row[0]][row[5]] = plassNr
                else: 
                    plassNrPaaRute[row[0]][row[5]] = plassNr
            else: 
                for i in range(1, row[3]*row[4] + 1, 2):
                    plassNr.append([i, i+1])
                if (row[0] not in plassNrPaaRute.keys()):
                    plassNrPaaRute[row[0]] = {}
                    plassNrPaaRute[row[0]][row[5]] = plassNr
                else: 
                    plassNrPaaRute[row[0]][row[5]] = plassNr
        return plassNrPaaRute
    
    plassNrPaaRute_3 = finn_alle_seter("2023-04-03")
    plassNrPaaRute_4 = finn_alle_seter("2023-04-04")

    def fjern_opptatte_seter(plassNrPaaRute, overlappende_billetter):
        alle_seter = plassNrPaaRute
        ruteNr = int(rute)
        print('Alle seter', alle_seter)
        for tup in overlappende_billetter:
            if ruteNr in alle_seter and tup[0] in alle_seter[ruteNr]:
                array2 = alle_seter[ruteNr][tup[0]]
                if (all(isinstance(item, list) and len(item) == 2 for item in array2)):
                    for subarray in array2:
                        if tup[1] in subarray:
                            array2.remove(subarray)
                            break
                else: 
                    alle_seter[ruteNr][tup[0]].remove(tup[1])
    
        return alle_seter
    
    ledige_seter_3 = fjern_opptatte_seter(plassNrPaaRute_3, overlappende_billetter_3)
    ledige_seter_4 = fjern_opptatte_seter(plassNrPaaRute_4, overlappende_billetter_4)
    # print(plassNrPaaRute)
    # Presenterer plasser
    def presenter_seter(ledige_seter, dato):
        dtstring = "2023-04-03"
        if (dato == 4):
            dtstring = "2023-04-04"
        for n, vogn in ledige_seter.items():
            output_str = f"Dato: {dtstring},\n Rute {n}: "
            for key, values in vogn.items():
                output_str += f"Vogn {key} har følgende plasser: {values}. "
            print(output_str)

    presenter_seter(ledige_seter_3, 3)
    presenter_seter(ledige_seter_4, 4)


# cursor.execute("SELECT * FROM Billett")
# ledigePlasser = plassNrPaaRute
# billetter = cursor.fetchall()

# for billett in billetter:
#     try: 
#         del ledigePlasser[3][]


con.close()
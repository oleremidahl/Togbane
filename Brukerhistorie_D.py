import sqlite3
con = sqlite3.connect('jernbane.db')
cursor = con.cursor()

start_stasjon = input("Velg en Startstasjon: ")
ende_stasjon = input("Velg en EndeStasjon: ")
dato = input("Velg en dato: ")
tid = input("Når på dagen vil du reise? ")
imorgen = dato[:-1] + str(int(dato[-1])+1)
print('IMorgen: ',imorgen)

cursor.execute('''
        SELECT SPR.ruteNr, TRF.dato, SPR.stasjonsNavn1, SPR.stasjonsNavn2, SPR.avgangsTid
        FROM (
                SELECT *
                FROM TogRuteForekomst
                WHERE TogRuteForekomst.dato = ? OR TogRuteForekomst.dato = ?
        ) AS TRF
        INNER JOIN (
                SELECT spr1.ruteNr, spr1.stasjonsNavn AS stasjonsNavn1, spr1.avgangsTid, spr2.stasjonsNavn AS stasjonsNavn2
                FROM stasjonPaaRute AS spr1
                INNER JOIN stasjonPaaRute AS spr2 ON spr1.ruteNr = spr2.ruteNr
                WHERE spr1.stasjonsNavn = ? AND spr2.stasjonsNavn = ?
        ) AS SPR ON SPR.ruteNr = TRF.ruteNr
        WHERE (TRF.dato = ? AND SPR.stasjonsNavn1 = ? AND SPR.avgangsTid > ?)
        OR (TRF.dato = ? AND SPR.stasjonsNavn1 = ?)
        ORDER BY TRF.dato
        ''',(dato, imorgen, start_stasjon, ende_stasjon, dato, start_stasjon, tid, imorgen, start_stasjon,))

# SELECT SPR.ruteNr, TRF.dato, SPR.stasjonsNavn1, SPR.stasjonsNavn2, SPR.avgangsTid
# FROM (
#   SELECT *
#   FROM TogRuteForekomst
#   WHERE TogRuteForekomst.dato = '2023-04-05' OR TogRuteForekomst.dato = '2023-04-06'
# ) AS TRF
# INNER JOIN (
#   SELECT spr1.ruteNr, spr1.stasjonsNavn AS stasjonsNavn1, spr1.avgangsTid, spr2.stasjonsNavn AS stasjonsNavn2
#   FROM stasjonPaaRute AS spr1
#   INNER JOIN stasjonPaaRute AS spr2 ON spr1.ruteNr = spr2.ruteNr
#   WHERE spr1.stasjonsNavn = 'Trondheim' AND spr2.stasjonsNavn = 'Bodø'
# ) AS SPR ON SPR.ruteNr = TRF.ruteNr
# WHERE (TRF.dato = '2023-04-05' AND SPR.stasjonsNavn1 = 'Trondheim' AND SPR.avgangsTid > '09:00')
#    OR (TRF.dato = '2023-04-06' AND SPR.stasjonsNavn1 = 'Trondheim');
p = cursor.fetchall()
print(p)
con.close()

# SELECT *
# FROM (( Select *
# 	FROM TogRuteForekomst  WHERE TogRuteForekomst.dato == "2023-04-05" OR TogRuteForekomst.dato == "2023-04-06") as TRF1
# INNER JOIN 
# StasjonPaaRute ON StasjonPaaRute.ruteNr == TRF1.ruteNr )
# WHERE StasjonPaaRute.stasjonsNavn == "Trondheim"
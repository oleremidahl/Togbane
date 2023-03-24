import sqlite3

# Establish connection to database
conn = sqlite3.connect('jernbane.db')
c = conn.cursor()

# Drop tables if they exist
c.execute("DROP TABLE IF EXISTS TogRuteForekomst")
c.execute("DROP TABLE IF EXISTS ForekomstDato")
c.execute("DROP TABLE IF EXISTS Billett")
c.execute("DROP TABLE IF EXISTS Kundeordre")
c.execute("DROP TABLE IF EXISTS Kunde")
c.execute("DROP TABLE IF EXISTS Sovevogn")
c.execute("DROP TABLE IF EXISTS Sittevogn")
c.execute("DROP TABLE IF EXISTS oppsettPaaRute")
c.execute("DROP TABLE IF EXISTS Vogn")
c.execute("DROP TABLE IF EXISTS DelstrekningPaaRute")
c.execute("DROP TABLE IF EXISTS StasjonPaaRute")
c.execute("DROP TABLE IF EXISTS Delstrekning")
c.execute("DROP TABLE IF EXISTS Togrute")
c.execute("DROP TABLE IF EXISTS BaneStrekning")
c.execute("DROP TABLE IF EXISTS JernbaneStasjon")
c.execute("DROP TABLE IF EXISTS Operator")

# Create JernbaneStasjon table
c.execute('''CREATE TABLE JernbaneStasjon (
                navn VARCHAR(50) PRIMARY KEY,
	            moh INT NOT NULL
)''')

# Create Togrute table
c.execute('''CREATE TABLE Togrute (
                ruteNr INT NOT NULL,
                operator VARCHAR(20) NOT NULL,
                baneNavn VARCHAR(50) NOT NULL,
                CONSTRAINT rute_pk PRIMARY KEY(ruteNr),
                CONSTRAINT op_fk FOREIGN KEY(operator) REFERENCES Operator(navn) 
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT bane_fk FOREIGN KEY(baneNavn) REFERENCES BaneStrekning(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create BaneStrekning table
c.execute('''CREATE TABLE BaneStrekning (
                navn VARCHAR(50),
                energi VARCHAR(20),
                antStasjoner INT,
                antDelstrekninger INT,
                hovedretning VARCHAR(50),
                startStasjon VARCHAR(50) NOT NULL,
                endeStasjon VARCHAR(50) NOT NULL,
                CONSTRAINT bane_pk PRIMARY KEY(navn),
                CONSTRAINT startStasjon_fk FOREIGN KEY (startStasjon) REFERENCES JernbaneStasjon(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT endestasjon_fk FOREIGN KEY (endeStasjon) REFERENCES JernbaneStasjon(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create Delstrekning table
c.execute('''CREATE TABLE Delstrekning (
                startStasjon VARCHAR(50) NOT NULL,
                endeStasjon VARCHAR(50) NOT NULL,
                lengde INT,
                DobbeltSpor BOOLEAN,
                baneNavn VARCHAR(50) NOT NULL,
                CONSTRAINT delstrek_pk PRIMARY KEY (startStasjon, endeStasjon),
                CONSTRAINT startstasjon_fk FOREIGN KEY (startStasjon) REFERENCES JernbaneStasjon(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT endestasjon_fk FOREIGN KEY (endeStasjon) REFERENCES JernbaneStasjon(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT banenavn_fk FOREIGN KEY (baneNavn) REFERENCES BaneStrekning(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create StasjonPaaRute table
c.execute('''CREATE TABLE StasjonPaaRute (
                stasjonsNavn VARCHAR(50) NOT NULL,
                ruteNr INT NOT NULL,
                ankomstTid TIME,
                avgangsTid TIME,
                CONSTRAINT stasjon_pk PRIMARY KEY (stasjonsNavn, ruteNr),
                CONSTRAINT navn_fk FOREIGN KEY (stasjonsNavn) REFERENCES JernbaneStasjon(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT ruteNr_fk FOREIGN KEY (ruteNr) REFERENCES Togrute(ruteNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create DelstrekningPaaRute table
c.execute('''CREATE TABLE DelstrekningPaaRute (
                startStasjon VARCHAR(50) NOT NULL,
                endeStasjon VARCHAR(50) NOT NULL,
                ruteNr INT NOT NULL,
                CONSTRAINT delstrek_pk PRIMARY KEY (startStasjon, endeStasjon, ruteNr),
                CONSTRAINT startende_fk FOREIGN KEY (startStasjon, endestasjon) REFERENCES Delstrekning(startStasjon, endeStasjon)
                    ON UPDATE CASCADE 
                    ON DELETE NO ACTION,
                CONSTRAINT ruteNr_fk FOREIGN KEY (ruteNr) REFERENCES Togrute(ruteNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create Operator table
c.execute('''CREATE TABLE Operator (
                navn VARCHAR(20),
	            CONSTRAINT navn_pk PRIMARY KEY (navn)
)''')

# Create oppsettPaaRute table
c.execute('''CREATE TABLE oppsettPaaRute (
                ruteNr INT NOT NULL,
                serieNr INT NOT NULL,
                vognNr INT NOT NULL,
                CONSTRAINT oppsett_pk PRIMARY KEY (ruteNr, vognNr),
                CONSTRAINT ruteNr_fk FOREIGN KEY (ruteNr) REFERENCES Togrute(ruteNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT serieNr_fk FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create Vogn table
c.execute('''CREATE TABLE Vogn (
                serieNr INT NOT NULL,
                operatornavn VARCHAR(20) NOT NULL,
                CONSTRAINT serieNr_pk PRIMARY KEY (serieNr),
                CONSTRAINT operator_fk FOREIGN KEY (operatornavn) REFERENCES Operator(navn)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create Sittevogn table
c.execute('''CREATE TABLE Sittevogn (
                serieNr INT NOT NULL,
                antRader INT,
                antSeterPrRad INT,
                CONSTRAINT serie_pk PRIMARY KEY (serieNr),
                CONSTRAINT serie_fk FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
)''')

# Create Sovevogn table
c.execute('''CREATE TABLE Sovevogn (
                serieNr INT NOT NULL,
                antKupeer INT,
                antSengerPrKupe INT,
                CONSTRAINT sove_pk PRIMARY KEY (serieNr),
                CONSTRAINT serie_fk FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION  
)''')

# Create Kunde table
c.execute('''CREATE TABLE Kunde (
                kundeNr INT NOT NULL,
                navn VARCHAR(50),
                email VARCHAR(50),
                tlf INT,
                CONSTRAINT kunde_pk PRIMARY KEY (kundeNr)
)''')

# Create Kundeordre table
c.execute('''CREATE TABLE Kundeordre (
                ordreNr INT NOT NULL,
                dato DATE,
                tid TIME,
                kundeNr INT NOT NULL,
                CONSTRAINT ordre_pk PRIMARY KEY (ordreNr),
                CONSTRAINT kunde_fk FOREIGN KEY (kundeNr) REFERENCES Kunde(kundeNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION 
)''')

# Create Billett table
c.execute('''CREATE TABLE Billett (
                ordreNr INT NOT NULL,
                dato DATE NOT NULL,
                ruteNr INT NOT NULL,
                vognNr INT NOT NULL,
                plassNr INT,
                startStasjon VARCHAR(50),
                endeStasjon VARCHAR(50),
                avgangsTid TIME,
                ankomstTid TIME,
                CONSTRAINT billett_pk PRIMARY KEY (ordreNr, dato, ruteNr, vognNr, plassNr, startStasjon, endeStasjon),
                CONSTRAINT ordre_fk FOREIGN KEY (ordreNr) REFERENCES Kundeordre
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT forekomst_fk FOREIGN KEY (dato, ruteNr) REFERENCES TogRuteForekomst(dato, ruteNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT oppsett_fk FOREIGN KEY (vognNr) REFERENCES oppsettPaaRute(vognNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT stasjon_fk FOREIGN KEY (startStasjon, endeStasjon) REFERENCES JernbaneStasjon(startStasjon, endeStasjon)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
                CONSTRAINT tid_fk FOREIGN KEY (avgangsTid, ankomstTid) REFERENCES StasjonPaaRute(avgangsTid, ankomstTid)
)''')

# Create TogruteForekomst table
c.execute('''CREATE TABLE TogRuteForeKomst (
                ruteNr INT,
                dato date,
                CONSTRAINT forekomst_pk PRIMARY KEY (ruteNr, dato),
                CONSTRAINT togrute_fk FOREIGN KEY(rutenr) REFERENCES Togrute(ruteNr)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION,
                CONSTRAINT dato_fk FOREIGN KEY(dato) REFERENCES ForekomstDato(dato)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION  
)''')

# Create ForekomstDato table
c.execute('''CREATE TABLE ForekomstDato (
                dato date,
            ukedag VARCHAR(10),
            CONSTRAINT dato_pk PRIMARY KEY (dato)
)''')

# Insert data into tables

# Insert data into JernbaneStasjon table
c.execute('''INSERT INTO JernbaneStasjon VALUES ("Trondheim",5.1)''')
c.execute('''INSERT INTO JernbaneStasjon VALUES ("Steinkjer",3.8)''')
c.execute('''INSERT INTO JernbaneStasjon VALUES ("Mosjøen",6.8)''')
c.execute('''INSERT INTO JernbaneStasjon VALUES ("Mo i Rana",3.5)''')
c.execute('''INSERT INTO JernbaneStasjon VALUES ("Fauske",34.0)''')
c.execute('''INSERT INTO JernbaneStasjon VALUES ("Bodø",4.1)''')

# Insert data into BaneStrekning table
c.execute('''INSERT INTO BaneStrekning VALUES ("NordlandsBanen", "Diesel", 6, 5, "Trondheim-Bodø", "Trondheim", "Bodø")''')

# Insert data into Delstrekning table
c.execute('''INSERT INTO Delstrekning VALUES ("Trondheim", "Steinkjer", 120, TRUE, "NordlandsBanen")''')
c.execute('''INSERT INTO Delstrekning VALUES ("Steinkjer", "Mosjøen", 280, FALSE, "NordlandsBanen")''')
c.execute('''INSERT INTO Delstrekning VALUES ("Mosjøen", "Mo i Rana", 90, FALSE, "NordlandsBanen")''')
c.execute('''INSERT INTO Delstrekning VALUES ("Mo i Rana", "Fuaske", 170, FALSE, "NordlandsBanen")''')
c.execute('''INSERT INTO Delstrekning VALUES ("Fauske", "Bodø", 60, FALSE, "NordlandsBanen")''')
c.execute('''INSERT INTO Delstrekning VALUES ("Steinkjer", "Trondheim", 120, TRUE, "NordlandsBanen");''')
c.execute('''INSERT INTO Delstrekning VALUES ("Mosjøen", "Steinkjer", 280, FALSE, "NordlandsBanen");''')
c.execute('''INSERT INTO Delstrekning VALUES ("Mo i Rana", "Mosjøen", 90, FALSE, "NordlandsBanen");''')

# Insert data into Operator table
c.execute("INSERT INTO Operator VALUES ('SJ')")

# Togrute 1 
c.execute('''INSERT INTO Togrute VALUES (1, "SJ", "NordlandsBanen")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Trondheim", 1, "07:49", "07:49")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Steinkjer", 1, "09:51", "09:51")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Mosjøen", 1, "13:20", "13:20")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Mo i Rana", 1, "14:31", "14:31")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Fauske", 1, "16:49", "16:49")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Bodø", 1, "17:34", "17:34")''')
c.execute('''INSERT INTO Vogn VALUES (1, "SJ")''')
c.execute('''INSERT INTO Vogn VALUES (2, "SJ")''')
c.execute('''INSERT INTO Sittevogn VALUES (1, 3, 4)''')
c.execute('''INSERT INTO Sittevogn VALUES (2, 3, 4)''')
c.execute('''INSERT INTO oppsettPaaRute VALUES (1, 1, 1)''')
c.execute('''INSERT INTO oppsettPaaRute VALUES (1, 2, 2)''')
c.execute('''INSERT INTO DelstrekningPaaRute VALUES ("Trondheim", "Steinkjer", 1)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Steinkjer", "Mosjøen", 1)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Mosjøen", "Mo i Rana", 1)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Mo i Rana", "Fauske", 1)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Fauske", "Bodø", 1)''')

# Togrute 2
c.execute('''INSERT INTO Togrute VALUES (2, "SJ", "NordlandsBanen")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Trondheim", 2, "23:05", "23:05")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Steinkjer", 2, "00:57", "00:57")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Mosjøen", 2, "04:41", "04:41")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Mo i Rana", 2, "05:55", "05:55")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Fauske", 2, "08:19", "08:19")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Bodø", 2, "09:05", "09:05")''')
c.execute('''INSERT INTO Vogn VALUES (3, "SJ")''')
c.execute('''INSERT INTO Vogn VALUES (4, "SJ")''')
c.execute('''INSERT INTO Sittevogn VALUES (3, 3, 4)''')
c.execute('''INSERT INTO Sovevogn VALUES (4, 4, 2)''')
c.execute('''INSERT INTO oppsettPaaRute VALUES (2, 3, 1)''')
c.execute('''INSERT INTO oppsettPaaRute VALUES (2, 4, 2)''')
c.execute('''INSERT INTO DelstrekningPaaRute VALUES ("Trondheim", "Steinkjer", 2)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Steinkjer", "Mosjøen", 2)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Mosjøen", "Mo i Rana", 2)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Mo i Rana", "Fauske", 2)''')
c.execute('''INSERT INTO DelstrekningPaaRute Values ("Fauske", "Bodø", 2)''')

# Togrute 3
c.execute('''INSERT INTO Togrute VALUES (3, "SJ", "NordlandsBanen")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Mo i Rana", 3, "08:11", "08:11")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Mosjøen", 3, "09:14", "09:14")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Steinkjer", 3, "12:31", "12:31")''')
c.execute('''INSERT INTO StasjonPaaRute VALUES ("Trondheim", 3, "14:13", "14:13")''')
c.execute('''INSERT INTO Vogn VALUES (5, "SJ")''')
c.execute('''INSERT INTO Sittevogn VALUES (5, 3, 4)''')
c.execute('''INSERT INTO oppsettPaaRute VALUES (3, 5, 1)''')
c.execute('''INSERT INTO DelstrekningPaaRute VALUES ("Mo i Rana", "Mosjøen", 3)''')
c.execute('''INSERT INTO DelstrekningPaaRute VALUES ("Mosjøen", "Steinkjer", 3)''')
c.execute('''INSERT INTO DelstrekningPaaRute VALUES ("Steinkjer", "Trondheim", 3)''')

# Dager
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-03", "Mandag")''')
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-04", "Tirsdag")''')
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-05", "Onsdag")''')
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-06", "Torsdag")''')
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-07", "Fredag")''')
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-08", "Lørdag")''')
c.execute('''INSERT INTO ForekomstDato VALUES ("2023-04-09", "Søndag")''')

# TogRuteForekomst
c.execute('''INSERT INTO TogRuteForekomst VALUES (1, "2023-04-03")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (1, "2023-04-04")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (1, "2023-04-05")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (1, "2023-04-06")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (1, "2023-04-07")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-03")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-04")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-05")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-06")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-07")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-08")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (2, "2023-04-09")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (3, "2023-04-03")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (3, "2023-04-04")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (3, "2023-04-05")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (3, "2023-04-06")''')
c.execute('''INSERT INTO TogRuteForekomst VALUES (3, "2023-04-07")''')

# Kundeordre
c.execute('''INSERT INTO KundeOrdre VALUES (2, "2023-03-23", "10:31", 1)''')
c.execute('''INSERT INTO KundeOrdre VALUES (1, "2023-02-01", "12:25", 2)''')
c.execute('''INSERT INTO KundeOrdre VALUES (3, "2023-03-12", "12:40", 1)''')

# Billett
c.execute('''INSERT INTO Billett VALUES (1, "2023-03-24", 1, 1, 1, "Trondheim", "Steinkjer", "07:49", "09:51")''')
c.execute('''INSERT INTO Billett VALUES (2, "2023-04-03", 1, 1, 2, "Steinkjer", "Mosjøen", "09:51", "13:20")''')
c.execute('''INSERT INTO Billett VALUES (1, "2023-04-03", 1, 2, 6, "Trondheim", "Fauske", "07:49", "16:49")''')
c.execute('''INSERT INTO Billett VALUES (1, "2023-04-03", 1, 1, 6, "Trondheim", "Fauske", "07:49", "16:49")''')
c.execute('''INSERT INTO Billett VALUES (2, "2023-04-03", 3, 1, 6, "Steinkjer", "Trondheim", "12:31", "14:13")''')
c.execute('''INSERT INTO Billett VALUES (2, "2023-02-03", 2, 1, 6, "Trondheim", "Steinkjer", "23:05", "00:57")''')
c.execute('''INSERT INTO Billett VALUES (2, "2023-03-20", 2, 1, 6, "Steinkjer", "Bodø", "00:57", "09:05")''')
c.execute('''INSERT INTO Billett VALUES (2, "2023-04-03", 2, 2, 8, "Trondheim", "Mo i Rana", "23:05", "05:55")''')
c.execute('''INSERT INTO Billett VALUES (2, "2023-04-03", 1, 1, 3, "Mo i Rana", "Fauske", "14:31", "16:49")''')
c.execute('''INSERT INTO Billett VALUES (3, "2023-04-03", 3, 2, 6, "Mo i Rana", "Trondheim", "08:11", "14:13")''')

conn.commit()
c.close()
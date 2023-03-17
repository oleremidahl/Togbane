-- oppretter tabeller

DROP TABLE IF EXISTS ForekomstDato;
DROP TABLE IF EXISTS TogRuteForekomst;
DROP TABLE IF EXISTS Billett;
DROP TABLE IF EXISTS Kundeordre;
DROP TABLE IF EXISTS Kunde;
DROP TABLE IF EXISTS Sovevogn;
DROP TABLE IF EXISTS Sittevogn;
DROP TABLE IF EXISTS Vogn;
DROP TABLE IF EXISTS oppsettPaaRute;
DROP TABLE IF EXISTS Operator;
DROP TABLE IF EXISTS DelstrekningPaaRute;
DROP TABLE IF EXISTS StasjonPaaRute;
DROP TABLE IF EXISTS Delstrekning;
DROP TABLE IF EXISTS BaneStrekning;
DROP TABLE IF EXISTS Togrute;
DROP TABLE IF EXISTS JernbaneStasjon;

CREATE TABLE JernbaneStasjon (
navn VARCHAR(50) PRIMARY KEY,
moh INT NOT NULL
);

CREATE TABLE Togrute (
	ruteNr	INT NOT NULL,
	operator	VARCHAR(20) NOT NULL,
	baneNavn	VARCHAR(50) NOT NULL,
	PRIMARY KEY(ruteNr),
	FOREIGN KEY(operator) REFERENCES Operator(navn) 
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
	FOREIGN KEY(baneNavn) REFERENCES BaneStrekning(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE BaneStrekning (
navn VARCHAR(50) PRIMARY KEY,
energi VARCHAR(20),
antStasjoner INT,
antDelstrekninger INT,
hovedretning VARCHAR(50),
startStasjon VARCHAR(50) NOT NULL,
endeStasjon VARCHAR(50) NOT NULL,
FOREIGN KEY (startStasjon) REFERENCES JernbaneStasjon(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
FOREIGN KEY (endeStasjon) REFERENCES JernbaneStasjon(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE Delstrekning (
startStasjon VARCHAR(50) NOT NULL,
endeStasjon VARCHAR(50) NOT NULL,
lengde INT,
DobbeltSpor BOOLEAN,
baneNavn VARCHAR(50) NOT NULL,
PRIMARY KEY (startStasjon, endeStasjon),
FOREIGN KEY (startStasjon) REFERENCES JernbaneStasjon(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
FOREIGN KEY (endeStasjon) REFERENCES JernbaneStasjon(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
FOREIGN KEY (baneNavn) REFERENCES BaneStrekning(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE StasjonPaaRute (
stasjonsNavn VARCHAR(50) NOT NULL,
ruteNr INT NOT NULL,
ankomstTid TIME,
avgangsTid TIME,
PRIMARY KEY (stasjonsNavn, ruteNr),
FOREIGN KEY (stasjonsNavn) REFERENCES JernbaneStasjon(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
FOREIGN KEY (ruteNr) REFERENCES Togrute(ruteNr)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE DelstrekningPaaRute (
startStasjon VARCHAR(50) NOT NULL,
endeStasjon VARCHAR(50) NOT NULL,
ruteNr INT NOT NULL,
PRIMARY KEY (startStasjon, endeStasjon, ruteNr),
FOREIGN KEY (startStasjon, endeStasjon) REFERENCES Delstrekning(startStasjon, endeStasjon)
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
FOREIGN KEY (ruteNr) REFERENCES Togrute(ruteNr)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE Operator (
navn VARCHAR(20),
PRIMARY KEY (navn)
);

CREATE TABLE oppsettPaaRute (
ruteNr INT NOT NULL,
serieNr INT NOT NULL,
vognNr INT NOT NULL,
PRIMARY KEY (ruteNr, serieNr),
FOREIGN KEY (ruteNr) REFERENCES Togrute(ruteNr)
	ON UPDATE CASCADE
	ON DELETE NO ACTION,
FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE Vogn (
serieNr INT PRIMARY KEY,
operatornavn VARCHAR(20) NOT NULL,
FOREIGN KEY (operatornavn) REFERENCES Operator(navn)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE Sittevogn (
serieNr INT NOT NULL,
antRader INT,
antSeterPrRad INT,
PRIMARY KEY (serieNr),
FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE Sovevogn (
serieNr INT NOT NULL,
antKupeer INT,
antSengerPrKupe INT,
PRIMARY KEY (serieNr),
FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
	ON UPDATE CASCADE
	ON DELETE NO ACTION
);

CREATE TABLE Kunde (
kundeNr INT PRIMARY KEY,
navn VARCHAR(50),
epost VARCHAR(50),
tlf INT
);

CREATE TABLE Kundeordre (
	ordreNr INT NOT NULL,
	dato DATE,
	tid TIME,
	kundeNr INT NOT NULL,
	CONSTRAINT ordre_pk PRIMARY KEY (ordreNr),
	CONSTRAINT kunde_fk FOREIGN KEY (kundeNr) REFERENCES Kunde(kundeNr)
		ON UPDATE CASCADE
		ON DELETE NO ACTION
);

CREATE TABLE Billett (
	ordreNr INT NOT NULL,
	dato DATE NOT NULL,
	ruteNr INT NOT NULL,
	serieNr INT NOT NULL,
	plassNr INT,
	startStasjon VARCHAR(50),
	endeStasjon VARCHAR(50),
	CONSTRAINT billett_pk PRIMARY KEY (ordreNr, dato, ruteNr, serieNr, plassNr),
	CONSTRAINT ordre_fk FOREIGN KEY (ordreNr) REFERENCES Kundeordre
		ON UPDATE CASCADE
		ON DELETE NO ACTION,
	CONSTRAINT forekomst_fk FOREIGN KEY (dato, ruteNr) REFERENCES TogRuteForekomst(dato, ruteNR)
		ON UPDATE CASCADE
		ON DELETE NO ACTION,
	CONSTRAINT vogn_fk FOREIGN KEY (serieNr) REFERENCES Vogn(serieNr)
		ON UPDATE CASCADE
		ON DELETE NO ACTION,
	CONSTRAINT stasjon_fk FOREIGN KEY (startStasjon, endeStasjon) REFERENCES JernbaneStasjon(startStasjon, endeStasjon)
		ON UPDATE CASCADE
		ON DELETE NO ACTION
);

CREATE TABLE TogRuteForekomst(
	ruteNr INT,
	dato date,
	CONSTRAINT forekomst_pk PRIMARY KEY (ruteNr, dato),
	CONSTRAINT togrute_fk FOREIGN KEY(rutenr) REFERENCES Togrute(ruteNr)
		ON UPDATE CASCADE
		ON DELETE NO ACTION
);

CREATE TABLE ForekomstDato (
	dato date,
	ukedag VARCHAR(10),
	CONSTRAINT dato_pk PRIMARY KEY (dato),
	CONSTRAINT forekomst_fk FOREIGN KEY (dato) REFERENCES TogRuteForekomst(dato)
		ON UPDATE CASCADE
		ON DELETE NO ACTION
);

-- legger inn data 

-- JernbaneStasjoner
INSERT INTO JernbaneStasjon VALUES ("Trondheim", 5.1);
INSERT INTO JernbaneStasjon VALUES ("Steinkjer", 3.8);
INSERT INTO JernbaneStasjon VALUES ("Mosjøen",  6.8);
INSERT INTO JernbaneStasjon VALUES ("Mo i Rana", 3.5);
INSERT INTO JernbaneStasjon VALUES ("Fauske", 34.0);
INSERT INTO JernbaneStasjon VALUES ("Bodø", 4.1);

-- BaneStrekning
INSERT INTO BaneStrekning VALUES ("NordlandsBanen", "Diesel", 6, 5, "Trondheim-Bodø","Trondheim","Bodø");

-- Delstrekninger
INSERT INTO Delstrekning VALUES ("Trondheim", "Steinkjer", 120, TRUE, "NordlandsBanen");
INSERT INTO Delstrekning VALUES ("Steinkjer", "Mosjøen", 280, FALSE, "NordlandsBanen");
INSERT INTO Delstrekning VALUES ("Mosjøen", "Mo i Rana", 90, FALSE, "NordlandsBanen");
INSERT INTO Delstrekning VALUES ("Mo i Rana", "Fauske", 170, FALSE, "NordlandsBanen");
INSERT INTO Delstrekning VALUES ("Fauske", "Bodø", 60, FALSE, "NordlandsBanen");

-- Operatør
INSERT INTO Operator VALUES ("SJ");

-- Togrute
INSERT INTO Togrute VALUES (1, "SJ", "NordlandsBanen");
INSERT INTO StasjonPaaRute VALUES ("Trondheim", 1, NULL, "07:49");
INSERT INTO StasjonPaaRute VALUES ("Steinkjer", 1, "09:51", "09:51");
INSERT INTO StasjonPaaRute VALUES ("Mosjøen", 1, "13:20", "13:20");
INSERT INTO StasjonPaaRute VALUES ("Mo i Rana", 1, "14:31", "14:31");
INSERT INTO StasjonPaaRute VALUES ("Fauske", 1, "16:49", "16:49");
INSERT INTO StasjonPaaRute VALUES ("Bodø", 1, "17:34", "17:34");
INSERT INTO Vogn VALUES (1, "SJ");
INSERT INTO Vogn VALUES (2, "SJ");
INSERT INTO Sittevogn VALUES (1, 3, 4);
INSERT INTO Sittevogn VALUES (2, 3, 4);
INSERT INTO oppsettPaaRute VALUES (1, 1, 1);
INSERT INTO oppsettPaaRute VALUES (1, 2, 2);
INSERT INTO DelstrekningPaaRute VALUES ("Trondheim", "Steinkjer", 1);
INSERT INTO DelstrekningPaaRute Values ("Steinkjer", "Mosjøen", 1);
INSERT INTO DelstrekningPaaRute Values ("Mosjøen", "Mo i Rana", 1);
INSERT INTO DelstrekningPaaRute Values ("Mo i Rana", "Fauske", 1);
INSERT INTO DelstrekningPaaRute Values ("Fauske", "Bodø", 1);

-- Togrute
INSERT INTO Togrute VALUES (2, "SJ", "NordlandsBanen");
INSERT INTO StasjonPaaRute VALUES ("Trondheim", 2, NULL, "23:05");
INSERT INTO StasjonPaaRute VALUES ("Steinkjer", 2, "00:57", "00:57");
INSERT INTO StasjonPaaRute VALUES ("Mosjøen", 2, "04:41", "04:41");
INSERT INTO StasjonPaaRute VALUES ("Mo i Rana", 2, "05:55", "05:55");
INSERT INTO StasjonPaaRute VALUES ("Fauske", 2, "08:19", "08:19");
INSERT INTO StasjonPaaRute VALUES ("Bodø", 2, "09:05", "09:05");
INSERT INTO Vogn VALUES (3, "SJ");
INSERT INTO Vogn VALUES (4, "SJ");
INSERT INTO Sittevogn VALUES (3, 3, 4);
INSERT INTO Sovevogn VALUES (4, 4, 2);
INSERT INTO oppsettPaaRute VALUES (2, 3, 1);
INSERT INTO oppsettPaaRute VALUES (2, 4, 2);
INSERT INTO DelstrekningPaaRute VALUES ("Trondheim", "Steinkjer", 2);
INSERT INTO DelstrekningPaaRute VALUES ("Steinkjer", "Mosjøen", 2);
INSERT INTO DelstrekningPaaRute VALUES ("Mosjøen", "Mo i Rana", 2);
INSERT INTO DelstrekningPaaRute VALUES ("Mo i Rana", "Fauske", 2);
INSERT INTO DelstrekningPaaRute VALUES ("Fauske", "Bodø", 2);

-- Togrute 
INSERT INTO Togrute VALUES (3, "SJ", "NordlandsBanen");
INSERT INTO StasjonPaaRute VALUES ("Mo i Rana", 3, NULL, "08:11");
INSERT INTO StasjonPaaRute VALUES ("Mosjøen", 3, "09:14", "09:14");
INSERT INTO StasjonPaaRute VALUES ("Steinkjer", 3, "12:31", "12:31");
INSERT INTO StasjonPaaRute VALUES ("Trondheim", 3, "14:13", "14:13");
INSERT INTO Vogn VALUES (5, "SJ");
INSERT INTO Sittevogn VALUES (5, 3, 4);
INSERT INTO oppsettPaaRute VALUES (3, 5, 1);
INSERT INTO DelstrekningPaaRute VALUES ("Mo i Rana", "Mosjøen", 3);
INSERT INTO DelstrekningPaaRute VALUES ("Mosjøen", "Steinkjer", 3);
INSERT INTO DelstrekningPaaRute VALUES ("Steinkjer", "Trondheim", 3);

-- TogruteForekomst
INSERT INTO TogRuteForekomst VALUES (1, "2016-01-01");
INSERT INTO ForekomstDato VALUES ("2016-01-01", "Fredag");
INSERT INTO TogruteForekomst VALUES (1, "2016-01-02");
INSERT INTO ForekomstDato VALUES ("2016-01-02", "Lørdag");
INSERT INTO TogruteForekomst VALUES (1, "2016-01-03");
INSERT INTO ForekomstDato VALUES ("2016-01-03", "Søndag");
INSERT INTO TogRuteForekomst VALUES (2, "2016-01-01");
INSERT INTO TogRuteForekomst VALUES (2, "2016-01-02");
INSERT INTO TogRuteForekomst VALUES (2, "2016-01-03");
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-01");	
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-02");
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-03");
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-04");
INSERT INTO ForekomstDato VALUES ("2016-01-04", "Mandag");
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-05");
INSERT INTO ForekomstDato VALUES ("2016-01-05", "Tirsdag");
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-06");
INSERT INTO ForekomstDato VALUES ("2016-01-06", "Onsdag");
INSERT INTO TogRuteForekomst VALUES (3, "2016-01-07");
INSERT INTO ForekomstDato VALUES ("2016-01-07", "Torsdag");
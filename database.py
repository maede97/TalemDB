import sqlite3
from person import Person
import config

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE)
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS personen(id INTEGER PRIMARY KEY, vorname TEXT,nachname TEXT,adresse TEXT,plz INTEGER,ort TEXT,land TEXT DEFAULT 'CH', email TEXT, telefon TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kunden(id INTEGER PRIMARY KEY, kunden_id INTEGER, FOREIGN KEY (kunden_id) REFERENCES personen (id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS mitglieder(id INTEGER PRIMARY KEY, mitglieder_id INTEGER, FOREIGN KEY (mitglieder_id) REFERENCES personen (id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS aufgaben(id INTEGER PRIMARY KEY, beschreib TEXT, zeitpunkt DATETIME)")

    def insertTestData(self):
        p1 = Person("Max","Müller", "Teststrasse 1", "8344", "Bäretswil","CH","email@mail.com","079 886 12 45")
        p1.setKunde(True)
        p2 = Person("Zweiter","Müller", "Teststrasse 1", "8344", "Bäretswil","CH","email@mail.com","079 886 12 45")
        p2.setMitglied(True)
        p3 = Person("Dritter","Müller", "Teststrasse 1", "8344", "Bäretswil","CH","email@mail.com","079 886 12 45")
        p3.setKunde(True)
        p3.setMitglied(True)
        
        self.insertPerson(p1, True, False)
        self.insertPerson(p2, False, True)
        self.insertPerson(p3, True, True)

    def insertPerson(self, person, kunde=False, mitglied=False):
        values = [person.vorname, person.nachname, person.adresse, person.plz, person.ort, person.land, person.email, person.telefon]
        self.cursor.execute("INSERT INTO personen(vorname,nachname,adresse,plz,ort,land,email,telefon) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
        if(kunde or mitglied):
            last_id = str(self.cursor.lastrowid)
            if kunde:
                self.cursor.execute("INSERT INTO kunden(kunden_id) VALUES(?)", last_id)
            if mitglied:
                self.cursor.execute("INSERT INTO mitglieder(mitglieder_id) VALUES(?)", last_id)
        self.conn.commit()

    def dropAll(self):
        self.cursor.execute("DELETE FROM kunden")
        self.cursor.execute("DELETE FROM mitglieder")
        self.cursor.execute("DELETE FROM personen")
        self.cursor.execute("DELETE FROM aufgaben")

    def getPersonen(self):
        personen = []
        for row in self.cursor.execute("SELECT * FROM personen ORDER BY nachname ASC"):
            p = Person(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            p.setID(row[0])
            personen.append(p)
        return personen
    def getKunden(self):
        personen = []
        for row in self.cursor.execute("SELECT * FROM personen,kunden WHERE kunden_id = personen.id ORDER BY personen.nachname ASC"):
            p = Person(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            p.setID(row[0])
            personen.append(p)
        return personen
    def getMitglieder(self):
        personen = []
        for row in self.cursor.execute("SELECT * FROM personen,mitglieder WHERE mitglieder_id = personen.id ORDER BY personen.nachname ASC"):
            p = Person(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            p.setID(row[0])
            personen.append(p)
        return personen
    
    def isKunde(self, id):
        self.cursor.execute("SELECT * FROM kunden WHERE kunden_id=?",str(id))
        return not self.cursor.fetchone() == None

    def isMitglied(self, id):
        self.cursor.execute("SELECT * FROM mitglieder WHERE mitglieder_id=?",str(id))
        return not self.cursor.fetchone() == None

    def updatePerson(self, person, kunde, mitglied):
        print("updatePerson",person.id, kunde,mitglied)
        values = [person.vorname, person.nachname, person.adresse, person.plz, person.ort, person.land, person.email, person.telefon, str(person.id)]
        self.cursor.execute("UPDATE personen SET vorname=?, nachname=?, adresse=?, plz=?, ort=?, land=?, email=?, telefon=? WHERE id=?", values)
        if kunde:
            if not self.isKunde(person.id):
                self.cursor.execute("INSERT INTO kunden(kunden_id) VALUES(?)",str(person.id))
        else:
            self.cursor.execute("DELETE FROM kunden WHERE kunden_id=?",str(person.id))

        if mitglied:
            if not self.isMitglied(person.id):
                self.cursor.execute("INSERT INTO mitglieder(mitglieder_id) VALUES(?)",str(person.id))
        else:
            self.cursor.execute("DELETE FROM mitglieder WHERE mitglieder_id=?",str(person.id))
        self.conn.commit()
    
    def getPersonByID(self, id):
        personen = []
        for row in self.cursor.execute("SELECT * FROM personen WHERE id=?", str(id)):
            p = Person(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            p.setID(row[0])
            if(self.isKunde(row[0])):
                p.setKunde(True)
            if(self.isMitglied(row[0])):
                p.setMitglied(True)
            personen.append(p)
        assert(len(personen) == 1)
        return personen[0]

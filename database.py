import sqlite3
from person import Person
import config


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE)
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS personen(\
            id INTEGER PRIMARY KEY, anrede TEXT DEFAULT '', vorname TEXT,nachname TEXT,adresse TEXT DEFAULT '',\
            plz INTEGER DEFAULT 0,ort TEXT DEFAULT '',land TEXT DEFAULT 'CH', email TEXT DEFAULT '', telefon TEXT DEFAULT '', abonnement INTEGER DEFAULT 0)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS rechnungen(\
            id INTEGER PRIMARY KEY, personen_id INTEGER, rechnungsart TEXT DEFAULT '', rechnungsintervall INTEGER DEFAULT 0, erstbestellung DATE DEFAULT 0,\
            FOREIGN KEY (personen_id) REFERENCES personen(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS bestellungen(id INTEGER PRIMARY KEY, personen_id INTEGER,\
            sorte_dalo REAL DEFAULT 0, sorte_star REAL DEFAULT 0, sorte_dachi REAL DEFAULT 0, sonstiges TEXT DEFAULT '',\
            FOREIGN KEY(personen_id) REFERENCES personen(id))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS kunden(id INTEGER PRIMARY KEY, kunden_id INTEGER, FOREIGN KEY (kunden_id) REFERENCES personen (id))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS mitglieder(id INTEGER PRIMARY KEY, mitglieder_id INTEGER, FOREIGN KEY (mitglieder_id) REFERENCES personen (id))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS aufgaben(id INTEGER PRIMARY KEY, beschreib TEXT DEFAULT '', zeitpunkt DATETIME)")

    def insertTestData(self):
        p1 = Person("Herr", "Max", "Müller", "Teststrasse 1", "8344",
                    "Bäretswil", "CH", "email@mail.com", "079 886 12 45")
        p1.setKunde(True)
        p2 = Person("Frau", "Zweiter", "Müller", "Teststrasse 1",
                    "8344", "Bäretswil", "CH", "email@mail.com", "079 886 12 45")
        p2.setMitglied(True)
        p3 = Person("Anrede BSP", "Dritter", "Müller", "Teststrasse 1",
                    "8344", "Bäretswil", "CH", "email@mail.com", "079 886 12 45")
        p3.setKunde(True)
        p3.setMitglied(True)

        p1.setAbo(True)
        p2.setAbo(True)

        id1 = self.insertPerson(p1, True, False)
        self.insertPerson(p2, False, True)
        self.insertPerson(p3, True, True)

        self.updateBestellungen(id1, 1.5, 2.5, 3.5, "Sonstiges")
        self.insertRechnungsData(id1, "rechnung", 12)

    def getBestellungenById(self, id):
        """return array of [dalo,star,dachi] in kg each"""
        kaffees = []
        for row in self.cursor.execute("SELECT sorte_dalo,sorte_star,sorte_dachi,sonstiges FROM bestellungen WHERE personen_id=?", [str(id)]):
            kaffees.append([row[0], row[1], row[2], row[3]])
        # should only be one entry per person
        return kaffees[0] if len(kaffees) > 0 else [0, 0, 0, ""]

    def insertRechnungsData(self, pid, rechnungsart, rechnungsintervall):
        values = [pid, rechnungsart, rechnungsintervall]
        self.cursor.execute(
            "INSERT INTO rechnungen(personen_id, rechnungsart, rechnungsintervall) VALUES (?, ?, ?)", values)
        self.conn.commit()

    def getRechnungsData(self, pid):
        """get rechnungsart,rechnungsintervall,erstbestellung from personen_id"""
        for row in self.cursor.execute("SELECT rechnungsart,rechnungsintervall,erstbestellung FROM rechnungen WHERE personen_id=?", [str(pid)]):
            return row
        return None

    def updateBestellungen(self, pid, dalo, star, dachi, sonstiges):
        values = [str(pid), str(dalo), str(star), str(dachi), sonstiges]
        has = False
        for _ in self.cursor.execute("SELECT * FROM bestellungen WHERE personen_id=?", [str(pid)]):
            has = True
        if(has):
            values = [str(dalo), str(star), str(dachi), sonstiges, str(pid)]
            self.cursor.execute(
                "UPDATE bestellungen SET sorte_dalo=?, sorte_star=?,sorte_dachi=?,sonstiges=? WHERE personen_id=?", values)
        else:
            self.cursor.execute(
                "INSERT INTO bestellungen(personen_id, sorte_dalo, sorte_star, sorte_dachi, sonstiges) VALUES (?, ?, ?, ?, ?)", values)
        self.conn.commit()

    def insertPerson(self, person, kunde=False, mitglied=False):
        values = [person.anrede, person.vorname, person.nachname, person.adresse,
                  person.plz, person.ort, person.land, person.email, person.telefon]
        self.cursor.execute(
            "INSERT INTO personen(anrede,vorname,nachname,adresse,plz,ort,land,email,telefon) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
        pid = str(self.cursor.lastrowid)
        if(kunde or mitglied):
            if kunde:
                self.cursor.execute(
                    "INSERT INTO kunden(kunden_id) VALUES(?)", [pid])
            if mitglied:
                self.cursor.execute(
                    "INSERT INTO mitglieder(mitglieder_id) VALUES(?)", [pid])
        self.conn.commit()
        return pid

    def dropAll(self):
        self.cursor.execute("DELETE FROM kunden")
        self.cursor.execute("DELETE FROM mitglieder")
        self.cursor.execute("DELETE FROM personen")
        self.cursor.execute("DELETE FROM bestellungen")
        self.cursor.execute("DELETE FROM rechnungen")
        self.cursor.execute("DELETE FROM aufgaben")

    def getPersonen(self):
        personen = []
        for row in self.cursor.execute("SELECT id,anrede,vorname,nachname,adresse,plz,ort,land,email,telefon FROM personen ORDER BY nachname ASC"):
            p = Person(row[1], row[2], row[3], row[4],
                       row[5], row[6], row[7], row[8], row[9])
            p.setID(row[0])
            personen.append(p)
        return personen

    def getKunden(self):
        personen = []
        for row in self.cursor.execute("SELECT personen.id,anrede,vorname,nachname,adresse,plz,ort,land,email,telefon FROM personen,kunden WHERE kunden_id = personen.id ORDER BY personen.nachname ASC"):
            p = Person(row[1], row[2], row[3], row[4],
                       row[5], row[6], row[7], row[8], row[9])
            p.setID(row[0])
            personen.append(p)
        return personen

    def getMitglieder(self):
        personen = []
        for row in self.cursor.execute("SELECT personen.id,anrede,vorname,nachname,adresse,plz,ort,land,email,telefon FROM personen,mitglieder WHERE mitglieder_id = personen.id ORDER BY personen.nachname ASC"):
            p = Person(row[1], row[2], row[3], row[4],
                       row[5], row[6], row[7], row[8], row[9])
            p.setID(row[0])
            personen.append(p)
        return personen

    def isKunde(self, id):
        self.cursor.execute(
            "SELECT * FROM kunden WHERE kunden_id=?", [str(id)])
        return not self.cursor.fetchone() == None

    def isMitglied(self, id):
        self.cursor.execute(
            "SELECT * FROM mitglieder WHERE mitglieder_id=?", [str(id)])
        return not self.cursor.fetchone() == None

    def updatePerson(self, person, kunde, mitglied):
        values = [person.anrede, person.vorname, person.nachname, person.adresse,
                  person.plz, person.ort, person.land, person.email, person.telefon, str(person.id)]
        self.cursor.execute(
            "UPDATE personen SET anrede=?, vorname=?, nachname=?, adresse=?, plz=?, ort=?, land=?, email=?, telefon=? WHERE id=?", values)
        if kunde:
            if not self.isKunde(person.id):
                self.cursor.execute(
                    "INSERT INTO kunden(kunden_id) VALUES(?)", [str(person.id)])
        else:
            self.cursor.execute(
                "DELETE FROM kunden WHERE kunden_id=?", [str(person.id)])

        if mitglied:
            if not self.isMitglied(person.id):
                self.cursor.execute(
                    "INSERT INTO mitglieder(mitglieder_id) VALUES(?)", [str(person.id)])
        else:
            self.cursor.execute(
                "DELETE FROM mitglieder WHERE mitglieder_id=?", [str(person.id)])
        self.conn.commit()

    def getPersonByID(self, id):
        personen = []
        for row in self.cursor.execute("SELECT id,anrede, vorname,nachname,adresse,plz,ort,land,email,telefon FROM personen WHERE id=?", [str(id)]):
            p = Person(row[1], row[2], row[3], row[4],
                       row[5], row[6], row[7], row[8], row[9])
            p.setID(row[0])
            if(self.isKunde(row[0])):
                p.setKunde(True)
            if(self.isMitglied(row[0])):
                p.setMitglied(True)
            personen.append(p)
        assert(len(personen) == 1)
        return personen[0]

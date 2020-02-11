import sqlite3
from person import Person
import config


class DataBase:
    def __init__(self, logger):
        self.logger = logger
        self.conn = sqlite3.connect(config.DATABASE)
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS personen(\
            id INTEGER PRIMARY KEY, anrede TEXT DEFAULT '', vorname TEXT,nachname TEXT,adresse TEXT DEFAULT '',\
            plz INTEGER DEFAULT 0,ort TEXT DEFAULT '',land TEXT DEFAULT 'CH', email TEXT DEFAULT '', telefon TEXT DEFAULT '', abonnement INTEGER DEFAULT 0, kommentar TEXT DEFAULT '')")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS rechnungen(\
            id INTEGER PRIMARY KEY, personen_id INTEGER, rechnungsart TEXT DEFAULT '', rechnungsintervall INTEGER DEFAULT 0, erstbestellung DATE DEFAULT 0,\
            FOREIGN KEY (personen_id) REFERENCES personen(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS bestellungen(id INTEGER PRIMARY KEY, personen_id INTEGER,\
            sorte_dalo REAL DEFAULT 0, sorte_star REAL DEFAULT 0, sorte_dachi REAL DEFAULT 0, sonstiges TEXT DEFAULT '',\
            FOREIGN KEY(personen_id) REFERENCES personen(id))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS kunden(id INTEGER PRIMARY KEY, kunden_id INTEGER, gefunden_via TEXT DEFAULT '', FOREIGN KEY (kunden_id) REFERENCES personen (id))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS mitglieder(id INTEGER PRIMARY KEY, mitglieder_id INTEGER, FOREIGN KEY (mitglieder_id) REFERENCES personen (id))")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS aufgaben(id INTEGER PRIMARY KEY, beschreib TEXT DEFAULT '', zeitpunkt DATETIME)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS infos(id INTEGER PRIMARY KEY, personen_id INTEGER, zwei_jaehrlich INTEGER DEFAULT 0, kafi_updates INTEGER DEFAULT 0, FOREIGN KEY (personen_id) REFERENCES personen(id))"
        )
        self.logger.info("database __init__ done")
    
    def getAllPersonenNames(self):
        """returns an array with all vornamen and nachnamen"""
        ret = set()
        try:
            for row in self.cursor.execute("SELECT vorname, nachname FROM personen"):
                ret.add(row[0])
                ret.add(row[1])
            ret = list(ret)
        except Exception as e:
            self.logger.error("getAllPersonenNames")
            self.logger.error(str(e))
            ret = []
        return ret

    def executeSQL(self, sql):
        """dangerous function, execute user inputed sql"""
        ret = []
        try:
            for row in self.cursor.execute(sql):
                ret.append(row[:])
            self.logger.info("database executeSQL " + sql)
            self.conn.commit() 
        except Exception as e:
            self.logger.error("executeSQL")
            self.logger.error(str(e))
            ret = [["An error occured. Please check your SQL-command."]]
        return ret

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

        p4 = Person("a","","","","","","","","")
        id4 = self.insertPerson(p4,False,False)
        self.deletePerson(id4)

        p1.setAbo(True)
        p2.setAbo(True)

        id1 = self.insertPerson(p1, True, False)
        self.insertPerson(p2, False, True)
        self.insertPerson(p3, True, True)

        self.updateBestellungen(id1, 1.5, 2.5, 3.5, "Sonstiges")
        self.insertRechnungsData(id1, "rechnung", 12)
        self.logger.info("database insertTestData done")


    def getBestellungenById(self, id):
        """return array of [dalo,star,dachi] in kg each"""
        kaffees = []
        try:
            for row in self.cursor.execute("SELECT sorte_dalo,sorte_star,sorte_dachi,sonstiges FROM bestellungen WHERE personen_id=?", [str(id)]):
                kaffees.append([row[0], row[1], row[2], row[3]])
            # should only be one entry per person
            self.logger.info("database getBestellungenById " + str(id))
        except Exception as e:
            self.logger.error("getBestellungenById")
            self.logger.error(str(e))
            return [0, 0, 0, "FEHLER."]
        return kaffees[0] if len(kaffees) > 0 else [0, 0, 0, ""]

    def insertRechnungsData(self, pid, rechnungsart, rechnungsintervall):
        values = [pid, rechnungsart, rechnungsintervall]
        try:
            self.cursor.execute("INSERT INTO rechnungen(personen_id, rechnungsart, rechnungsintervall) VALUES (?, ?, ?)", values)
            self.conn.commit()
            self.logger.info("database insertRechnungsData done")
        except Exception as e:
            self.logger.error("insertRechnungsData")
            self.logger.error(str(e))

    def getRechnungsData(self, pid):
        """get rechnungsart,rechnungsintervall,erstbestellung from personen_id"""
        try:
            self.logger.info("database getRechnungsData")
            for row in self.cursor.execute("SELECT rechnungsart,rechnungsintervall,erstbestellung FROM rechnungen WHERE personen_id=?", [str(pid)]):
                return row
            return None
        except Exception as e:
            self.logger.error("getRechnungsData " + str(pid))
            self.logger.error(str(e))

    def updateBestellungen(self, pid, dalo, star, dachi, sonstiges):
        try:
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
            self.logger.info("database updateBestellungen " + str(pid))
        except Exception as e:
            self.logger.error("updateBestellungen")
            self.logger.error(str(e))

    def deletePerson(self, pid):
        try:
            self.cursor.execute("DELETE FROM kunden WHERE kunden_id=?",[str(pid)])
            self.cursor.execute("DELETE FROM mitglieder WHERE mitglieder_id=?",[str(pid)])
            self.cursor.execute("DELETE FROM bestellungen WHERE personen_id=?",[str(pid)])
            self.cursor.execute("DELETE FROM rechnungen WHERE personen_id=?",[str(pid)])
            self.cursor.execute("DELETE FROM personen WHERE id=?",[str(pid)])
            self.conn.commit()
            self.logger.info("database deletePerson " + str(pid))
            return True
        except Exception as e:
            self.logger.error("deletePerson")
            self.logger.error(str(e))
            return False

    def insertPerson(self, person, kunde=False, mitglied=False, abo=False):
        try:
            values = [person.anrede, person.vorname, person.nachname, person.adresse,
                    person.plz, person.ort, person.land, person.email, person.telefon, abo]
            self.cursor.execute(
                "INSERT INTO personen(anrede,vorname,nachname,adresse,plz,ort,land,email,telefon, abonnement) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
            pid = str(self.cursor.lastrowid)
            if(kunde or mitglied):
                if kunde:
                    self.cursor.execute(
                        "INSERT INTO kunden(kunden_id) VALUES(?)", [pid])
                if mitglied:
                    self.cursor.execute(
                        "INSERT INTO mitglieder(mitglieder_id) VALUES(?)", [pid])
            self.conn.commit()
            self.logger.info("database insertPerson done")
            return pid
        except Exception as e:
            self.logger.error("insertPerson")
            self.logger.error(str(e))
            return -1

    def dropAll(self):
        try:
            self.cursor.execute("DELETE FROM kunden")
            self.cursor.execute("DELETE FROM mitglieder")
            self.cursor.execute("DELETE FROM personen")
            self.cursor.execute("DELETE FROM bestellungen")
            self.cursor.execute("DELETE FROM rechnungen")
            self.cursor.execute("DELETE FROM aufgaben")
            self.logger.info("database dropAll done")
        except:
            self.logger.error("DropAll")

    def getPersonen(self, where_clause=''):
        try:
            personen = []
            for row in self.cursor.execute("SELECT id,anrede,vorname,nachname,adresse,plz,ort,land,email,telefon,abonnement FROM personen {} ORDER BY nachname ASC".format(where_clause)):
                p = Person(row[1], row[2], row[3], row[4],
                        row[5], row[6], row[7], row[8], row[9])
                p.setID(row[0])
                p.setAbo(row[10])
                personen.append(p)
            self.logger.info("database getPersonen " + str(len(personen)))
        except Exception as e:
            self.logger.error("database getPersonen")
            self.logger.error(str(e))
            return []
        return personen

    def getKunden(self):
        try:
            personen = []
            for row in self.cursor.execute("SELECT personen.id,anrede,vorname,nachname,adresse,plz,ort,land,email,telefon,abonnement FROM personen,kunden WHERE kunden_id = personen.id ORDER BY personen.nachname ASC"):
                p = Person(row[1], row[2], row[3], row[4],
                        row[5], row[6], row[7], row[8], row[9])
                p.setID(row[0])
                p.setAbo(row[10])
                personen.append(p)
            self.logger.info("database getKunden " + str(len(personen)))
            return personen
        except Exception as e:
            self.logger.error("getKunden")
            self.logger.error(str(e))
            return []

    def getMitglieder(self):
        try:
            personen = []
            for row in self.cursor.execute("SELECT personen.id,anrede,vorname,nachname,adresse,plz,ort,land,email,telefon,abonnement FROM personen,mitglieder WHERE mitglieder_id = personen.id ORDER BY personen.nachname ASC"):
                p = Person(row[1], row[2], row[3], row[4],
                        row[5], row[6], row[7], row[8], row[9])
                p.setID(row[0])
                p.setAbo(row[10])
                personen.append(p)
            self.logger.info("database getMitglieder " + str(len(personen)))
            return personen
        except Exception as e:
            self.logger.error("getMitglieder")
            self.logger.error(str(e))
            return []

    def isKunde(self, id):
        try:
            self.cursor.execute(
                "SELECT * FROM kunden WHERE kunden_id=?", [str(id)])
            self.logger.info("database isKunde " + str(id))
            return not self.cursor.fetchone() == None
        except Exception as e:
            self.logger.error("isKunde " + str(id))
            self.logger.error(str(e))
            return False


    def isMitglied(self, id):
        try:
            self.cursor.execute(
                "SELECT * FROM mitglieder WHERE mitglieder_id=?", [str(id)])
            self.logger.info("database isMitglied " + str(id))
            return not self.cursor.fetchone() == None
        except Exception as e:
            self.logger.error("isMitglied " + str(id))
            self.logger.error(str(e))
            return False

    def updatePerson(self, person, kunde, mitglied, abo):
        try:
            values = [person.anrede, person.vorname, person.nachname, person.adresse,
                    person.plz, person.ort, person.land, person.email, person.telefon, abo, str(person.id)]
            self.cursor.execute(
                "UPDATE personen SET anrede=?, vorname=?, nachname=?, adresse=?, plz=?, ort=?, land=?, email=?, telefon=?, abonnement=? WHERE id=?", values)
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
            self.logger.info("database updatePerson " + str(person.id))
        except Exception as e:
            self.logger.error("updatePerson " + str(person.id))
            self.logger.error(str(e))

    def getPersonByID(self, id):
        try:
            personen = []
            for row in self.cursor.execute("SELECT id,anrede, vorname,nachname,adresse,plz,ort,land,email,telefon,abonnement FROM personen WHERE id=?", [str(id)]):
                p = Person(row[1], row[2], row[3], row[4],
                        row[5], row[6], row[7], row[8], row[9])
                p.setID(row[0])
                p.setAbo(row[10])
                if(self.isKunde(row[0])):
                    p.setKunde(True)
                if(self.isMitglied(row[0])):
                    p.setMitglied(True)
                personen.append(p)
            if(len(personen) == 1):
                self.logger.info("database getPersonByID " + str(id))
            else:
                self.logger.error("database getPersonByID " + str(id))
                exit(1)
            return personen[0]
        except Exception as e:
            self.logger.error("getPersonByID " + str(id))
            self.logger.error(str(e))
            return Person("","Fehler","","","","","","","")

    def getAufgaben(self):
        try:
            aufgaben = []
            for row in self.cursor.execute("SELECT * FROM aufgaben"):
                # id, beschreib, zeitpunkt
                aufgaben.append([row[0], row[1], row[2]])
            return aufgaben
        except Exception as e:
            self.logger.error("getAufgaben " + str(id))
            self.logger.error(str(e))
            return []
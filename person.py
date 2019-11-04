class Person:
    """ class to hold a person """
    def __init__(self, anrede, vorname, nachname, adresse, plz, ort, land, email, tel):
        self.anrede = anrede
        self.vorname = vorname
        self.nachname = nachname
        self.adresse = adresse
        self.plz = plz
        self.ort = ort
        self.land = land
        self.email = email
        self.telefon = tel

        self.abonnement = False
        self.id = False
        self.kunde = False
        self.mitglied = False
    def setID(self, i):
        self.id = i
    def setAbo(self, a):
        self.abonnement = a
    def setKunde(self, k):
        self.kunde = k
    def setMitglied(self, m):
        self.mitglied = m
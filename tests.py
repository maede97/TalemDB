from person import Person
from database import DataBase

# Test class, to use with pytest -q tests.py

class Tests:
    def test_person_creation(self):
        p1 = Person("M","B","Adresse","8000","Zürich","CH","email","Telefon")
        assert(p1.id == 0)
        assert(p1.kunde == False)
        assert(p1.mitglied == False)
        p1.setKunde(True)
        assert(p1.kunde == True)
    def test_database(self):
        db = DataBase()
        assert(len(db.getKunden()) <= len(db.getPersonen()))
        assert(len(db.getMitglieder()) <= len(db.getPersonen()))
    
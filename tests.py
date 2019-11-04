from person import Person
from database import DataBase
from updatechecker import check_versions

# Test class, to use with pytest -q tests.py
class Tests:
    def test_person_creation(self):
        p1 = Person("Herr","M","B","Adresse","8000","Zürich","CH","email","Telefon")
        assert(p1.id == 0)
        assert(p1.kunde == False)
        assert(p1.mitglied == False)
        p1.setKunde(True)
        assert(p1.kunde == True)
    def test_database(self):
        db = DataBase()
        db.dropAll()
        db.insertTestData() # insert 4, delete 1
        assert(len(db.getPersonen()) == 3)
        assert(len(db.getKunden()) <= len(db.getPersonen()))
        assert(len(db.getMitglieder()) <= len(db.getPersonen()))
    def test_update_versions(self):
        assert(check_versions("v1.0","v1.0"))
        assert(check_versions("v1.0.3.4.4", "v1.0.3.4.4"))
        assert(not check_versions("v1.0.3.4.4", "v1.0.5.4.4"))
        assert(not check_versions("v1.0.3.4.4", "v1.0.3.4.5"))
        assert(not check_versions("v2.0", "v1.0"))
        assert(not check_versions("v1.0", "v1.0.1"))
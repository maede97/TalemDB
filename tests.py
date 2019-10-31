from person import Person

class Tests:
    def test_person_creation(self):
        p1 = Person("M","B","Adresse","8000","Zürich","CH","email","Telefon")
        assert(p1.id == 0)
        assert(p1.kunde == False)
        assert(p1.mitglied == False)
        p1.setKunde(True)
        assert(p1.kunde == True)
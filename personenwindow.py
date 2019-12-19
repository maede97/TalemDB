from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
import excelwriter
import config

class PersonenWindow(QWidget):
    def __init__(self, master, dbHandler):

        super().__init__()

        self.master = master
        self.setWindowIcon(QIcon('logo.png'))
        self.dbHandler = dbHandler

        self.setWindowTitle("TalemDB | Personen")

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        
        button = QPushButton("Neue Person erfassen", self)
        button.clicked.connect(self.neue_person)
        layout.addWidget(button, 0,0)

        button = QPushButton("Personen exportieren", self)
        button.clicked.connect(self.export_personen)
        layout.addWidget(button, 1, 0)

        layout.addWidget(QLabel("Personen"), 2, 0)
        button = QPushButton("Markierte Person löschen", self)
        button.clicked.connect(self.ask_delete_person)
        layout.addWidget(button, 3, 0)

        self.tableView = QTableView(self)
        self.model = QStandardItemModel(self)
        self.tableView.setModel(self.model)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.model.setHorizontalHeaderLabels(['Anrede','Vorname', 'Nachname', 'Adresse', 'PLZ', 'Ort','Land','Email','Telefon', 'Kunde', 'Mitglied', 'Abonnent'])

        self.model.itemChanged.connect(self.update)

        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.setLayout(windowLayout)

        layout.addWidget(self.tableView, 4, 0)

        self.loadListBox(self.model)
        self.show()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.destroy()

    def ask_delete_person(self):
        # get selected row:
        if(len(self.tableView.selectedIndexes()) < 1):
            return
        pid = self.p_id_list[self.tableView.selectedIndexes()[0].row()]
        p = self.dbHandler.getPersonByID(pid)

        msg = QMessageBox.question(self, "Person löschen", "Soll die Person "+p.vorname + " "+p.nachname+" wirklich endgültig gelöscht werden?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.dbHandler.deletePerson(pid)
            self.model.removeRow(self.tableView.selectedIndexes()[0].row())

    def export_personen(self):
        excelwriter.write_person_array_to_excel(
            "TalemDB_Personen.xlsx", self.dbHandler.getPersonen(), "Personenverzeichnis")

    def loadListBox(self, model):
        self.p_id_list = []
        for p in self.dbHandler.getPersonen():
            model.appendRow([QStandardItem(str(i)) for i in [p.anrede, p.vorname, p.nachname, p.adresse, p.plz, p.ort, p.land, p.email, p.telefon, int(self.dbHandler.isKunde(p.id)), int(self.dbHandler.isMitglied(p.id)), p.abonnement]])
            self.p_id_list.append(p.id)

    def insert(self):
        if(self.vorname_field.text() == "" or self.nachname_field.text() == ""):
            return

        p = Person(self.anrede_field.text(), self.vorname_field.text(), self.nachname_field.text(), self.adresse_field.text(),
            self.plz_field.text(), self.ort_field.text(), self.land_field.text(), self.email_field.text(), self.telefon_field.text())

        pid = self.dbHandler.insertPerson(
            p,
            int(self.kunden_check.checkState() == Qt.Checked),
            int(self.mitglieder_check.checkState() == Qt.Checked),
            int(self.abo_check.checkState() == Qt.Checked))
        self.window.destroy()
        # insert new entry into listbox
        self.model.appendRow(
            [QStandardItem(str(i)) for i in [
                p.anrede, p.vorname, p.nachname, p.adresse, p.plz, p.ort, p.land, p.email, p.telefon,
                int(self.kunden_check.checkState() == Qt.Checked),
                int(self.mitglieder_check.checkState() == Qt.Checked),
                int(self.abo_check.checkState() == Qt.Checked)
                ]
            ])
        self.p_id_list.append(pid)

    def update(self, item):
        row = item.row()
        if(self.model.item(row, 1).text() == "" or self.model.item(row, 2).text() == ""):
            return
        p = Person(self.model.item(row, 0).text(), self.model.item(row, 1).text(), self.model.item(row, 2).text(), self.model.item(row, 3).text(),
            self.model.item(row, 4).text(), self.model.item(row, 5).text(), self.model.item(row, 6).text(), self.model.item(row, 7).text(),
            self.model.item(row, 8).text())
        p.setID(self.p_id_list[row])
        self.dbHandler.updatePerson(p, int(self.model.item(row,9).text()), int(self.model.item(row,10).text()), int(self.model.item(row,11).text()))

    def neue_person(self):
        self.window = QWidget()
        self.window.show()
        self.window.setWindowTitle("TalemDB | Neue Person")
        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(QLabel("Personen-Details eingeben"), 0, 0)
        layout.addWidget(QLabel("Anrede"), 1, 0)
        layout.addWidget(QLabel("Vorname"), 2, 0)
        layout.addWidget(QLabel("Nachname"), 3, 0)
        layout.addWidget(QLabel("Adresse"), 4, 0)
        layout.addWidget(QLabel("PLZ"), 5, 0)
        layout.addWidget(QLabel("Ort"), 6, 0)
        layout.addWidget(QLabel("Land"), 7, 0)
        layout.addWidget(QLabel("Email"), 8, 0)
        layout.addWidget(QLabel("Telefon"), 9, 0)

        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.window.setLayout(windowLayout)

        self.anrede_field = QLineEdit(self.window)
        layout.addWidget(self.anrede_field, 1, 1)
        self.vorname_field = QLineEdit(self.window)
        layout.addWidget(self.vorname_field, 2, 1)
        self.nachname_field = QLineEdit(self.window)
        layout.addWidget(self.nachname_field, 3, 1)
        self.adresse_field = QLineEdit(self.window)
        layout.addWidget(self.adresse_field, 4, 1)
        self.plz_field = QLineEdit(self.window)
        layout.addWidget(self.plz_field, 5, 1)
        self.ort_field = QLineEdit(self.window)
        layout.addWidget(self.ort_field, 6, 1)
        self.land_field = QLineEdit(self.window)
        layout.addWidget(self.land_field, 7, 1)
        self.email_field = QLineEdit(self.window)
        layout.addWidget(self.email_field, 8, 1)
        self.telefon_field = QLineEdit(self.window)
        layout.addWidget(self.telefon_field, 9, 1)

        self.kunden_check = QCheckBox("Kunde",self.window)
        layout.addWidget(self.kunden_check, 10, 0)

        self.mitglieder_check = QCheckBox("Mitglied",self.window)
        layout.addWidget(self.mitglieder_check, 11, 0)

        self.abo_check = QCheckBox("Abonnement",self.window)
        layout.addWidget(self.abo_check, 12, 0)

        button = QPushButton("Hinzufügen",self.window)
        layout.addWidget(button, 13, 0)
        button.clicked.connect(self.insert)

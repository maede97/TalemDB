from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import config

class MitgliederWindow:
    def __init__(self, master, dbHandler):
        self.master = master
        self.frame = QWidget()

        self.frame.show()

        self.dbHandler = dbHandler

        self.frame.setWindowTitle("TalemDB | Mitglieder")
        
        # TODO set icon

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(QLabel("Mitglieder", self.frame), 1, 0)

        tableview = QTableView(self.frame)
        layout.addWidget(tableview, 2, 0)
        model = QStandardItemModel(self.frame)
        tableview.setModel(model)
        tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        model.setHorizontalHeaderLabels(['Vorname', 'Nachname', 'Adresse', 'PLZ', 'Ort'])
        self.loadListBox(model)
        
        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.frame.setLayout(windowLayout)

    def destroy(self,e=None):
        self.frame.destroy()

    def loadListBox(self, model):
        self.p_id_list = []

        for p in self.dbHandler.getMitglieder():
            model.appendRow([QStandardItem(str(i)) for i in [p.vorname, p.nachname, p.adresse, p.plz, p.ort]])
            self.p_id_list.append(p.id)
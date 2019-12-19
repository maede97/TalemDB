from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
import config

class MitgliederWindow(QWidget):
    def __init__(self, master, dbHandler):
        super().__init__()
        self.master = master

        self.show()

        self.dbHandler = dbHandler

        self.setWindowTitle("TalemDB | Mitglieder")
        
        # TODO set icon

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(QLabel("Mitglieder", self), 1, 0)

        tableview = QTableView(self)
        layout.addWidget(tableview, 2, 0)
        model = QStandardItemModel(self)
        tableview.setModel(model)
        tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        model.setHorizontalHeaderLabels(['Vorname', 'Nachname', 'Adresse', 'PLZ', 'Ort'])
        self.loadListBox(model)
        
        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.setLayout(windowLayout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.destroy()

    def loadListBox(self, model):
        self.p_id_list = []

        for p in self.dbHandler.getMitglieder():
            model.appendRow([QStandardItem(str(i)) for i in [p.vorname, p.nachname, p.adresse, p.plz, p.ort]])
            self.p_id_list.append(p.id)
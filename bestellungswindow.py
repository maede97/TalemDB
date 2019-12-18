from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import excelwriter
import config

class BestellungsWindow:
    def __init__(self, master, dbHandler):
        self.master = master
        self.frame = QWidget()
        self.frame.show()
        self.dbHandler = dbHandler

        self.frame.setWindowTitle("TalemDB | Bestellungen")
        
        # TODO Icon

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(QLabel("Bestellungen", self.frame), 1, 0)

        tableview = QTableView(self.frame)
        layout.addWidget(tableview, 2, 0)
        self.model = QStandardItemModel(self.frame)
        tableview.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Vorname', 'Nachname', 'Dalo', 'Star', 'Dachi', 'Sonstiges'])
        self.fillTable(self.model)
        for row in range(0, self.model.rowCount()):
            self.model.item(row,0).setFlags(Qt.ItemIsEnabled)
            self.model.item(row,1).setFlags(Qt.ItemIsEnabled)
        self.model.itemChanged.connect(self.update)

        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.frame.setLayout(windowLayout)

        # TODO bind escape

    def fillTable(self, model):
        self.p_id_list = []
        pers = self.dbHandler.getPersonen()
        # create header
        for i, p in enumerate(pers):
            best = self.dbHandler.getBestellungenById(p.id)
            self.p_id_list.append(p.id)
            model.appendRow([QStandardItem(str(j)) for j in [p.vorname, p.nachname, best[0], best[1], best[2], best[3]]])

    def update(self, item):
        row = item.row()
        # TODO: check for empty
        self.dbHandler.updateBestellungen(self.p_id_list[row], self.model.item(row, 2).text(), self.model.item(row, 3).text(), self.model.item(row, 4).text(), self.model.item(row, 5).text())
        self.logger.info("Bestellung aktualisiert " + str(self.p_id_list[row]))

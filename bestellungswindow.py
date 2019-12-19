from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
import excelwriter
import config

class BestellungsWindow(QWidget):
    def __init__(self, master, dbHandler):
        super().__init__()
        self.master = master
        self.show()
        self.dbHandler = dbHandler

        self.setWindowTitle("TalemDB | Bestellungen")
        
        self.setWindowIcon(QIcon('logo.png'))

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(QLabel("Bestellungen", self), 1, 0)

        tableview = QTableView(self)
        layout.addWidget(tableview, 2, 0)
        self.model = QStandardItemModel(self)
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
        self.setLayout(windowLayout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.destroy()

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
        self.dbHandler.updateBestellungen(self.p_id_list[row], self.model.item(row, 2).text(), self.model.item(row, 3).text(), self.model.item(row, 4).text(), self.model.item(row, 5).text())
        self.logger.info("Bestellung aktualisiert " + str(self.p_id_list[row]))

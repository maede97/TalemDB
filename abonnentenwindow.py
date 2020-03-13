from bestellungswindow import BestellungsWindow
from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
import excelwriter
import config

class AbonnentenWindow(QWidget):
    def __init__(self, master, dbHandler):
        super().__init__()
        self.master = master
        self.showMaximized()
        self.dbHandler = dbHandler

        self.setWindowTitle("TalemDB | Abonnenten")
        
        self.setWindowIcon(QIcon('logo.png'))

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        self.titleLabel = QLabel("Abonnenten", self)

        layout.addWidget(self.titleLabel, 1, 0)

        self.tableView = QTableView(self)
        layout.addWidget(self.tableView, 2, 0)
        self.model = QStandardItemModel(self)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Vorname', 'Nachname', 'Dalo', 'Star', 'Dachi', 'Sonstiges', 'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
        self.fillTable(self.model)
        self.tableView.setSortingEnabled(True)
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
        try:
            self.p_id_list = []
            pers = self.dbHandler.getPersonen('WHERE abonnement=1')
            # create header
            for i, p in enumerate(pers):
                best = self.dbHandler.getBestellungenById(p.id)
                bezahlt = self.dbHandler.getBezahlt(p.id)
                self.p_id_list.append(p.id)
                curr = [p.vorname, p.nachname, best[0], best[1], best[2], best[3]]
                row = [QStandardItem(str(j)) for j in curr]
                for j in bezahlt:
                    item = QStandardItem("Ja" if j else "Nein")
                    if j:
                        item.setBackground(QBrush(QColor("green")))
                    else:
                        item.setBackground(QBrush(QColor("red")))
                    #curr.append("ja" if j else "nein")
                    row.append(item)
                model.appendRow(row)
        except Exception as e:
            self.master.logger.error("abowindow: fillTable")
            self.master.logger.error(str(e))

    def update(self, item):
        row = item.row()
        pid = self.p_id_list[row]
        strings = [self.model.item(row, i).text() for i in range(6,18)]
        bez = []
        for i,s in enumerate(strings):
            if s.lower() == "ja":
                self.model.item(row, i+6).setBackground(QBrush(QColor("green")))
                bez.append(True)
            elif s.lower() == "nein":
                self.model.item(row, i+6).setBackground(QBrush(QColor("red")))
                bez.append(False)
            else:
                return # error...
        self.dbHandler.setBezahlt(pid, bez)
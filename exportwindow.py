from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
import excelwriter
import config
#
# selectionBehavior to QAbstractItemView::SelectRows
class ExportWindow(QWidget):
    def __init__(self, master, dbHandler):
        super().__init__()
        self.master = master
        self.show()
        # TODO: Icon
        self.dbHandler = dbHandler

        self.setWindowTitle("TalemDB | Export")

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(QLabel("Export", self), 1, 0)
        layout.addWidget(QLabel("Wähle alle Personen aus, die du exportieren möchtest.", self), 2, 0)


        self.tableView = QTableView(self)
        self.model = QStandardItemModel(self)
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.model.setHorizontalHeaderLabels(['Vorname', 'Nachname', 'Adresse', 'PLZ', 'Ort'])
        
        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.setLayout(windowLayout)

        layout.addWidget(QLabel("Dateiname nach dem Export (ohne .xlsx)", self), 3, 0)
        self.filename = QLineEdit("Personen_Export", self)
        layout.addWidget(self.filename, 4, 0)

        button = QPushButton("Personen Exportieren")
        button.clicked.connect(self.export_personen)
        layout.addWidget(button, 5, 0)

        button = QPushButton("Alle auswählen")
        button.clicked.connect(self.tableView.selectAll)
        layout.addWidget(button, 6, 0)

        button = QPushButton("Keine auswählen")
        button.clicked.connect(self.tableView.clearSelection)
        layout.addWidget(button, 7, 0)

        button = QPushButton("Kunden auswählen")
        button.clicked.connect(self.selectKunden)
        layout.addWidget(button, 8, 0)

        button = QPushButton("Mitglieder auswählen")
        button.clicked.connect(self.selectMitglieder)
        layout.addWidget(button, 9, 0)

        layout.addWidget(self.tableView, 10, 0)

        self.loadListBox(self.model)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.destroy()

    def selectKunden(self):
        self.tableView.clearSelection()
        kunden = self.dbHandler.getKunden()
        kunden_ids = [k.id for k in kunden]
        for i in range(len(self.p_id_list)):
            if self.p_id_list[i] in kunden_ids:
                self.tableView.selectRow(i)

    def selectMitglieder(self):
        self.tableView.clearSelection()
        mitglieder = self.dbHandler.getMitglieder()
        mitglieder_ids = [m.id for m in mitglieder]
        for i in range(len(self.p_id_list)):
            if self.p_id_list[i] in mitglieder_ids:
                self.tableView.selectRow(i)

    def export_personen(self):
        if(self.filename.text() == ""):
            return
        ids = list(set([self.p_id_list[i.row()] for i in self.tableView.selectedIndexes()]))
        personen = []
        for id in ids:
            personen.append(self.dbHandler.getPersonByID(id))
        if excelwriter.write_person_array_to_excel(self.filename.text() + ".xlsx", personen, "Personenverzeichnis"):
            self.master.logger.info("Export done " + self.filename.text())
        
    def loadListBox(self, model):
        self.p_id_list = []
        for p in self.dbHandler.getPersonen():
            model.appendRow([QStandardItem(str(i)) for i in [p.vorname, p.nachname, p.adresse, p.plz, p.ort]])
            self.p_id_list.append(p.id)
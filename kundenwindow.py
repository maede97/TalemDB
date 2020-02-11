from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
import config

class KundenWindow(QWidget):
    def __init__(self, master, dbHandler):
        super().__init__()
        self.master = master

        self.showMaximized()

        self.dbHandler = dbHandler

        self.setWindowTitle("TalemDB | Kunden")
        
        self.setWindowIcon(QIcon('logo.png'))

        horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        temp = QPushButton('Mailadressen kopieren', self)
        temp.clicked.connect(self.sendEmail)        
        layout.addWidget(temp, 1,0)

        layout.addWidget(QLabel("Kunden", self), 2, 0)

        tableview = QTableView(self)
        layout.addWidget(tableview, 3, 0)
        model = QStandardItemModel(self)
        tableview.setModel(model)
        tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        model.setHorizontalHeaderLabels(['Vorname', 'Nachname', 'Adresse', 'PLZ', 'Ort'])
        self.loadListBox(model)
        
        horizontalGroupBox.setLayout(layout)
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        self.setLayout(windowLayout)

    def sendEmail(self):
        """ opens email client to send email to all persons here"""
        emails = []
        for p in self.dbHandler.getKunden():
            # simple check if email even exists
            if('@' in p.email):
                emails.append(p.email)
            else:
                QMessageBox.warning(self, "Email nicht vollständig","Die Email-Adresse von " + p.vorname + " " + p.nachname + " existiert nicht.\nDas heisst, kein @-Zeichen wurde darin gefunden.")
        clip = QGuiApplication.clipboard()
        clip.setText(";\n".join(emails))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.destroy()

    def loadListBox(self, model):
        try:
            self.p_id_list = []

            for p in self.dbHandler.getKunden():
                model.appendRow([QStandardItem(str(i)) for i in [p.vorname, p.nachname, p.adresse, p.plz, p.ort]])
                self.p_id_list.append(p.id)
        except:
            self.master.logger.error("kundenwindow: loadListBox")

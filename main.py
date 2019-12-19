from person import Person
from database import DataBase
import sys
import os

# different windows
from personenwindow import PersonenWindow
from mitgliederwindow import MitgliederWindow
from kundenwindow import KundenWindow
from exportwindow import ExportWindow
from bestellungswindow import BestellungsWindow

# varia
import updatechecker
import config

# GUI stuff
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import Qt

from logger import Logger

class MainApplication(QMainWindow):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.frame = QWidget(self) # set frame to hold all content

        # TODO icon
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(os.path.join(scriptDir,'icon.png')))

        self.logger.info("MainApplication started")

        self.setWindowTitle("TalemDB")
        self.setGeometry(100,100,320,300)
        self.frame.setGeometry(0,20,320,200)

        # set up a layout
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        
        # Add Main buttons
        button = QPushButton("Personen", self)
        button.setToolTip("Zeige Personen")
        button.clicked.connect(self.showPersonen)
        layout.addWidget(button,0,0)

        button = QPushButton("Mitglieder", self)
        button.setToolTip("Zeige Mitglieder")
        button.clicked.connect(self.showMitglieder)
        layout.addWidget(button,1,0)

        button = QPushButton("Kunden", self)
        button.setToolTip("Zeige Kunden")
        button.clicked.connect(self.showKunden)
        layout.addWidget(button,2,0)

        button = QPushButton("Export", self)
        button.setToolTip("Exportieren")
        button.clicked.connect(self.showExport)
        layout.addWidget(button,3,0)

        button = QPushButton("Bestellungen", self)
        button.setToolTip("Zeige Bestellungen")
        button.clicked.connect(self.showBestellungen)
        layout.addWidget(button,4,0)

        self.statusBar().showMessage('Program geladen.')
        
        self.horizontalGroupBox.setLayout(layout)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.frame.setLayout(windowLayout)        

        self.addMenubar()

        self.dbHandler = DataBase(self.logger)

        self.papp = None
        self.mapp = None
        self.kapp = None
        self.eapp = None
        self.bapp = None

        self.popupsql = None

        self.logger.info("MainApplication __init__ done")

        # Show the GUI
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            self.showPersonen()
        elif event.key() == Qt.Key_E:
            self.showExport()
        elif event.key() == Qt.Key_M:
            self.showMitglieder()
        elif event.key() == Qt.Key_K:
            self.showKunden()
        elif event.key() == Qt.Key_B:
            self.showBestellungen()
        elif event.key() == Qt.Key_Escape:
            qapp.quit()

    def donothing(self):
        self.logger.info("main donothing")
        pass

    def sqlPopup(self):
        self.popupsql = QWidget()
        self.popupsql.setWindowTitle("SQL ausführen")
        self.sql_horizontalGroupBox = QGroupBox()
        self.sql_layout = QGridLayout()
        self.sqlentry = QTextEdit(self.popupsql)
        self.sql_layout.addWidget(self.sqlentry,1,0)

        button = QPushButton("Ausführen",self.popupsql)
        button.clicked.connect(self.execSQLPrompt)
        self.sql_layout.addWidget(button, 2, 0)

        self.sql_horizontalGroupBox.setLayout(self.sql_layout)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.sql_horizontalGroupBox)
        self.popupsql.setLayout(windowLayout)

        self.popupsql.show()
        self.logger.info("main sqlPopup shown")
    
    def execSQLPrompt(self):
        ret = self.dbHandler.executeSQL(self.sqlentry.toPlainText())
        tableview = QTableView(self.popupsql)
        self.sql_layout.addWidget(tableview, 3, 0)
        model = QStandardItemModel(self.popupsql)
        tableview.setModel(model)
        tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for row in ret:
            model.appendRow([QStandardItem(str(i)) for i in row])
        self.logger.info("main execSQLPrompt done")

        # example for clicker
    #     self.table.doubleClicked.connect(self.on_click)
 
    # def on_click(self, signal):
    #     row = signal.row()  # RETRIEVES ROW OF CELL THAT WAS DOUBLE CLICKED
    #     column = signal.column()  # RETRIEVES COLUMN OF CELL THAT WAS DOUBLE CLICKED
    #     cell_dict = self.model.itemData(signal)  # RETURNS DICT VALUE OF SIGNAL
    #     cell_value = cell_dict.get(0)  # RETRIEVE VALUE FROM DICT
 
    #     index = signal.sibling(row, 0)
    #     index_dict = self.model.itemData(index)
    #     index_value = index_dict.get(0)
    #     print(
    #         'Row {}, Column {} clicked - value: {}\nColumn 1 contents: {}'.format(row, column, cell_value, index_value))

    def addMenubar(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&Datei')
        runSQL = QAction(QIcon('logo.png'), 'SQL ausführen', self)
        runSQL.setStatusTip('SQL ausführen') # wird automatisch in status bar angezeigt!
        runSQL.triggered.connect(self.sqlPopup)
        filemenu.addAction(runSQL)

        exitAct = QAction(QIcon('.'), 'Beenden', self)        
        exitAct.setStatusTip('Applikation beenden')
        exitAct.triggered.connect(qApp.quit)
        filemenu.addAction(exitAct) 
        
        windowmenu = menubar.addMenu('&Fenster')

        temp = QAction('Personen',self)
        temp.triggered.connect(self.showPersonen)
        windowmenu.addAction(temp)

        temp = QAction('Kunden',self)
        temp.triggered.connect(self.showKunden)
        windowmenu.addAction(temp)

        temp = QAction('Mitglieder',self)
        temp.triggered.connect(self.showMitglieder)
        windowmenu.addAction(temp)

        temp = QAction('Bestellungen',self)
        temp.triggered.connect(self.showBestellungen)
        windowmenu.addAction(temp)

        temp = QAction('Rechnungen',self)
        temp.setStatusTip("Noch nicht verfügbar")
        windowmenu.addAction(temp)

        helpmenu = menubar.addMenu('Hilfe')

        temp = QAction('Hilfe',self)
        temp.triggered.connect(self.donothing)
        helpmenu.addAction(temp)

        temp = QAction('Über',self)
        temp.triggered.connect(self.donothing)
        helpmenu.addAction(temp)

        temp = QAction('Updates suchen',self)
        temp.triggered.connect(self.checkUpdates)
        helpmenu.addAction(temp)

        self.logger.info("main addMenubar done")

    def checkUpdates(self):
        self.setStatusTip("Stelle Verbindung mit Server her...")
        self.update()

        ret = updatechecker.check_for_updates()
        if(ret == None):
            self.setStatusTip("Ein Fehler ist aufgetreten.")

        elif(ret):
            print("No update was found")
            self.setStatusTip("Keine Updates gefunden.")
        else:
            self.setStatusTip("Das Update wird automatisch heruntergeladen.")
            self.update()
            ret = updatechecker.download_and_export_updates()
            if(ret):
                self.setStatusTip("Erfolgreich heruntergeladen. Bitte starte das Programm aus dem neuen Ordner neu.")
            else:
                self.setStatusTip("Ein Fehler ist aufgetreten.")
            self.logger.info("main downloadUpdates done")
        self.logger.info("main checkUpdates done")

    @pyqtSlot()
    def showBestellungen(self):
        if(not self.bapp):
            self.bapp = BestellungsWindow(self, self.dbHandler)
        else:
            self.bapp.destroy()
            self.bapp = BestellungsWindow(self, self.dbHandler)
        self.logger.info("main showBestellungen done")

    @pyqtSlot()
    def showExport(self):
        if(not self.eapp):
            self.eapp = ExportWindow(self, self.dbHandler)
        else:
            self.eapp.destroy()
            self.eapp = ExportWindow(self, self.dbHandler)
        self.logger.info("main showExport done")

    @pyqtSlot()
    def showPersonen(self):
        if(not self.papp):
            self.papp = PersonenWindow(self, self.dbHandler)
            pass
        else:
            self.papp.destroy()
            self.papp = PersonenWindow(self, self.dbHandler)
        self.logger.info("main showPersonen done")

    @pyqtSlot()
    def showKunden(self):
        if(not self.kapp):
            self.kapp = KundenWindow(self, self.dbHandler)
        else:
            self.kapp.destroy()
            self.kapp = KundenWindow(self, self.dbHandler)
        self.logger.info("main showKunden done")

    @pyqtSlot()
    def showMitglieder(self):
        if(not self.mapp):
            self.mapp = MitgliederWindow(self, self.dbHandler)
        else:
            self.mapp.destroy()
            self.mapp = MitgliederWindow(self, self.dbHandler)
        self.logger.info("main showMitglieder done")

if __name__ == "__main__":
    logger = Logger(config.LOGGER_FILE, False) # turn off logger
    app = QApplication(sys.argv)
    ex = MainApplication(logger)
    sys.exit(app.exec_())
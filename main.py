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
from abonnentenwindow import AbonnentenWindow

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
    """
    Main Window for TalemDB
    """
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

        self.frame = QWidget() # set frame to hold all content
        self.setCentralWidget(self.frame)

        self.setWindowIcon(QIcon('logo.png'))

        self.logger.info("MainApplication started")

        self.setWindowTitle("TalemDB")
        self.setGeometry(100,100,370,520)

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

        button = QPushButton("Abonennten", self)
        button.setToolTip("Zeige Abonennten")
        button.clicked.connect(self.showAbonnenten)
        layout.addWidget(button,3,0)

        button = QPushButton("Export", self)
        button.setToolTip("Exportieren")
        button.clicked.connect(self.showExport)
        layout.addWidget(button,4,0)

        button = QPushButton("Bestellungen", self)
        button.setToolTip("Zeige Bestellungen")
        button.clicked.connect(self.showBestellungen)
        layout.addWidget(button,5,0)

        self.statusBar().showMessage('Program geladen.')
        
        self.horizontalGroupBox.setLayout(layout)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.frame.setLayout(windowLayout)        

        self.addMenubar()

        self.dbHandler = DataBase(self.logger)

        layout.addWidget(QLabel("Aufgaben",self.frame), 6, 0)
        layout.addWidget(self.showAufgaben(), 7, 0)

        self.papp = None
        self.mapp = None
        self.kapp = None
        self.eapp = None
        self.bapp = None
        self.aapp = None

        self.popupsql = None

        self.logger.info("MainApplication __init__ done")

        # Show the GUI
        self.show() # others are maximised, however this is not
    
    def showAufgaben(self):
        """
        Create a QTableView to show all tasks to do

        Retuns
        ------
        QTableView holding all tasks inside it's model

        """
        try:
            self.aufgabe_id_list = []
            tableview = QTableView(self.frame)
            model = QStandardItemModel(self.frame)
            tableview.setModel(model)
            tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
            model.setHorizontalHeaderLabels(["Beschreib","Zeitpunkt"])
            for a in self.dbHandler.getAufgaben():
                model.appendRow([QStandardItem(str(i)) for i in a[1:]])
                self.aufgabe_id_list.append(a[0])
            return tableview
        except:
            self.logger.error("showAufgaben")

    def keyPressEvent(self, event):
        """
        Handle key press event
        
        Parameters
        ----------
        event : QEvent
            Event of key press
        """
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
        elif event.key() == Qt.Key_A:
            self.showAbonnenten()
        elif event.key() == Qt.Key_Escape:
            qApp.quit()

    def sqlPopup(self):
        """
        Show a popup to enter SQL code
        """
        self.popupsql = QWidget()
        self.popupsql.setWindowTitle("SQL ausführen")
        self.popupsql.setWindowIcon(QIcon('logo.png'))
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
        """
        Execute the entered SQL command
        
        Requires
        --------
        sqlPopup to be called, for self.sqlentry to exist
        """
        try:
            ret = self.dbHandler.executeSQL(self.sqlentry.toPlainText())
            tableview = QTableView(self.popupsql)
            self.sql_layout.addWidget(tableview, 3, 0)
            model = QStandardItemModel(self.popupsql)
            tableview.setModel(model)
            tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
            for row in ret:
                model.appendRow([QStandardItem(str(i)) for i in row])
            self.logger.info("main execSQLPrompt done")
        except:
            pass

    def addMenubar(self):
        """
        Add a menubar to the main window
        """
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

        temp = QAction('Abonnenten', self)
        temp.triggered.connect(self.showAbonnenten)
        windowmenu.addAction(temp)

        temp = QAction('Rechnungen',self)
        temp.setStatusTip("Noch nicht verfügbar")
        windowmenu.addAction(temp)

        helpmenu = menubar.addMenu('Hilfe')

        temp = QAction('Hilfe',self)
        #temp.triggered.connect(self.donothing)
        helpmenu.addAction(temp)

        temp = QAction('Über',self)
        #temp.triggered.connect(self.donothing)
        helpmenu.addAction(temp)

        temp = QAction('Updates suchen',self)
        temp.triggered.connect(self.checkUpdates)
        helpmenu.addAction(temp)

        self.logger.info("main addMenubar done")

    def checkUpdates(self):
        """
        Checks for updates
        """
        try:
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
        except:
            self.logger.error("UpdateCheck: error")

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

    @pyqtSlot()
    def showAbonnenten(self):
        if(not self.aapp):
            self.aapp = AbonnentenWindow(self, self.dbHandler)
        else:
            self.aapp.destroy()
            self.aapp = AbonnentenWindow(self, self.dbHandler)
        self.logger.info("main showAbonnenten done")

if __name__ == "__main__":
    logger = Logger(config.LOGGER_FILE, True)
    app = QApplication(sys.argv)
    ex = MainApplication(logger)
    sys.exit(app.exec_())
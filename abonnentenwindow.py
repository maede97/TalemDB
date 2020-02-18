from bestellungswindow import BestellungsWindow
from person import Person
from database import DataBase
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
import excelwriter
import config

class AbonnentenWindow(BestellungsWindow):
    def __init__(self, master, dbHandler):
        super().__init__(master, dbHandler)
        self.setWindowTitle("TalemDB | Abonnenten")
        self.titleLabel.setText("Abonnenten")

    def fillTable(self, model):
        try:
            self.p_id_list = []
            pers = self.dbHandler.getPersonen('WHERE abonnement=1')
            # create header
            for i, p in enumerate(pers):
                best = self.dbHandler.getBestellungenById(p.id)
                self.p_id_list.append(p.id)
                model.appendRow([QStandardItem(str(j)) for j in [p.vorname, p.nachname, best[0], best[1], best[2], best[3]]])
        except Exception as e:
            self.master.logger.error("abowindow: fillTable")
            self.master.logger.error(str(e))

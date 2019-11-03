# write to excel:
# https://www.geeksforgeeks.org/python-simple-registration-form-using-tkinter/

from person import Person
from database import DataBase
import tkinter as tk
from personenwindow import PersonenWindow
from mitgliederwindow import MitgliederWindow
from kundenwindow import KundenWindow
from exportwindow import ExportWindow
from bestellungswindow import BestellungsWindow
import updatechecker

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.parent.title("TalemDB")

        self.addMenubar()

        self.parent.geometry("500x400")

        self.dbHandler = DataBase()

        tk.Button(self, text="Personen", command=self.showPersonen).pack()
        tk.Button(self, text="Mitglieder", command=self.showMitglieder).pack()
        tk.Button(self, text="Kunden", command=self.showKunden).pack()
        tk.Button(self, text="Export", command=self.showExport).pack()
        tk.Button(self, text="Bestellungen",
                  command=self.showBestellungen).pack()
        tk.Button(self, text="Rechnungen (noch nicht verfügbar)").pack()
        self.papp = None
        self.mapp = None
        self.kapp = None
        self.eapp = None
        self.bapp = None

        self.parent.bind("<Escape>", self.close)

    def close(self, e=None):
        exit()

    def donothing(self):
        pass

    def addMenubar(self):
        menubar = tk.Menu(self.parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Beenden", command=self.parent.quit)
        menubar.add_cascade(label="Datei",menu=filemenu)
        
        windowmenu = tk.Menu(menubar, tearoff=0)
        windowmenu.add_command(label="Personen", command=self.showPersonen)
        windowmenu.add_command(label="Kunden", command=self.showKunden)
        windowmenu.add_command(label="Mitglieder", command=self.showMitglieder)
        windowmenu.add_command(label="Bestellungen",command=self.showBestellungen)
        windowmenu.add_command(label="Rechnungen (noch nicht verfügbar)")
        menubar.add_cascade(label="Fenster", menu=windowmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="Über...", command=self.donothing)
        helpmenu.add_command(label="Updates suchen", command=self.checkUpdates)
        menubar.add_cascade(label="Hilfe", menu=helpmenu)
        self.parent.config(menu=menubar)

    def downloadUpdates(self):
        ret = updatechecker.download_and_export_updates()
        if(ret):
            self.label.configure(
                text="Erfolgreich heruntergeladen.\nBitte starte das Program aus dem neuen Ordner neu.")
        else:
            self.label.configure(text="Ein Fehler ist aufgetreten.")

    def checkUpdates(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.geometry("500x300")
        self.newWindow.title("Updates suchen")
        self.label = tk.Label(
            self.newWindow, text="Stelle Verbindung mit Server her...")
        self.label.pack()

        ret = updatechecker.check_for_updates()
        if(ret == None):
            print("An error occured")
            self.label.configure(text="Ein Fehler ist aufgetreten.")
            tk.Button(self.newWindow, text="Schliessen",
                      command=self.newWindow.destroy).pack()

        elif(ret):
            print("No update was found")
            self.label.configure(text="Keine Updates gefunden.")
            tk.Button(self.newWindow, text="Schliessen",
                      command=self.newWindow.destroy).pack()

        else:
            tk.Button(self.newWindow, text="Update herunterladen",
                      command=self.downloadUpdates).pack()
            self.label.configure(
                text="Ein Update wurde gefunden.\nJetzt herunterladen?\nAchtung:\nDies kann eine Weile dauern!")
            tk.Button(self.newWindow, text="Schliessen",
                      command=self.newWindow.destroy).pack()
        self.newWindow.bind("<Escape>", lambda e: self.newWindow.destroy())

    def showBestellungen(self):
        self.newWindow = tk.Toplevel(self.parent)
        if(not self.bapp):
            self.bapp = BestellungsWindow(self.newWindow, self.dbHandler)
        else:
            self.bapp.destroy()
            self.bapp = BestellungsWindow(self.newWindow, self.dbHandler)

    def showExport(self):
        self.newWindow = tk.Toplevel(self.parent)
        if(not self.eapp):
            self.eapp = ExportWindow(self.newWindow, self.dbHandler)
        else:
            self.eapp.destroy()
            self.eapp = ExportWindow(self.newWindow, self.dbHandler)

    def showPersonen(self):
        self.newWindow = tk.Toplevel(self.parent)
        if(not self.papp):
            self.papp = PersonenWindow(self.newWindow, self.dbHandler)
        else:
            self.papp.destroy()
            self.papp = PersonenWindow(self.newWindow, self.dbHandler)

    def showKunden(self):
        self.newWindow = tk.Toplevel(self.parent)
        if(not self.kapp):
            self.kapp = KundenWindow(self.newWindow, self.dbHandler)
        else:
            self.kapp.destroy()
            self.kapp = KundenWindow(self.newWindow, self.dbHandler)

    def showMitglieder(self):
        self.newWindow = tk.Toplevel(self.parent)
        if(not self.mapp):
            self.mapp = MitgliederWindow(self.newWindow, self.dbHandler)
        else:
            self.mapp.destroy()
            self.mapp = MitgliederWindow(self.newWindow, self.dbHandler)


if __name__ == "__main__":
    root = tk.Tk()
    gui = MainApplication(root)
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='logo.png'))
    gui.pack(side="top", fill="both", expand=True)
    root.mainloop()

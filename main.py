# write to excel:
# https://www.geeksforgeeks.org/python-simple-registration-form-using-tkinter/

from person import Person
from database import DataBase
import tkinter as tk
from personenwindow import *
from mitgliederwindow import *
from kundenwindow import *
import updatechecker

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.parent.title("TalemDB")

        self.addMenubar()

        # tk.Button(self, text="Bla",width=25).pack()
        self.parent.geometry("500x400")

        self.dbHandler = DataBase()

        self.dbHandler.dropAll()
        self.dbHandler.insertTestData()

        self.papp = None
        self.mapp = None
        self.kapp = None

    def donothing(self):
        pass

    def addMenubar(self):
        menubar = tk.Menu(self.parent)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Personen",command=self.showPersonen)
        filemenu.add_command(label="Kunden",command=self.showKunden)
        filemenu.add_command(label="Mitglieder",command=self.showMitglieder)
        filemenu.add_separator()
        filemenu.add_command(label="Beenden",command=self.parent.quit)
        menubar.add_cascade(label="Datei", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="Über...", command=self.donothing)
        helpmenu.add_command(label="Updates suchen", command=updatechecker.check_for_updates)
        menubar.add_cascade(label="Hilfe", menu=helpmenu)
        self.parent.config(menu=menubar)
    def showPersonen(self):
        self.newWindow = tk.Toplevel(self.master)
        if(not self.papp):
            self.papp = PersonenWindow(self.newWindow, self.dbHandler)
        else:
            self.papp.destroy()
            self.papp = PersonenWindow(self.newWindow, self.dbHandler)
    def showKunden(self):
        self.newWindow = tk.Toplevel(self.master)
        if(not self.kapp):
            self.kapp = KundenWindow(self.newWindow, self.dbHandler)
        else:
            self.kapp.destroy()
            self.kapp = KundenWindow(self.newWindow, self.dbHandler)
    def showMitglieder(self):
        self.newWindow = tk.Toplevel(self.master)
        if(not self.mapp):
            self.mapp = MitgliederWindow(self.newWindow, self.dbHandler)
        else:
            self.mapp.destroy()
            self.mapp = MitgliederWindow(self.newWindow, self.dbHandler)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MainApplication(root)
    gui.pack(side="top",fill="both",expand=True)
    root.mainloop()
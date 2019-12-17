from person import Person
from database import DataBase
import tkinter as tk
import excelwriter
import config

class ExportWindow:
    def __init__(self, master, dbHandler):
        self.master = master

        self.master.tk.call('wm', 'iconphoto', self.master._w, tk.PhotoImage(file='logo.ico'))

        self.dbHandler = dbHandler

        self.master.title("TalemDB | Export")
        self.master.geometry(config.WINDOW_SIZE)
        self.frame = tk.Frame(self.master)

        tk.Label(self.master, text="Wähle alle Personen aus,\ndie du exportieren möchtest.").pack()

        tk.Label(self.master,text="Dateiname nach dem Export (ohne .xlsx)").pack()
        self.filename = tk.Entry(self.master)
        self.filename.pack()
        self.filename.insert(0, "TalemDB_Export")
        tk.Button(self.master,text="Personen exportieren",width=25,command=self.export_personen).pack()

        tk.Label(self.master, text="Personen").pack()

        self.listNodes = tk.Listbox(self.frame, width=29, height=20, font=("Helvetica", 12), selectmode=tk.MULTIPLE)

        tk.Button(self.master,text="Alle auswählen",width=25,command=lambda: self.listNodes.selection_set(0, tk.END)).pack()
        tk.Button(self.master,text="Keine auswählen",width=25,command=lambda: self.listNodes.selection_clear(0, tk.END)).pack()
        tk.Button(self.master,text="Alle Kunden auswählen",width=25,command=self.selectKunden).pack()
        tk.Button(self.master,text="Alle Mitglieder auswählen",width=25,command=self.selectMitglieder).pack()

        self.listNodes.pack(side="left",fill="y")

        scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        scrollbar.config(command=self.listNodes.yview)
        scrollbar.pack(side="right",fill="y")

        self.listNodes.config(yscrollcommand=scrollbar.set)

        self.loadListBox()
        
        self.frame.pack()

        self.master.bind("<Escape>",self.destroy)
    def selectKunden(self):
        self.listNodes.selection_clear(0, tk.END)
        kunden = self.dbHandler.getKunden()
        kunden_ids = [k.id for k in kunden]
        for i in range(len(self.p_id_list)):
            if self.p_id_list[i] in kunden_ids:
                self.listNodes.selection_set(i)

    def selectMitglieder(self):
        self.listNodes.selection_clear(0, tk.END)
        mitglieder = self.dbHandler.getMitglieder()
        mitglieder_ids = [m.id for m in mitglieder]
        for i in range(len(self.p_id_list)):
            if self.p_id_list[i] in mitglieder_ids:
                self.listNodes.selection_set(i)

    def export_personen(self):
        if(self.filename.get() == ""):
            return
        ids = [self.p_id_list[idx] for idx in self.listNodes.curselection()]
        personen = []
        for id in ids:
            personen.append(self.dbHandler.getPersonByID(id))
        excelwriter.write_person_array_to_excel(self.filename.get() + ".xlsx", personen, "Personenverzeichnis")
        
    def destroy(self,e=None):

        
        self.master.destroy()

    def loadListBox(self):
        self.listNodes.delete(0, tk.END)
        self.p_id_list = []
        for p in self.dbHandler.getPersonen():
            self.listNodes.insert(tk.END, p.vorname + " " +p.nachname)
            self.p_id_list.append(p.id)
    def close_windows(self):
        self.master.destroy()
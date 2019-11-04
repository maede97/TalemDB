from person import Person
from database import DataBase
import tkinter as tk
import tkinter.messagebox as messagebox
import excelwriter
import config

class PersonenWindow:
    def __init__(self, master, dbHandler):
        self.master = master

        self.dbHandler = dbHandler

        self.master.title("TalemDB | Personen")
        self.master.geometry(config.WINDOW_SIZE)
        self.master.tk.call('wm', 'iconphoto', self.master._w,
                            tk.PhotoImage(file='logo.png'))
        self.frame = tk.Frame(self.master)

        #self.frame.rowconfigure(0, weight=1)

        tk.Button(self.master, text="Neue Person erfassen",
                  width=25, command=self.neue_person).grid(row=0,column=0)

        tk.Button(self.master, text="Personen exportieren",
                  width=25, command=self.export_personen).grid(row=1,column=0)

        tk.Label(self.master, text="Personen").grid(row=2,column=0)
        self.listNodes = tk.Listbox(self.frame, font=(
            "Helvetica", 12), selectmode=tk.SINGLE, height=25,width=50)
        self.listNodes.grid(row=3,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

        scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        scrollbar.config(command=self.listNodes.yview)
        scrollbar.grid(row=3,column=1,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.listNodes.bind('<Double-Button>', self.onSelect)

        self.listNodes.config(yscrollcommand=scrollbar.set)

        self.loadListBox()

        self.frame.grid()

        self.master.bind("<Escape>", self.destroy)

    def ask_delete_person(self, pid):
        p = self.dbHandler.getPersonByID(pid)

        msg = messagebox.askokcancel("Person löschen", "Soll die Person "+p.vorname +
                                     " "+p.nachname+" wirklich endgültig gelöscht werden?", icon='warning')
        if msg == True:
            self.dbHandler.deletePerson(pid)
            self.window.destroy()
            self.loadListBox()

    def export_personen(self):
        excelwriter.write_person_array_to_excel(
            "TalemDB_Personen.xlsx", self.dbHandler.getPersonen(), "Personenverzeichnis")

    def destroy(self, e=None):
        self.master.destroy()

    def onSelect(self, evt):
        w = evt.widget
        if(len(w.curselection()) > 0):
            index = int(w.curselection()[0])
            self.edit_person(self.p_id_list[index])

    def loadListBox(self):
        # delete all content from listbox
        self.listNodes.delete(0, tk.END)

        self.p_id_list = []

        for p in self.dbHandler.getPersonen():
            self.listNodes.insert(tk.END, p.vorname + " " + p.nachname)
            self.p_id_list.append(p.id)

    def close_windows(self):
        self.master.destroy()

    def insert(self):
        if(not self.__check_for_empty__()):
            return

        p = Person(self.anrede_field.get(), self.vorname_field.get(), self.nachname_field.get(), self.adresse_field.get(
        ), self.plz_field.get(), self.ort_field.get(), self.land_field.get(), self.email_field.get(), self.telefon_field.get())

        self.dbHandler.insertPerson(
            p, self.kunden_check_var.get(), self.mitglieder_check_var.get(), self.abo_check_var.get())
        self.window.destroy()
        self.loadListBox()

    def __check_for_empty__(self):
        if (self.vorname_field.get() == ""):
            self.vorname_field.focus_set()
            return False
        elif(self.nachname_field.get() == ""):
            self.nachname_field.focus_set()
            return False
        else:
            return True

    def update(self):
        if(not self.__check_for_empty__()):
            return
        p = Person(self.anrede_field.get(), self.vorname_field.get(), self.nachname_field.get(), self.adresse_field.get(
        ), self.plz_field.get(), self.ort_field.get(), self.land_field.get(), self.email_field.get(), self.telefon_field.get())
        p.setID(self.curr_id)
        self.dbHandler.updatePerson(
            p, self.kunden_check_var.get(), self.mitglieder_check_var.get(), self.abo_check_var.get())
        self.window.destroy()
        self.loadListBox()

    def edit_person(self, id):
        p = self.dbHandler.getPersonByID(id)
        self.curr_id = id
        self.window = tk.Toplevel(self.master)
        self.window.tk.call('wm', 'iconphoto', self.window._w,
                            tk.PhotoImage(file='logo.png'))

        heading = tk.Label(self.window, text="Person bearbeiten")
        anrede_lb = tk.Label(self.window, text="Anrede")
        vorname_lb = tk.Label(self.window, text="Vorname")
        nachname_lb = tk.Label(self.window, text="Nachname")
        adresse_lb = tk.Label(self.window, text="Adresse")
        plz_lb = tk.Label(self.window, text="PLZ")
        ort_lb = tk.Label(self.window, text="Ort")
        land_lb = tk.Label(self.window, text="Land")
        email_lb = tk.Label(self.window, text="Email")
        telefon_lb = tk.Label(self.window, text="Telefon")
        anrede_lb.grid(row=0, column=1)
        heading.grid(row=1, column=1)
        vorname_lb.grid(row=2, column=0)
        nachname_lb.grid(row=3, column=0)
        adresse_lb.grid(row=4, column=0)
        plz_lb.grid(row=5, column=0)
        ort_lb.grid(row=6, column=0)
        land_lb.grid(row=7, column=0)
        email_lb.grid(row=8, column=0)
        telefon_lb.grid(row=9, column=0)
        self.anrede_field = tk.Entry(self.window)
        self.anrede_field.insert(0, p.anrede)
        self.vorname_field = tk.Entry(self.window)
        self.vorname_field.insert(0, p.vorname)
        self.nachname_field = tk.Entry(self.window)
        self.nachname_field.insert(0, p.nachname)
        self.adresse_field = tk.Entry(self.window)
        self.adresse_field.insert(0, p.adresse)
        self.plz_field = tk.Entry(self.window)
        self.plz_field.insert(0, p.plz)
        self.ort_field = tk.Entry(self.window)
        self.ort_field.insert(0, p.ort)
        self.land_field = tk.Entry(self.window)
        self.land_field.insert(0, p.land)
        self.email_field = tk.Entry(self.window)
        self.email_field.insert(0, p.email)
        self.telefon_field = tk.Entry(self.window)
        self.telefon_field.insert(0, p.telefon)

        self.kunden_check_var = tk.BooleanVar(value=p.kunde)
        self.mitglieder_check_var = tk.BooleanVar(value=p.mitglied)
        self.kunden_check = tk.Checkbutton(
            self.window, text="Kunde", variable=self.kunden_check_var)
        self.mitglieder_check = tk.Checkbutton(
            self.window, text="Mitglied", variable=self.mitglieder_check_var)
        self.abo_check_var = tk.BooleanVar(value=p.abonnement)
        self.abo_check = tk.Checkbutton(
            self.window, text="Abonnement", variable=self.abo_check_var)

        self.anrede_field.grid(row=1, column=1, ipadx="100")
        self.vorname_field.grid(row=2, column=1, ipadx="100")
        self.nachname_field.grid(row=3, column=1, ipadx="100")
        self.adresse_field.grid(row=4, column=1, ipadx="100")
        self.plz_field.grid(row=5, column=1, ipadx="100")
        self.ort_field.grid(row=6, column=1, ipadx="100")
        self.land_field.grid(row=7, column=1, ipadx="100")
        self.email_field.grid(row=8, column=1, ipadx="100")
        self.telefon_field.grid(row=9, column=1, ipadx="100")
        self.kunden_check.grid(row=10, column=1, ipadx="100")
        self.mitglieder_check.grid(row=11, column=1, ipadx="100")
        self.abo_check.grid(row=12, column=1, ipadx="100")

        submit = tk.Button(self.window, text="Speichern", command=self.update, bg="green", width=30)
        tk.Button(self.window, text="Person löschen",
                  command=lambda: self.ask_delete_person(id),bg="red", width=30).grid(row=13, column=0, columnspan=2)

        submit.grid(row=14, column=0, columnspan=2)

        self.vorname_field.focus_set()  # set focus to first field
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def neue_person(self):
        self.window = tk.Toplevel(self.master)
        self.window.tk.call('wm', 'iconphoto', self.window._w,
                            tk.PhotoImage(file='logo.png'))
        heading = tk.Label(self.window, text="Person bearbeiten")
        anrede_lb = tk.Label(self.window, text="Anrede")
        vorname_lb = tk.Label(self.window, text="Vorname")
        nachname_lb = tk.Label(self.window, text="Nachname")
        adresse_lb = tk.Label(self.window, text="Adresse")
        plz_lb = tk.Label(self.window, text="PLZ")
        ort_lb = tk.Label(self.window, text="Ort")
        land_lb = tk.Label(self.window, text="Land")
        email_lb = tk.Label(self.window, text="Email")
        telefon_lb = tk.Label(self.window, text="Telefon")
        heading.grid(row=0, column=1)
        anrede_lb.grid(row=1, column=0)
        vorname_lb.grid(row=2, column=0)
        nachname_lb.grid(row=3, column=0)
        adresse_lb.grid(row=4, column=0)
        plz_lb.grid(row=5, column=0)
        ort_lb.grid(row=6, column=0)
        land_lb.grid(row=7, column=0)
        email_lb.grid(row=8, column=0)
        telefon_lb.grid(row=9, column=0)

        self.anrede_field = tk.Entry(self.window)
        self.vorname_field = tk.Entry(self.window)
        self.nachname_field = tk.Entry(self.window)
        self.adresse_field = tk.Entry(self.window)
        self.plz_field = tk.Entry(self.window)
        self.ort_field = tk.Entry(self.window)
        self.land_field = tk.Entry(self.window)
        self.email_field = tk.Entry(self.window)
        self.telefon_field = tk.Entry(self.window)

        self.kunden_check_var = tk.BooleanVar()
        self.mitglieder_check_var = tk.BooleanVar()
        self.abo_check_var = tk.BooleanVar()
        self.kunden_check = tk.Checkbutton(
            self.window, text="Kunde", variable=self.kunden_check_var)
        self.mitglieder_check = tk.Checkbutton(
            self.window, text="Mitglied", variable=self.mitglieder_check_var)
        self.abo_check = tk.Checkbutton(self.window, text="Abonnement",variable=self.abo_check_var)

        self.anrede_field.grid(row=1, column=1, ipadx="100")
        self.vorname_field.grid(row=2, column=1, ipadx="100")
        self.nachname_field.grid(row=3, column=1, ipadx="100")
        self.adresse_field.grid(row=4, column=1, ipadx="100")
        self.plz_field.grid(row=5, column=1, ipadx="100")
        self.ort_field.grid(row=6, column=1, ipadx="100")
        self.land_field.grid(row=7, column=1, ipadx="100")
        self.email_field.grid(row=8, column=1, ipadx="100")
        self.telefon_field.grid(row=9, column=1, ipadx="100")
        self.kunden_check.grid(row=10, column=1, ipadx="100")
        self.mitglieder_check.grid(row=11, column=1, ipadx="100")
        self.abo_check.grid(row=12,column=1,ipadx="100")

        submit = tk.Button(self.window, text="Hinzufügen", command=self.insert)

        submit.grid(row=13, column=1)

        self.vorname_field.focus_set()  # set focus to first field
        self.window.bind("<Escape>", lambda e: self.window.destroy())

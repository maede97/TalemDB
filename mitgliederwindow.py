from person import Person
from database import DataBase
import tkinter as tk
import config

class MitgliederWindow:
    def __init__(self, master, dbHandler):
        self.master = master

        self.dbHandler = dbHandler

        self.master.title("TalemDB | Mitglieder")
        self.master.geometry(config.WINDOW_SIZE)
        self.master.tk.call('wm', 'iconphoto', self.master._w, tk.PhotoImage(file='logo.png'))
        self.frame = tk.Frame(self.master)

        tk.Label(self.master, text="Mitglieder").pack()
        self.listNodes = tk.Listbox(self.frame, font=(
            "Helvetica", 12), selectmode=tk.SINGLE, height=25,width=50)
        self.listNodes.pack(side="left",fill="y")

        scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        scrollbar.config(command=self.listNodes.yview)
        scrollbar.pack(side="right",fill="y")

        self.listNodes.config(yscrollcommand=scrollbar.set)

        self.loadListBox()
        
        self.frame.pack()
        self.master.bind("<Escape>",self.destroy)

    def destroy(self,e=None):
        self.master.destroy()

    def loadListBox(self):
        # delete all content from listbox
        self.listNodes.delete(0, tk.END)

        self.p_id_list = []

        for p in self.dbHandler.getMitglieder():
            self.listNodes.insert(tk.END, p.vorname + " " +p.nachname)
            self.p_id_list.append(p.id)
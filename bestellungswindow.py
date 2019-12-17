from person import Person
from database import DataBase
import tkinter as tk
import excelwriter
import config
import scrollable_frame


class BestellungsWindow:
    def __init__(self, master, dbHandler):
        self.master = master

        self.dbHandler = dbHandler

        self.master.title("TalemDB | Bestellungen")
        self.master.geometry(config.WINDOW_SIZE)
        self.master.tk.call('wm', 'iconphoto', self.master._w,
                            tk.PhotoImage(file='logo.png'))
        self.frame = scrollable_frame.VerticalScrolledFrame(
            self.master, height=int(config.WINDOW_SIZE.split("x")[1]))
        self.frame.pack()
        self.fillTable()

        self.master.bind("<Escape>", self.destroy)

    def destroy(self, e=None):
        self.master.destroy()

    def close_windows(self):
        self.master.destroy()

    def fillTable(self):
        pers = self.dbHandler.getPersonen()
        # create header
        tk.Label(self.frame.interior, text="Vorname").grid(row=0, column=0)
        tk.Label(self.frame.interior, text="Nachname").grid(row=0, column=1)
        tk.Label(self.frame.interior, text="Dalo").grid(row=0, column=2)
        tk.Label(self.frame.interior, text="Star").grid(row=0, column=3)
        tk.Label(self.frame.interior, text="Dachi").grid(row=0, column=4)
        tk.Label(self.frame.interior, text="Sonstiges").grid(row=0, column=5)

        for i, p in enumerate(pers):
            best = self.dbHandler.getBestellungenById(p.id)
            tk.Button(self.frame.interior, text=p.vorname, width=15,
                      command=lambda curr=p.id: self.showEditScreen(curr)).grid(row=i+1, column=0)
            tk.Label(self.frame.interior, text=p.nachname).grid(
                row=i+1, column=1)
            tk.Label(self.frame.interior, text=best[0]).grid(row=i+1, column=2)
            tk.Label(self.frame.interior, text=best[1]).grid(row=i+1, column=3)
            tk.Label(self.frame.interior, text=best[2]).grid(row=i+1, column=4)
            tk.Label(self.frame.interior, text=best[3]).grid(
                row=i+1, column=5)  # sonstiges

    def update(self):
        # check for empty
        self.dbHandler.updateBestellungen(
            self.curr_id, self.dalo_field.get(), self.star_field.get(), self.dachi_field.get(), self.sonstiges_field.get())
        self.window.destroy()
        self.frame.destroy()
        self.frame = scrollable_frame.VerticalScrolledFrame(
            self.master, height=700)
        self.frame.pack()
        self.fillTable()

    def showEditScreen(self, id):
        p = self.dbHandler.getPersonByID(id)
        best = self.dbHandler.getBestellungenById(id)
        # fill toplevel

        self.curr_id = id
        self.window = tk.Toplevel(self.master)
        self.window.tk.call('wm', 'iconphoto', self.window._w,
                            tk.PhotoImage(file='logo.png'))
        heading = tk.Label(self.window, text="Bestellungen bearbeiten")
        vorname_lb = tk.Label(self.window, text="Vorname")
        nachname_lb = tk.Label(self.window, text="Nachname")
        dalo_lb = tk.Label(self.window, text="Dalo")
        star_lb = tk.Label(self.window, text="Star")
        dachi_lb = tk.Label(self.window, text="Dachi")
        sonstiges_lb = tk.Label(self.window, text="Sonstiges")

        heading.grid(row=0, column=1)
        vorname_lb.grid(row=1, column=0)
        nachname_lb.grid(row=2, column=0)
        dalo_lb.grid(row=3, column=0)
        star_lb.grid(row=4, column=0)
        dachi_lb.grid(row=5, column=0)
        sonstiges_lb.grid(row=6, column=0)

        # add sonstiges

        self.vorname_field = tk.Label(self.window, text=p.vorname)
        self.nachname_field = tk.Label(self.window, text=p.nachname)
        self.dalo_field = tk.Entry(self.window)
        self.dalo_field.insert(0, best[0])
        self.star_field = tk.Entry(self.window)
        self.star_field.insert(0, best[1])
        self.dachi_field = tk.Entry(self.window)
        self.dachi_field.insert(0, best[2])
        self.sonstiges_field = tk.Entry(self.window)
        self.sonstiges_field.insert(0, best[3])

        self.vorname_field.grid(row=1, column=1, ipadx="100")
        self.nachname_field.grid(row=2, column=1, ipadx="100")
        self.dalo_field.grid(row=3, column=1, ipadx="100")
        self.star_field.grid(row=4, column=1, ipadx="100")
        self.dachi_field.grid(row=5, column=1, ipadx="100")
        self.sonstiges_field.grid(row=6, column=1, ipadx="100")

        submit = tk.Button(self.window, text="Speichern", command=self.update)

        submit.grid(row=11, column=1)

        self.dalo_field.focus_set()  # set focus to first field
        self.window.bind("<Escape>", lambda e: self.window.destroy())

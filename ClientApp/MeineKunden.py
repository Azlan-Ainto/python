
from pickle import FRAME
import tkinter as tk
from tkinter import messagebox, ttk
import json
import array
from collections import deque
from datetime import datetime


class Kunde:

    def __init_(self,kid, vorname, nachname, alter, geburtsdatum, beruf, gehalt):

        self.kid = kid
        self.vorname = vorname
        self.nachname = nachname
        self.alter = int(alter)
        self.geburtsdatum = geburtsdatum
        self.beruf = beruf
        self.gehalt = float(gehalt)
    
    def toDict(self):
        return self.__dict__

    @staticmethod
    def fromDict(data):

        return Kunde(**data)



class KundenApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Kunden Management Pro")
        self.root.geometry("400x700")

        self.kundenListe = []
        self.berufsSet = set()
        self.operations = deque()
        # Dictionary
        self.idMap = {}

        self.setupGui()

    def setupGui(self):

        fields = [("ID","id"),
                  ("Vorname", "vn"),
                  ("Nachname","nn"),
                  ("Alter","al"),
                  ("Geburtsdatum(JJJJ-MM-TT)","gb"),
                  ("Beruf","be"),
                  ("Gehalt", "ge")]
        self.entries = {}

        for labelText, key in fields:

            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)

            tk.Label(frame, text= labelText, width=20, anchor="w").pack(side="left")
            entry = tk.Entry(frame).pack(side="right", expand = True, fill="x")

            self.entries[key] = entry

        btnFrame = tk.Frame(self.root)
        btnFrame.pack(pady=10)

        tk.Button(btnFrame, text="hinzufügen", command=self.addKunde).grid(row=0, column=0, padx=5)
        tk.Button(btnFrame, text="Speichern(JSON)", command=self.saveToJson).grid(row=0, column=1, padx=5)
        tk.Button(btnFrame, text="Laden(JSON)", command=self.loadFromJson).grid(row=0, column=2, padx=5)
        tk.Button(btnFrame, text="Statistik(Array)", command=self.showStatistics).grid(row=0, column=3, padx=5)

        tk.Label(self.root, text="Operations-Log(Queue):").pack()
        self.logListbox = tk.Listbox(self.root, height)
        self.LogListbox.pack(fill="x"  , padx = 10)

                


if __name__ == "__main__":
     root = tk.Tk()
     app = KundenApp(root)
     root.mainloop()

    


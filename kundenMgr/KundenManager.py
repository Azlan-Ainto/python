import sqlite3
import tkinter as tk
from tkinter import ttk

#------------------------------------------------------------------
# Datenbank vorbereiten
#------------------------------------------------------------------

def initialisiere_Datenbank():

    conn = sqlite3.connect("kunden.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kunden (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vorname TEXT,
            nachname TEXT,
            email TEXT
        )
    """)

    # Pseudo-Daten einfügen, falls Tabelle leer ist
    cursor.execute("SELECT COUNT(*) FROM kunden")
    if cursor.fetchone()[0] == 0:
        daten = [
            ("Max", "Mustermann", "max@sample.com"),
            ("Erika", "Musterfrau", "erika@sample.com"),
            ("Hans", "Meier", "hans@sample.com")
        ]
        cursor.executemany(
            "INSERT INTO kunden (vorname, nachname, email) VALUES (?, ?, ?)",
            daten
        )
    conn.commit()
    conn.close()

#------------------------------------------------------------------
# Datensätze aus der Datenbank laden
#------------------------------------------------------------------

def lade_Daten():
    conn = sqlite3.connect("kunden.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, vorname, nachname, email FROM kunden")
    daten = cursor.fetchall()
    conn.close()
    return daten

#------------------------------------------------------------------
# GUI - Kundentabelle
#------------------------------------------------------------------

def main():

    root = tk.Tk()
    root.title("Kundenübersicht")
    

    # Tabelle - Spalten Überschrift
    columns = ("ID", "Vorname", "Nachname", "Email")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill=tk.BOTH, expand=True)

    # Daten einfügen
    for row in lade_Daten():
        tree.insert("", tk.END, values=row)

    root.mainloop()
#------------------------------------------------------------------
# Start
#------------------------------------------------------------------

if __name__ == "__main__":
    initialisiere_Datenbank()
    main()

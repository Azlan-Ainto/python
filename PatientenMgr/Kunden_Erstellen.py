import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql

# ----- Erstellt von Azlan Ainto am 19.02.2026 um 21.29 Uhr -----

# ----- Dieses Skript speichert Kundeninformationen in einer SQLite-Datenbank. -----


def kunde_speichern():

    # ---- Eingabedaten validieren ----
    name = entryName.get()
    alter = entryAlter.get()

    if not name or not alter:
        messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus!")
        return

    try:
        connection = sql.connect('customers.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customers(name, age) VALUES(?,?)",(name,alter))
        connection.commit()
        connection.close()

        #--- Eingabefelder zurücksetzen ---
        entryName.delete(0, tk.END)
        entryAlter.delete(0,tk.END)
        messagebox.showinfo("Erfolg", "Kunde wurde erfolgreich gespeichert!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:{e}")


#------ GUI ---------

fenster = tk.Tk()
fenster.title("Schritt 2: Kunden erstellen")
# ---- Position des Fensters mittig einstellen -------
window_width = 400
window_height = 300
screen_width = fenster.winfo_screenwidth()
screen_height = fenster.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
fenster.geometry(f"{window_width}x{window_height}+{x}+{y}")

# --- Eingabefelder und Labels ---

tk.Label(fenster, text="Name:").pack(pady=(10,0))
entryName = tk.Entry(fenster)
entryName.pack(pady=5)

tk.Label(fenster, text="Alter:").pack(pady=(10,0))
entryAlter = tk.Entry(fenster)
entryAlter.pack(pady=5)

SaveButton = tk.Button(fenster, text="Kunde speichern", command= kunde_speichern)
SaveButton.pack(pady=20)
fenster.mainloop()

    

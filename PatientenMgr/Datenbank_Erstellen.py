
import tkinter as tk
from tkinter import messagebox
import sqlite3


def create_database():

    connection = sqlite3.connect('customers.db')
    cursor = connection.cursor()

    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS customers(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL)
                ''')
    
    connection.commit()
    connection.close()
    messagebox.showinfo("Erfolg", "Datenbank und Tabelle wurden erfolgreich erstellt!")
# ..........................................................................................


# ---- GUI---------

root = tk.Tk()
root.title("Schritt 1:Datenbank Setup")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

#----- Setze die Größe des Fensters-----

window_width = 350
window_height = 150


#------Bildschirmgröße ermitteln-----------
screen_width = root.winfo_screenwidth()
screen_height =  root.winfo_screenheight()

#------Position des Fensters berechnen, um es in der Mitte zu platzieren------

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

label = tk.Label(root, text="Willkommen zum Tkinter & SQLite Tutorial!!", pady=10)
label.pack()

dbButton = tk.Button(root, text="Datenbank & Tabelle erstellen", command=create_database)
dbButton.pack(pady=20)

root.mainloop()


    

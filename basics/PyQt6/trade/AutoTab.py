
import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox)


from PyQt6.QtCore import Qt





DB_NAME = "personen.db"


class PersonenTabelle(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Personenverwaltung")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tabelle erstellen
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Vorname", "Nachname", "Geburtsdatum", "Telefon", "Beruf", "Gehalt"
        ])
        self.table.cellChanged.connect(self.auto_save)

        self.layout.addWidget(self.table)

        # Button: Neue Zeile
        btn_add = QPushButton("Neue Zeile hinzufügen")
        btn_add.clicked.connect(self.add_row)
        self.layout.addWidget(btn_add)

        # Datenbank vorbereiten
        self.init_db()
        self.load_data()

    # -----------------------------
    #
    # Datenbank initialisieren
    #
    # -----------------------------

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS personen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vorname TEXT,
                nachname TEXT,
                geburtsdatum TEXT,
                telefon TEXT,
                beruf TEXT,
                gehalt TEXT
            )
        """)
        conn.commit()
        conn.close()

    # -----------------------------
    #
    # Daten aus DB laden
    #
    # -----------------------------

    def load_data(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT vorname, nachname, geburtsdatum, telefon, beruf, gehalt FROM personen")
        rows = c.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    # -----------------------------
    #
    # Neue Zeile hinzufügen
    #
    # -----------------------------

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Leeren Datensatz in DB anlegen
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO personen (vorname, nachname, geburtsdatum, telefon, beruf, gehalt) VALUES ('','','','','','')")
        conn.commit()
        conn.close()

        self.load_data()

    # -----------------------------
    #
    # Automatisches Speichern
    #
    # -----------------------------

    def auto_save(self, row, col):

        # Werte aus der Tabelle lesen

        values = []
        for i in range(6):
            item = self.table.item(row, i)
            values.append(item.text() if item else "")

        # Datensatz aktualisieren

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # ID bestimmen (entspricht Tabellenzeile + 1)
        record_id = row + 1

        c.execute("""
            UPDATE personen SET
                vorname = ?, nachname = ?, geburtsdatum = ?, telefon = ?, beruf = ?, gehalt = ?
            WHERE id = ?
        """, (*values, record_id))

        conn.commit()
        conn.close()


# -----------------------------
#
# Hauptprogramm
#
# -----------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonenTabelle()
    window.resize(800, 400)
    window.show()
    sys.exit(app.exec())


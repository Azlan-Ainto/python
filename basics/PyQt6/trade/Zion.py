

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt


DB_NAME = "personen.db"


class PersonenFenster(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Personenverwaltung (QSqlTableModel)")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Datenbank verbinden
        self.init_db()

        # Modell erstellen
        self.model = QSqlTableModel()
        self.model.setTable("personen")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()

        # Spaltennamen setzen
        self.model.setHeaderData(1,  Qt.Orientation.Horizontal, "Vorname")
        self.model.setHeaderData(2,  Qt.Orientation.Horizontal, "Nachname")
        self.model.setHeaderData(3,  Qt.Orientation.Horizontal, "Geburtsdatum")
        self.model.setHeaderData(4,  Qt.Orientation.Horizontal, "Telefon")
        self.model.setHeaderData(5,  Qt.Orientation.Horizontal, "Beruf")
        self.model.setHeaderData(6,  Qt.Orientation.Horizontal, "Gehalt")

        # Tabelle anzeigen
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        # Button: Neue Zeile
        btn_add = QPushButton("Neue Zeile hinzufügen")
        btn_add.clicked.connect(self.add_row)
        layout.addWidget(btn_add)

    # -----------------------------------
    # Datenbank initialisieren
    # -----------------------------------

    def init_db(self):

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DB_NAME)
        if not db.open():
            raise Exception("Konnte Datenbank nicht öffnen")

        query = db.exec("""
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

    # -----------------------------------
    # Neue Zeile einfügen
    # -----------------------------------
    def add_row(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        # Leere Felder werden automatisch gespeichert (wegen OnFieldChange)


# -----------------------------------
# Hauptprogramm
# -----------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonenFenster()
    window.resize(900, 400)
    window.show()
    sys.exit(app.exec())


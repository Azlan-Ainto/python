
import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QStackedWidget, QLabel,
    QFormLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt


class DatabaseGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern SQL Database Manager")
        self.resize(1200, 720)  # 16:9 Format

        # Datenbank initialisieren
        self.init_db()

        # Dictionary für Tabellen-Seiten (für refresh_tables)
        self.table_pages = {}

        # Haupt-Widget und Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar (Navigation)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.currentRowChanged.connect(self.change_page)
        main_layout.addWidget(self.sidebar)

        # Stacked Widget (Inhaltsbereich)
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Seiten initialisieren
        self.setup_pages()
        self.apply_styling()

        # Tabellen initial laden
        self.refresh_tables()

    def init_db(self):
        """Erstellt die Tabellen in der SQLite Datenbank."""
        conn = sqlite3.connect("business.db")
        cursor = conn.cursor()

        # Tabelle für Kunden
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS kunden (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vorname TEXT,
                nachname TEXT,
                email TEXT,
                telefon TEXT
            )
            """
        )

        # Tabelle für Produkte
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS produkte (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artnr TEXT,
                name TEXT,
                preis REAL,
                lager INTEGER
            )
            """
        )

        # Beispiel-Tabellen für weitere Bereiche (minimal gehalten)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bestellungen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kunden_id INTEGER,
                produkt_id INTEGER,
                menge INTEGER,
                datum TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rechnungen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bestell_id INTEGER,
                betrag REAL,
                faellig TEXT,
                status TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lieferanten (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firmenname TEXT,
                ansprechpartner TEXT,
                email TEXT,
                telefon TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mitarbeiter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vorname TEXT,
                nachname TEXT,
                abteilung TEXT,
                position TEXT
            )
            """
        )

        conn.commit()
        conn.close()

    def save_to_db(self, table_name, input_widgets):
        """Extrahiert Text aus Widgets und führt SQL INSERT aus."""
        data = [w.text().strip() for w in input_widgets]

        if any(not d for d in data):  # Einfache Validierung
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen!")
            return

        try:
            conn = sqlite3.connect("business.db")
            cursor = conn.cursor()

            # Spalten je Tabelle (ohne id)
            columns_map = {
                "kunden": ["vorname", "nachname", "email", "telefon"],
                "produkte": ["artnr", "name", "preis", "lager"],
                "bestellungen": ["kunden_id", "produkt_id", "menge", "datum"],
                "rechnungen": ["bestell_id", "betrag", "faellig", "status"],
                "lieferanten": ["firmenname", "ansprechpartner", "email", "telefon"],
                "mitarbeiter": ["vorname", "nachname", "abteilung", "position"],
            }

            columns = columns_map.get(table_name)
            if not columns or len(columns) != len(data):
                raise ValueError("Spaltenanzahl passt nicht zu den Eingabedaten.")

            columns_sql = ", ".join(columns)
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table_name} ({columns_sql}) VALUES ({placeholders})"

            cursor.execute(query, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Erfolg", f"Daten erfolgreich in '{table_name}' gespeichert!")

            # Felder leeren
            for w in input_widgets:
                w.clear()

            # Tabellen aktualisieren
            self.refresh_tables()

        except Exception as e:
            QMessageBox.critical(self, "Datenbankfehler", str(e))

    def refresh_tables(self):
        """Lädt die Daten aus der DB neu in die QTableWidgets."""
        conn = sqlite3.connect("business.db")
        cursor = conn.cursor()

        mapping = {
            "kunden": "Kunden",
            "produkte": "Produkte",
            "bestellungen": "Bestellungen",
            "lieferanten": "Lieferanten",
            "mitarbeiter": "Mitarbeiter",
            "rechnungen": "Rechnungen",
        }

        for table_name, title in mapping.items():
            page_widget = self.table_pages.get(title)
            if not page_widget:
                continue

            table_widget = page_widget.findChild(QTableWidget)
            if not table_widget:
                continue

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            table_widget.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    # Bei Status-Spalten mit ComboBox: nur Text setzen, wenn keine ComboBox dort ist
                    if isinstance(table_widget.cellWidget(row_idx, col_idx), QComboBox):
                        combo = table_widget.cellWidget(row_idx, col_idx)
                        if value is not None and str(value) in [combo.itemText(i) for i in range(combo.count())]:
                            combo.setCurrentText(str(value))
                    else:
                        table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        conn.close()

    def setup_pages(self):
        # Navigations-Einträge
        navigation = [
            "1. Startseite",
            "2. Kunde erstellen",
            "3. Produkt erstellen",
            "4. Bestellung erstellen",
            "5. Rechnung erstellen",
            "6. Lieferant erstellen",
            "7. Mitarbeiter erstellen",
            "8. Übersicht: Bestellungen",
            "9. Übersicht: Kunden",
            "10. Übersicht: Produkte",
            "11. Übersicht: Lieferanten",
            "12. Übersicht: Mitarbeiter",
            "13. Übersicht: Rechnungen",
        ]

        self.sidebar.addItems(navigation)

        # Startseite
        start_page = QWidget()
        start_layout = QVBoxLayout(start_page)
        welcome_label = QLabel("Willkommen im Dashboard")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        start_layout.addWidget(welcome_label)
        self.stacked_widget.addWidget(start_page)

        # Erstellen-Seiten (Formulare)
        self.stacked_widget.addWidget(
            self.create_form(
                "Neuen Kunden anlegen",
                ["Vorname", "Nachname", "E-Mail", "Telefon"],
                "kunden",
            )
        )
        self.stacked_widget.addWidget(
            self.create_form(
                "Neues Produkt anlegen",
                ["Artikelnummer", "Bezeichnung", "Preis (€)", "Lagerbestand"],
                "produkte",
            )
        )
        self.stacked_widget.addWidget(
            self.create_form(
                "Neue Bestellung anlegen",
                ["Kunden ID", "Produkt ID", "Menge", "Datum"],
                "bestellungen",
            )
        )
        self.stacked_widget.addWidget(
            self.create_form(
                "Neue Rechnung anlegen",
                ["Bestell ID", "Betrag (€)", "Fälligkeitsdatum", "Status"],
                "rechnungen",
            )
        )
        self.stacked_widget.addWidget(
            self.create_form(
                "Neuen Lieferanten anlegen",
                ["Firmenname", "Ansprechpartner", "E-Mail", "Telefon"],
                "lieferanten",
            )
        )
        self.stacked_widget.addWidget(
            self.create_form(
                "Neuen Mitarbeiter anlegen",
                ["Vorname", "Nachname", "Abteilung", "Position"],
                "mitarbeiter",
            )
        )

        # Tabellen-Seiten
        # Bestellungen
        bestellungen_page = self.create_table_page(
            "Bestellungen",
            ["ID", "Kunden ID", "Produkt ID", "Menge", "Datum", "Status"],
            status_options=["erledigt", "gesendet", "in Bearbeitung", "storniert"],
        )
        self.table_pages["Bestellungen"] = bestellungen_page
        self.stacked_widget.addWidget(bestellungen_page)

        # Kunden
        kunden_page = self.create_table_page(
            "Kunden",
            ["ID", "Vorname", "Nachname", "E-Mail", "Telefon"],
        )
        self.table_pages["Kunden"] = kunden_page
        self.stacked_widget.addWidget(kunden_page)

        # Produkte
        produkte_page = self.create_table_page(
            "Produkte",
            ["ID", "Artikelnummer", "Bezeichnung", "Preis", "Lagerbestand"],
        )
        self.table_pages["Produkte"] = produkte_page
        self.stacked_widget.addWidget(produkte_page)

        # Lieferanten
        lieferanten_page = self.create_table_page(
            "Lieferanten",
            ["ID", "Firmenname", "Ansprechpartner", "E-Mail", "Telefon"],
        )
        self.table_pages["Lieferanten"] = lieferanten_page
        self.stacked_widget.addWidget(lieferanten_page)

        # Mitarbeiter
        mitarbeiter_page = self.create_table_page(
            "Mitarbeiter",
            ["ID", "Vorname", "Nachname", "Abteilung", "Position"],
        )
        self.table_pages["Mitarbeiter"] = mitarbeiter_page
        self.stacked_widget.addWidget(mitarbeiter_page)

        # Rechnungen
        rechnungen_page = self.create_table_page(
            "Rechnungen",
            ["ID", "Bestell ID", "Betrag", "Fälligkeitsdatum", "Status"],
            status_options=["gesendet", "bezahlt", "offen", "nicht gesendet"],
        )
        self.table_pages["Rechnungen"] = rechnungen_page
        self.stacked_widget.addWidget(rechnungen_page)

    def create_form(self, title, fields, table_name):
        """Erstellt eine standardisierte Seite mit einem Eingabeformular."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        input_widgets = []

        for field in fields:
            input_widget = QLineEdit()
            input_widget.setPlaceholderText(f"{field} eingeben...")
            form_layout.addRow(QLabel(field + ":"), input_widget)
            input_widgets.append(input_widget)

        layout.addLayout(form_layout)

        save_btn = QPushButton("Speichern")
        save_btn.setFixedWidth(150)
        save_btn.setStyleSheet("margin-top: 20px;")
        save_btn.clicked.connect(lambda: self.save_to_db(table_name, input_widgets))

        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addStretch()
        return page

    def create_table_page(self, title, columns, status_options=None):
        """Erstellt eine standardisierte Seite mit einer Tabelle."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title_label = QLabel(f"Übersicht: {title}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Falls es eine Status-Spalte gibt, Dropdowns einfügen (werden bei refresh_tables mit Daten gefüllt)
        if status_options and "Status" in columns:
            status_col_index = columns.index("Status")
            # Wir legen erstmal 0 Zeilen an; Dropdowns werden dynamisch bei Bedarf gesetzt
            table.setRowCount(0)
            # Beim späteren Füllen können wir bei Bedarf Comboboxen setzen
            # (hier nur Struktur, Logik in refresh_tables berücksichtigt)
        layout.addWidget(table)
        return page

    def change_page(self, index):
        """Wechselt die angezeigte Seite basierend auf der Sidebar-Auswahl."""
        self.stacked_widget.setCurrentIndex(index)

    def apply_styling(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1e1e2e;
            }
            QListWidget {
                background-color: #181825;
                color: #cdd6f4;
                border: none;
                font-size: 14px;
                padding-top: 20px;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-bottom: 1px solid #313244;
            }
            QListWidget::item:selected {
                background-color: #89b4fa;
                color: #11111b;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: #313244;
            }
            QWidget {
                color: #cdd6f4;
                background-color: #1e1e2e;
            }
            QLineEdit {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 5px;
                padding: 8px;
                color: #cdd6f4;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QTableWidget {
                background-color: #1e1e2e;
                gridline-color: #45475a;
                border: 1px solid #45475a;
                color: #cdd6f4;
            }
            QHeaderView::section {
                background-color: #313244;
                padding: 5px;
                border: 1px solid #45475a;
                font-weight: bold;
                color: #cdd6f4;
            }
            QComboBox {
                background-color: #313244;
                border: 1px solid #45475a;
                color: #cdd6f4;
                padding: 5px;
            }
            """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseGUI()
    window.show()
    sys.exit(app.exec())




import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QStackedWidget, QLabel,
    QFormLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QMessageBox,
    QToolBar, QSpacerItem, QSizePolicy
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
                datum TEXT,
                status TEXT
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
                "bestellungen": ["kunden_id", "produkt_id", "menge", "datum", "status"],
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

    def update_row_in_db(self, table_name: str, row_id: int, column_names: list, values: list):
        """Aktualisiert eine Zeile in der DB basierend auf id."""
        try:
            conn = sqlite3.connect("business.db")
            cursor = conn.cursor()
            set_clause = ", ".join([f"{col}=?" for col in column_names])
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            cursor.execute(query, values + [row_id])
            conn.commit()
            conn.close()
            return True, None
        except Exception as e:
            return False, str(e)

    def delete_row_in_db(self, table_name: str, row_id: int):
        """Löscht eine Zeile in der DB basierend auf id."""
        try:
            conn = sqlite3.connect("business.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (row_id,))
            conn.commit()
            conn.close()
            return True, None
        except Exception as e:
            return False, str(e)

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
                    # Wenn Zelle bereits ein Widget (z.B. ComboBox) ist, behandeln wir separat
                    cell_widget = table_widget.cellWidget(row_idx, col_idx)
                    if isinstance(cell_widget, QComboBox):
                        combo = cell_widget
                        if value is not None and str(value) in [combo.itemText(i) for i in range(combo.count())]:
                            combo.setCurrentText(str(value))
                    else:
                        item = QTableWidgetItem("" if value is None else str(value))
                        # ID-Spalte nicht editierbar
                        if col_idx == 0:
                            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        table_widget.setItem(row_idx, col_idx, item)

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
                ["Kunden ID", "Produkt ID", "Menge", "Datum", "Status"],
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
            table_name="bestellungen",
            status_options=["erledigt", "gesendet", "in Bearbeitung", "storniert"],
        )
        self.table_pages["Bestellungen"] = bestellungen_page
        self.stacked_widget.addWidget(bestellungen_page)

        # Kunden
        kunden_page = self.create_table_page(
            "Kunden",
            ["ID", "Vorname", "Nachname", "E-Mail", "Telefon"],
            table_name="kunden",
        )
        self.table_pages["Kunden"] = kunden_page
        self.stacked_widget.addWidget(kunden_page)

        # Produkte
        produkte_page = self.create_table_page(
            "Produkte",
            ["ID", "Artikelnummer", "Bezeichnung", "Preis", "Lagerbestand"],
            table_name="produkte",
        )
        self.table_pages["Produkte"] = produkte_page
        self.stacked_widget.addWidget(produkte_page)

        # Lieferanten
        lieferanten_page = self.create_table_page(
            "Lieferanten",
            ["ID", "Firmenname", "Ansprechpartner", "E-Mail", "Telefon"],
            table_name="lieferanten",
        )
        self.table_pages["Lieferanten"] = lieferanten_page
        self.stacked_widget.addWidget(lieferanten_page)

        # Mitarbeiter
        mitarbeiter_page = self.create_table_page(
            "Mitarbeiter",
            ["ID", "Vorname", "Nachname", "Abteilung", "Position"],
            table_name="mitarbeiter",
        )
        self.table_pages["Mitarbeiter"] = mitarbeiter_page
        self.stacked_widget.addWidget(mitarbeiter_page)

        # Rechnungen
        rechnungen_page = self.create_table_page(
            "Rechnungen",
            ["ID", "Bestell ID", "Betrag", "Fälligkeitsdatum", "Status"],
            table_name="rechnungen",
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

    def create_table_page(self, title, columns, table_name=None, status_options=None):
        """Erstellt eine standardisierte Seite mit einer Tabelle und Edit-Buttons."""
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
        table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.SelectedClicked)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Falls es eine Status-Spalte gibt, wir merken uns die Indexe für später
        if status_options and "Status" in columns:
            status_col_index = columns.index("Status")
        else:
            status_col_index = None

        layout.addWidget(table)

        # Toolbar / Buttons unter der Tabelle
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("Neu laden")
        save_changes_btn = QPushButton("Änderungen speichern")
        delete_btn = QPushButton("Ausgewählte Zeile löschen")

        refresh_btn.clicked.connect(lambda _, tn=table_name: self.refresh_tables())
        save_changes_btn.clicked.connect(lambda _, t=table, tn=table_name, cols=columns: self.save_table_changes(t, tn, cols))
        delete_btn.clicked.connect(lambda _, t=table, tn=table_name: self.delete_selected_row(t, tn))

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(save_changes_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Speichere Referenz auf table und table_name in page für refresh_tables
        page._table = table
        page._table_name = table_name
        page._status_col_index = status_col_index

        return page

    def save_table_changes(self, table_widget: QTableWidget, table_name: str, columns: list):
        """Liest alle Zeilen aus der Tabelle und speichert geänderte Zeilen in die DB.
           Vereinfachung: wir gehen jede Zeile durch und updaten anhand der ID (Spalte 0)."""
        if not table_name:
            QMessageBox.warning(self, "Fehler", "Kein Tabellenname angegeben.")
            return

        # Spaltennamen ohne ID (ID ist Spalte 0)
        column_names = [c for c in columns[1:]]  # z.B. ["Vorname","Nachname",...]
        rows = table_widget.rowCount()
        errors = []
        updates = 0

        for r in range(rows):
            id_item = table_widget.item(r, 0)
            if id_item is None:
                continue
            try:
                row_id = int(id_item.text())
            except ValueError:
                continue

            # Werte aus Zellen lesen (Spalten 1..n)
            values = []
            for c_idx in range(1, table_widget.columnCount()):
                cell_widget = table_widget.cellWidget(r, c_idx)
                if isinstance(cell_widget, QComboBox):
                    values.append(cell_widget.currentText())
                else:
                    item = table_widget.item(r, c_idx)
                    values.append("" if item is None else item.text())

            # Update in DB
            success, err = self.update_row_in_db(table_name, row_id, column_names, values)
            if not success:
                errors.append(f"ID {row_id}: {err}")
            else:
                updates += 1

        if errors:
            QMessageBox.critical(self, "Fehler beim Speichern", "\n".join(errors))
        else:
            QMessageBox.information(self, "Erfolg", f"{updates} Zeilen erfolgreich aktualisiert.")
        self.refresh_tables()

    def delete_selected_row(self, table_widget: QTableWidget, table_name: str):
        """Löscht die aktuell ausgewählte Zeile aus DB und Tabelle."""
        sel = table_widget.currentRow()
        if sel < 0:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Zeile auswählen.")
            return

        id_item = table_widget.item(sel, 0)
        if id_item is None:
            QMessageBox.warning(self, "Fehler", "ID nicht gefunden.")
            return

        try:
            row_id = int(id_item.text())
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Ungültige ID.")
            return

        confirm = QMessageBox.question(self, "Löschen bestätigen", f"Zeile mit ID {row_id} wirklich löschen?")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        success, err = self.delete_row_in_db(table_name, row_id)
        if not success:
            QMessageBox.critical(self, "Fehler beim Löschen", err)
        else:
            QMessageBox.information(self, "Gelöscht", f"Zeile mit ID {row_id} wurde gelöscht.")
        self.refresh_tables()

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

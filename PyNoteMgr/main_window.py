
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QLineEdit, QPushButton,
    QListWidgetItem, QMessageBox, QLabel
)
from db_manager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_note_id = None
        self.build_ui()
        self.load_notes()   


    def build_ui(self):
        self.setWindowTitle("Notizenverwaltung")
        self.resize(800,600)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        # Linke Seite: Notizliste
        left = QVBoxLayout()
        left.addWidget(QLabel("Meine Notizen"))
        self.note_list = QListWidget()
        self.note_list.currentItemChanged.connect(self.on_note_selected)
        left.addWidget(self.note_list)

        btn_new = QPushButton("+ Neue Notiz")
        btn_new.clicked.connect(self.new_note)
        btn_delete = QPushButton("- Löschen")
        btn_delete.clicked.connect(self.delete_note)
        left.addWidget(btn_new)
        left.addWidget(btn_delete)
        # Rechte Seite: Editor        
        right = QVBoxLayout()
        right.addWidget(QLabel("Titel:"))
        self.title_input = QLineEdit()
        right.addWidget(self.title_input)
        right.addWidget(QLabel("Inhalt"))
        self.content_input = QTextEdit()
        right.addWidget(self.content_input)
        btn_save = QPushButton("Speichern")
        btn_save.clicked.connect(self.save_note)
        right.addWidget(btn_save)
        layout.addLayout(left,1)
        layout.addLayout(right,2)

    def load_notes(self):
        self.note_list.clear()
        for note in self.db.getall_notes():
            item = QListWidgetItem(note["title"])
            item.setData(256, note["id"])
            self.note_list.addItem(item)

    def on_note_selected(self, item):
            if item:
                note_id = item.data(256)
                notes = self.db.getall_notes()
                note = next((n for n in notes if n["id"]==note_id))
                if note:
                    self.current_note_id = note_id
                    self.title_input.setText(note["title"])
                    self.content_input.setPlainText(note["content"] or "")

    def new_note(self):
        self.current_note_id = None
        self.title_input.clear()
        self.content_input.clear()
        self.title_input.setFocus()
        

    def save_note(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Fehler", "Titel darf nicht leer sein!")
            return
        content = self.content_input.toPlainText()
        if self.current_note_id:
            self.db.update_note(self.current_note_id, title, content)
        else:
            self.db.create_note(title, content)
        self.load_notes()


    def delete_note(self):
        if self.current_note_id:
            reply = QMessageBox.question(self, "Löschen", "Notiz wirklich löschen?")
            if  reply == QMessageBox.StandardButton.Yes:
                self.db.delete_note(self.current_note_id)
                self.new_note()
                self.load_notes()


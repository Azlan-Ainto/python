
import sqlite3 as sql
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "notes.db"):        
        self.db_path = db_path
        self.init_db()

    
       
    def init_db(self):
        with sql.connect(self.db_path) as conn:
            conn.execute(""" CREATE TABLE IF NOT EXISTS notes(                         
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         content TEXT,
                         created TEXT DEFAULT(datetime('now')))""")
    

    def getall_notes(self) -> list[dict] :
        with sql.connect(self.db_path)  as conn:
            conn.row_factory = sql.Row
            rows = conn.execute("SELECT * FROM notes ORDER BY created DESC").fetchall()
            return [dict(row) for row in rows]
        
    
    def create_note(self, title:str, content:str) -> int:
        with sql.connect(self.db_path) as conn:
            cursor = conn.execute("INSERT INTO notes(title,content) VALUES(?,?)",(title,content))
            conn.commit()
            return cursor.lastrowid
        
    



    def update_note(self, note_id:int, title:str, content:str):
        with sql.connect(self.db_path) as conn:
            conn.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
        conn.commit()
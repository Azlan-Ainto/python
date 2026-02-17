
import sqlite3


conn = sqlite3.connect("kunden.db")
c = conn.cursor()
c.execute("DROP TABLE kunden")
conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("site.db")

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario TEXT UNIQUE,

    senha TEXT

)

""")

conn.commit()

conn.close()

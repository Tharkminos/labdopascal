import sqlite3

conn = sqlite3.connect("site.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE progresso (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER NOT NULL,

    post TEXT NOT NULL,

    xp_ganho INTEGER DEFAULT 0,

    concluido INTEGER DEFAULT 0,

    data_conclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

conn.close()

print("Tabela criada!")

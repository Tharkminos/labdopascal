import sqlite3

# conecta/cria banco
conn = sqlite3.connect("site.db")

# controla comandos SQL
cursor = conn.cursor()

# ================= USUÁRIOS =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario TEXT UNIQUE,

    senha TEXT,

    xp INTEGER DEFAULT 0,

    nivel INTEGER DEFAULT 1,

    avatar TEXT,

    bio TEXT

)

""")

# ================= ACHIEVEMENTS =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS achievements (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nome TEXT,

    descricao TEXT,

    icone TEXT

)

""")

# ================= RELAÇÃO =================

cursor.execute("""

CREATE TABLE IF NOT EXISTS user_achievements (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario_id INTEGER,

    achievement_id INTEGER,

    data_desbloqueio TEXT

)

""")

# salva mudanças
conn.commit()

# fecha banco
conn.close()

print("Banco criado.")

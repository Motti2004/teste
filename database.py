import sqlite3

def criar_tabela():
    con = sqlite3.connect("arvores_cadastradas.db")
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS arvores_cadastradas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        telefone TEXT,
        altura REAL,
        diametro REAL,
        caracteristicas TEXT,
        coordenadas TEXT,
        foto_path TEXT
    )
    """)
    con.commit()
    con.close()

def inserir_arvore(nome, email, telefone, altura, diametro, caracteristicas, coordenadas, foto_path):
    con = sqlite3.connect("arvores_cadastradas.db")
    cursor = con.cursor()
    cursor.execute("""
    INSERT INTO arvores_cadastradas (nome, email, telefone, altura, diametro, caracteristicas, coordenadas, foto_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, email, telefone, altura, diametro, caracteristicas, coordenadas, foto_path))
    con.commit()
    con.close()

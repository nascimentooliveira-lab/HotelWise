import sqlite3

DB_PATH = "hotel.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def listar_reservas_completas():
    conn = get_db()
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT * FROM vw_reservas_completas"
    ).fetchall()

    conn.close()
    return rows

def reset_db():
    """
    Remove todos os dados do banco (desenvolvimento).
    Mantém as tabelas.
    """
    conn = get_db()
    cur = conn.cursor()

    # Desativa FK temporariamente para limpeza segura
    cur.execute("PRAGMA foreign_keys = OFF;")

    cur.execute("DELETE FROM reservas;")
    cur.execute("DELETE FROM hospedes;")
    cur.execute("DELETE FROM quartos;")
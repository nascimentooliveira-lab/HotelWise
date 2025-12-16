from persistencia.dados import get_db
from modelos.adicional import Adicional
import sqlite3


def adicionar_adicional(a: Adicional):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO adicionais (reserva_id, descricao, valor)
        VALUES (?, ?, ?)
    """, (a.reserva_id, a.descricao, a.valor))
    conn.commit()
    a.id = cur.lastrowid
    return a.id


def listar_adicionais(reserva_id: int):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM adicionais WHERE reserva_id=?",
        (reserva_id,)
    ).fetchall()
    return [Adicional.from_db_row(r) for r in rows]

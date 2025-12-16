from persistencia.dados import get_db
from modelos.pagamento import Pagamento
import sqlite3


def registrar_pagamento(p: Pagamento):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pagamentos (reserva_id, valor, forma, data_pagamento)
        VALUES (?, ?, ?, ?)
    """, (p.reserva_id, p.valor, p.forma, p.data_pagamento))
    conn.commit()
    p.id = cur.lastrowid
    return p.id


def listar_pagamentos(reserva_id: int):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM pagamentos WHERE reserva_id=?",
        (reserva_id,)
    ).fetchall()
    return [Pagamento.from_db_row(r) for r in rows]

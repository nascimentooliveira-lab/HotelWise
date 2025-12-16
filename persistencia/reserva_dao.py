from persistencia.dados import get_db
from persistencia.hospede_dao import buscar_hospede
from persistencia.quarto_dao import buscar_quarto_por_numero
from modelos.reserva import Reserva
from datetime import datetime, date
import sqlite3
from persistencia.pagamento_dao import listar_pagamentos


# ----------------------------
# UTILITÁRIOS
# ----------------------------

def _row_para_reserva(row):
    if not row:
        return None

    hospede = buscar_hospede(row["hospede_id"])
    if not hospede:
        raise ValueError(
            f"Reserva {row['id']} referencia hóspede inexistente ({row['hospede_id']})"
        )

    quarto = buscar_quarto_por_numero(row["quarto_numero"])
    if not quarto:
        raise ValueError(
            f"Reserva {row['id']} referencia quarto inexistente ({row['quarto_numero']})"
        )

    # 1️⃣ cria a reserva
    r = Reserva(
        id=row["id"],
        hospede=hospede,
        quarto=quarto,
        data_entrada=date.fromisoformat(row["data_entrada"]),
        data_saida=date.fromisoformat(row["data_saida"]),
        num_hospedes=row["num_hospedes"],
        origem=row["origem"],
        estado=row["estado"]
    )

    # 2️⃣ campos opcionais
    if row["check_in_real"]:
        r.check_in_real = datetime.fromisoformat(row["check_in_real"])

    if row["check_out_real"]:
        r.check_out_real = datetime.fromisoformat(row["check_out_real"])

    if row["data_cancelamento"]:
        r.data_cancelamento = date.fromisoformat(row["data_cancelamento"])

    if row["data_no_show"]:
        r.data_no_show = date.fromisoformat(row["data_no_show"])

    # 3️⃣ 🔥 CARREGA PAGAMENTOS (ESSENCIAL)
    for p in listar_pagamentos(r.id):
        r.adicionar_pagamento(p)

    return r

# ----------------------------
# CRUD
# ----------------------------

def criar_reserva(reserva: Reserva) -> int:
    """
    Persiste uma reserva a partir do objeto de domínio.
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reservas (
            hospede_id, quarto_numero, data_entrada, data_saida,
            num_hospedes, estado, origem,
            check_in_real, check_out_real, data_cancelamento, data_no_show
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        reserva.hospede.id,
        reserva.quarto.numero,
        reserva.data_entrada.isoformat(),
        reserva.data_saida.isoformat(),
        reserva.num_hospedes,
        reserva.estado,
        reserva.origem,
        reserva.check_in_real.isoformat() if reserva.check_in_real else None,
        reserva.check_out_real.isoformat() if reserva.check_out_real else None,
        reserva.data_cancelamento.isoformat() if reserva.data_cancelamento else None,
        reserva.data_no_show.isoformat() if reserva.data_no_show else None
    ))

    conn.commit()
    reserva.id = cur.lastrowid
    return reserva.id

def listar_reservas_completas():
    conn = get_db()
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT
            r.id AS reserva_id,
            h.nome AS hospede_nome,
            h.documento AS hospede_documento,
            q.numero AS quarto_numero,
            q.tipo AS quarto_tipo,
            q.capacidade AS quarto_capacidade,
            q.tarifa_base AS tarifa_base,
            r.data_entrada,
            r.data_saida,
            r.num_hospedes,
            r.origem,
            r.estado,
            r.check_in_real,
            r.check_out_real,
            r.data_cancelamento,
            r.data_no_show,
            COALESCE(SUM(DISTINCT p.valor), 0) AS total_pago,
            COALESCE(SUM(DISTINCT a.valor), 0) AS total_adicionais
        FROM reservas r
        JOIN hospedes h ON h.id = r.hospede_id
        JOIN quartos q ON q.numero = r.quarto_numero
        LEFT JOIN pagamentos p ON p.reserva_id = r.id
        LEFT JOIN adicionais a ON a.reserva_id = r.id
        GROUP BY r.id
        ORDER BY r.id
    """).fetchall()

    conn.close()
    return rows

def buscar_reserva(id: int):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM reservas WHERE id=?", (id,)).fetchone()
    return _row_para_reserva(row)


def atualizar_reserva(reserva: Reserva):
    conn = get_db()
    conn.execute("""
        UPDATE reservas SET
            hospede_id=?, quarto_numero=?, data_entrada=?, data_saida=?,
            num_hospedes=?, estado=?, origem=?,
            check_in_real=?, check_out_real=?, data_cancelamento=?, data_no_show=?
        WHERE id=?
    """, (
        reserva.hospede.id,
        reserva.quarto.numero,
        reserva.data_entrada.isoformat(),
        reserva.data_saida.isoformat(),
        reserva.num_hospedes,
        reserva.estado,
        reserva.origem,
        reserva.check_in_real.isoformat() if reserva.check_in_real else None,
        reserva.check_out_real.isoformat() if reserva.check_out_real else None,
        reserva.data_cancelamento.isoformat() if reserva.data_cancelamento else None,
        reserva.data_no_show.isoformat() if reserva.data_no_show else None,
        reserva.id
    ))
    conn.commit()

def remover_reserva(id: int):
    conn = get_db()
    conn.execute("DELETE FROM reservas WHERE id=?", (id,))
    conn.commit()

def atualizar_estado_reserva(reserva_id: int, novo_estado: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE reservas SET estado = ? WHERE id = ?",
        (novo_estado, reserva_id)
    )

    conn.commit()
    conn.close()

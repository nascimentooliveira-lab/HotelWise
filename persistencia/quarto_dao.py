from persistencia.dados import get_db
from modelos.quarto import Quarto
import sqlite3
from datetime import date
from typing import List


def criar_quarto(dados: dict):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO quartos (
            numero, tipo, capacidade, tarifa_base, status,
            motivo_bloqueio, bloqueio_inicio, bloqueio_fim
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["numero"],
        dados["tipo"],
        dados["capacidade"],
        dados["tarifa_base"],
        dados.get("status", "DISPONIVEL"),
        None,
        None,
        None
    ))
    conn.commit()
    conn.close()


def listar_quartos() -> List[Quarto]:
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM quartos").fetchall()
    conn.close()
    return [Quarto.from_db_row(r) for r in rows]

def buscar_quarto_por_numero(numero: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT numero, tipo, capacidade, tarifa_base, status
        FROM quartos
        WHERE numero = ?
    """, (numero,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    tipo = row[1].strip().upper()
    status = row[4].strip().upper()

    return Quarto(
        numero=row[0],
        tipo=tipo,
        capacidade=row[2],
        tarifa_base=row[3],
        status=status
    )

def atualizar_quarto(dados: dict):
    conn = get_db()
    conn.execute("""
        UPDATE quartos SET
            tipo=?, capacidade=?, tarifa_base=?, status=?,
            motivo_bloqueio=?, bloqueio_inicio=?, bloqueio_fim=?
        WHERE numero=?
    """, (
        dados.get("tipo"),
        dados.get("capacidade"),
        dados.get("tarifa_base"),
        dados.get("status", "DISPONIVEL"),
        dados.get("motivo_bloqueio"),
        dados.get("bloqueio_inicio"),
        dados.get("bloqueio_fim"),
        dados["numero"]
    ))
    conn.commit()
    conn.close()


def excluir_quarto(numero: int):
    conn = get_db()
    conn.execute("DELETE FROM quartos WHERE numero=?", (numero,))
    conn.commit()
    conn.close()


# ----------------------------
# Bloqueio / Desbloqueio
# ----------------------------
def bloquear_quarto(numero: int, inicio: date, fim: date, motivo: str):
    """
    Marca bloqueio no quarto (persistente).
    inicio/fim devem ser date ou strings ISO (YYYY-MM-DD).
    """
    conn = get_db()
    # garantimos strings no formato ISO no banco
    inicio_iso = inicio.isoformat() if isinstance(inicio, date) else inicio
    fim_iso = fim.isoformat() if isinstance(fim, date) else fim

    conn.execute("""
        UPDATE quartos
        SET status = 'MANUTENCAO', motivo_bloqueio = ?, bloqueio_inicio = ?, bloqueio_fim = ?
        WHERE numero = ?
    """, (motivo, inicio_iso, fim_iso, numero))
    conn.commit()
    conn.close()


def desbloquear_quarto(numero: int):
    conn = get_db()
    conn.execute("""
        UPDATE quartos
        SET status = 'DISPONIVEL', motivo_bloqueio = NULL, bloqueio_inicio = NULL, bloqueio_fim = NULL
        WHERE numero = ?
    """, (numero,))
    conn.commit()
    conn.close()

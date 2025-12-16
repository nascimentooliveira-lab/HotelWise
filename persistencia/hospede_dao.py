from persistencia.dados import get_db
from modelos.hospede import Hospede
import sqlite3
from typing import List, Optional


def criar_hospede(dados: dict) -> int:
    """
    Cria hóspede no banco. Dados esperados: nome, documento, email, telefone
    Retorna id do novo hóspede.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO hospedes (nome, documento, email, telefone)
        VALUES (?, ?, ?, ?)
    """, (dados.get("nome"), dados.get("documento"), dados.get("email"), dados.get("telefone")))
    conn.commit()
    hid = cur.lastrowid
    conn.close()
    return hid


def listar_hospedes() -> List[Hospede]:
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM hospedes").fetchall()
    conn.close()
    return [Hospede.from_db_row(r) for r in rows]


def buscar_hospede(id: int) -> Optional[Hospede]:
    conn = get_db()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM hospedes WHERE id=?", (id,)).fetchone()
    conn.close()
    return Hospede.from_db_row(row) if row else None


def atualizar_hospede(dados: dict):
    """
    Atualiza hóspede. Recebe dict com chave 'id' obrigatória.
    """
    conn = get_db()
    conn.execute("""
        UPDATE hospedes SET nome=?, documento=?, email=?, telefone=? WHERE id=?
    """, (dados.get("nome"), dados.get("documento"), dados.get("email"), dados.get("telefone"), dados["id"]))
    conn.commit()
    conn.close()


def excluir_hospede(id: int):
    conn = get_db()
    conn.execute("DELETE FROM hospedes WHERE id=?", (id,))
    conn.commit()
    conn.close()

def buscar_hospede_por_documento(documento: str) -> Optional[Hospede]:
    conn = get_db()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM hospedes WHERE documento = ?",
        (documento,)
    ).fetchone()
    conn.close()
    return Hospede.from_db_row(row) if row else None

def buscar_hospede_por_id(hospede_id: int):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nome, documento, email, telefone
        FROM hospedes
        WHERE id = ?
    """, (hospede_id,))
    row = cur.fetchone()
    conn.close()

    return Hospede.from_db_row(row) if row else None

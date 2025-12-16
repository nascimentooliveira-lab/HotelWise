# persistencia/temporada_dao.py
from persistencia.dados import get_db_connection
from datetime import date


def listar_temporadas():
    """Retorna todas as temporadas do banco."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM temporadas").fetchall()
    return [dict(r) for r in rows]


def buscar_temporada_por_data(data_str: str):
    """
    Retorna a temporada que inclui a data informada.
    data_str deve ser no formato YYYY-MM-DD.
    """

    conn = get_db_connection()

    row = conn.execute("""
        SELECT *
        FROM temporadas
        WHERE data_inicio <= ? AND data_fim >= ?
        LIMIT 1
    """, (data_str, data_str)).fetchone()

    return dict(row) if row else None


def fator_para_data(data_str: str) -> float:
    """
    Retorna o fator de multiplicação baseado na temporada.
    Se nenhuma temporada for encontrada → retorna 1.0 (normal).
    """

    temp = buscar_temporada_por_data(data_str)
    if temp:
        return float(temp["fator_multiplicador"])

    return 1.0


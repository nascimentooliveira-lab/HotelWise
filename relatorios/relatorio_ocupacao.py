from datetime import date, timedelta
import sqlite3

DB = "hotelwise.db"

def calcular_ocupacao(inicio: date, fim: date):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    resultados = []

    dia = inicio
    while dia <= fim:
        dia_str = dia.isoformat()

        # Conta reservas que estão ativas nesse dia
        cur.execute("""
            SELECT COUNT(*) 
            FROM reservas
            WHERE estado = 'CONFIRMADA'
              AND data_entrada <= ?
              AND data_saida > ?
        """, (dia_str, dia_str))

        ocupados = cur.fetchone()[0]

        # Número total de quartos
        cur.execute("SELECT COUNT(*) FROM quartos")
        total_quartos = cur.fetchone()[0]

        livres = total_quartos - ocupados
        taxa = (ocupados / total_quartos * 100) if total_quartos > 0 else 0

        resultados.append({
            "data": dia_str,
            "ocupados": ocupados,
            "livres": livres,
            "taxa": round(taxa, 2)
        })

        dia += timedelta(days=1)

    conn.close()
    return resultados






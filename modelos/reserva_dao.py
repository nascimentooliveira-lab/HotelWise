import sqlite3
from datetime import datetime, date
from persistencia.dados import get_db_connection 

# FUNÇÕES DE LEITURA (READ)

def buscar_reservas_por_hospede(hospede_id: int):
    """Busca todas as reservas de um hóspede específico no BD (Usado em Lazy Loading)."""
    from .reserva import Reserva   

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM reservas WHERE hospede_id = ?
    """, (hospede_id,))

    rows = cursor.fetchall()
    conn.close()
    
    return [Reserva.from_db_row(row) for row in rows]


def buscar_reserva_por_id(reserva_id: int):
    """Busca uma reserva específica pelo seu ID."""
    from .reserva import Reserva   

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
    row = cursor.fetchone()
    conn.close()
    
    return Reserva.from_db_row(row) if row else None


# FUNÇÕES DE CRIAÇÃO/INSERÇÃO (CREATE)

def inserir_reserva(reserva):
    """Insere uma nova reserva no BD e retorna o ID gerado."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO reservas (
                hospede_id, quarto_numero, data_entrada, data_saida, 
                num_hospedes, estado, origem, valor_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        dados = (
            reserva.hospede.id,
            reserva.quarto.numero,
            reserva.data_entrada.isoformat(),
            reserva.data_saida.isoformat(),
            reserva.numero_hospedes,
            reserva.estado,
            reserva.origem,
            reserva.valor_total()
        )
        
        cursor.execute(sql, dados)
        reserva.id = cursor.lastrowid
        conn.commit()
        
        return reserva.id

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erro ao inserir nova reserva: {e}")
        return None

    finally:
        conn.close()


# FUNÇÃO DE ATUALIZAÇÃO (UPDATE)

def salvar_reserva(reserva):
    """Persiste alterações de estado e atualiza status do quarto."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql_reserva = """
            UPDATE reservas 
            SET estado = ?, 
                valor_total = ?, 
                data_cancelamento = ?, 
                data_no_show = ?,
                check_in_real = ?,      
                check_out_real = ?      
            WHERE id = ?
        """
        
        dados_reserva = (
            reserva.estado,
            reserva.valor_total(),
            reserva.data_cancelamento.isoformat() if reserva.data_cancelamento else None,
            reserva.data_no_show.isoformat() if reserva.data_no_show else None,
            reserva.check_in_real.isoformat() if reserva.check_in_real else None,
            reserva.check_out_real.isoformat() if reserva.check_out_real else None,
            reserva.id
        )
        

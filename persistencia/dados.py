from datetime import date, timedelta
import sqlite3
import os

DATABASE_NAME = 'hotelwise.db'

" " " configura o retorno por nome da coluna."""
    
def get_db_connection():

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row # Permite acesso por nome
        return conn
    
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

def _criar_tabelas(conn):

  cursor = conn.cursor()
  cursor.execute("""
      CREATE TABLE IF NOT EXISTS quartos (
         numero INTEGER PRIMARY KEY,
         tipo TEXT NOT NULL,
         capacidade INTEGER NOT NULL,
         tarifa_base REAL NOT NULL,
         status TEXT NOT NULL,
         bloqueio_inicio TEXT,         
         bloqueio_fim TEXT
      );
  """)

  cursor.execute("""
      CREATE TABLE IF NOT EXISTS hospedes (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         nome TEXT NOT NULL,
         documento TEXT UNIQUE NOT NULL, 
         email TEXT,
         telefone TEXT
      );
  """)

  cursor.execute("""
      CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospede_id INTEGER NOT NULL,          -- Chave estrangeira para Hospedes
        quarto_numero INTEGER NOT NULL,       -- Chave estrangeira para Quartos
        data_entrada TEXT NOT NULL,
        data_saida TEXT NOT NULL,
        num_hospedes INTEGER NOT NULL,
        estado TEXT NOT NULL,
        origem TEXT NOT NULL,
        valor_total REAL,                     -- Valor calculado (deve ser persistido)

        FOREIGN KEY (hospede_id) REFERENCES hospedes(id),
        FOREIGN KEY (quarto_numero) REFERENCES quartos(numero)
      );
  """)

  cursor.execute("""
      CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reserva_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        forma TEXT NOT NULL,
        data TEXT NOT NULL,  -- Usaremos ISO format (YYYY-MM-DD HH:MM:SS)

        FOREIGN KEY (reserva_id) REFERENCES reservas(id)
      );
  """)

  conn.commit()

  def seed_dados():
    """Cria tabelas e insere dados iniciais de Quartos e Temporadas se estiverem vazios."""
    
    conn = get_db_connection()
    _criar_tabelas(conn)
    cursor = conn.cursor()

    print("Iniciando rotina de persistência (seed)...")

    # Seed de Quartos
    cursor.execute("SELECT COUNT(*) FROM quartos")
    if cursor.fetchone()[0] == 0:
        quartos_seed = [

            # (numero, tipo, capacidade, tarifa_base, status, motivo_bloqueio, bloqueio_inicio, bloqueio_fim)

            (101, "SIMPLES", 1, 120.00, "DISPONIVEL", None, None, None),
            (102, "SIMPLES", 1, 120.00, "DISPONIVEL", None, None, None),
            (201, "DUPLO", 2, 180.00, "DISPONIVEL", None, None, None),
            (202, "DUPLO", 2, 180.00, "DISPONIVEL", None, None, None),
            (301, "LUXO", 4, 350.00, "DISPONIVEL", None, None, None),
            (302, "LUXO", 4, 350.00, "MANUTENCAO", "Pintura", '2026-01-01', '2026-01-10'),
            (401, "LUXO", 5, 450.00, "DISPONIVEL", None, None, None),
        ]
        cursor.executemany("""
            INSERT INTO quartos (numero, tipo, capacidade, tarifa_base, status, motivo_bloqueio, bloqueio_inicio, bloqueio_fim) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, quartos_seed)
        print(f" Seed concluída: {len(quartos_seed)} quartos criados.")
    else:
        print("Quartos já populados.")
    
    # Seed de Temporadas

    cursor.execute("SELECT COUNT(*) FROM temporadas")
    if cursor.fetchone()[0] == 0:
        temporadas_seed = [
            ("Baixa", "2026-03-01", "2026-05-31", 1.00),
            ("Média", "2026-06-01", "2026-08-31", 1.25),
            ("Alta", "2025-12-15", "2026-02-28", 1.50),
        ]
        cursor.executemany("""
            INSERT INTO temporadas (nome, data_inicio, data_fim, fator_multiplicador) 
            VALUES (?, ?, ?, ?)
        """, temporadas_seed)
        print(f" Seed concluída: {len(temporadas_seed)} temporadas criadas.")
    else:
        print("Temporadas já populadas.")
    
    conn.commit()
    conn.close()
    print("Rotina de persistência finalizada.")


    from datetime import date, timedelta

def relatorio_ocupacao(inicio: date, fim: date):
    """
    Gera relatório de ocupação diária entre duas datas (fim não incluso).
    Retorna um dicionário: { data: {ocupados, livres, taxa} }
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Total de quartos cadastrados
    cursor.execute("SELECT COUNT(*) as total FROM quartos")
    total_quartos = cursor.fetchone()["total"]

    # Busca reservas que INTERSECTAM o período
    
    cursor.execute("""
        SELECT quarto_numero, data_entrada, data_saida
        FROM reservas
        WHERE NOT (data_saida <= ? OR data_entrada >= ?)
    """, (inicio.isoformat(), fim.isoformat()))

    reservas = cursor.fetchall()

    conn.close()

    # Monta relatório dia a dia
    relatorio = {}
    dia = inicio

    while dia < fim:
        ocupados = 0

        for r in reservas:
            entrada = date.fromisoformat(r["data_entrada"])
            saida = date.fromisoformat(r["data_saida"])

            # Este quarto está ocupado neste dia?
            if entrada <= dia < saida:
                ocupados += 1

        livres = total_quartos - ocupados
        taxa = (ocupados / total_quartos * 100) if total_quartos > 0 else 0

        relatorio[dia] = {
            "ocupados": ocupados,
            "livres": livres,
            "taxa_ocupacao": round(taxa, 2)
        }

        dia += timedelta(days=1)

    return relatorio

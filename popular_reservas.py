from datetime import date, timedelta
import sqlite3

DATABASE_NAME = "hotelwise.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()

# Inserir 3 hóspedes
hospedes = [
    ("João da Silva", "123456789"),
    ("Maria Oliveira", "987654321"),
    ("Carlos Souza", "555555555")
]

for nome, doc in hospedes:
    conn.execute(
        "INSERT INTO hospedes (nome, documento) VALUES (?, ?)",
        (nome, doc)
    )

# Inserir 3 quartos (se ainda não existirem)
quartos = [
    (101, "SIMPLES", 2, 150.0, "DISPONIVEL"),
    (102, "DUPLO", 3, 220.0, "DISPONIVEL"),
    (201, "LUXO", 2, 350.0, "DISPONIVEL")
]

for numero, tipo, cap, tarifa, status in quartos:
    conn.execute(
        "INSERT OR IGNORE INTO quartos (numero, tipo, capacidade, tarifa_base, status) VALUES (?, ?, ?, ?, ?)",
        (numero, tipo, cap, tarifa, status)
    )

hoje = date(2025, 1, 1)

# Inserir 3 reservas de teste
reservas = [
    (1, 101, hoje.isoformat(), (hoje + timedelta(days=2)).isoformat(), 1, "CONFIRMADA", "SITE", 300.0),
    (2, 102, hoje.isoformat(), (hoje + timedelta(days=3)).isoformat(), 2, "CONFIRMADA", "RECEPCAO", 660.0),
    (3, 201, (hoje + timedelta(days=1)).isoformat(), (hoje + timedelta(days=4)).isoformat(), 2, "CONFIRMADA", "SITE", 1050.0)
]

for r in reservas:
    conn.execute(
        """INSERT INTO reservas
        (hospede_id, quarto_numero, data_entrada, data_saida, num_hospedes, estado, origem, valor_total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        r
    )

conn.commit()
conn.close()

print("Banco populado com reservas de teste!")

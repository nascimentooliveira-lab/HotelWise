import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Apaga tabelas antigas só se existirem
cursor.executescript("""
DROP TABLE IF EXISTS hospedes;
DROP TABLE IF EXISTS quartos;
DROP TABLE IF EXISTS reservas;
""")

# Tabela de Hóspedes
cursor.execute("""
CREATE TABLE hospedes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    documento TEXT NOT NULL,
    email TEXT,
    telefone TEXT
)
""")

# Tabela de Quartos
cursor.execute("""
CREATE TABLE quartos (
    numero INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    capacidade INTEGER NOT NULL,
    tarifa_base REAL NOT NULL,
    status TEXT NOT NULL,
    bloqueio_inicio TEXT,
    bloqueio_fim TEXT,
    motivo_bloqueio TEXT
)
""")

# Tabela de Reservas
cursor.execute("""
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospede_id INTEGER NOT NULL,
    quarto_numero INTEGER NOT NULL,
    data_entrada TEXT NOT NULL,
    data_saida TEXT NOT NULL,
    num_hospedes INTEGER NOT NULL,
    estado TEXT NOT NULL,
    origem TEXT NOT NULL,
    valor_total REAL,
    check_in_real TEXT,
    check_out_real TEXT,
    data_cancelamento TEXT,
    data_no_show TEXT
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")


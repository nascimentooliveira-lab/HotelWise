import sqlite3

conn = sqlite3.connect("hotel.db")
cur = conn.cursor()

# limpa dados
cur.execute("DELETE FROM reservas")
cur.execute("DELETE FROM hospedes")
cur.execute("DELETE FROM pagamentos")
cur.execute("DELETE FROM adicionais")
cur.execute("DELETE FROM quartos")

# reseta os IDs
cur.execute("DELETE FROM sqlite_sequence")

conn.commit()
conn.close()

print("Banco resetado com sucesso")

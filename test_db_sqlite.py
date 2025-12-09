from persistencia.dados import get_db_connection

print(" Testando conexão com o banco SQLite...")

try:
    conn = get_db_connection()
    cur = conn.cursor()

    print("Conectou no banco!")

    #Testar criação de tabela simples
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teste_conexao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT
        );
    """)

    print("Tabela de teste criada/verificada!")

    # Inserir dado
    cur.execute("INSERT INTO teste_conexao (mensagem) VALUES (?)", ("funcionando",))
    conn.commit()

    print("Registro inserido!")

    # Buscar dado
    cur.execute("SELECT * FROM teste_conexao ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()

    if row:
        print("Banco funcionando! Última mensagem:")
        print( row["mensagem"])
    else:
        print("Não encontrou nenhum registro no banco")

    conn.close()

except Exception as e:
    print("ERRO AO TESTAR O BANCO:")
    print(e)

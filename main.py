from flask import Flask, jsonify, request
from datetime import date

from persistencia.dados import (
    get_db_connection,
    seed_dados,
    relatorio_ocupacao
)

app = Flask(__name__)


seed_dados()


# Rotas simples

@app.route("/")
def home():
    return jsonify({"mensagem": "API HotelWise funcionando!"})

@app.route("/quartos", methods=["GET"])
def listar_quartos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quartos")
    dados = cursor.fetchall()

    conn.close()

    # Converte SQLite Row → dicionário
    quartos = [dict(row) for row in dados]
    return jsonify(quartos)

@app.route("/reservas", methods=["GET"])
def listar_reservas():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservas")
    dados = cursor.fetchall()

    conn.close()

    reservas = [dict(row) for row in dados]
    return jsonify(reservas)

@app.route("/relatorio", methods=["GET"])
def api_relatorio():
    inicio = request.args.get("inicio")   # formato "2025-12-01"
    fim = request.args.get("fim")

    if not inicio or not fim:
        return jsonify({
            "erro": "Informe ?inicio=AAAA-MM-DD&fim=AAAA-MM-DD"
        })

    inicio_date = date.fromisoformat(inicio)
    fim_date = date.fromisoformat(fim)

    rel = relatorio_ocupacao(inicio_date, fim_date)

    # Convertendo chaves (date) para string
    rel_convertido = {
        d.isoformat(): rel[d] for d in rel
    }

    return jsonify(rel_convertido)

if __name__ == "__main__":
    app.run(debug=True)

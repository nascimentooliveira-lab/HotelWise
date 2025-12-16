from flask import Blueprint, jsonify, request
from persistencia.quarto_dao import (
    criar_quarto, listar_quartos, buscar_quarto,
    atualizar_quarto, excluir_quarto,
    bloquear_quarto, desbloquear_quarto
)
from datetime import datetime

quartos_bp = Blueprint("quartos", __name__, url_prefix="/quartos")


@quartos_bp.get("/")
def api_listar_quartos():
    quartos = listar_quartos()
    return jsonify([q.to_dict() for q in quartos])


@quartos_bp.post("/")
def api_criar_quarto():
    dados = request.json
    criar_quarto(dados)
    return jsonify({"mensagem": "Quarto criado"}), 201


@quartos_bp.get("/<int:numero>")
def api_buscar_quarto(numero):
    q = buscar_quarto(numero)
    if not q:
        return jsonify({"erro": "Quarto não encontrado"}), 404
    return jsonify(q.to_dict())


@quartos_bp.put("/<int:numero>")
def api_atualizar_quarto(numero):
    q = buscar_quarto(numero)
    if not q:
        return jsonify({"erro": "Quarto não encontrado"}), 404

    dados = request.json
    dados["numero"] = numero
    atualizar_quarto(dados)
    q2 = buscar_quarto(numero)
    return jsonify(q2.to_dict())


@quartos_bp.delete("/<int:numero>")
def api_excluir_quarto(numero):
    excluir_quarto(numero)
    return jsonify({"mensagem": "Quarto removido"})


@quartos_bp.post("/<int:numero>/bloquear")
def api_bloquear_quarto(numero):
    q = buscar_quarto(numero)
    if not q:
        return jsonify({"erro": "Quarto não encontrado"}), 404

    dados = request.json
    inicio = datetime.fromisoformat(dados["inicio"]).date()
    fim = datetime.fromisoformat(dados["fim"]).date()
    motivo = dados.get("motivo", "manutenção")

    bloquear_quarto(numero, inicio, fim, motivo)
    return jsonify(buscar_quarto(numero).to_dict())


@quartos_bp.post("/<int:numero>/desbloquear")
def api_desbloquear_quarto(numero):
    q = buscar_quarto(numero)
    if not q:
        return jsonify({"erro": "Quarto não encontrado"}), 404

    desbloquear_quarto(numero)
    return jsonify(buscar_quarto(numero).to_dict())

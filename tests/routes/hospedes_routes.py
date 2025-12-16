from flask import Blueprint, jsonify, request
from persistencia.hospede_dao import (
    criar_hospede, listar_hospedes, buscar_hospede,
    atualizar_hospede, excluir_hospede
)

hospedes_bp = Blueprint("hospedes", __name__, url_prefix="/hospedes")


@hospedes_bp.get("/")
def api_listar_hospedes():
    hospedes = listar_hospedes()
    return jsonify([h.to_dict() for h in hospedes])


@hospedes_bp.post("/")
def api_criar_hospede():
    dados = request.json
    hid = criar_hospede(dados)
    novo = buscar_hospede(hid)
    return jsonify(novo.to_dict()), 201


@hospedes_bp.get("/<int:id>")
def api_buscar_hospede(id):
    h = buscar_hospede(id)
    if not h:
        return jsonify({"erro": "Hóspede não encontrado"}), 404
    return jsonify(h.to_dict())


@hospedes_bp.put("/<int:id>")
def api_atualizar_hospede(id):
    h = buscar_hospede(id)
    if not h:
        return jsonify({"erro": "Hóspede não encontrado"}), 404
    dados = request.json
    dados["id"] = id
    atualizar_hospede(dados)
    h2 = buscar_hospede(id)
    return jsonify(h2.to_dict())


@hospedes_bp.delete("/<int:id>")
def api_excluir_hospede(id):
    excluir_hospede(id)
    return jsonify({"mensagem": "Hóspede removido"})

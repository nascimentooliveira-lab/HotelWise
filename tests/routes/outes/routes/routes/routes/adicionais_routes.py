from flask import Blueprint, jsonify, request
from persistencia.reserva_dao import buscar_reserva
from persistencia.adicional_dao import adicionar_adicional, listar_adicionais
from modelos.adicional import Adicional

adicionais_bp = Blueprint("adicionais", __name__)


@adicionais_bp.post("/reservas/<int:id>/adicionais")
def api_adicionar_adicional(id):
    reserva = buscar_reserva(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    dados = request.json
    adicional = Adicional(
        reserva_id=id,
        descricao=dados["descricao"],
        valor=dados["valor"]
    )
    adicionar_adicional(adicional)

    return jsonify(adicional.to_dict()), 201


@adicionais_bp.get("/reservas/<int:id>/adicionais")
def api_listar_adicionais(id):
    reserva = buscar_reserva(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    adicionais = listar_adicionais(id)
    return jsonify([a.to_dict() for a in adicionais])

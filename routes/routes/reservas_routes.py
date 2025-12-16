from flask import Blueprint, jsonify, request
from datetime import date, datetime

from modelos.reserva import Reserva
from persistencia.reserva_dao import (
    criar_reserva, listar_reservas, buscar_reserva,
    atualizar_reserva, remover_reserva
)

from persistencia.hospede_dao import buscar_hospede
from persistencia.quarto_dao import buscar_quarto

reservas_bp = Blueprint("reservas", __name__, url_prefix="/reservas")


@reservas_bp.post("/")
def api_criar_reserva():
    dados = request.json

    hospede = buscar_hospede(dados["hospede_id"])
    quarto = buscar_quarto(dados["quarto_numero"])

    if not hospede:
        return jsonify({"erro": "Hóspede não encontrado"}), 404
    if not quarto:
        return jsonify({"erro": "Quarto não encontrado"}), 404

    try:
        reserva = Reserva(
            hospede=hospede,
            quarto=quarto,
            data_entrada=date.fromisoformat(dados["data_entrada"]),
            data_saida=date.fromisoformat(dados["data_saida"]),
            num_hospedes=dados.get("num_hospedes", 1),
            origem=dados.get("origem", "SITE")
        )
        criar_reserva(reserva)
        return jsonify(reserva.to_dict()), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@reservas_bp.get("/")
def api_listar_reservas():
    return jsonify([r.to_dict() for r in listar_reservas()])


@reservas_bp.get("/<int:id>")
def api_buscar_reserva(id):
    r = buscar_reserva(id)
    if not r:
        return jsonify({"erro": "Reserva não encontrada"}), 404
    return jsonify(r.to_dict())


@reservas_bp.put("/<int:id>/checkin")
def api_checkin(id):
    r = buscar_reserva(id)
    if not r:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    try:
        r.fazer_checkin(datetime.now())
        atualizar_reserva(r)
        return jsonify(r.to_dict())
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@reservas_bp.put("/<int:id>/checkout")
def api_checkout(id):
    r = buscar_reserva(id)
    if not r:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    try:
        r.fazer_checkout(datetime.now())
        atualizar_reserva(r)
        return jsonify(r.to_dict())
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@reservas_bp.put("/<int:id>/cancelar")
def api_cancelar(id):
    r = buscar_reserva(id)
    if not r:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    try:
        r.cancelar(date.today())
        atualizar_reserva(r)
        return jsonify(r.to_dict())
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@reservas_bp.put("/<int:id>/noshow")
def api_no_show(id):
    r = buscar_reserva(id)
    if not r:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    try:
        r.marcar_no_show(datetime.now())
        atualizar_reserva(r)
        return jsonify(r.to_dict())
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@reservas_bp.delete("/<int:id>")
def api_excluir_reserva(id):
    remover_reserva(id)
    return jsonify({"mensagem": "Reserva removida"})

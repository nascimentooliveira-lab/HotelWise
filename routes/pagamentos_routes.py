from flask import Blueprint, jsonify, request
from datetime import date
from persistencia.reserva_dao import buscar_reserva
from persistencia.pagamento_dao import registrar_pagamento, listar_pagamentos
from modelos.pagamento import Pagamento

pagamentos_bp = Blueprint("pagamentos", __name__)


@pagamentos_bp.post("/reservas/<int:id>/pagamentos")
def api_registrar_pagamento(id):
    reserva = buscar_reserva(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    dados = request.json
    pagamento = Pagamento(
        reserva_id=id,
        valor=dados["valor"],
        forma=dados.get("forma", "PIX"),
        data_pagamento=dados.get("data_pagamento", date.today().isoformat())
    )
    registrar_pagamento(pagamento)

    return jsonify(pagamento.to_dict()), 201


@pagamentos_bp.get("/reservas/<int:id>/pagamentos")
def api_listar_pagamentos(id):
    reserva = buscar_reserva(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    pagamentos = listar_pagamentos(id)
    return jsonify([p.to_dict() for p in pagamentos])

from flask import Blueprint, jsonify, request
from datetime import date

from relatorios import (
    taxa_ocupacao,
    adr,
    revpar,
    relatorio_cancelamentos,
    relatorio_noshow
)

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


def _parse_datas():
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")

    if not inicio or not fim:
        return None, None, {"erro": "Use ?inicio=YYYY-MM-DD&fim=YYYY-MM-DD"}

    try:
        d1 = date.fromisoformat(inicio)
        d2 = date.fromisoformat(fim)
    except Exception:
        return None, None, {"erro": "Datas inválidas"}

    return d1, d2, None


@relatorios_bp.get("/ocupacao")
def api_relatorio_ocupacao():
    inicio, fim, erro = _parse_datas()
    if erro:
        return jsonify(erro), 400
    valor = taxa_ocupacao(inicio, fim)
    return jsonify({"taxa_ocupacao": valor})


@relatorios_bp.get("/adr")
def api_relatorio_adr():
    inicio, fim, erro = _parse_datas()
    if erro:
        return jsonify(erro), 400
    valor = adr(inicio, fim)
    return jsonify({"adr": valor})


@relatorios_bp.get("/revpar")
def api_relatorio_revpar():
    inicio, fim, erro = _parse_datas()
    if erro:
        return jsonify(erro), 400
    valor = revpar(inicio, fim)
    return jsonify({"revpar": valor})


@relatorios_bp.get("/cancelamentos")
def api_relatorio_cancelamentos():
    inicio, fim, erro = _parse_datas()
    if erro:
        return jsonify(erro), 400
    total = relatorio_cancelamentos(inicio, fim)
    return jsonify({"cancelamentos": total})


@relatorios_bp.get("/noshow")
def api_relatorio_noshow():
    inicio, fim, erro = _parse_datas()
    if erro:
        return jsonify(erro), 400
    total = relatorio_noshow(inicio, fim)
    return jsonify({"noshow": total})

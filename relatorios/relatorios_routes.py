from flask import Blueprint, request, jsonify
from datetime import date
from persistencia.reserva_dao import listar_reservas_completas
from persistencia.quarto_dao import listar_quartos
from persistencia.quarto_dao import buscar_quarto_por_numero

relatorios_bp = Blueprint("relatorios", __name__)

def sobrepoe_periodo(reserva, inicio, fim):
    return not (reserva.data_saida <= inicio or reserva.data_entrada >= fim)

@relatorios_bp.get("/ocupacao")
def taxa_ocupacao():
    inicio = date.fromisoformat(request.args["inicio"])
    fim = date.fromisoformat(request.args["fim"])

    reservas = listar_reservas_completas()
    quartos = listar_quartos()

    dias = (fim - inicio).days
    total_quartos = len(quartos)

    diarias_ocupadas = 0

    for r in reservas:
        if r.estado in {"CHECKIN", "CHECKOUT"} and sobrepoe_periodo(r, inicio, fim):
            entrada = max(r.data_entrada, inicio)
            saida = min(r.data_saida, fim)
            diarias_ocupadas += (saida - entrada).days

    taxa = (diarias_ocupadas / (total_quartos * dias)) * 100 if dias else 0

    return jsonify({
        "taxa_ocupacao_percentual": round(taxa, 2)
    })


@relatorios_bp.get("/receita-por-tipo-quarto")
def calcular_receita_por_tipo(inicio: date, fim: date) -> dict:
    reservas = listar_reservas_completas()
    resultado = {}

    for r in reservas:
        if r.estado not in {"CHECKIN", "CHECKOUT"}:
            continue

        if not sobrepoe_periodo(r, inicio, fim):
            continue

        quarto = buscar_quarto_por_numero(r.quarto_id)
        if not quarto:
            continue

        tipo = quarto.tipo

        entrada = max(r.data_entrada, inicio)
        saida = min(r.data_saida, fim)
        dias = (saida - entrada).days

        if dias <= 0:
            continue

        receita = dias * quarto.tarifa_base
        resultado[tipo] = resultado.get(tipo, 0) + receita

    return resultado


@relatorios_bp.get("/cancelamentos-noshow")
def cancelamentos_no_show():
    inicio = date.fromisoformat(request.args["inicio"])
    fim = date.fromisoformat(request.args["fim"])

    reservas = listar_reservas_completas()

    canceladas = 0
    noshow = 0

    for r in reservas:
        if r.estado == "CANCELADA" and r.data_cancelamento:
            if inicio <= r.data_cancelamento <= fim:
                canceladas += 1

        if r.estado == "NO_SHOW" and r.data_no_show:
            if inicio <= r.data_no_show <= fim:
                noshow += 1

    return jsonify({
        "cancelamentos": canceladas,
        "no_show": noshow
    })

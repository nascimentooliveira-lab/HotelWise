from datetime import date
from persistencia.reserva_dao import listar_reservas_completas
from persistencia.quarto_dao import listar_quartos


def sobrepoe_periodo(reserva, inicio, fim):
    return not (reserva.data_saida <= inicio or reserva.data_entrada >= fim)


def calcular_taxa_ocupacao(inicio: date, fim: date) -> float:
    reservas = listar_reservas_completas()
    quartos = listar_quartos()

    dias = (fim - inicio).days
    total_quartos = len(quartos)

    if dias <= 0 or total_quartos == 0:
        return 0.0

    diarias_ocupadas = 0

    for r in reservas:
        if r.estado in {"CHECKIN", "CHECKOUT"} and sobrepoe_periodo(r, inicio, fim):
            entrada = max(r.data_entrada, inicio)
            saida = min(r.data_saida, fim)
            diarias_ocupadas += (saida - entrada).days

    return round((diarias_ocupadas / (total_quartos * dias)) * 100, 2)


def calcular_receita_por_tipo(inicio: date, fim: date) -> dict:
    reservas = listar_reservas_completas()
    resultado = {}

    for r in reservas:
        if r.estado in {"CHECKIN", "CHECKOUT"} and sobrepoe_periodo(r, inicio, fim):
            tipo = r.quarto.tipo
            dias = (min(r.data_saida, fim) - max(r.data_entrada, inicio)).days
            receita = dias * r.quarto.tarifa_base
            resultado[tipo] = resultado.get(tipo, 0) + receita

    return resultado


def calcular_cancelamentos_noshow(inicio: date, fim: date) -> tuple[int, int]:
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

    return canceladas, noshow

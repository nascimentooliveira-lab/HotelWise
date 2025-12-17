from datetime import date
from persistencia.reserva_dao import listar_reservas_completas
from persistencia.quarto_dao import listar_quartos, buscar_quarto_por_numero

# ======================================================
# Utilitário: converte string ISO ou date em date
# ======================================================
def to_date(valor):
    if valor is None:
        return None
    if isinstance(valor, date):
        return valor
    # SQLite salva datas como string YYYY-MM-DD
    return date.fromisoformat(valor)


# ======================================================
# Verifica se reserva sobrepõe o período informado
# ======================================================
def sobrepoe_periodo(reserva, inicio: date, fim: date) -> bool:
    data_entrada = to_date(reserva["data_entrada"])
    data_saida = to_date(reserva["data_saida"])

    return not (
        data_saida <= inicio or
        data_entrada >= fim
    )


def calcular_taxa_ocupacao(inicio: date, fim: date) -> float:
    reservas = listar_reservas_completas()
    quartos = listar_quartos()

    dias = (fim - inicio).days
    total_quartos = len(quartos)

    if dias <= 0 or total_quartos == 0:
        return 0.0

    diarias_ocupadas = 0
    ESTADOS_OCUPAM = {"CHECKIN", "CHECKOUT", "CONFIRMADA"}

    for r in reservas:
        if r["estado"] not in ESTADOS_OCUPAM:
            continue

        if not sobrepoe_periodo(r, inicio, fim):
            continue

        entrada = max(to_date(r["data_entrada"]), inicio)
        saida = min(to_date(r["data_saida"]), fim)

        noites = (saida - entrada).days
        if noites > 0:
            diarias_ocupadas += noites

    return round((diarias_ocupadas / (total_quartos * dias)) * 100, 2)


# ======================================================
# Relatório: Receita por Tipo de Quarto
# ======================================================
def calcular_receita_por_tipo(inicio: date, fim: date) -> dict:
    reservas = listar_reservas_completas()
    resultado = {}

    for r in reservas:
        if r["estado"] not in {"CHECKIN", "CHECKOUT"}:
            continue

        if not sobrepoe_periodo(r, inicio, fim):
            continue

        # ✅ AQUI ESTÁ A CORREÇÃO
        quarto = buscar_quarto_por_numero(r["numero_quarto"])
        if not quarto:
            continue

        tipo = quarto["tipo"]

        entrada = max(to_date(r["data_entrada"]), inicio)
        saida = min(to_date(r["data_saida"]), fim)
        dias = (saida - entrada).days

        if dias <= 0:
            continue

        receita = dias * quarto["tarifa_base"]
        resultado[tipo] = resultado.get(tipo, 0) + receita

    return resultado

# ======================================================
# Relatório: Cancelamentos e No-show
# ======================================================
def calcular_cancelamentos_noshow(inicio: date, fim: date) -> tuple[int, int]:
    reservas = listar_reservas_completas()
    canceladas = 0
    noshow = 0

    for r in reservas:
        if r["estado"] == "CANCELADA" and r["data_cancelamento"]:
            data_cancel = to_date(r["data_cancelamento"])
            if inicio <= data_cancel <= fim:
                canceladas += 1

        if r["estado"] == "NO_SHOW" and r["data_no_show"]:
            data_ns = to_date(r["data_no_show"])
            if inicio <= data_ns <= fim:
                noshow += 1

    return canceladas, noshow


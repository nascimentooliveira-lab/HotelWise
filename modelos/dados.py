import json
from datetime import date, datetime

from modelos.hospede import Hospede
from modelos.quarto import Quarto
from modelos.reserva import Reserva
from modelos.pagamento import Pagamento
from modelos.adicional import Adicional


# ==========================
#   SERIALIZAÇÃO
# ==========================

def date_to_str(d: date):
    return d.strftime("%Y-%m-%d")

def str_to_date(s: str):
    return datetime.strptime(s, "%Y-%m-%d").date()

def quarto_to_dict(quarto: Quarto):
    return {
        "numero": quarto.numero,
        "tipo": quarto.tipo,
        "capacidade": quarto.capacidade,
        "tarifa_base": quarto.tarifa_base,
        "status": quarto.status
    }

def dict_to_quarto(data: dict) -> Quarto:
    return Quarto(
        numero=data["numero"],
        tipo=data["tipo"],
        capacidade=data["capacidade"],
        tarifa_base=data["tarifa_base"],
        status=data.get("status", "DISPONIVEL")
    )

def hospede_to_dict(h: Hospede):
    return {
        "nome": h.nome,
        "documento": h.documento,
        "email": h.email,
        "telefone": h.telefone
    }

def dict_to_hospede(data: dict) -> Hospede:
    return Hospede(
        nome=data["nome"],
        documento=data["documento"],
        email=data["email"],
        telefone=data["telefone"]
    )

def pagamento_to_dict(pag: Pagamento):
    return {
        "valor": pag.valor,
        "forma": pag.forma,
        "data": pag.data.strftime("%Y-%m-%d %H:%M:%S")
    }

def dict_to_pagamento(data: dict) -> Pagamento:
    return Pagamento(
        valor=data["valor"],
        forma=data["forma"],
        data=datetime.strptime(data["data"], "%Y-%m-%d %H:%M:%S")
    )

def adicional_to_dict(ad: Adicional):
    return {
        "nome": ad.nome,
        "valor": ad.valor
    }

def dict_to_adicional(data: dict) -> Adicional:
    return Adicional(
        nome=data["nome"],
        valor=data["valor"]
    )

def reserva_to_dict(r: Reserva):
    return {
        "hospede": r.hospede.documento,  # referência pelo documento
        "quarto": r.quarto.numero,       # referência pelo nº do quarto
        "data_entrada": date_to_str(r.data_entrada),
        "data_saida": date_to_str(r.data_saida),
        "numero_hospedes": r.numero_hospedes,
        "pagamentos": [pagamento_to_dict(p) for p in r.pagamentos],
        "adicionais": [adicional_to_dict(a) for a in r.adicionais],
    }

def dict_to_reserva(data: dict, hospedes, quartos) -> Reserva:
    h = hospedes[data["hospede"]]  # pega pelo documento
    q = quartos[data["quarto"]]     # pega pelo número

    res = Reserva(
        hospede=h,
        quarto=q,
        data_entrada=str_to_date(data["data_entrada"]),
        data_saida=str_to_date(data["data_saida"]),
        numero_hospedes=data["numero_hospedes"]
    )

    # Carregar pagamentos
    for p in data.get("pagamentos", []):
        res.adicionar_pagamento(dict_to_pagamento(p))

    # Carregar adicionais
    for a in data.get("adicionais", []):
        res.adicionar_adicional(dict_to_adicional(a))

    return res

def salvar_quartos(lista, arquivo="quartos.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump([quarto_to_dict(q) for q in lista], f, indent=4)

def carregar_quartos(arquivo="quartos.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return []
    return [dict_to_quarto(q) for q in dados]

def salvar_hospedes(lista, arquivo="hospedes.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump([hospede_to_dict(h) for h in lista], f, indent=4)

def carregar_hospedes(arquivo="hospedes.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return []
    return [dict_to_hospede(h) for h in dados]

def salvar_reservas(lista, arquivo="reservas.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump([reserva_to_dict(r) for r in lista], f, indent=4)

def carregar_reservas(arquivo="reservas.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return []

    hospedes = {h.documento: h for h in carregar_hospedes()}
    quartos = {q.numero: q for q in carregar_quartos()}

    reservas = []
    for r in dados:
        reservas.append(dict_to_reserva(r, hospedes, quartos))

    return reservas

def criar_seed():
    quartos = [
        Quarto(101, "SIMPLES", 2, 150),
        Quarto(102, "SIMPLES", 2, 150),
        Quarto(201, "DUPLO", 3, 250),
        Quarto(202, "DUPLO", 3, 250),
        Quarto(301, "LUXO", 4, 500),
        Quarto(302, "LUXO", 4, 600),
    ]

    hospedes = [
        Hospede("João Silva", "11111111111", "joao@email.com", "99999-0000"),
        Hospede("Maria Souza", "22222222222", "maria@email.com", "88888-0000"),
    ]

    salvar_quartos(quartos)
    salvar_hospedes(hospedes)
    salvar_reservas([])

    print("Seed inicial criado")


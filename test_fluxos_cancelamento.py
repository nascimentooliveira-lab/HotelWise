from datetime import date
from modelos.hospede import Hospede
from modelos.quarto import Quarto
from modelos.reserva import Reserva
from modelos.pagamento import Pagamento


def criar_reserva():
    h = Hospede("AAA", "123", "a@a.com", "9999")
    q = Quarto(101, "DUPLO", 2, 200)
    r = Reserva(h, q, date(2025, 3, 10), date(2025, 3, 15))
    return r

# CANCELAMENTO SEM MULTA (mais de 7 dias antes)
def test_cancelamento_sem_multa():
    r = criar_reserva()

    # Cancelamento 20 dias antes
    data_cancelamento = date(2025, 2, 20)
    r.cancelar(data_cancelamento)

    assert r.estado == "CANCELADA"
    assert r.data_cancelamento == data_cancelamento

    # multa deve ser zero
    assert r.total_devido() == 0

# 2) CANCELAMENTO COM MULTA DE 1 DIÁRIA

def test_cancelamento_com_multa_1_diaria():
    r = criar_reserva()

    # 5 dias antes da entrada → multa de 1 diária
    data_cancelamento = date(2025, 3, 5)
    r.cancelar(data_cancelamento)

    # Preço diário base
    diaria = r.quarto.tarifa_base

    assert r.estado == "CANCELADA"
    assert r.total_devido() == diaria

# 3) CANCELAMENTO NO DIA (MÁXIMA MULTA)

def test_cancelamento_no_dia_multa_total():
    r = criar_reserva()

    # A reserva vai do dia 10 ao 15 → 5 diárias
    data_cancelamento = date(2025, 3, 10)
    r.cancelar(data_cancelamento)

    total_reserva = r.valor_total()

    assert r.estado == "CANCELADA"
    assert r.total_devido() == total_reserva


# CANCELAMENTO E PAGAMENTO JÁ EFETUADO

def test_cancelamento_com_pagamento_previo():
    r = criar_reserva()

    # adicionar pagamento antes do cancelamento
    pg = Pagamento(300, "PIX")
    r.adicionar_pagamento(pg)

    r.cancelar(date(2025, 3, 7))  # menos de 7 dias → multa 1 diária

    multa = r.quarto.tarifa_base
    pago = r.total_pago()

    # total devido = multa - valor já pago (não negativo)
    total_final = max(multa - pago, 0)

    assert r.total_devido() == total_final

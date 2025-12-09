from datetime import date, timedelta, datetime
from modelos.hospede import Hospede
from modelos.quarto import Quarto
from modelos.reserva import Reserva
from modelos.pagamento import Pagamento


def criar_reserva_basica():
    h = Hospede("Teste", "999", "teste@mail.com", "9999")
    q = Quarto(101, "DUPLO", 2, 200)
    r = Reserva(h, q, date(2025, 1, 10), date(2025, 1, 12))
    return r

#  TESTE: CONFIRMAÇÃO

def test_confirmacao():
    r = criar_reserva_basica()
    r.confirmar()
    assert r.estado == "CONFIRMADA"

#  TESTE: CHECK-IN

def test_checkin():
    r = criar_reserva_basica()
    r.confirmar()

    r.fazer_checkin(date(2025, 1, 10))

    assert r.estado == "CHECKIN"
    assert r.check_in_real is not None
    assert r.quarto.status == "OCUPADO"



#  TESTE: CHECK-OUT

def test_checkout():
    r = criar_reserva_basica()
    r.confirmar()
    r.fazer_checkin(date(2025, 1, 10))

    # pagamento total fictício
    pagamento = Pagamento(400, "PIX")
    r.adicionar_pagamento(pagamento)

    r.fazer_checkout(date(2025, 1, 12))

    assert r.estado == "CHECKOUT"
    assert r.check_out_real is not None
    assert r.quarto.status == "DISPONIVEL"

#  TESTE: CANCELAMENTO

def test_cancelamento():
    r = criar_reserva_basica()
    r.cancelar(date(2025, 1, 5))

    assert r.estado == "CANCELADA"
    assert r.data_cancelamento == date(2025, 1, 5)

#  TESTE: NO SHOW

def test_no_show():
    r = criar_reserva_basica()
    r.confirmar()

    r.marcar_no_show(date(2025, 1, 15))

    assert r.estado == "NO_SHOW"
    assert r.data_no_show == date(2025, 1, 15)

#  TESTE: BLOQUEIO DE QUARTO

def test_bloqueio_quarto():
    q = Quarto(102, "SIMPLES", 1, 150)
    q.bloquear("2025-02-01", "2025-02-10", "Pintura")

    assert q.status == "MANUTENCAO"
    assert q.esta_bloqueado("2025-02-05")
    assert not q.esta_bloqueado("2025-02-15")

    # tentativa de reserva durante bloqueio → deve falhar
    h = Hospede("AAA", "123", "a@a.com", "9999")

    try:
        Reserva(h, q, date(2025, 2, 3), date(2025, 2, 6))
        assert False, "Reserva deveria falhar pois o quarto está bloqueado"
    except ValueError:
        assert True

    
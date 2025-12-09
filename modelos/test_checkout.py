from datetime import date
from modelos.hospede import Hospede
from modelos.quarto import Quarto
from modelos.reserva import Reserva


def criar_reserva():
    h = Hospede("Teste", "111", "t@mail.com", "999")
    q = Quarto(101, "SIMPLES", 1, 100)
    return Reserva(h, q, date(2025,1,10), date(2025,1,13))  # 3 diárias


#  CHECKOUT ANTECIPADO 

def test_checkout_antecipado():
    r = criar_reserva()
    r.confirmar()
    r.fazer_checkin(date(2025,1,10))

    r.fazer_checkout(date(2025,1,11))  # saiu antes

    assert r.total_devido() == 1 * 100  # 1 diária


# CHECKOUT NORMAL (DATA EXATA)

def test_checkout_normal():
    r = criar_reserva()
    r.confirmar()
    r.fazer_checkin(date(2025,1,10))

    r.fazer_checkout(date(2025,1,13))  # saiu certo

    assert r.total_devido() == r.valor_total()


#  CHECKOUT TARDIO 

def test_checkout_tardio():
    r = criar_reserva()
    r.confirmar()
    r.fazer_checkin(date(2025,1,10))

    r.fazer_checkout(date(2025,1,14))  # 1 dia extra

    total_original = r.valor_total()       # 3 diárias
    extra = 100                            # 1 diária extra

    assert r.total_devido() == total_original + extra

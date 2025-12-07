import pytest
from .quarto import Quarto
from .hospede import Hospede
from .reserva import Reserva
from datetime import date



def test_criar_quarto():
    q = Quarto(101, "SIMPLES", 2, 150.0)
    assert q.numero == 101
    assert q.tipo == "SIMPLES"
    assert q.capacidade == 2
    assert q.tarifa_base == 150.0


def test_quarto_str():
    q = Quarto(202, "LUXO", 3, 500)
    assert "Quarto 202" in str(q)


def test_quarto_lt():
    q1 = Quarto(100, "SIMPLES", 2, 100)
    q2 = Quarto(200, "DUPLO", 2, 150)
    assert q1 < q2


def test_criar_hospede():
    h = Hospede("Ana", "123", "ana@mail.com", "8899")
    assert h.nome == "Ana"


def test_criar_reserva():
    h = Hospede("João", "777", "joao@mail.com", "9999")
    q = Quarto(101, "DUPLO", 2, 200)

    r = Reserva(h, q, date(2025, 1, 10), date(2025, 1, 12))  # Estado padrão

    assert len(r) == 2
    assert r.quarto.capacidade == 2
    assert r.hospede.nome == "João"

def criar_reserva_basica():
    h = Hospede(id=1, nome="Teste", telefone="0000")
    q = Quarto(numero=1, tipo="SIMPLES", capacidade=2, tarifa_base=100)
    return Reserva(h, q, date(2025,1,10), date(2025,1,12))

def test_confirmar():
    r = criar_reserva_basica()
    r.confirmar()
    assert r.estado == "CONFIRMADA"

def test_checkin():
    r = criar_reserva_basica()
    r.confirmar()
    r.fazer_checkin(date(2025,1,10))
    assert r.estado == "CHECKIN"

def test_cancelamento():
    r = criar_reserva_basica()
    r.cancelar()
    assert r.estado == "CANCELADA"

def test_no_show():
    r = criar_reserva_basica()
    r.confirmar()
    r.marcar_no_show(date(2025,1,11))
    assert r.estado == "NO_SHOW"
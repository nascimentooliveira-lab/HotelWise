import pytest
from modelos.quarto import Quarto
from modelos.hospede import Hospede
from modelos.reserva import Reserva
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


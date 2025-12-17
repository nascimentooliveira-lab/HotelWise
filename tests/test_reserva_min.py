import pytest
from datetime import date, timedelta

from modelos.reserva import Reserva


# ===== DUMMIES =====

class HospedeFake:
    def __init__(self):
        self.id = 1

    def adicionar_reserva(self, reserva):
        pass


class QuartoFake:
    def __init__(self):
        self.numero = 101
        self.tipo = "SIMPLES"
        self.capacidade = 2
        self.tarifa_base = 100.0
        self.reservas = []
        self.status = "DISPONIVEL"

    def adicionar_reserva(self, reserva):
        self.reservas.append(reserva)

    def ocupar(self):
        self.status = "OCUPADO"

    def liberar(self):
        self.status = "DISPONIVEL"


# ===== FIXTURE =====

@pytest.fixture
def reserva():
    hoje = date.today()
    return Reserva(
        hospede=HospedeFake(),
        quarto=QuartoFake(),
        data_entrada=hoje,
        data_saida=hoje + timedelta(days=2),
        num_hospedes=2
    )


# ===== TESTES ESSENCIAIS =====

def test_criar_reserva():
    hoje = date.today()
    reserva = Reserva(
        HospedeFake(),
        QuartoFake(),
        hoje,
        hoje + timedelta(days=1)
    )
    assert reserva.estado == "PENDENTE"


def test_confirmar_reserva(reserva):
    reserva.confirmar()
    assert reserva.estado == "CONFIRMADA"


def test_checkin(reserva):
    reserva.confirmar()
    reserva.fazer_checkin(agora=date.today())
    assert reserva.estado == "CHECKIN"
    assert reserva.quarto.status == "OCUPADO"


def test_checkout(reserva):
    reserva.confirmar()
    reserva.fazer_checkin(agora=date.today())
    reserva.fazer_checkout(agora=date.today())
    assert reserva.estado == "CHECKOUT"
    assert reserva.quarto.status == "DISPONIVEL"

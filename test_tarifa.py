from datetime import date
from modelos.hospede import Hospede
from modelos.quarto import Quarto
from modelos.reserva import Reserva

def test_tarifa_diaria():
    h = Hospede("Teste", "123")
    q = Quarto(101, "SIMPLES", 1, 150)

    r = Reserva(h, q, date(2025,1,10), date(2025,1,12))

    assert r.tarifa_diaria() == 150

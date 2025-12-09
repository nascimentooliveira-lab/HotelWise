from datetime import date
from modelos.quarto import Quarto
from modelos.reserva import Reserva
from modelos.hospede import Hospede

# Criar o quarto com tarifa base 100
quarto = Quarto(numero=101, tipo="SIMPLES", capacidade=2, tarifa_base=100)

# Criar hóspede
hospede = Hospede(nome="Teste", documento="123456789")

# Reserva só em dia de semana (terça a quinta)
reserva1 = Reserva(hospede, quarto, date(2025, 1, 7), date(2025, 1, 9))  # Terça e quarta
print("Reserva dias normais (sem fim de semana ou temporada):", reserva1.valor_total())
# Esperado: 2 diárias * 100 = 200

# Reserva incluindo sexta-feira (fim de semana)
reserva2 = Reserva(hospede, quarto, date(2025, 1, 10), date(2025, 1, 12))  # Sexta e sábado
print("Reserva com fim de semana:", reserva2.valor_total())
# Esperado:
# Sexta (tarifa_base * 1.2) = 120
# Sábado (tarifa_base * 1.2) = 120
# Total = 240

# Reserva em dezembro (alta temporada)
reserva3 = Reserva(hospede, quarto, date(2025, 12, 10), date(2025, 12, 12))  # Dezembro
print("Reserva em alta temporada (dezembro):", reserva3.valor_total())
# Esperado:
# 2 diárias * (tarifa_base * 1.3) = 2 * 130 = 260

# Reserva com fim de semana e alta temporada juntas (dezembro sexta e sábado)
reserva4 = Reserva(hospede, quarto, date(2025, 12, 12), date(2025, 12, 14))  # Sexta e sábado em dezembro
print("Reserva fim de semana + alta temporada:", reserva4.valor_total())

# Sexta: 100 * 1.2 * 1.3 = 156
# Sábado: 100 * 1.2 * 1.3 = 156
# Total: 312

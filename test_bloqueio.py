from datetime import date
from modelos.quarto import Quarto
from modelos.reserva import Reserva
from modelos.hospede import Hospede

# Cria o quarto
q = Quarto(numero=101, tipo="SIMPLES", capacidade=2, tarifa_base=100)

# Bloqueia o quarto para manutenção de 10/01/2025 até 15/01/2025
q.bloquear(motivo="Reforma do piso", inicio=date(2025, 1, 10), fim=date(2025, 1, 15))

# Cria hóspede para teste
h = Hospede(nome="Teste", documento="123456789")

# Tenta reservar no período bloqueado -> deve falhar
try:
    r1 = Reserva(hospede=h, quarto=q, data_entrada=date(2025,1,12), data_saida=date(2025,1,14))
    print("Erro: Reserva criada dentro do período bloqueado, mas deveria falhar!")
except ValueError as e:
    print("Reserva bloqueada corretamente:", e)

# Tenta reservar fora do período bloqueado -> deve passar
try:
    r2 = Reserva(hospede=h, quarto=q, data_entrada=date(2025,1,16), data_saida=date(2025,1,18))
    print("Reserva criada fora do período bloqueado com sucesso.")
except ValueError as e:
    print("Erro inesperado:", e)

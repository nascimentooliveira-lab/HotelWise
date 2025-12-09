from datetime import date
from relatorios.relatorio_ocupacao import calcular_ocupacao

print("\nTestando relatório de OCUPAÇÃO...\n")

inicio = date(2025, 1, 1)
fim = date(2025, 1, 5)

resultado = calcular_ocupacao(inicio, fim)

for linha in resultado:
    print(
        linha["data"],
        "| Ocupados:", linha["ocupados"],
        "| Livres:", linha["livres"],
        "| Taxa:", linha["taxa"], "%"
    )


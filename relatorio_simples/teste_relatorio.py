from datetime import date
from persistencia.dados import relatorio_ocupacao

inicio = date(2025, 12, 1)
fim = date(2025, 12, 10)

rel = relatorio_ocupacao(inicio, fim)

for dia, info in rel.items():
    print(
        dia,
        "| Ocupados:", info["ocupados"],
        "| Livres:", info["livres"],
        "| Ocupação:", f"{info['taxa_ocupacao']}%"
    )

from datetime import date
from persistencia.dados import relatorio_ocupacao, seed_dados


def imprimir_relatorio_detalhado(rel):
    print("\n=========== RELATÓRIO DE OCUPAÇÃO ===========")
    print("Data       | Ocupados | Livres | Taxa  | Visual")
    print("-----------------------------------------------")

    for dia, info in rel.items():
        ocup = info["ocupados"]
        livres = info["livres"]
        taxa = info["taxa_ocupacao"]

        print(f"{dia} |    {ocup:^3}   |   {livres:^3}  | {taxa:>5} % ")

    print("-----------------------------------------------")

    total_dias = len(rel)
    media_ocupacao = sum(info["taxa_ocupacao"] for info in rel.values()) / total_dias

    print(f"Média geral de ocupação: {media_ocupacao:.2f}%")
    print("===============================================\n")


inicio = date(2025, 12, 1)
fim = date(2025, 12, 10)

rel = relatorio_ocupacao(inicio, fim)
imprimir_relatorio_detalhado(rel)

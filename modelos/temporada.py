from datetime import datetime, date

class Temporada:
    """
    Representa um intervalo de temporada com multiplicador.
    Ex.: alta temporada, férias, feriados, etc.
    """
    def __init__(self, nome: str, inicio: date, fim: date, multiplicador: float):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.multiplicador = multiplicador

    @staticmethod
    def from_dict(data: dict):
        return Temporada(
            nome=data.get("nome"),
            inicio=datetime.fromisoformat(data["inicio"]).date(),
            fim=datetime.fromisoformat(data["fim"]).date(),
            multiplicador=float(data["multiplicador"])
        )

    def contains(self, dia: date):
        return self.inicio <= dia <= self.fim

    def to_dict(self):
        return {
            "nome": self.nome,
            "inicio": self.inicio.isoformat(),
            "fim": self.fim.isoformat(),
            "multiplicador": self.multiplicador
        }

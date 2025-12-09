from datetime import date

class Bloqueio:
    def __init__(self, motivo: str, inicio: date, fim: date):
        self.motivo = motivo
        self.inicio = inicio
        self.fim = fim

    def esta_bloqueado(self, data: date) -> bool:
        return self.inicio <= data <= self.fim

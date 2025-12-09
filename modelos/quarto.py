from datetime import date, datetime
import sqlite3
from .bloqueio import Bloqueio

class Quarto:
    TIPOS_VALIDOS = {"SIMPLES", "DUPLO", "LUXO"}
    STATUS_VALIDOS = {"DISPONIVEL", "OCUPADO", "MANUTENCAO", "BLOQUEADO"}

    def __init__(self, numero: int, tipo: str, capacidade: int, tarifa_base: float, status="DISPONIVEL"):
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.tarifa_base = tarifa_base
        self.status = status
        self.bloqueio = []
        self.__reservas = []   
        self.__motivo_bloqueio = None
        self.__inicio_bloqueio = None
        self.__fim_bloqueio = None

    def bloquear(self, motivo: str, inicio: date, fim: date):
        self.bloqueios.append(Bloqueio(motivo, inicio, fim))

    def esta_bloqueado(self, data: date) -> bool:
        return any(bloqueio.esta_bloqueado(data) for bloqueio in self.bloqueios)
    
    # Função auxiliar
    
    def _to_date(self, valor):
        if isinstance(valor, date):
            return valor
        if isinstance(valor, str):
            return datetime.strptime(valor, "%Y-%m-%d").date()
        raise TypeError("Data deve ser datetime.date ou string no formato YYYY-MM-DD")

    
    # Relacionamentos
    
    @property
    def reservas(self):
        return list(self.__reservas)

    def adicionar_reserva(self, reserva):
        self.__reservas.append(reserva)

    
    # Propriedades diversas
    
    @property
    def periodo_bloqueio(self):
        return (self.__inicio_bloqueio, self.__fim_bloqueio)
    
    @property
    def bloqueios(self):
      """Retorna informações do bloqueio atual."""
      if not self.__inicio_bloqueio or not self.__fim_bloqueio:
          return None

      return {
        "motivo": self.__motivo_bloqueio,
        "inicio": self.__inicio_bloqueio,
        "fim": self.__fim_bloqueio
    }

    # BLOQUEIO CORRIGIDO
    
    def bloquear(self, inicio, fim, motivo: str):
        """Bloqueia o quarto para manutenção."""
        inicio = self._to_date(inicio)
        fim = self._to_date(fim)

        if inicio > fim:
            raise ValueError("Data inicial não pode ser maior que a data final.")

        self.status = "MANUTENCAO"
        self.__motivo_bloqueio = motivo
        self.__inicio_bloqueio = inicio
        self.__fim_bloqueio = fim

    def desbloquear(self):
        self.status = "DISPONIVEL"
        self.__motivo_bloqueio = None
        self.__inicio_bloqueio = None
        self.__fim_bloqueio = None

    def esta_bloqueado(self, data):
        data = self._to_date(data)

        if self.status != "MANUTENCAO":
            return False
        if not self.__inicio_bloqueio or not self.__fim_bloqueio:
            return False

        return self.__inicio_bloqueio <= data <= self.__fim_bloqueio

    # Representações
    
    def __str__(self):
        return f"Quarto {self.numero} ({self.tipo}) - Capacidade: {self.capacidade}"

    def __lt__(self, other):
        return self.numero < other.numero


    # Persistência
    
    def to_tuple(self):
        return (
            self.numero,
            self.tipo,
            self.capacidade,
            self.tarifa_base,
            self.status,
            self.__motivo_bloqueio,
            self.__inicio_bloqueio.isoformat() if self.__inicio_bloqueio else None,
            self.__fim_bloqueio.isoformat() if self.__fim_bloqueio else None
        )

    @staticmethod
    def from_db_row(row: sqlite3.Row):
        quarto = Quarto(
            numero=row['numero'],
            tipo=row['tipo'],
            capacidade=row['capacidade'],
            tarifa_base=row['tarifa_base'],
            status=row['status']
        )

        # Converter datas do banco
        inicio = row['inicio_bloqueio']
        fim = row['fim_bloqueio']

        quarto._Quarto__motivo_bloqueio = row['motivo_bloqueio']
        quarto._Quarto__inicio_bloqueio = (
            date.fromisoformat(inicio) if inicio else None
        )
        quarto._Quarto__fim_bloqueio = (
            date.fromisoformat(fim) if fim else None
        )

        return quarto

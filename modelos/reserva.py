from datetime import date
from modelos.hospede import Hospede
from modelos.quarto import Quarto

class Reserva:
    """
    Representa uma reserva básica do hotel (estrutura da Semana 2).
    """

    def __init__(self, hospede: Hospede, quarto: Quarto,
                 data_entrada: date, data_saida: date, numero_hospedes: int):

        self.hospede = hospede
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.numero_hospedes = numero_hospedes

    # -------- PROPRIEDADES --------

    @property
    def hospede(self):
        return self.__hospede

    @hospede.setter
    def hospede(self, valor):
        if not isinstance(valor, Hospede):
            raise TypeError("hospede deve ser um objeto Hospede.")
        self.__hospede = valor

    @property
    def quarto(self):
        return self.__quarto

    @quarto.setter
    def quarto(self, valor):
        if not isinstance(valor, Quarto):
            raise TypeError("quarto deve ser um objeto Quarto.")
        self.__quarto = valor

    @property
    def data_entrada(self):
        return self.__data_entrada

    @data_entrada.setter
    def data_entrada(self, valor):
        if not isinstance(valor, date):
            raise TypeError("data_entrada deve ser um objeto date.")
        self.__data_entrada = valor

    @property
    def data_saida(self):
        return self.__data_saida

    @data_saida.setter
    def data_saida(self, valor):
        if not isinstance(valor, date):
            raise TypeError("data_saida deve ser um objeto date.")
        if hasattr(self, "_Reserva__data_entrada") and valor <= self.__data_entrada:
            raise ValueError("data_saida deve ser maior que data_entrada.")
        self.__data_saida = valor

    @property
    def numero_hospedes(self):
        return self.__numero_hospedes

    @numero_hospedes.setter
    def numero_hospedes(self, valor):
        if valor < 1:
            raise ValueError("A reserva deve ter pelo menos 1 hóspede.")
        if hasattr(self, "_Reserva__quarto") and valor > self.quarto.capacidade:
            raise ValueError("Número de hóspedes excede a capacidade do quarto.")
        self.__numero_hospedes = valor

    # -------- MÉTODO ESPECIAL --------

    def __len__(self):
        """Retorna o número de diárias."""
        return (self.data_saida - self.data_entrada).days


from datetime import date, timedelta
from modelos.hospede import Hospede
from modelos.quarto import Quarto


class Reserva:
    """
    Representa uma reserva completa do hotel.
    - Valida capacidade
    - Impede overbooking
    - Controla estados
    - Calcula valor total
    """

    ESTADOS_VALIDOS = {
        "PENDENTE", "CONFIRMADA", "CHECKIN",
        "CHECKOUT", "CANCELADA", "NO_SHOW"
    }

    ORIGENS_VALIDAS = {"SITE", "TELEFONE", "BALCAO"}

    def __init__(self, hospede: Hospede, quarto: Quarto,
                 data_entrada: date, data_saida: date,
                 numero_hospedes: int, origem: str = "SITE"):

        self.hospede = hospede
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.numero_hospedes = numero_hospedes
        self.estado = "PENDENTE"
        self.origem = origem.upper()

        if self.origem not in self.ORIGENS_VALIDAS:
            raise ValueError(f"Origem deve ser um de: {self.ORIGENS_VALIDAS}")

        # Agregações
        self.__pagamentos = []
        self.__adicionais = []

        # Impedir overbooking
        self.__validar_disponibilidade(quarto)

        # Registrar relação bidirecional
        hospede.adicionar_reserva(self)
        quarto.adicionar_reserva(self)

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

        if hasattr(self, "_Reserva__data_entrada") and valor <= self.data_entrada:
            raise ValueError("data_saida deve ser ao menos 1 dia após data_entrada.")

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

    # MÉTODOS DE NEGÓCIO 

    def alterar_estado(self, novo_estado: str):
        novo_estado = novo_estado.upper()
        if novo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado deve ser um de: {self.ESTADOS_VALIDOS}")
        self.estado = novo_estado

    def __validar_disponibilidade(self, quarto: Quarto):
        """Impede overbooking verificando reservas existentes."""
        for r in quarto.reservas:
            # Se datas se sobrepõem → conflito
            if not (self.data_saida <= r.data_entrada or self.data_entrada >= r.data_saida):
                raise ValueError(
                    f"Quarto {quarto.numero} indisponível no período solicitado."
                )

    #CÁLCULO DE VALOR 

    def valor_total(self):
        total = 0
        diaria = self.quarto.tarifa_base

        atual = self.data_entrada
        while atual < self.data_saida:

            preco = diaria

            # Fim de semana (+20%)
            if atual.weekday() in (4, 5):  # sexta/sábado
                preco *= 1.20

            # Temporada (exemplo: dezembro)
            if atual.month == 12:
                preco *= 1.30

            total += preco
            atual += timedelta(days=1)

        return round(total, 2)

    # AGREGADOS

    @property
    def pagamentos(self):
        return list(self.__pagamentos)

    def adicionar_pagamento(self, pagamento):
        self.__pagamentos.append(pagamento)

    @property
    def adicionais(self):
        return list(self.__adicionais)

    def adicionar_adicional(self, adicional):
        self.__adicionais.append(adicional)

    # MÉTODOS ESPECIAIS

    def __len__(self):
        """Número de diárias."""
        return (self.data_saida - self.data_entrada).days

    def __str__(self):
        return f"Reserva de {self.hospede.nome} no quarto {self.quarto.numero}"


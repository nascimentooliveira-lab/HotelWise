class Adicional:
    """
    Representa um lançamento extra na reserva (ex.: frigobar, estacionamento).
    """

    def __init__(self, nome: str, valor: float):
        if not nome.strip():
            raise ValueError("Nome do adicional não pode ser vazio.")

        if valor <= 0:
            raise ValueError("Valor do adicional deve ser maior que zero.")

        self.__nome = nome
        self.__valor = valor

    @property
    def nome(self):
        return self.__nome

    @property
    def valor(self):
        return self.__valor

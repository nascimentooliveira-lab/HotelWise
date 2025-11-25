from datetime import datetime

class Pagamento:
    """
    Representa um pagamento efetuado para uma reserva.
    """

    FORMAS_VALIDAS = {"DINHEIRO", "CREDITO", "DEBITO", "PIX"}

    def __init__(self, valor: float, forma: str, data: datetime = None):
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero.")
        
        forma = forma.upper()
        if forma not in Pagamento.FORMAS_VALIDAS:
            raise ValueError(f"Forma de pagamento inválida. Use: {Pagamento.FORMAS_VALIDAS}")

        self.__valor = valor
        self.__forma = forma
        self.__data = data if data else datetime.now()

    @property
    def valor(self):
        return self.__valor

    @property
    def forma(self):
        return self.__forma

    @property
    def data(self):
        return self.__data

    
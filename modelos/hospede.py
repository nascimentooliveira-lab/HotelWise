from modelos.pessoa import Pessoa

class Hospede(Pessoa):
    def __init__(self, nome: str, documento: str, email: str, telefone: str):
        super().__init__(nome, documento, email, telefone)
        self.__reservas = []

    def adicionar_reserva(self, reserva):
        self.__reservas.append(reserva)


    

from pessoa import pessoa 
class Hospede(pessoa):
    """
    Representa um hóspede do hotel.
    """
    def __init__(self, nome: str, documento: str, email: str, telefone: str,):
      super().__init__(self, nome, documento, email, telefone)
      self.__reservas = []   # << RELACIONAMENTO

    def adicionar_reserva(self, reserva):
        self.__reservas.append(reserva)

    

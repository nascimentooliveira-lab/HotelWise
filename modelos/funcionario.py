from .pessoa import Pessoa

class Funcionario(Pessoa):
    """
    Representa um funcionário do hotel.
    """
    def __init__(self, nome, documento, email, telefone, cargo):
        super().__init__(nome, documento, email, telefone)
        self.cargo = cargo
        
    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, valor):
        if not valor.strip():
            raise ValueError("Cargo não pode ser vazio.")
        self.__cargo = valor.strip()

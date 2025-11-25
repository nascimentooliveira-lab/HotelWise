class Hospede:
    """
    Representa um hóspede do hotel.
    """

    def __init__(self, nome: str, documento: str, email: str, telefone: str):
        self.nome = nome
        self.documento = documento
        self.email = email
        self.telefone = telefone
        self.__reservas = []   # << RELACIONAMENTO

    @property
    def reservas(self):
        return list(self.__reservas)

    def adicionar_reserva(self, reserva):
        self.__reservas.append(reserva)

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = valor

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not valor.strip():
            raise ValueError("Documento não pode ser vazio.")
        self.__documento = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("E-mail inválido.")
        self.__email = valor

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, valor):
        if not valor.strip():
            raise ValueError("Telefone não pode ser vazio.")
        self.__telefone = valor

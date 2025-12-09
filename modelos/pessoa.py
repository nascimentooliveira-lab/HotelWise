class Pessoa:
    """
    Classe base para representar pessoas do sistema (hóspedes e funcionários).
    """
    def __init__(self, id=None, nome="", documento="", email="", telefone=""):
        self.id = id
        self.nome = nome
        self.documento = documento
        self.email = email
        self.telefone = telefone



    # -------- PROPRIEDADES --------

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def documento(self):
        return self.__documento
    
    @documento.setter
    def documento(self, valor):
        self._documento = valor  

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
       self._email = valor  # não validar

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, valor):
        if not valor.replace(" ", "").isdigit():
            raise ValueError("Telefone deve conter apenas números.")
        self.__telefone = valor

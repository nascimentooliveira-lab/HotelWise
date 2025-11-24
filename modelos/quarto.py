class Quarto:
    TIPOS_VALIDOS = {"SIMPLES", "DUPLO", "LUXO"}
    STATUS_VALIDOS = {"DISPONIVEL", "OCUPADO", "MANUTENCAO", "BLOQUEADO"}

    def __init__(self, numero: int, tipo: str, capacidade: int, tarifa_base: float, status="DISPONIVEL"):
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.tarifa_base = tarifa_base
        self.status = status

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Número deve ser inteiro positivo.")
        self.__numero = valor

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        if valor.upper() not in Quarto.TIPOS_VALIDOS:
            raise ValueError("Tipo inválido.")
        self.__tipo = valor.upper()

    @property
    def capacidade(self):
        return self.__capacidade

    @capacidade.setter
    def capacidade(self, valor):
        if valor < 1:
            raise ValueError("Capacidade deve ser ≥ 1.")
        self.__capacidade = valor

    @property
    def tarifa_base(self):
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):
        if valor <= 0:
            raise ValueError("Tarifa base deve ser > 0.")
        self.__tarifa_base = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor.upper() not in Quarto.STATUS_VALIDOS:
            raise ValueError("Status inválido.")
        self.__status = valor.upper()

    # --- Métodos Especiais ---
    def __str__(self):
        return f"Quarto {self.numero} ({self.tipo}) - Capacidade: {self.capacidade}"

    def __lt__(self, other):
        if not isinstance(other, Quarto):
            return NotImplemented
        return (self.tipo, self.numero) < (other.tipo, other.numero)

class Quarto:
    TIPOS_VALIDOS = {"SIMPLES", "DUPLO", "LUXO"}
    STATUS_VALIDOS = {"DISPONIVEL", "OCUPADO", "MANUTENCAO", "BLOQUEADO"}

    def __init__(self, numero: int, tipo: str, capacidade: int, tarifa_base: float, status="DISPONIVEL"):
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.tarifa_base = tarifa_base
        self.status = status
        self.__reservas = []   # << RELACIONAMENTO
        self.__motivo_bloqueio = None
        self.__inicio_bloqueio = None
        self.__fim_bloqueio = None

    @property
    def reservas(self):
        return list(self.__reservas)

    def adicionar_reserva(self, reserva):
        self.__reservas.append(reserva)

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
    
    @property
    def periodo_bloqueio(self):
        return (self.__inicio_bloqueio, self.__fim_bloqueio)

    def bloquear(self, motivo: str, inicio: date, fim: date):
        """Bloqueia o quarto para manutenção ou outro motivo."""
        if inicio > fim:
            raise ValueError("Data inicial não pode ser maior que a data final.")

        self.status = "MANUTENCAO"
        self.__motivo_bloqueio = motivo
        self.__inicio_bloqueio = inicio
        self.__fim_bloqueio = fim

    def desbloquear(self):
        """Remove bloqueio e devolve o quarto como DISPONIVEL."""
        self.status = "DISPONIVEL"
        self.__motivo_bloqueio = None
        self.__inicio_bloqueio = None
        self.__fim_bloqueio = None

    def esta_bloqueado(self, data: date) -> bool:
        """Verifica se o quarto está bloqueado em uma data."""
        if self.status != "MANUTENCAO":
            return False
        if not self.__inicio_bloqueio or not self.__fim_bloqueio:
            return False
        return self.__inicio_bloqueio <= data <= self.__fim_bloqueio

    # --- Métodos Especiais ---
    def __str__(self):
        return f"Quarto {self.numero} ({self.tipo}) - Capacidade: {self.capacidade}"

    def __lt__(self, other):
        if not isinstance(other, Quarto):
            return NotImplemented
        return (self.tipo, self.numero) < (other.tipo, other.numero)

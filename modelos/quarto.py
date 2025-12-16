from datetime import date

class Quarto:
    TIPOS_VALIDOS = {"SIMPLES", "DUPLO", "LUXO"}
    STATUS_VALIDOS = {"DISPONIVEL", "OCUPADO", "MANUTENCAO", "BLOQUEADO"}

    def __init__(self, numero, tipo, capacidade, tarifa_base, status="DISPONIVEL"):
       if status not in Quarto.STATUS_VALIDOS:
            raise ValueError("Status inválido")

       if tipo not in Quarto.TIPOS_VALIDOS:
           raise ValueError("Tipo inválido")

       self.numero = numero
       self.tipo = tipo
       self.capacidade = capacidade
       self.tarifa_base = tarifa_base
       self._status = status

       self._bloqueios = []   # (inicio, fim, motivo)
       self._reservas = []    # lista de objetos Reserva
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, valor):
       if valor not in self.STATUS_VALIDOS:
           raise ValueError("Status inválido")
       self._status = valor

    
    def liberar(self):
       """
        Libera o quarto após checkout.
       """
       self._status = "DISPONIVEL"
       self._bloqueios.clear()

    # Associação OOP
    def adicionar_reserva(self, reserva):
        self._reservas.append(reserva)

    # Funções de bloqueio
    def bloquear(self, inicio: date, fim: date, motivo: str):
        if fim < inicio:
           raise ValueError("Data final inválida")

        self._status = "BLOQUEADO"
        self._bloqueios.append((inicio, fim, motivo))


    def desbloquear(self):
        self._status = "DISPONIVEL"
        self._bloqueios.clear()

    def esta_bloqueado(self, data: date):
        for inicio, fim, motivo in self._bloqueios:
            if inicio <= data <= fim:
                return True
        return False
    
    def ocupar(self):
        if self.status != "DISPONIVEL":
            raise ValueError(f"Quarto {self.numero} já está ocupado ou em manutenção.")
        self.status = "OCUPADO"
        
    def esta_disponivel(self, data: date | None = None) -> bool:
       if self._status != "DISPONIVEL":
           return False

       if data and self.esta_bloqueado(data):
           return False

       return True
    
    # JSON para API
    def to_dict(self):
        bloqueio = None
        if self._bloqueios:
            i, f, m = self._bloqueios[-1]
            bloqueio = {
                "inicio": i.isoformat(),
                "fim": f.isoformat(),
                "motivo": m
            }

        return {
            "numero": self.numero,
            "tipo": self.tipo,
            "capacidade": self.capacidade,
            "tarifa_base": self.tarifa_base,
            "status": self.status,
            "bloqueio": bloqueio
        }

    @staticmethod
    def from_db_row(row):
        tipo = row["tipo"].strip().upper() if row["tipo"] else "SIMPLES"
        status = row["status"].strip().upper() if "status" in row.keys() and row["status"] else "DISPONIVEL"

        q = Quarto(
           numero=row["numero"],
           tipo=tipo,
           capacidade=row["capacidade"],
           tarifa_base=row["tarifa_base"],
           status=status
        )

        if "bloqueio_inicio" in row.keys() and row["bloqueio_inicio"]:
           q._bloqueios.append((
               date.fromisoformat(row["bloqueio_inicio"]),
               date.fromisoformat(row["bloqueio_fim"]),
               row["motivo_bloqueio"]
        ))

        return q


    # MÉTODOS EXIGIDOS PELOS TESTES

    def __str__(self):
        return f"Quarto {self.numero}"

    def __lt__(self, other):
        if not isinstance(other, Quarto):
            return NotImplemented
        return self.numero < other.numero


class Adicional:
    def __init__(self, id=None, reserva_id=None, descricao="", valor=0.0):
        self.id = id
        self.reserva_id = reserva_id
        self.descricao = descricao
        self.valor = valor

    def to_dict(self):
        return {
            "id": self.id,
            "reserva_id": self.reserva_id,
            "descricao": self.descricao,
            "valor": self.valor
        }

    @staticmethod
    def from_db_row(row):
        return Adicional(
            id=row["id"],
            reserva_id=row["reserva_id"],
            descricao=row["descricao"],
            valor=row["valor"]
        )

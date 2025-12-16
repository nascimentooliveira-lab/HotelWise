class Pagamento:
    def __init__(self, id=None, reserva_id=None, valor=0.0, forma="PIX", data_pagamento=None):
        self.id = id
        self.reserva_id = reserva_id
        self.valor = valor
        self.forma = forma
        self.data_pagamento = data_pagamento

    def to_dict(self):
        return {
            "id": self.id,
            "reserva_id": self.reserva_id,
            "valor": self.valor,
            "forma": self.forma,
            "data_pagamento": self.data_pagamento,
        }

    @staticmethod
    def from_db_row(row):
        return Pagamento(
            id=row["id"],
            reserva_id=row["reserva_id"],
            valor=row["valor"],
            forma=row["forma"],
            data_pagamento=row["data_pagamento"],
        )

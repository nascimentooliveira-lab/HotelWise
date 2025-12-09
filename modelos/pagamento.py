from datetime import datetime
import sqlite3


class Pagamento:
    FORMAS_VALIDAS = {"DINHEIRO", "CREDITO", "DEBITO", "PIX"}

    def __init__(self, valor, forma, data=None, id=None):
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero.")

        forma = forma.upper()
        if forma not in self.FORMAS_VALIDAS:
            raise ValueError(f"Forma inválida. Use: {self.FORMAS_VALIDAS}")

        self.id = id
        self.__valor = valor
        self.__forma = forma
        self.__data = data if data else datetime.now()

    # PROPRIEDADES
    @property
    def valor(self):
        return self.__valor

    @property
    def forma(self):
        return self.__forma

    @property
    def data(self):
        return self.__data
    
    def adicionar_pagamento(self, pagamento):
        """Adiciona um pagamento à reserva."""
        self.__pagamentos.append(pagamento)

    # PERSISTÊNCIA 
    def to_tuple_insert(self, reserva_id: int):
        return (
            reserva_id,
            self.valor,
            self.forma,
            self.data.isoformat()
        )

    def to_tuple_update(self):
        return (
            self.valor,
            self.forma,
            self.data.isoformat(),
            self.id
        )

    @staticmethod
    def from_db_row(row: sqlite3.Row):
        data_obj = datetime.fromisoformat(row["data"])

        # reserva_id será ligado fora da classe — está ok
        pagamento = Pagamento(
            valor=row['valor'],
            forma=row['forma'],
            data=data_obj,
            id=row['id']
        )

        return pagamento


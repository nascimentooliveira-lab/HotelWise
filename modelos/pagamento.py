from datetime import datetime

class Pagamento:
    """
    Representa um pagamento efetuado para uma reserva.
    """

    FORMAS_VALIDAS = {"DINHEIRO", "CREDITO", "DEBITO", "PIX"}

    def __init__(self, valor: float, forma: str, data: datetime = None):
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero.")
        
        forma = forma.upper()
        if forma not in Pagamento.FORMAS_VALIDAS:
            raise ValueError(f"Forma de pagamento inválida. Use: {Pagamento.FORMAS_VALIDAS}")

        self.__valor = valor
        self.__forma = forma
        self.__data = data if data else datetime.now()

    @property
    def valor(self):
        return self.__valor

    @property
    def forma(self):
        return self.__forma

    @property
    def data(self):
        return self.__data

    from datetime import datetime
# from modelos.reserva import Reserva # Se necessário para type hinting

class Pagamento:
    # ... (Seu código original, mas com atributos ajustados: self.reserva_id e self.id)

    # --- MÉTODOS DE PERSISTÊNCIA ---

    def to_tuple_insert(self, reserva_id: int):
        """Converte para tupla para INSERT, ligando-o ao ID da Reserva."""
        return (
            reserva_id,                  # A ID da reserva que já deve estar salva
            self.valor,
            self.forma,
            self.data.isoformat()        # Salva a data e hora completa
        )

    def to_tuple_update(self):
        """Converte para tupla para UPDATE."""
        return (
            self.valor,
            self.forma,
            self.data.isoformat(),
            self.id # ID do pagamento no final para WHERE
        )

    @staticmethod
    def from_db_row(row: sqlite3.Row):
        """Cria um objeto Pagamento a partir de uma linha retornada pelo DB."""
        
        # O módulo de persistência deve converter a string de data de volta para datetime
        data_obj = datetime.fromisoformat(row['data'])
        
        # Cria um objeto dummy/placeholder para a Reserva
        reserva_dummy = type('Reserva', (object,), {'id': row['reserva_id']})()

        pagamento = Pagamento(
            reserva=reserva_dummy, 
            valor=row['valor'],
            forma=row['forma'],
            data=data_obj,
            id=row['id']
        )
        return pagamento
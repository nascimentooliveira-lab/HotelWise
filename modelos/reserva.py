from datetime import date, timedelta
import sqlite3
from .hospede import Hospede
from .quarto import Quarto


class Reserva:

    ESTADOS_VALIDOS = {
        "PENDENTE", "CONFIRMADA", "CHECKIN",
        "CHECKOUT", "CANCELADA", "NO_SHOW"
    }

    ORIGENS_VALIDAS = {"SITE", "TELEFONE", "BALCAO"}

    def __init__(self, hospede: Hospede, quarto: Quarto,
             data_entrada: date, data_saida: date,
             numero_hospedes: int = 1, origem: str = "SITE",
             estado: str = "PENDENTE", id: int = None):
        
        self.id = id
        self.hospede = hospede
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.numero_hospedes = numero_hospedes
        self.estado = estado.upper()
        self.origem = origem.upper()

        if self.origem not in self.ORIGENS_VALIDAS:
            raise ValueError(f"Origem deve ser um de: {self.ORIGENS_VALIDAS}")

        # Agregações
        self.__pagamentos = []
        self.__adicionais = []

        # Impedir overbooking
        self.__validar_disponibilidade(quarto)

        # Registrar relação bidirecional
        hospede.adicionar_reserva(self)
        quarto.adicionar_reserva(self)

    @property
    def hospede(self):
        return self.__hospede

    @hospede.setter
    def hospede(self, valor):
        if not isinstance(valor, Hospede):
            raise TypeError("hospede deve ser um objeto Hospede.")
        self.__hospede = valor

    @property
    def quarto(self):
        return self.__quarto

    @quarto.setter
    def quarto(self, valor):
        if not isinstance(valor, Quarto):
            raise TypeError("quarto deve ser um objeto Quarto.")
        self.__quarto = valor

    @property
    def data_entrada(self):
        return self.__data_entrada

    @data_entrada.setter
    def data_entrada(self, valor):
        if not isinstance(valor, date):
            raise TypeError("data_entrada deve ser um objeto date.")
        self.__data_entrada = valor

    @property
    def data_saida(self):
        return self.__data_saida

    @data_saida.setter
    def data_saida(self, valor):
        if not isinstance(valor, date):
            raise TypeError("data_saida deve ser um objeto date.")

        if hasattr(self, "_Reserva__data_entrada") and valor <= self.data_entrada:
            raise ValueError("data_saida deve ser ao menos 1 dia após data_entrada.")

        self.__data_saida = valor

    @property
    def numero_hospedes(self):
        return self.__numero_hospedes

    @numero_hospedes.setter
    def numero_hospedes(self, valor):
        if valor < 1:
            raise ValueError("A reserva deve ter pelo menos 1 hóspede.")
        if hasattr(self, "_Reserva__quarto") and valor > self.quarto.capacidade:
            raise ValueError("Número de hóspedes excede a capacidade do quarto.")
        self.__numero_hospedes = valor

    # FLUXOS COMPLETOS DO HOTE
    def confirmar(self):
        if self.estado != "PENDENTE":
            raise ValueError("Só é possível confirmar reservas pendentes.")
        self.estado = "CONFIRMADA"

    def cancelar(self, data_hoje: date = date.today()):
        if self.estado in {"CHECKIN", "CHECKOUT"}:
           raise ValueError("Não é possível cancelar após check-in.")
        self.estado = "CANCELADA"
        self.data_cancelamento = data_hoje

    def marcar_no_show(self, data_hoje: date = date.today()):
        if self.estado != "CONFIRMADA":
           raise ValueError("Só é possível marcar no-show em reservas confirmadas.")
        if data_hoje <= self.data_entrada:
           raise ValueError("A data de entrada ainda não passou.")
        self.estado = "NO_SHOW"
        self.data_no_show = data_hoje

    def fazer_checkin(self, data_hoje: date):
        if self.estado != "CONFIRMADA":
            raise ValueError("Check-in permitido apenas para reservas CONFIRMADAS.")
        if data_hoje < self.data_entrada:
            raise ValueError("Check-in antecipado não permitido.")
        if data_hoje > self.data_saida:
            raise ValueError("Data da reserva já passou. Avaliar no-show.")

        self.estado = "CHECKIN"
        if hasattr(self.quarto, "ocupado"):
            self.quarto.ocupado = True

    def fazer_checkout(self, data_saida_real: date):
        if self.estado != "CHECKIN":
            raise ValueError("Check-out permitido apenas após o check-in.")

        valor_final = self.total_devido(data_saida_real)

        if self.total_pago() < valor_final:
            raise ValueError(
                f"Pagamento insuficiente. Total devido: {valor_final:.2f}, "
                f"total pago: {self.total_pago():.2f}"
            )

        self.estado = "CHECKOUT"
        if hasattr(self.quarto, "ocupado"):
            self.quarto.ocupado = False

        return valor_final

    def __validar_disponibilidade(self, quarto: Quarto):
        """Impede overbooking verificando reservas existentes."""
        
        ESTADOS_BLOQUEANTES = {"PENDENTE", "CONFIRMADA", "CHECKIN"}

        for r in quarto.reservas:
            
            # Se a reserva existente não está em um estado bloqueante, ela é ignorada.
            if r.estado not in ESTADOS_BLOQUEANTES:
                continue
                
            # Se datas se sobrepõem → conflito (Overbooking)
            if not (self.data_saida <= r.data_entrada or self.data_entrada >= r.data_saida):
                raise ValueError(
                    f"Quarto {quarto.numero} indisponível no período solicitado."
                )

    #CÁLCULO DE VALOR 

    def valor_total(self):
        total = 0
        diaria = self.quarto.tarifa_base

        atual = self.data_entrada
        while atual < self.data_saida:

            preco = diaria

            # Fim de semana (+20%)
            if atual.weekday() in (4, 5):  # sexta/sábado
                preco *= 1.20

            # Temporada (exemplo: dezembro)
            if atual.month == 12:
                preco *= 1.30

            total += preco
            atual += timedelta(days=1)

        return round(total, 2)
    
    def total_pago(self):
        return sum(p.valor for p in self.__pagamentos)

    def total_adicionais(self):
        return sum(a.valor for a in self.__adicionais)

    def total_devido(self, data_saida_real=None):
        total = self.valor_total() + self.total_adicionais()

        if data_saida_real and data_saida_real > self.data_saida:
             dias_extras = (data_saida_real - self.data_saida).days
             total += dias_extras * self.quarto.tarifa_base

        return round(total, 2)


    # AGREGADOS

    @property
    def pagamentos(self):
        return list(self.__pagamentos)

    def adicionar_pagamento(self, pagamento):
        self.__pagamentos.append(pagamento)

    @property
    def adicionais(self):
        return list(self.__adicionais)

    def adicionar_adicional(self, adicional):
        self.__adicionais.append(adicional)
    
    # auxiliar
    def __len__(self):
        """Número de diárias."""
        return (self.data_saida - self.data_entrada).days

    def __str__(self):
        return f"Reserva de {self.hospede.nome} no quarto {self.quarto.numero}"

    # --- MÉTODOS DE PERSISTÊNCIA ---
    
    #data.isoformat() para garantir o formato 'YYYY-MM-DD'
    
    def to_tuple(self):
        """Converte o objeto Reserva em uma tupla para comandos SQL."""
        return (
            self.hospede.id,            # Chave estrangeira (ID do hospede)
            self.quarto.numero,         # Chave estrangeira (Numero do quarto)
            self.data_entrada.isoformat(),
            self.data_saida.isoformat(),
            self.numero_hospedes,
            self.estado,
            self.origem,
            self.valor_total,
            self.data_cancelamento.isoformat() if self.data_cancelamento else None,
            self.data_no_show.isoformat() if self.data_no_show else None,
            self.id # Incluído para UPDATE no final
        )

    @staticmethod
    def from_db_row(row: sqlite3.Row):
        from datetime import date

        # Cria objetos Hospede e Quarto simplificados para evitar dependência cíclica
        hospede_dummy = type('Hospede', (object,), {'id': row['hospede_id']})()
        quarto_dummy = type('Quarto', (object,), {'numero': row['quarto_numero']})()

        # O datetime.date deve ser importado e usado para converter a string de volta para date
        from datetime import date
      
        obj = Reserva(
            hospede=hospede_dummy,
            quarto=quarto_dummy,
            data_entrada=date.fromisoformat(row['data_entrada']),
            data_saida=date.fromisoformat(row['data_saida']),
            numero_hospedes=row['num_hospedes'],
            origem=row['origem'],
            estado=row['estado'],
            id=row['id']
        )
    
        obj.data_cancelamento = (
           date.fromisoformat(row["data_cancelamento"])
           if row["data_cancelamento"] else None
        )

        obj.data_no_show = (
           date.fromisoformat(row["data_no_show"])
           if row["data_no_show"] else None
        )

        return obj
from __future__ import annotations
from datetime import date, timedelta, datetime
import sqlite3
from .hospede import Hospede
from .quarto import Quarto


class Reserva:

    ESTADOS_VALIDOS = {
        "PENDENTE", "CONFIRMADA", "CHECKIN",
        "CHECKOUT", "CANCELADA", "NO_SHOW"
    }

    ORIGENS_VALIDAS = {"SITE", "TELEFONE", "BALCAO"}

    def __init__(
        self, hospede, quarto,
        data_entrada: date, data_saida: date,
        numero_hospedes: int = 1, origem: str = "SITE",
        estado: str = "PENDENTE", id: int = None,
        check_in_real: datetime = None, check_out_real: datetime = None
    ):

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

        self.check_in_real = check_in_real
        self.check_out_real = check_out_real
        self.data_cancelamento = None
        self.data_no_show = None

        self.__pagamentos = []
        self.__adicionais = []

        # Evita overbooking
        self.__validar_disponibilidade(quarto)

        # Relação bidirecional
        hospede.adicionar_reserva(self)
        quarto.adicionar_reserva(self)

    # PROPRIEDADES E VALIDACOES

    @property
    def hospede(self):
        return self.__hospede

    @hospede.setter
    def hospede(self, valor):
        from .hospede import Hospede
        if not isinstance(valor, Hospede):
            raise TypeError("hospede deve ser um objeto Hospede.")
        self.__hospede = valor

    @property
    def quarto(self):
        return self.__quarto

    @quarto.setter
    def quarto(self, valor):
        from .quarto import Quarto
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
            raise ValueError("data_saida deve ser depois de data_entrada.")
        self.__data_saida = valor

    # FLUXOS
    def fazer_checkin(self, data_real: date):
        if self.estado != "CONFIRMADA":
            raise ValueError("Só é possível fazer check-in de reservas confirmadas.")
        if data_real < self.data_entrada:
            raise ValueError("Check-in não pode ocorrer antes da data de entrada.")

        self.estado = "CHECKIN"
        self.check_in_real = data_real


    def fazer_checkout(self, data_real: date):
        if self.estado != "CHECKIN":
            raise ValueError("Só é possível fazer checkout de reservas em CHECKIN.")

        if data_real < self.data_entrada:
            raise ValueError("Checkout inválido: data antes do início da reserva.")

        self.estado = "CHECKOUT"
        self.check_out_real = data_real

    def confirmar(self):
        if self.estado != "PENDENTE":
            raise ValueError("Só é possível confirmar reservas pendentes.")
        self.estado = "CONFIRMADA"

    def cancelar(self, data_hoje=date.today()):
       if self.estado in {"CHECKIN", "CHECKOUT"}:
            raise ValueError("Não é possível cancelar após check-in.")

       self.estado = "CANCELADA"
       self.data_cancelamento = data_hoje

       dias_antes = (self.data_entrada - data_hoje).days

       # Regras de multa
       if dias_antes > 7:
           self.multa_cancelamento = 0
       elif dias_antes >= 1:
           self.multa_cancelamento = self.quarto.tarifa_base
       else:  # cancelou no dia
           self.multa_cancelamento = self.valor_total()
 
    def marcar_no_show(self, data_hoje=date.today()):
        if self.estado != "CONFIRMADA":
            raise ValueError("Só é possível no-show em reservas confirmadas.")
        if data_hoje <= self.data_entrada:
            raise ValueError("A data de entrada ainda não passou.")
        self.estado = "NO_SHOW"
        self.data_no_show = data_hoje

    # CÁLCULO DE DIÁRIAS

    def valor_total(self):
        total = 0
        diaria = self.quarto.tarifa_base

        atual = self.data_entrada
        while atual < self.data_saida:

            preco = diaria

            if atual.weekday() in (4, 5):  # sexta/sabado
                preco *= 1.20

            if atual.month == 12:
                preco *= 1.30

            total += preco
            atual += timedelta(days=1)

        return round(total, 2)
    
    def tarifa_diaria(self):
      """Retorna somente a tarifa base diária do quarto."""
      return self.quarto.tarifa_base

    
    # agregados
    
    def __len__(self):
        """Retorna o número de diárias."""
        return (self.data_saida - self.data_entrada).days


    # AGREGADOS

    def total_pago(self):
        return sum(p.valor for p in self.__pagamentos)
    
    def adicionar_pagamento(self, pagamento):
        """Adiciona um pagamento à reserva."""
        self.__pagamentos.append(pagamento)

    def total_adicionais(self):
        return sum(a.valor for a in self.__adicionais)
    
    def total_devido(self):
        """Calcula o valor devido considerando cancelamentos, checkout antecipado/tardio e pagamentos prévios."""

        # CANCELAMENTO 
        if self.estado == "CANCELADA":
            multa = getattr(self, "multa_cancelamento", 0)
            pago = self.total_pago()
            return max(multa - pago, 0)

        # CHECKOUT (normal, antecipado, tardio)
        if self.estado == "CHECKOUT" and self.check_out_real:

            if self.check_out_real < self.data_saida:
                # checkout antecipado → cobra só as diárias usadas
                dias = (self.check_out_real - self.data_entrada).days
                return dias * self.quarto.tarifa_base + self.total_adicionais()

            # checkout tardio → cobra diárias extras
            dias_originais = (self.data_saida - self.data_entrada).days
            dias_reais = (self.check_out_real - self.data_entrada).days
            extras = max(0, dias_reais - dias_originais)

            return (
                self.valor_total()
                + extras * self.quarto.tarifa_base
                + self.total_adicionais()
            )

        #  CASO NORMAL 
        return self.valor_total() + self.total_adicionais()

    # PERSISTÊNCIA

    def to_tuple(self):
        return (
            self.hospede.id,
            self.quarto.numero,
            self.data_entrada.isoformat(),
            self.data_saida.isoformat(),
            self.numero_hospedes,
            self.estado,
            self.origem,
            self.id,
        )

    # VALIDAÇÃO DE DISPONIBILIDADE 

    def __validar_disponibilidade(self, quarto: Quarto):
        """Evita overbooking e respeita bloqueios de manutenção (se disponíveis)."""
        # checar bloqueios de manutenção (se método existir)
        atual = self.data_entrada
        while atual < self.data_saida:
            if hasattr(quarto, "esta_bloqueado") and quarto.esta_bloqueado(atual):
                # tenta ler motivos/início/fim se existirem; se não, mensagem genérica
                motivo = getattr(quarto, "_Quarto__motivo_bloqueio", "manutenção")
                inicio = getattr(quarto, "_Quarto__inicio_bloqueio", "??")
                fim = getattr(quarto, "_Quarto__fim_bloqueio", "??")
                raise ValueError(
                    f"Quarto {quarto.numero} está bloqueado para manutenção "
                    f"de {inicio} até {fim}. Motivo: {motivo}"
                )
            atual += timedelta(days=1)

        # checar overbooking com reservas existentes (se `quarto.reservas` existir)
        ESTADOS_BLOQUEANTES = {"PENDENTE", "CONFIRMADA", "CHECKIN"}
        for r in getattr(quarto, "reservas", []):
            if r is self:
                continue
            if r.estado not in ESTADOS_BLOQUEANTES:
                continue
            # se os períodos se sobrepõem -> indisponível
            if not (self.data_saida <= r.data_entrada or self.data_entrada >= r.data_saida):
                raise ValueError(f"Quarto {quarto.numero} indisponível no período solicitado.")

    # RECRIAR OBJETO DO BANCO 

    @staticmethod
    def from_db_row(row: sqlite3.Row):
        """Reconstrói uma reserva a partir do row retornado pelo DAO."""
        if not row:
            return None

        def to_datetime_or_none(value):
            return datetime.fromisoformat(value) if value else None

        # Criar objetos mínimos (dummy) — o DAO/serviço pode substituir por objetos completos depois
        hospede_dummy = Hospede(
            id=row["hospede_id"],
            nome="",
            documento="",
            email="",
            telefone=""
        )

        quarto_dummy = Quarto(
            numero=row["quarto_numero"],
            tipo="SIMPLES",
            capacidade=1,
            tarifa_base=0
        )

        obj = Reserva(
            hospede=hospede_dummy,
            quarto=quarto_dummy,
            data_entrada=date.fromisoformat(row["data_entrada"]),
            data_saida=date.fromisoformat(row["data_saida"]),
            numero_hospedes=row["numero_hospedes"],
            origem=row["origem"],
            estado=row["estado"],
            id=row["id"],
            check_in_real=to_datetime_or_none(row["check_in_real"]),
            check_out_real=to_datetime_or_none(row["check_out_real"]),
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


from datetime import date, datetime, timedelta, time
from services.config_service import config_service
from persistencia.adicional_dao import listar_adicionais
from persistencia.pagamento_dao import listar_pagamentos



class Reserva:
    ESTADOS = {"PENDENTE", "CONFIRMADA", "CHECKIN", "CHECKOUT", "CANCELADA", "NO_SHOW"}

    def __init__(
        self,
        hospede,
        quarto,
        data_entrada: date,
        data_saida: date,
        num_hospedes=1,
        origem="SITE",
        estado="PENDENTE",
        id=None,
        check_in_real=None,
        check_out_real=None
    ):
        if data_saida <= data_entrada:
            raise ValueError("data_saida deve ser depois de data_entrada.")

        if num_hospedes > quarto.capacidade:
            raise ValueError("Número de hóspedes maior que a capacidade do quarto.")

        self.id = id
        self.hospede = hospede
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.num_hospedes = num_hospedes
        self.origem = origem.upper()
        self.estado = estado.upper()

        if self.estado not in Reserva.ESTADOS:
           raise ValueError("Estado da reserva inválido.")

        self.check_in_real = check_in_real
        self.check_out_real = check_out_real

        self.data_cancelamento = None
        self.data_no_show = None

        self.pagamentos = []

    
        if hasattr(self.hospede, "adicionar_reserva"):
            self.hospede.adicionar_reserva(self)

        if hasattr(self.quarto, "adicionar_reserva"):
            self.quarto.adicionar_reserva(self)

        self._validar_overbooking()

    # VALIDACOES
    
    def _validar_overbooking(self):
        if not hasattr(self.quarto, "reservas"):
            return

        for r in self.quarto.reservas:
            if r is self:
                continue

            if r.estado in {"PENDENTE", "CONFIRMADA", "CHECKIN", "CHECKOUT"}:
                if not (self.data_saida <= r.data_entrada or self.data_entrada >= r.data_saida):
                    raise ValueError(f"Quarto {self.quarto.numero} já reservado no período.")
    # CALCULOS
  
    def calcular_valor_total(self):
        dias = (self.data_saida - self.data_entrada).days
        dias = max(dias, 1)
        return dias * self.quarto.tarifa_base

    @property
    def valor_total(self):
        return self.calcular_valor_total()

    def total_pago(self):
       pagamentos = listar_pagamentos(self.id)
       return round(sum(p.valor for p in pagamentos), 2)

    def total_adicionais(self):
       adicionais = listar_adicionais(self.id)
       return round(sum(a.valor for a in adicionais), 2)

    def total_devido(self):
        # NO_SHOW ou CANCELADA → cobra multa
        if self.estado in {"NO_SHOW", "CANCELADA"}:
            total = getattr(self, "multa", 0.0)

         # CHECKOUT → cobra diárias reais
        elif self.check_out_real:
            # 👉 normaliza check_out_real para date
            data_checkout = (
               self.check_out_real.date()
               if isinstance(self.check_out_real, datetime)
               else self.check_out_real
            )

            dias = (data_checkout - self.data_entrada).days
            dias = max(dias, 1)
            total = dias * self.quarto.tarifa_base

        # RESERVA NORMAL
        else:
           total = self.valor_total

        # soma adicionais
        total += self.total_adicionais()

        # subtrai pagamentos
        total -= self.total_pago()

        return round(max(total, 0), 2)

    def adicionar_pagamento(self, pagamento):
        self.pagamentos.append(pagamento)

    # FLUXOS
   
    def confirmar(self):
        if self.estado != "PENDENTE":
            raise ValueError("Somente reservas pendentes podem ser confirmadas.")
        self.estado = "CONFIRMADA"

    from datetime import datetime, date, timedelta

    def fazer_checkin(self, agora=None):
        if self.estado != "CONFIRMADA":
            raise ValueError("Check-in só para reservas CONFIRMADAS.")

        # 👉 se não passar nada, usa datetime real (CLI)
        if agora is None:
            agora = datetime.now()

        # 👉 se vier DATE, assume check-in válido no dia (sem regra de hora)
        if isinstance(agora, date) and not isinstance(agora, datetime):
            self.check_in_real = datetime.combine(agora, datetime.min.time())
            self.estado = "CHECKIN"
            self.quarto.ocupar()
            return

        # 👇 daqui para baixo, só DATETIME (CLI real)

        hora_base = config_service.checkin_hora()
        h, m = map(int, hora_base.split(":"))

        inicio = datetime.combine(
        self.data_entrada,
        datetime.min.time()
        ).replace(hour=h, minute=m)

        fim = inicio + timedelta(
        minutes=config_service.get("tolerancia_checkin_minutos", 120)
        )

        if not (inicio <= agora <= fim):
            raise ValueError("Check-in fora do horário permitido.")

        self.check_in_real = agora
        self.estado = "CHECKIN"
        self.quarto.ocupar()
 

    from datetime import datetime, date

    def fazer_checkout(self, agora=None):
        if self.estado != "CHECKIN":
            raise ValueError("Checkout só pode ser feito de reservas em CHECKIN.")

        if agora is None:
            agora = datetime.now()
        elif isinstance(agora, date) and not isinstance(agora, datetime):
            agora = datetime.combine(agora, datetime.min.time())

        self.check_out_real = agora
        self.estado = "CHECKOUT"
        self.quarto.liberar()

    def cancelar(self, hoje=None):
        hoje = hoje or date.today()

        if self.estado in {"CHECKIN", "CHECKOUT"}:
            raise ValueError("Não é possível cancelar reservas já iniciadas.")

        dias_antes = (self.data_entrada - hoje).days
        multa_pct = config_service.multa_cancelamento_percentual()

        self.multa = 0.0

        # cancelamento no mesmo dia ou depois
        if dias_antes <= 0:
             self.multa = round(self.valor_total * multa_pct, 2)

        self.data_cancelamento = hoje
        self.estado = "CANCELADA"
        self.quarto.liberar()

    def marcar_no_show(self, hoje=None):
        hoje = hoje or date.today()

        if self.estado != "CONFIRMADA":
            raise ValueError("Somente reservas CONFIRMADAS podem virar NO_SHOW.")

        if hoje < self.data_entrada:
            raise ValueError("Ainda não é possível marcar no-show.")

        self.estado = "NO_SHOW"
        self.data_no_show = hoje
        self.quarto.liberar()

    def _hora_str_para_time(hora_str):
        h, m = hora_str.split(":")
        return time(int(h), int(m))
    
    def __str__(self):
      return (
        f"\n========== RESERVA #{self.id} ==========\n"
        f"Hóspede........: {self.hospede}\n"
        f"Quarto.........: {self.quarto.numero} ({self.quarto.tipo})\n"
        f"Capacidade.....: {self.quarto.capacidade}\n"
        f"Entrada........: {self.data_entrada}\n"
        f"Saída..........: {self.data_saida}\n"
        f"Nº hóspedes....: {self.num_hospedes}\n"
        f"Origem.........: {self.origem}\n"
        f"Estado.........: {self.estado}\n"
        f"---------------------------------------\n"
        f"Diárias........: R$ {self.calcular_valor_total():.2f}\n"
        f"Adicionais.....: R$ {self.total_adicionais():.2f}\n"
        f"Total pago.....: R$ {self.total_pago():.2f}\n"
        f"Saldo devido...: R$ {self.total_devido():.2f}\n"
        f"---------------------------------------\n"
        f"Check-in real..: {self.check_in_real}\n"
        f"Check-out real.: {self.check_out_real}\n"
        f"Cancelamento...: {self.data_cancelamento}\n"
        f"No-show........: {self.data_no_show}\n"
        f"=======================================\n"
    )

    # SERIALIZACAO

    def __len__(self):
        return (self.data_saida - self.data_entrada).days

    def to_dict(self):
        return {
            "id": self.id,
            "hospede_id": self.hospede.id,
            "quarto_numero": self.quarto.numero,
            "data_entrada": self.data_entrada.isoformat(),
            "data_saida": self.data_saida.isoformat(),
            "num_hospedes": self.num_hospedes,
            "origem": self.origem,
            "estado": self.estado,
            "valor_diarias": self.valor_total,
            "total_adicionais": self.total_adicionais(),
            "total_pago": self.total_pago(),
            "total_geral": self.valor_total + self.total_adicionais(),
            "saldo": self.total_devido(),
            "check_in_real": self.check_in_real.isoformat() if self.check_in_real else None,
            "check_out_real": self.check_out_real.isoformat() if self.check_out_real else None,
            "data_cancelamento": self.data_cancelamento.isoformat() if self.data_cancelamento else None,
            "data_no_show": self.data_no_show.isoformat() if self.data_no_show else None
        }

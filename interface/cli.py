import click
import sys
# Importe as funções reais dos seus módulos
# Por exemplo:
# from modelos.quarto import cadastrar_quarto, bloquear_quarto
# from modelos.reserva import fazer_reserva, fazer_checkin, fazer_checkout
# from modelos.pagamento import registrar_pagamento
# from relatorios import relatorio_ocupacao, relatorio_receita

# --- GRUPO PRINCIPAL: O COMANDO 'hotel' ---

@click.group()
def hotel():
    """
    Sistema de Gerenciamento de Reservas de Hotel (CLI).

    Use 'hotel [comando] --help' para ver as opções.
    Exemplo: 'hotel quarto cadastrar --help'
    """
    pass

# =================================================================
# 1. SUBCOMANDOS DE QUARTO (hotel quarto ...)
# =================================================================

@hotel.group()
def quarto():
    """Gerencia quartos: cadastro, bloqueio, listagem, etc."""
    pass

@quarto.command('cadastrar') # Comando: hotel quarto cadastrar [numero] [tipo]
@click.argument('numero')
@click.argument('tipo')
@click.option('-v', '--valor-diaria', type=float, required=True, 
              help='Valor da diária do quarto.')
def cadastrar_quarto_cmd(numero, tipo, valor_diaria):
    """CADASTRAR um novo quarto (Ex: 101, LUXO)."""
    click.echo(f"➡️ Tentando cadastrar Quarto {numero} de tipo {tipo} com valor R${valor_diaria:.2f}...")
    try:
        # Chamar sua função: cadastrar_quarto(numero, tipo, valor_diaria)
        click.echo("✅ Quarto cadastrado com sucesso.")
    except Exception as e:
        click.echo(f"❌ Erro ao cadastrar quarto: {e}", err=True)

@quarto.command('bloquear') # Comando: hotel quarto bloquear [numero]
@click.argument('numero')
@click.option('-m', '--motivo', default='Manutenção', help='Motivo do bloqueio.')
def bloquear_quarto_cmd(numero, motivo):
    """BLOQUEAR um quarto para manutenção ou indisponibilidade."""
    click.echo(f"➡️ Bloqueando Quarto {numero}. Motivo: {motivo}")
    try:
        # Chamar sua função: bloquear_quarto(numero, motivo)
        click.echo("✅ Quarto bloqueado com sucesso.")
    except Exception as e:
        click.echo(f"❌ Erro ao bloquear quarto: {e}", err=True)

# =================================================================
# 2. SUBCOMANDOS DE RESERVA E HOSPEDAGEM (hotel reservar, checkin, checkout)
# =================================================================

@hotel.command('reservar') # Comando: hotel reservar [quarto] [hospede]
@click.argument('quarto_numero')
@click.argument('hospede_nome')
@click.option('-d', '--dias', type=int, default=1, help='Número de diárias.')
def reservar_cmd(quarto_numero, hospede_nome, dias):
    """Fazer uma NOVA RESERVA."""
    click.echo(f"➡️ Criando reserva de {dias} dias para {hospede_nome} no Quarto {quarto_numero}...")
    try:
        # Chamar sua função: fazer_reserva(quarto_numero, hospede_nome, dias)
        click.echo("✅ Reserva criada com sucesso.")
    except Exception as e:
        click.echo(f"❌ Erro ao reservar: {e}", err=True)

@hotel.command('checkin') # Comando: hotel checkin [reserva_id]
@click.argument('reserva_id')
def checkin_cmd(reserva_id):
    """Registrar CHECKIN para uma reserva."""
    click.echo(f"➡️ Registrando Checkin para a Reserva ID {reserva_id}...")
    try:
        # Chamar sua função: fazer_checkin(reserva_id)
        click.echo("✅ Checkin realizado. Hóspede alocado.")
    except Exception as e:
        click.echo(f"❌ Erro no checkin: {e}", err=True)

@hotel.command('checkout') # Comando: hotel checkout [reserva_id]
@click.argument('reserva_id')
def checkout_cmd(reserva_id):
    """Registrar CHECKOUT e encerrar a hospedagem."""
    click.echo(f"➡️ Registrando Checkout para a Reserva ID {reserva_id}...")
    try:
        # Chamar sua função: fazer_checkout(reserva_id)
        click.echo("✅ Checkout realizado. Quarto liberado e conta fechada.")
    except Exception as e:
        click.echo(f"❌ Erro no checkout: {e}", err=True)

# =================================================================
# 3. SUBCOMANDOS DE FINANÇAS/SERVIÇOS (hotel pagar, adicional)
# =================================================================

@hotel.command('pagar') # Comando: hotel pagar [reserva_id] [valor]
@click.argument('reserva_id')
@click.argument('valor', type=float)
@click.option('-m', '--metodo', default='Cartão', help='Método de pagamento.')
def pagar_cmd(reserva_id, valor, metodo):
    """Registrar um PAGAMENTO parcial ou total para uma reserva/hospedagem."""
    click.echo(f"➡️ Registrando pagamento de R${valor:.2f} (Método: {metodo}) para Reserva ID {reserva_id}...")
    try:
        # Chamar sua função: registrar_pagamento(reserva_id, valor, metodo)
        click.echo("✅ Pagamento registrado com sucesso.")
    except Exception as e:
        click.echo(f"❌ Erro no pagamento: {e}", err=True)

@hotel.command('adicional') # Comando: hotel adicional [reserva_id] [descricao] [valor]
@click.argument('reserva_id')
@click.argument('descricao')
@click.argument('valor', type=float)
def adicional_cmd(reserva_id, descricao, valor):
    """Adicionar um consumo/serviço ADICIONAL à conta do hóspede."""
    click.echo(f"➡️ Adicionando R${valor:.2f} ({descricao}) à conta da Reserva ID {reserva_id}...")
    try:
        # Chamar sua função: adicionar_adicional(reserva_id, descricao, valor)
        click.echo("✅ Adicional registrado com sucesso.")
    except Exception as e:
        click.echo(f"❌ Erro ao adicionar adicional: {e}", err=True)

# =================================================================
# 4. SUBCOMANDOS DE RELATÓRIO (hotel relatorio ...)
# =================================================================

@hotel.group()
def relatorio():
    """Gera relatórios diversos (ocupação, receita, etc.)."""
    pass

@relatorio.command('ocupacao') # Comando: hotel relatorio ocupacao
@click.option('-d', '--data', default=None, help='Data específica (YYYY-MM-DD) ou hoje.')
def relatorio_ocupacao_cmd(data):
    """Gerar relatório de OCUPAÇÃO de quartos."""
    click.echo(f"➡️ Gerando Relatório de Ocupação para a data: {data if data else 'hoje'}...")
    try:
        # Chamar sua função: dados = relatorio_ocupacao(data)
        # Exibir os dados (usando click.echo para formatação)
        click.echo("📊 Resultado do Relatório de Ocupação:")
        click.echo("- Total de Quartos: 50")
        click.echo("- Quartos Ocupados: 40 (80%)")
    except Exception as e:
        click.echo(f"❌ Erro ao gerar relatório: {e}", err=True)

@relatorio.command('receita') # Comando: hotel relatorio receita
@click.option('-p', '--periodo', default='mensal', help='Período: diario, mensal, anual.')
def relatorio_receita_cmd(periodo):
    """Gerar relatório de RECEITA (total faturado)."""
    click.echo(f"➡️ Gerando Relatório de Receita ({periodo})...")
    try:
        # Chamar sua função: dados = relatorio_receita(periodo)
        # Exibir os dados
        click.echo("💰 Resultado do Relatório de Receita:")
        click.echo(f"- Receita {periodo.upper()}: R$ 15.000,00")
    except Exception as e:
        click.echo(f"❌ Erro ao gerar relatório: {e}", err=True)

# =================================================================
# PONTO DE ENTRADA
# =================================================================

if __name__ == '__main__':
    hotel()
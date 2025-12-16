from datetime import date, datetime, time

from persistencia.hospede_dao import (
    criar_hospede, listar_hospedes, buscar_hospede,
    atualizar_hospede, excluir_hospede, buscar_hospede_por_documento, buscar_hospede_por_id
)
from persistencia.quarto_dao import (
    criar_quarto, listar_quartos, buscar_quarto_por_numero,
    atualizar_quarto, excluir_quarto,
    bloquear_quarto, desbloquear_quarto
)
from persistencia.reserva_dao import (
    criar_reserva, listar_reservas_completas, buscar_reserva,
    atualizar_reserva, remover_reserva
)
from persistencia.pagamento_dao import registrar_pagamento, listar_pagamentos
from persistencia.adicional_dao import adicionar_adicional, listar_adicionais


from serv.relatorios import (
    calcular_taxa_ocupacao,
    calcular_receita_por_tipo,
    calcular_cancelamentos_noshow
)

from modelos.reserva import Reserva
from modelos.pagamento import Pagamento
from modelos.adicional import Adicional

# HÓSPEDES

def criar_hospede_menu():
    print("\n== Criar Hóspede ==")

    while True:
      nome = input("Nome: ").strip()
      if not nome:
          print("Nome não pode ficar vazio")
      else:
          break
      
    while True:
        documento = input("CPF (somente números): ").strip()

        if not documento.isdigit() or len(documento) != 11:
            print("CPF inválido. Deve conter exatamente 11 números.")
            continue

        if buscar_hospede_por_documento(documento):
            print("Já existe um hóspede com esse CPF. Tente outro.")
            continue

        break  # CPF válido e único

    email = input("Email: ")
    telefone = input("Telefone: ")

    try:
        criar_hospede({
            "nome": nome,
            "documento": documento,
            "email": email,
            "telefone": telefone
        })
        print(" Hóspede criado com sucesso")
    except Exception as e:
        print(f" Erro ao criar hóspede: {e}")


def listar_hospedes_menu():
    for h in listar_hospedes():
        print(h.to_dict())


def atualizar_hospede_menu():
    id = int(input("ID do hóspede: "))
    h = buscar_hospede(id)
    if not h:
        print("Hóspede não encontrado")
        return

    nome = input(f"Nome [{h.nome}]: ") or h.nome
    email = input(f"Email [{h.email}]: ") or h.email
    telefone = input(f"Telefone [{h.telefone}]: ") or h.telefone

    atualizar_hospede({
        "id": id,
        "nome": nome,
        "email": email,
        "telefone": telefone
    })
    print("✔ Hóspede atualizado")

def excluir_hospede_menu():
    id = int(input("ID do hóspede: "))
    excluir_hospede(id)
    print("✔ Hóspede excluído")

# QUARTOS

def criar_quarto_menu():
    print("\n== Criar Quarto ==")

    while True:
        try:
            numero = int(input("Número do quarto: "))
        except ValueError:
            print("Digite um número válido")
            continue

        if buscar_quarto_por_numero(numero):
            print("Já existe um quarto com esse número. Tente outro.")
        else:
            break  # número válido e livre

    tipo = input("Tipo: ")
    capacidade = int(input("Capacidade: "))
    tarifa = float(input("Tarifa base: "))

    try:
        criar_quarto({
            "numero": numero,
            "tipo": tipo,
            "capacidade": capacidade,
            "tarifa_base": tarifa
        })
        print("✔ Quarto criado com sucesso")
    except Exception as e:
        print(f"Erro ao criar quarto: {e}")

def listar_quartos_menu():
    for q in listar_quartos():
        print(q.to_dict())

def atualizar_quarto_menu():
    numero = int(input("Número do quarto: "))
    q = buscar_quarto_por_numero(numero)
    if not q:
        print(" Quarto não encontrado")
        return

    tipo = input(f"Tipo [{q.tipo}]: ") or q.tipo
    capacidade = int(input(f"Capacidade [{q.capacidade}]: ") or q.capacidade)
    tarifa = float(input(f"Tarifa [{q.tarifa_base}]: ") or q.tarifa_base)

    atualizar_quarto({
        "numero": numero,
        "tipo": tipo,
        "capacidade": capacidade,
        "tarifa_base": tarifa
    })
    print(" Quarto atualizado")

def excluir_quarto_menu():
    numero = int(input("Número do quarto: "))
    excluir_quarto(numero)
    print("Quarto excluído")

def bloquear_quarto_menu():
    numero = int(input("Número do quarto: "))
    inicio = date.fromisoformat(input("Início (YYYY-MM-DD): "))
    fim = date.fromisoformat(input("Fim (YYYY-MM-DD): "))
    motivo = input("Motivo: ")
    bloquear_quarto(numero, inicio, fim, motivo)
    print("Quarto bloqueado")

def desbloquear_quarto_menu():
    numero = int(input("Número do quarto: "))
    desbloquear_quarto(numero)
    print(" Quarto desbloqueado")

# RESERVAS

def criar_reserva_menu():
    print("\n== Criar Reserva ==")

    # HÓSPEDE (OBRIGATÓRIO)
    
    while True:
        entrada = input("ID hóspede: ").strip()

        if not entrada:
            print("❌ ID do hóspede é obrigatório.")
            continue

        if not entrada.isdigit():
            print("❌ ID deve ser um número.")
            continue

        hospede_id = int(entrada)
        hospede = buscar_hospede_por_id(hospede_id)

        if not hospede:
            print("❌ Hóspede não encontrado.")
            continue

        break

    # QUARTO (OBRIGATÓRIO)
    
    while True:
        entrada = input("Número do quarto: ").strip()

        if not entrada:
            print(" Número do quarto é obrigatório.")
            continue

        if not entrada.isdigit():
            print(" Número do quarto deve ser numérico.")
            continue

        quarto_numero = int(entrada)
        quarto = buscar_quarto_por_numero(quarto_numero)

        if not quarto:
            print(" Quarto não encontrado.")
            continue

        if not quarto.esta_disponivel():
           print("Quarto não está disponível")
           return

        break

    # DATAS (OBRIGATÓRIAS)

    while True:
        try:
            entrada = date.fromisoformat(input("Entrada (YYYY-MM-DD): ").strip())
            saida = date.fromisoformat(input("Saída (YYYY-MM-DD): ").strip())

            if saida <= entrada:
                print("Data de saída deve ser após a entrada.")
                continue

            break
        except ValueError:
            print("Data inválida. Use o formato YYYY-MM-DD.")

    # CRIA RESERVA

    reserva = Reserva(hospede, quarto, entrada, saida)
    criar_reserva(reserva)

    print("Reserva criada com sucesso")
     

def confirmar_reserva_menu():
    id = int(input("ID reserva: "))
    r = buscar_reserva(id)
    r.confirmar()
    atualizar_reserva(r)
    print(" Reserva confirmada")

def checkin_menu():
    id_reserva = int(input("ID da reserva: "))
    reserva = buscar_reserva(id_reserva)

    if not reserva:
        print("Reserva não encontrada.")
        return

    hora_str = input("Hora do check-in (HH:MM): ")
    try:
        h, m = map(int, hora_str.split(":"))
        agora = datetime.combine(reserva.data_entrada, time(h, m))
        reserva.fazer_checkin(agora)
        atualizar_reserva(reserva)
        print("Check-in realizado com sucesso.")
    except ValueError as e:
        print(f"Erro: {e}")


def checkout_menu():
    id = int(input("ID reserva: "))
    r = buscar_reserva(id)
    r.fazer_checkout(datetime.now())
    atualizar_reserva(r)
    print("Check-out realizado")


def cancelar_menu():
    id = int(input("ID reserva: "))
    r = buscar_reserva(id)
    r.cancelar(date.today())
    atualizar_reserva(r)
    print("Reserva cancelada")


def noshow_menu():
    id = int(input("ID reserva: "))
    r = buscar_reserva(id)
    r.marcar_no_show(date.today())
    atualizar_reserva(r)
    print("No-show registrado")


def excluir_reserva_menu():
    id = int(input("ID reserva: "))
    remover_reserva(id)
    print("Reserva excluída")


from persistencia.reserva_dao import listar_reservas_completas

def listar_reservas_menu():
    reservas = listar_reservas_completas()

    if not reservas:
        print("Nenhuma reserva cadastrada.")
        return

    for r in reservas:
        print(f"""
========= RESERVA #{r['reserva_id']} =========
Hóspede: {r['hospede_nome']} ({r['hospede_documento']})
Quarto: {r['quarto_numero']} ({r['quarto_tipo']})
Capacidade: {r['quarto_capacidade']}
Entrada: {r['data_entrada']}
Saída: {r['data_saida']}
Hóspedes: {r['num_hospedes']}
Origem: {r['origem']}
Estado: {r['estado']}
---------------------------------------
Tarifa base: R$ {r['tarifa_base']}
Adicionais: R$ {r['total_adicionais']}
Pago: R$ {r['total_pago']}
---------------------------------------
Check-in real: {r['check_in_real']}
Check-out real: {r['check_out_real']}
Cancelamento: {r['data_cancelamento']}
No-show: {r['data_no_show']}
=======================================
""")

# Parte financeira

def pagamento_menu():
    id = int(input("ID da reserva: "))
    reserva = buscar_reserva(id)

    if not reserva:
        print(" Reserva não encontrada")
        return

    valor = float(input("Valor pago: "))
    forma = input("Forma de pagamento [PIX]: ") or "PIX"

    try:
        pagamento = Pagamento(
            reserva_id=id,
            valor=valor,
            forma=forma,
            data_pagamento=date.today().isoformat()
        )
        registrar_pagamento(pagamento)
        print("Pagamento registrado")
    except Exception as e:
        print(f"Erro ao registrar pagamento: {e}")

def listar_pagamentos_menu():
    id = int(input("ID reserva: "))
    for p in listar_pagamentos(id):
        print(p.to_dict())


def adicional_menu():
    id = int(input("ID da reserva: "))
    reserva = buscar_reserva(id)

    if not reserva:
        print("Reserva não encontrada")
        return

    descricao = input("Descrição: ")
    valor = float(input("Valor: "))

    try:
        adicional = Adicional(
            reserva_id=id,
            descricao=descricao,
            valor=valor
        )
        adicionar_adicional(adicional)
        print("✔ Adicional lançado")
    except Exception as e:
        print(f"Erro ao adicionar adicional: {e}")


def relatorio_taxa_ocupacao_menu():
    inicio = date.fromisoformat(input("Data início (YYYY-MM-DD): "))
    fim = date.fromisoformat(input("Data fim (YYYY-MM-DD): "))

    taxa = calcular_taxa_ocupacao(inicio, fim)
    print(f"\nTaxa de ocupação: {taxa}%")


def relatorio_receita_menu():
    inicio = date.fromisoformat(input("Data início (YYYY-MM-DD): "))
    fim = date.fromisoformat(input("Data fim (YYYY-MM-DD): "))

    receitas = calcular_receita_por_tipo(inicio, fim)

    print("\nReceita por tipo de quarto")
    for tipo, valor in receitas.items():
        print(f"- {tipo}: R$ {valor:.2f}")


def relatorio_cancelamentos_menu():
    inicio = date.fromisoformat(input("Data início (YYYY-MM-DD): "))
    fim = date.fromisoformat(input("Data fim (YYYY-MM-DD): "))

    canceladas, noshow = calcular_cancelamentos_noshow(inicio, fim)

    print("\nCancelamentos e No-show")
    print(f"Canceladas: {canceladas}")
    print(f"No-show: {noshow}")


def menu():
    while True:
        print("""
╔══════════════════════════════════════════════════════╗
║                    HOTEL WISE                        ║
╚══════════════════════════════════════════════════════╝

┌─────────────── HÓSPEDES ───────────────┐──────────┐
│  1 Criar     │  2 Listar   │3 Atualiza.│4 Excluir │
└───────────────────────────────────────────────────┘

┌──────────────── QUARTOS ────────────────┐
│  5 Criar     │  6 Listar   │ 7 Atualizar│   
│  9 Bloquear  │ 10 Desbloq. │ 8 Excluir  │            
└─────────────────────────────────────────┘

┌──────────────── RESERVAS ───────────────┐
│ 11 Criar     │ 12 Listar   │ 13 Confirm.│ 14 Check-in │
│ 15 Check-out │ 16 Cancelar │ 17 No-show │ 18 Excluir  │
└─────────────────────────────────────────┘

┌─────────────── FINANCEIRO ──────────────┐─────────────┐
│ 19 Pagamento │ 20 Listar  │ 21 Adicional│ 22 Listar   │
└─────────────────────────────────────────┘─────────────┘

┌─────────────── RELATÓRIOS ──────────────┐
│ 23 Taxa de Ocupação                     │
│ 24 Receita por Tipo de Quarto           │
│ 25 Cancelamentos / No-show              │
└─────────────────────────────────────────┘
              
┌─────────────── SISTEMA ─────────────────┐
│  0 Sair                                 │
└─────────────────────────────────────────┘
""")

        op = input("Escolha uma opção: ").strip()

        if op == "1": criar_hospede_menu()
        elif op == "2": listar_hospedes_menu()
        elif op == "3": atualizar_hospede_menu()
        elif op == "4": excluir_hospede_menu()
        elif op == "5": criar_quarto_menu()
        elif op == "6": listar_quartos_menu()
        elif op == "7": atualizar_quarto_menu()
        elif op == "8": excluir_quarto_menu()
        elif op == "9": bloquear_quarto_menu()
        elif op == "10": desbloquear_quarto_menu()
        elif op == "11": criar_reserva_menu()
        elif op == "12": listar_reservas_menu()
        elif op == "13": confirmar_reserva_menu()
        elif op == "14": checkin_menu()
        elif op == "15": checkout_menu()
        elif op == "16": cancelar_menu()
        elif op == "17": noshow_menu()
        elif op == "18": excluir_reserva_menu()
        elif op == "19": pagamento_menu()
        elif op == "20": listar_pagamentos_menu()
        elif op == "21": adicional_menu()
        elif op == "22": listar_adicionais()
        elif op == "23": relatorio_taxa_ocupacao_menu()
        elif op == "24": relatorio_receita_menu()
        elif op == "25": relatorio_cancelamentos_menu()
        elif op == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida")

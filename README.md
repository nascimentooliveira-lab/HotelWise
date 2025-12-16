## HotelWise 

# Descrição do Projeto

O HotelWise é um sistema de gerenciamento de reservas e inventário de hotéis, focado em fornecer uma solução robusta para o controle de acomodações e hóspedes.

O projeto pode ser acessado via Interface de Linha de Comando (CLI) para gestão interna, ou opcionalmente exposto como uma CLI para consumo por outras aplicações. A implementação enfatiza boas práticas de Orientação a Objetos, garantindo alta modularidade e facilidade de manutenção.


# Objetivos do Projeto e Foco Técnico

Este projeto possui um duplo foco: entregar um produto funcional e otimizar e automatizar o ciclo de vida de uma reserva, desde a busca inicial pelo hóspede até o controle de inventário e gestão financeira pelo hotel.


## ⚙️ Tecnologias e Dependência

![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) 
![Git](https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=git&logoColor=white) 
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)


## 🏗️ Estrutura Planejada de Classes

A modelagem de classes é o ponto central deste projeto, desenhada para demonstrar conceitos de Orientação a Objetos.

### 📚 Camadas Principais

| Camada | Responsabilidade Chave |
| :--- | :--- |
| **Domínio (Entidades)** | Lógica de Negócios, Validações e Modelos de Dados Centrais. |
| **Persistência** | Conexão e operações de salvamento/carga de dados SQLite. |
| **Serviço (Lógica)** | Orquestração de regras complexas (ex: cálculo de tarifa, verificação de disponibilidade). |
| **Interface CLI** | Interação com o usuário. |


## 🏨 UML Textual

## Classe Hospede 
---------------------------------
- id: int
- nome: str
- documento: str
- email: str
- telefone: str
---------------------------------
+ to_dict(): dict
+ __str__(): str
  
Relacionamentos

1 Hospede —— Reserva

Um hóspede pode ter várias reservas

## Classe Quarto
---------------------------------
- numero: int
- tipo: str
- capacidade: int
- tarifa_base: float
- _status: str
- _bloqueios: list
- _reservas: list
---------------------------------
+ status(): str
+ status(valor): void
+ ocupar(): void
+ desbloquear(): void
+ bloquear(inicio, fim, motivo): void
+ esta_bloqueado(data): bool
+ adicionar_reserva(reserva): void
+ to_dict(): dict
+ __str__(): str

Relacionamentos

1 Quarto —— * Reserva

Um quarto pode ter várias reservas

Agregação:

Quarto mantém lista de reservas associadas


## Classe Reserva
------------------------------------------------
- id: int
- hospede: Hospede
- quarto: Quarto
- data_entrada: date
- data_saida: date
- num_hospedes: int
- origem: str
- estado: str
- check_in_real: datetime
- check_out_real: datetime
- data_cancelamento: date
- data_no_show: date
------------------------------------------------
+ confirmar(): void
+ fazer_checkin(agora): void
+ fazer_checkout(agora): void
+ cancelar(): void
+ marcar_no_show(): void
+ calcular_valor_total(): float
+ total_adicionais(): float
+ total_pago(): float
+ total_devido(): float
+ to_dict(): dict
+ __str__(): str

Relacionamentos

1 Reserva —— 1 Hospede

1 Reserva —— 1 Quarto

Composição:

Reserva não existe sem hóspede e quarto 

## Class Pagamento
-------------------------------
- id: int
- reserva_id: int
- valor: float
- forma: str
- data_pagamento: date
-------------------------------
+ to_dict(): dict

Relacionamentos

1 Reserva —— * Pagamento

Uma reserva pode ter vários pagamentos

## Classe Adicional
-------------------------------
- id: int
- reserva_id: int
- descricao: str
- valor: float
-------------------------------
+ to_dict(): dict

Relacionamentos

1 Reserva —— * Adicional

Uma reserva pode ter vários adicionais


🚀 Como Executar
Siga os passos abaixo para executar o ChatBot Cariri Turismo em sua máquina local.

1. Pré-requisitos

Python 3.10 ou superior.
Git instalado.
2. Clone o Repositório - Abra seu terminal ou Git Bash e utilize o comando abaixo para criar uma cópia local do projeto.

git clone https://github.com/nascimentooliveira-lab/HotelWise.git
3. Navegue até a pasta - Entre na pasta do projeto que foi recém-criada.

RESERVA_HOTEIS_HOTELWISE
4. Execute - O programa principal que inicia a interface CLI. Para executá-lo, utilize o seguinte comando a partir da pasta raiz do projeto:

python menu.py


## Autor

* **Malaquias de oliveira** (GitHub: nascimentooliveira-lab)
* **Email:** nascimento.oliveira@aluno.edu.br

## 📜 licença
    Este projeto é disponibilizado somente para fins de visualização e aprendizado.
    Você pode ler o código, mas não tem permissão para modificá-lo, redistribuílo 
    seja de forma parcial ou total, sem autorização do autor.
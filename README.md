## HotelWise 

# Descrição do Projeto

O HotelWise é um sistema de gerenciamento de reservas e inventário de hotéis, focado em fornecer uma solução robusta para o controle de acomodações e hóspedes.

O projeto pode ser acessado via Interface de Linha de Comando (CLI) para gestão interna, ou opcionalmente exposto como uma API mínima (usando FastAPI/Flask) para consumo por outras aplicações. A implementação enfatiza  boas práticas de Orientação a Objetos, garantindo alta modularidade e facilidade de manutenção.


# Objetivos do Projeto e Foco Técnico

Este projeto possui um duplo foco: entregar um produto funcional e servir como um excelente laboratório para conceitos avançados de programação.

| Categoria | Detalhamento |
| :--- | :--- |
| **Arquitetura** | Desenvolver um sistema modular com forte aplicação de princípios de **Orientação a Objetos** (Herança, Encapsulamento, Composição e Polimorfismo). |
| **Funcionalidades** | Implementar o ciclo completo de reserva, incluindo **check-in/check-out**, **política de cancelamento** e **bloqueios** de quartos por manutenção. |
| **Modelagem** | Gerenciar a complexidade de **tarifas por temporada** e fornecer **relatórios de desempenho** (Taxa de Ocupação, ADR, RevPAR). |
| **Persistência** | Utilizar soluções simples e leves de persistência de dados: **JSON** ou **SQLite** (a ser definida na fase inicial). |
**Interface** | `argparse` (Python) | Para construção da Interface de Linha de Comando (CLI). |
---

## ⚙️ Tecnologias e Dependência


![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Git](https://img.shields.io/badge/GIT-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GITHUB-100000?style=for-the-badge&logo=github&logoColor=white)


## 🏗️ Estrutura Planejada de Classes

A modelagem de classes é o ponto central deste projeto, desenhada para demonstrar conceitos de Orientação a Objetos.

### 📚 Camadas Principais

| Camada | Responsabilidade Chave |
| :--- | :--- |
| **Domínio (Entidades)** | Lógica de Negócios, Validações e Modelos de Dados Centrais. |
| **Persistência** | Conexão e operações de salvamento/carga de dados (JSON/SQLite). |
| **Serviço (Lógica)** | Orquestração de regras complexas (ex: cálculo de tarifa, verificação de disponibilidade). |
| **Interface (CLI/API)** | Interação com o usuário ou recebimento de requisições HTTP. |

### 📝 Detalhamento das Classes e Aplicação de POO

| Classe | Conceito POO Aplicado | Descrição e Funcionalidades Chave |
| :--- | :--- | :--- |
| **Pessoa** | Herança (Classe Base) | Classe base para `Hospede` e `Funcionario`, contendo atributos comuns (nome, contato). |
| **Hospede** | Herança | Estende `Pessoa`. Contém dados específicos do hóspede e histórico de reservas. |
| **Acomodacao** | Encapsulamento (Classe Base) | Classe base para tipos de quartos. Garante que o status (`disponível`, `ocupado`, `bloqueado`) seja modificado apenas por métodos controlados. |
| **QuartoSimples** | Herança | Estende `Acomodacao`, com tarifa padrão. |
| **QuartoDeluxe** | Herança | Estende `Acomodacao`, com atributos adicionais (vista, frigobar). |
| **Tarifa** | Composição | Armazena a estrutura de preços. Uma `Reserva` **compõe** uma `Tarifa` para calcular o valor final. |
| **Reserva** | Validações/Lógica de Negócio | Contém a lógica de *check-in/check-out* e **validações** de regras (ex: data de check-out deve ser posterior à de check-in). |
| **InventarioManager** | Serviço / Composição | Gerencia a lista de todas as `Acomodacoes`, aplicando bloqueios de manutenção e consultando disponibilidade. |
---

## Autor

* **Malaquias de oliveira** (GitHub: nascimentooliveira-lab)
* **Email:** nascimento.oliveira@aluno.edu.br

## 📜 licença
    Este projeto é disponibilizado somente para fins de visualização e aprendizado.
    Você pode ler o código, mas não tem permissão para modificá-lo, redistribuílo 
    seja de forma parcial ou total, sem autorização do autor.
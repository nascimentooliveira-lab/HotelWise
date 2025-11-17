class Pessoa:
    """
    Classe base para todas as entidades humanas (Hóspede e Funcionário).
    
    Aplica o conceito de **Herança** ao fornecer atributos comuns (nome, contato).
    """
    def __init__(self):
        """Inicializa atributos comuns: nome e contato."""
        pass

class Hospede(Pessoa):
    """
    Representa um hóspede. Estende a classe Pessoa.
    
    Aplica o conceito de **Herança**. Contém dados específicos e histórico de reservas.
    """
    def __init__(self):
        """Inicializa o hóspede e seu histórico de reservas."""
        super().__init__()
        pass

class Acomodacao:
    """
    Classe base para todos os tipos de quartos do hotel.
    
    Aplica o conceito de **Encapsulamento** ao garantir que o status
    (disponível, ocupado, bloqueado) seja alterado apenas por métodos controlados.
    """
    def __init__(self):
        """Inicializa o número, tipo e status da acomodação."""
        pass

class QuartoSimples(Acomodacao):
    """
    Representa um tipo de quarto de tarifa padrão.
    
    Aplica o conceito de **Herança**. Estende Acomodacao.
    """
    def __init__(self):
        """Inicializa o Quarto Simples."""
        super().__init__()
        pass

class QuartoDeluxe(Acomodacao):
    """
    Representa um tipo de quarto premium com atributos adicionais.
    
    Aplica o conceito de **Herança**. Estende Acomodacao.
    """
    def __init__(self):
        """Inicializa o Quarto Deluxe com seus atributos extras (vista, frigobar)."""
        super().__init__()
        pass

class Tarifa:
    """
    Armazena a estrutura de preços.
    
    Uma Reserva **compõe** uma Tarifa para calcular o valor final, demonstrando **Composição**.
    """
    def __init__(self):
        """Inicializa os valores de tarifa (base, por temporada, etc.)."""
        pass

class Reserva:
    """
    Gerencia o ciclo de vida de uma reserva (criação, check-in/out, cancelamento).
    
    Contém a **Lógica de Negócio** central e validações (ex: datas).
    """
    def __init__(self):
        """Inicializa a reserva, ligando-a a um hóspede, acomodação e tarifa."""
        pass
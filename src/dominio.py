class Pessoa:
    """
    Classe base para todas as entidades humanas (Hóspede e Funcionário).
    """
    def __init__(self, nome, cpf, idade, endereco, email, telefone):
        self.nome = nome                  
        self.__cpf = cpf                  
        self.__idade = None               
        self.endereco = endereco          
        self.email = email                
        self.telefone = telefone          
        
        # Chama o setter para aplicar a regra de validação
        self.idade = idade 

    @property
    def cpf(self):
        # Getter para o atributo privado __cpf
        return self.__cpf

    @property
    def idade(self):
        # Getter para o atributo privado __idade
        return self.__idade
    
    @idade.setter
    def idade(self, valor):
        # Setter com lógica de validação
        if valor <= 0:
            raise ValueError("Idade inválida: O valor deve ser maior que zero.")
        self.__idade = valor

class Hospede(Pessoa):
    """
    Representa um hóspede. Estende a classe Pessoa.
    
    Aplica o conceito de **Herança**. Contém dados específicos e histórico de reservas.
    """
    def __init__(self, nome, cpf, idade, endereco, email, telefone):
        """Inicializa o hóspede e seu histórico de reservas."""
        # Chama o construtor da classe base (Pessoa)
        super().__init__(nome, cpf, idade, endereco, email, telefone)
        
        # Histórico de reservas é protegido (convenção _ )
        self._historico_reservas = []
        
    @property
    def historico_reservas(self):
        # Retorna uma cópia para evitar modificações externas diretas
        return list(self._historico_reservas)

    def adicionar_reserva(self, reserva):
        self._historico_reservas.append(reserva)

class Acomodacao:
    """
    Classe base para todos os tipos de quartos do hotel.
    
    Aplica o conceito de **Encapsulamento** ao garantir que o status
    (disponível, ocupado, bloqueado) seja alterado apenas por métodos controlados.
    """
    def __init__(self, numero, tipo):
        """Inicializa o número, tipo e status da acomodação."""
        self.numero = numero
        self.tipo = tipo
        self.__status = "disponível" # Atributo privado

    @property
    def status(self):
        return self.__status

    def ocupar(self):
        if self.__status != "disponível":
            raise Exception(f"Acomodação {self.numero} não está disponível para ocupação.")
        self.__status = "ocupado"

    def liberar(self):
        self.__status = "disponível"

    def bloquear(self):
        self.__status = "bloqueado"

class QuartoSimples(Acomodacao):
    """
    Representa um tipo de quarto de tarifa padrão.
    
    Aplica o conceito de **Herança**. Estende Acomodacao.
    """
    def __init__(self, numero):
        """Inicializa o Quarto Simples."""
        # Define o tipo específico e chama o construtor base
        super().__init__(numero, tipo="Quarto Simples")

class QuartoDeluxe(Acomodacao):
    """
    Representa um tipo de quarto premium com atributos adicionais.
    
    Aplica o conceito de **Herança**. Estende Acomodacao.
    """
    def __init__(self, numero, vista):
        """Inicializa o Quarto Deluxe com seus atributos extras (vista, frigobar)."""
        super().__init__(numero, tipo="Quarto Deluxe")
        self.vista = vista
        self.frigobar = True 
        
class Tarifa:
    """
    Armazena a estrutura de preços.
    
    Uma Reserva **compõe** uma Tarifa para calcular o valor final, demonstrando **Composição**.
    O valor base é encapsulado.
    """
    def __init__(self, valor_base, taxa_temporada=0):
        """Inicializa os valores de tarifa (base, por temporada, etc.)."""
        self.__valor_base = valor_base # Encapsulado
        self.taxa_temporada = taxa_temporada

    @property
    def valor_total(self):
        # Propriedade que calcula o valor final
        return self.__valor_base + self.taxa_temporada

class Reserva:
    """
    Gerencia o ciclo de vida de uma reserva (criação, check-in/out, cancelamento).
    
    Aplica o conceito de **Composição** por "ter um" Hospede, uma Acomodacao e uma Tarifa.
    Contém a **Lógica de Negócio** central e validações.
    """
    def __init__(self, hospede, acomodacao, tarifa, data_inicio, data_fim):
        """Inicializa a reserva, ligando-a a um hóspede, acomodação e tarifa."""
        self.hospede = hospede
        self.acomodacao = acomodacao
        self.tarifa = tarifa
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.__ativa = True # Estado da reserva é encapsulado

        # Lógica de negócio: a reserva ocupa o quarto e se adiciona ao histórico do hóspede
        self.acomodacao.ocupar()
        self.hospede.adicionar_reserva(self)
    
    @property
    def ativa(self):
        return self.__ativa

    def cancelar(self):
        if not self.__ativa:
            raise Exception("Reserva já cancelada.")
        
        # Lógica de negócio: liberar a acomodação ao cancelar
        self.acomodacao.liberar()
        self.__ativa = False

    def valor_reserva(self):
        return self.tarifa.valor_total

class InventarioManager:
    """
    Gerencia todas as acomodações do hotel.
    Aplica Composição e Encapsulamento.
    """

    def __init__(self):
        """Inicializa a coleção de acomodações."""
        self.__acomodacoes = []  # lista privada → composição e encapsulamento

    @property
    def acomodacoes(self):
        """Permite apenas leitura controlada da lista de acomodações."""
        return self.__acomodacoes

    def adicionar_acomodacao(self, acomodacao):
        """
        Adiciona uma acomodação à lista.
        """
        if not isinstance(acomodacao, Acomodacao):
            raise TypeError("Apenas objetos do tipo Acomodacao podem ser adicionados.")
        self.__acomodacoes.append(acomodacao)

    def listar_disponiveis(self):
        """
        Retorna todas as acomodações cujo status é 'disponível'.
        """
        return [q for q in self.__acomodacoes if q.status == "disponível"]

    def bloquear_quarto(self, numero):
        """
        Bloqueia um quarto para manutenção.
        """
        quarto = self.__encontrar_quarto(numero)
        if quarto:
            quarto.bloquear()
        else:
            raise ValueError(f"Quarto {numero} não encontrado.")

    def liberar_quarto(self, numero):
        """
        Libera um quarto bloqueado ou ocupado.
        """
        quarto = self.__encontrar_quarto(numero)
        if quarto:
            quarto.liberar()
        else:
            raise ValueError(f"Quarto {numero} não encontrado.")

    def __encontrar_quarto(self, numero):
        """
        Busca internamente uma acomodação pelo número.
        Encapsulado: método privado para uso interno apenas.
        """
        for q in self.__acomodacoes:
            if q.numero == numero:
                return q
        return None

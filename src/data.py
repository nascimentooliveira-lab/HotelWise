
import sqlite3

class Persistencia:
    """
    Classe de serviço para lidar com operações de persistência.
    
    Aplica **Encapsulamento** ao atributo privado __arquivo.
    """
    
    def __init__(self, caminho_arquivo="hotel.db"):
        """
        Inicializa o caminho do arquivo de banco de dados.
        O atributo é encapsulado.
        """
        self.__arquivo = caminho_arquivo   # atributo privado
        self.__conectar()

    @property
    def arquivo(self):
        """
        Permite apenas ler o caminho do arquivo.
        Encapsulamento: não permite alterar de fora.
        """
        return self.__arquivo

    def __conectar(self):
        """
        Método privado que cria a conexão com o SQLite.
        Faz parte do encapsulamento interno.
        """
        self.__conexao = sqlite3.connect(self.__arquivo)
        self.__cursor = self.__conexao.cursor()

    def salvar_dados(self):
        """
        Exemplo simples de operação.
        (Encapsulamento mantém __arquivo protegido)
        """
        print(f"Salvando dados usando o banco: {self.arquivo}")
        # lógica virá depois
        print("Dados salvos com sucesso.")

    def carregar_dados(self):
        """
        Apenas uma simulação.
        """
        print(f"Carregando dados do banco: {self.arquivo}")
        return {"status": "ok"}

    def fechar(self):
        """
        Fecha a conexão.
        """
        self.__conexao.close()
## tabelas a ser adiconadas futuramente
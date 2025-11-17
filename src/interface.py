import argparse

class HotelWiseCLI:
    """
    Classe para gerenciar a Interface de Linha de Comando (CLI) do sistema.
    
    Utilizará a biblioteca `argparse` para interagir com o usuário e
    chamar os métodos nas classes de Serviço.
    """
    def __init__(self):
        """Configura os comandos e o parser da CLI."""
        self.parser = argparse.ArgumentParser(description="Sistema de Gerenciamento HotelWise")
        pass

    def executar(self):
        """Processa a entrada do usuário e executa o comando correspondente."""
        pass
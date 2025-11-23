import argparse

class HotelWiseCLI:
    """
    Gerencia a interface de linha de comando (CLI) do sistema HotelWise.
    """

    def __init__(self):
        """Configura o parser e os comandos da CLI."""
        self.__parser = argparse.ArgumentParser(
            description="Sistema de Gerenciamento HotelWise"
        )

        # Encapsulando a lógica interna de comandos
        self.__subparsers = self.__parser.add_subparsers(
            dest="comando", help="Comandos disponíveis"
        )

        self.__configurar_comandos()

    def __configurar_comandos(self):
        """Define todos os comandos possíveis da CLI."""

        # Comando: listar quartos disponíveis
        listar = self.__subparsers.add_parser(
            "listar_quartos", help="Lista todos os quartos disponíveis"
        )
        listar.add_argument(
            "--tipo", type=str, default=None, help="Filtrar por tipo de quarto"
        )

        # Comando: adicionar hóspede
        adicionar = self.__subparsers.add_parser(
            "adicionar_hospede", help="Adiciona um novo hóspede"
        )
        adicionar.add_argument("nome", type=str, help="Nome do hóspede")
        adicionar.add_argument("cpf", type=str, help="CPF do hóspede")
        adicionar.add_argument("idade", type=int, help="Idade do hóspede")

    def __executar_comando(self, args):
        """
        Método privado que executa a ação de acordo com o comando.
        Encapsula toda a lógica interna da CLI.
        """
        if args.comando == "listar_quartos":
            tipo = args.tipo
            print(f"Listando quartos disponíveis do tipo: {tipo}")
            # Aqui você chamaria InventarioManager.listar_disponiveis()
        elif args.comando == "adicionar_hospede":
            nome = args.nome
            cpf = args.cpf
            idade = args.idade
            print(f"Adicionando hóspede: {nome}, CPF: {cpf}, Idade: {idade}")
            # Aqui você chamaria HospedeService.adicionar_hospede()
        else:
            self.__parser.print_help()

    def executar(self):
        """
        Método público que processa a entrada do usuário
        e executa o comando correspondente.
        """
        args = self.__parser.parse_args()
        self.__executar_comando(args)

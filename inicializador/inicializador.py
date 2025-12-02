
from persistencia.dados import seed_dados

def inicializar_aplicacao():
    """
    Função principal para garantir que o banco de dados seja criado
    e populado com os dados iniciais.
    """
    print("Iniciando Persistência HotelWise")
    try:
        # Chama a rotina que cria o arquivo hotelwise.db, tabelas e dados iniciais
        
        seed_dados() 
        print(" Inicialização do Banco de Dados concluída com sucesso.")
    except Exception as e:
        print(f"ERRO FATAL ao inicializar o banco de dados: {e}")
        return

if __name__ == "__main__":
    inicializar_aplicacao()

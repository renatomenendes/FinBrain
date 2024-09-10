# Expor a versão do pacote
__version__ = "1.0.0"

# Função para inicializar conexão com o banco de dados
import sqlite3

def conectar_banco_dados(caminho_banco='banco.db'):  # Use o caminho correto para o banco
    """Inicializa a conexão com o banco de dados SQLite"""
    return sqlite3.connect(caminho_banco)

# Criação de uma conexão global ao banco de dados para ser reutilizada
conexao_banco = conectar_banco_dados()

# Importar corretamente os módulos
from .persistencia import Persistencia

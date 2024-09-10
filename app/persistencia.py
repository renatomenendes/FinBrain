import sqlite3
from app.auditoria import Auditoria

class Persistencia:
    """
    Classe responsável por gerenciar a persistência de dados bancários no banco de dados SQLite.

    Esta classe oferece métodos para criar tabelas, salvar contas, registrar transações e 
    carregar dados do banco, além de registrar eventos de auditoria.
    """

    def __init__(self, banco_dados='banco.db'):
        """
        Inicializa a conexão com o banco de dados e cria as tabelas de contas e transações.

        Parâmetros:
        ----------
        banco_dados : str, opcional
            O nome do arquivo do banco de dados SQLite. O padrão é 'banco.db'.
        """
        self.conexao = sqlite3.connect(banco_dados)
        self.auditoria = Auditoria()  # Instancia a auditoria para registrar eventos
        self.criar_tabelas()

    def criar_tabelas(self):
        """
        Cria as tabelas de contas e transações no banco de dados, caso elas ainda não existam.

        As tabelas são:
        - `contas`: Armazena os dados das contas bancárias (número da conta, nome, senha hash, saldo).
        - `transacoes`: Armazena as transações realizadas (tipo, valor, data).
        """
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                numero_conta TEXT PRIMARY KEY,
                nome_cliente TEXT,
                senha_hash TEXT,
                saldo REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_conta TEXT,
                tipo TEXT,
                valor REAL,
                data TEXT
            )
        ''')
        self.conexao.commit()
        self.auditoria.registrar_evento("Tabelas criadas ou verificadas no banco de dados.")

    def salvar_conta(self, conta):
        """
        Insere ou atualiza uma conta bancária no banco de dados.

        Parâmetros:
        ----------
        conta : ContaBancaria
            A instância da conta bancária a ser salva ou atualizada no banco de dados.
        """
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO contas (numero_conta, nome_cliente, senha_hash, saldo)
            VALUES (?, ?, ?, ?)
        ''', (conta.numero_conta, conta.nome_cliente, conta.senha_hash, conta.saldo_atual()))
        self.conexao.commit()
        self.auditoria.registrar_evento(f"Conta {conta.numero_conta} salva no banco de dados.")

    def carregar_conta(self, numero_conta):
        """
        Carrega os dados de uma conta bancária a partir do banco de dados.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta que será carregada.

        Retorna:
        --------
        tuple
            Uma tupla contendo os dados da conta (numero_conta, nome_cliente, senha_hash, saldo) ou None se a conta não for encontrada.
        """
        cursor = self.conexao.cursor()
        cursor.execute("SELECT numero_conta, nome_cliente, senha_hash, saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
        conta_dados = cursor.fetchone()
        if conta_dados:
            self.auditoria.registrar_evento(f"Conta {numero_conta} carregada do banco de dados.")
            return conta_dados
        return None

    def registrar_transacao(self, numero_conta, tipo, valor):
        """
        Insere uma nova transação no banco de dados.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta em que a transação foi realizada.
        tipo : str
            O tipo da transação (ex: 'deposito', 'saque', 'transferencia').
        valor : float
            O valor da transação.

        Retorna:
        --------
        None
        """
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT INTO transacoes (numero_conta, tipo, valor, data)
            VALUES (?, ?, ?, datetime('now'))
        ''', (numero_conta, tipo, valor))
        self.conexao.commit()
        self.auditoria.registrar_evento(f"Transação '{tipo}' de R${valor:.2f} registrada para a conta {numero_conta}.")

    def carregar_transacoes(self, numero_conta):
        """
        Carrega todas as transações associadas a uma conta.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta cujas transações serão carregadas.

        Retorna:
        --------
        list
            Uma lista de tuplas contendo os dados das transações (id, numero_conta, tipo, valor, data).
        """
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM transacoes WHERE numero_conta = ?", (numero_conta,))
        transacoes = cursor.fetchall()
        self.auditoria.registrar_evento(f"Transações carregadas para a conta {numero_conta}.")
        return transacoes

    def fechar_conexao(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.conexao:
            self.conexao.close()
            self.auditoria.registrar_evento("Conexão com o banco de dados fechada.")
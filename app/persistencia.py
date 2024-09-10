import sqlite3
from app.auditoria import Auditoria

class Persistencia:
    def __init__(self, banco_dados='banco.db'):
        """Inicializa a conexão com o banco de dados e cria as tabelas se não existirem."""
        self.conexao = sqlite3.connect(banco_dados)
        self.auditoria = Auditoria()  # Usado para registrar eventos
        self.criar_tabelas()

    def criar_tabelas(self):
        """Cria as tabelas de contas e transações no banco de dados, caso não existam."""
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
        """Insere ou atualiza uma conta bancária no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO contas (numero_conta, nome_cliente, senha_hash, saldo)
            VALUES (?, ?, ?, ?)
        ''', (conta.numero_conta, conta.nome_cliente, conta.senha_hash, conta.saldo_atual()))
        self.conexao.commit()
        self.auditoria.registrar_evento(f"Conta {conta.numero_conta} salva no banco de dados.")

    def carregar_conta(self, numero_conta):
        """Carrega a conta a partir do banco de dados usando o número da conta."""
        cursor = self.conexao.cursor()
        # Seleciona apenas as colunas necessárias
        cursor.execute("SELECT numero_conta, nome_cliente, senha_hash, saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
        conta_dados = cursor.fetchone()
        if conta_dados:
            self.auditoria.registrar_evento(f"Conta {numero_conta} carregada do banco de dados.")
            return conta_dados
        return None

    def registrar_transacao(self, numero_conta, tipo, valor):
        """Insere uma nova transação no banco de dados."""
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT INTO transacoes (numero_conta, tipo, valor, data)
            VALUES (?, ?, ?, datetime('now'))
        ''', (numero_conta, tipo, valor))
        self.conexao.commit()
        self.auditoria.registrar_evento(f"Transação '{tipo}' de R${valor:.2f} registrada para a conta {numero_conta}.")


    def carregar_transacoes(self, numero_conta):
        """Carrega todas as transações de uma conta pelo número da conta."""
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM transacoes WHERE numero_conta = ?", (numero_conta,))
        transacoes = cursor.fetchall()
        self.auditoria.registrar_evento(f"Transações carregadas para a conta {numero_conta}.")
        return transacoes

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.conexao:
            self.conexao.close()
            self.auditoria.registrar_evento("Conexão com o banco de dados fechada.")
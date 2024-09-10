from app.persistencia import Persistencia
from app.autenticacao import Autenticacao
from app.transacoes import TransacaoBancaria

class ContaBancaria:
    """
    Classe para gerenciar operações básicas de uma conta bancária.

    Atributos:
    ----------
    numero_conta : str
        O número único da conta bancária.
    nome_cliente : str
        O nome do titular da conta bancária.
    senha_hash : str
        O hash da senha da conta, utilizado para autenticação.
    saldo : float
        O saldo atual da conta bancária.
    """
    def __init__(self, numero_conta, nome_cliente, senha_hash, saldo_inicial=0):
        """
        Inicializa uma nova conta bancária.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta.
        nome_cliente : str
            O nome do titular da conta.
        senha_hash : str
            O hash da senha do cliente.
        saldo_inicial : float, opcional
            O saldo inicial da conta. O padrão é 0.
        """
        self.numero_conta = numero_conta
        self.nome_cliente = nome_cliente
        self.senha_hash = senha_hash
        self.saldo = saldo_inicial

    def depositar(self, valor):
        """
        Deposita um valor na conta bancária.

        Parâmetros:
        ----------
        valor : float
            O valor a ser depositado.
        """
        self.saldo += valor

    def sacar(self, valor, taxa=0):
        """
        Saca um valor da conta, aplicando uma taxa, se houver saldo suficiente.

        Parâmetros:
        ----------
        valor : float
            O valor a ser sacado.
        taxa : float, opcional
            A taxa adicional aplicada ao saque. O padrão é 0.

        Retorna:
        --------
        bool
            Retorna True se o saque foi bem-sucedido, False caso contrário.
        """
        valor_total = valor + taxa
        if self.saldo >= valor_total:
            self.saldo -= valor_total
            return True
        return False

    def saldo_atual(self):
        """
        Retorna o saldo atual da conta.

        Retorna:
        --------
        float
            O saldo atual da conta bancária.
        """
        return self.saldo

class Banco:
    """
    Classe para gerenciar operações bancárias e persistência de dados.

    Atributos:
    ----------
    persistencia : Persistencia
        Instância para gerenciar a persistência de contas e transações.
    transacao_bancaria : TransacaoBancaria
        Instância para realizar operações de transferência bancária.
    """
    def __init__(self):
        """
        Inicializa o banco com persistência de dados e transações bancárias.
        """
        self.persistencia = Persistencia()
        self.transacao_bancaria = TransacaoBancaria()

    def transferencia(self, numero_conta_origem, numero_conta_destino, valor):
        """
        Realiza a transferência de um valor entre contas.

        Parâmetros:
        ----------
        numero_conta_origem : str
            O número da conta de origem.
        numero_conta_destino : str
            O número da conta de destino.
        valor : float
            O valor a ser transferido.

        Retorna:
        --------
        bool
            True se a transferência foi bem-sucedida, False caso contrário.
        """
        return self.transacao_bancaria.registrar_transferencia(numero_conta_origem, numero_conta_destino, valor)

    def criar_conta(self, nome_cliente, senha):
        """
        Cria uma nova conta bancária.

        Parâmetros:
        ----------
        nome_cliente : str
            O nome do cliente.
        senha : str
            A senha da conta.

        Retorna:
        --------
        ContaBancaria
            A instância da nova conta bancária criada.
        """
        numero_conta = self.gerar_numero_conta()
        senha_hash = Autenticacao.hash_senha(senha)
        nova_conta = ContaBancaria(numero_conta, nome_cliente, senha_hash)
        self.persistencia.salvar_conta(nova_conta)
        return nova_conta

    def autenticar(self, numero_conta, senha):
        """
        Autentica o usuário verificando a senha hash.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta do cliente.
        senha : str
            A senha em texto plano.

        Retorna:
        --------
        bool
            True se a autenticação foi bem-sucedida, False caso contrário.
        """
        conta_dados = self.persistencia.carregar_conta(numero_conta)
        if conta_dados:
            numero_conta, nome_cliente, senha_hash, saldo = conta_dados
            return Autenticacao.verificar_senha(senha, senha_hash)
        return False

    def gerar_numero_conta(self):
        """
        Gera um número único para uma nova conta bancária.

        Retorna:
        --------
        str
            Um número de conta único.
        """
        import random
        return str(random.randint(100000, 999999))

    def buscar_conta(self, numero_conta):
        """
        Busca uma conta pelo número.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta a ser buscada.

        Retorna:
        --------
        ContaBancaria
            A instância da conta bancária, ou None se não for encontrada.
        """
        dados_conta = self.persistencia.carregar_conta(numero_conta)
        if dados_conta:
            numero_conta, nome_cliente, senha_hash, saldo = dados_conta
            return ContaBancaria(numero_conta, nome_cliente, senha_hash, saldo)
        return None

    def deposito(self, numero_conta, valor):
        """
        Deposita um valor em uma conta bancária.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta onde o depósito será feito.
        valor : float
            O valor a ser depositado.

        Retorna:
        --------
        bool
            True se o depósito foi bem-sucedido, False caso contrário.
        """
        conta = self.buscar_conta(numero_conta)
        if conta:
            conta.depositar(valor)
            self.persistencia.salvar_conta(conta)
            self.persistencia.registrar_transacao(numero_conta, 'deposito', valor)
            return True
        return False

    def saque(self, numero_conta, valor, taxa=0):
        """
        Realiza o saque de um valor de uma conta bancária.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta.
        valor : float
            O valor a ser sacado.
        taxa : float, opcional
            A taxa aplicada ao saque. O padrão é 0.

        Retorna:
        --------
        bool
            True se o saque foi bem-sucedido, False caso contrário.
        """
        conta = self.buscar_conta(numero_conta)
        if conta and conta.sacar(valor, taxa):
            self.persistencia.salvar_conta(conta)
            self.persistencia.registrar_transacao(numero_conta, 'saque', valor)
            return True
        return False

    def extrato(self, numero_conta):
        """
        Gera o extrato de transações de uma conta bancária.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta.

        Retorna:
        --------
        str
            O extrato formatado das transações ou uma mensagem de erro.
        """
        transacoes = self.persistencia.carregar_transacoes(numero_conta)
        conta = self.buscar_conta(numero_conta)
        saldo = float(conta.saldo_atual())

        if not transacoes:
            return "Não foram realizadas movimentações."

        extrato = [f"Saldo atual: R${saldo:.2f}"]
        for transacao in transacoes:
            data = transacao[4]
            tipo = transacao[2]
            valor = transacao[3]

            try:
                valor = float(valor)
            except ValueError:
                return f"Erro ao formatar a transação: valor '{valor}' inválido"

            extrato.append(f"{data} - {tipo.capitalize()}: R${valor:.2f}")
        
        return "\n".join(extrato)
from app.persistencia import Persistencia
from app.autenticacao import Autenticacao
from app.transacoes import TransacaoBancaria

class ContaBancaria:
    def __init__(self, numero_conta, nome_cliente, senha_hash, saldo_inicial=0):
        """Inicializa a conta bancária."""
        self.numero_conta = numero_conta
        self.nome_cliente = nome_cliente
        self.senha_hash = senha_hash
        self.saldo = saldo_inicial

    def depositar(self, valor):
        """Deposita um valor na conta."""
        self.saldo += valor

    def sacar(self, valor, taxa=0):
        """Saca um valor da conta, aplicando taxa se houver saldo suficiente."""
        valor_total = valor + taxa
        if self.saldo >= valor_total:
            self.saldo -= valor_total
            return True
        return False

    def saldo_atual(self):
        """Retorna o saldo atual da conta."""
        return self.saldo

class Banco:
    def __init__(self):
        """Inicializa o banco com persistência de dados."""
        self.persistencia = Persistencia()
        self.transacao_bancaria = TransacaoBancaria()  # Instancia a classe de transações

    def transferencia(self, numero_conta_origem, numero_conta_destino, valor):
        """Delegar a transferência para a lógica de transações bancárias."""
        # Chama o método registrar_transferencia da classe TransacaoBancaria
        return self.transacao_bancaria.registrar_transferencia(numero_conta_origem, numero_conta_destino, valor)

    def criar_conta(self, nome_cliente, senha):
        """Cria uma nova conta bancária com um número de conta único."""
        numero_conta = self.gerar_numero_conta()
        senha_hash = Autenticacao.hash_senha(senha)  # Gera o hash da senha
        nova_conta = ContaBancaria(numero_conta, nome_cliente, senha_hash)
        self.persistencia.salvar_conta(nova_conta)  # Salva a conta no banco de dados
        return nova_conta

    def autenticar(self, numero_conta, senha):
        """Autentica o usuário verificando a senha hash."""
        conta_dados = self.persistencia.carregar_conta(numero_conta)
        if conta_dados:
            numero_conta, nome_cliente, senha_hash, saldo = conta_dados  # Obtém o hash da senha
            # Verifica se a senha fornecida corresponde ao hash armazenado
            return Autenticacao.verificar_senha(senha, senha_hash)  # Passa a senha e o hash
        return False

    def gerar_numero_conta(self):
        """Gera um número de conta único."""
        import random
        return str(random.randint(100000, 999999))

    def buscar_conta(self, numero_conta):
        """Busca uma conta pelo número."""
        dados_conta = self.persistencia.carregar_conta(numero_conta)
        if dados_conta:
            numero_conta, nome_cliente, senha_hash, saldo = dados_conta
            return ContaBancaria(numero_conta, nome_cliente, senha_hash, saldo)
        return None

    def deposito(self, numero_conta, valor):
        """Deposita um valor na conta."""
        conta = self.buscar_conta(numero_conta)
        if conta:
            conta.depositar(valor)
            self.persistencia.salvar_conta(conta)
            self.persistencia.registrar_transacao(numero_conta, 'deposito', valor)
            return True
        return False

    def saque(self, numero_conta, valor, taxa=0):
        """Saca um valor da conta."""
        conta = self.buscar_conta(numero_conta)
        if conta and conta.sacar(valor, taxa):
            self.persistencia.salvar_conta(conta)
            self.persistencia.registrar_transacao(numero_conta, 'saque', valor)
            return True  # Retorna True para indicar que o saque foi bem-sucedido
        return False  # Retorna False se o saque falhar


    # def saque(self, numero_conta, valor, taxa=0):
    #     """Saca um valor da conta."""
    #     conta = self.buscar_conta(numero_conta)
    #     if conta and conta.sacar(valor, taxa):
    #         self.persistencia.salvar_conta(conta)
    #         self.persistencia.registrar_transacao(numero_conta, 'saque', valor)
    #         return True
    #     return False

    # def transferencia(self, numero_conta_origem, numero_conta_destino, valor, taxa=0):
    #     """Transfere um valor entre contas."""
    #     conta_origem = self.buscar_conta(numero_conta_origem)
    #     conta_destino = self.buscar_conta(numero_conta_destino)
    #     if conta_origem and conta_destino and conta_origem.sacar(valor, taxa):
    #         conta_destino.depositar(valor)
    #         self.persistencia.salvar_conta(conta_origem)
    #         self.persistencia.salvar_conta(conta_destino)
    #         self.persistencia.registrar_transacao(numero_conta_origem, 'transferencia_envio', valor)
    #         self.persistencia.registrar_transacao(numero_conta_destino, 'transferencia_recebido', valor)
    #         return True
    #     return False

    def extrato(self, numero_conta):
        """Gera o extrato de transações de uma conta."""
        transacoes = self.persistencia.carregar_transacoes(numero_conta)
        conta = self.buscar_conta(numero_conta)  # Carrega a conta para obter o saldo
        saldo = float(conta.saldo_atual())  # Converte o saldo para float
        
        if not transacoes:
            return "Não foram realizadas movimentações."
        
        # Primeira linha do extrato com o saldo atual
        extrato = [f"Saldo atual: R${saldo:.2f}"]
        
        # Iterar sobre as transações e formatar corretamente
        for transacao in transacoes:
            data = transacao[4]  # Data da transação (posição 4)
            tipo = transacao[2]  # Tipo de transação (posição 2)
            valor = transacao[3]  # Valor da transação (posição 3)

            try:
                valor = float(valor)  # Converte o valor para float
            except ValueError:
                return f"Erro ao formatar a transação: valor '{valor}' inválido"

            # Formatar a transação no extrato
            extrato.append(f"{data} - {tipo.capitalize()}: R${valor:.2f}")
        
        return "\n".join(extrato)
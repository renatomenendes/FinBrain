from app.persistencia import Persistencia

class TransacaoBancaria:
    def __init__(self):
        self.persistencia = Persistencia()

    def calcular_taxa_saque(self, valor):
        """Calcula taxa de 1% para saques"""
        return valor * 0.01  # Taxa de 1%

    def calcular_taxa_transferencia(self, valor):
        """Calcula taxa de 1.5% para transferências"""
        return valor * 0.015  # Taxa de 1.5%

    def verificar_limite_saques_diarios(self, numero_conta):
        """Verifica se o limite de 3 saques/transferências diários foi atingido."""
        transacoes = self.persistencia.carregar_transacoes(numero_conta)
        
        # Obter a data atual no formato YYYY-MM-DD
        from datetime import datetime
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        # Verificar em qual índice está a data (suponho que seja o índice 4)
        # Ajuste para o índice correto da data no seu banco de dados
        transacoes_hoje = [t for t in transacoes if (t[2] == 'saque' or t[2] == 'transferencia_envio') and t[4].startswith(data_atual)]
        
        # Verifica se o limite de 3 transações (saques/transferências) foi atingido
        return len(transacoes_hoje) < 3  # Retorna True se o limite não foi atingido

    def data_hoje(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    def registrar_saque(self, numero_conta, valor):
        """Registra um saque com verificação de limites e saldo."""
        
        # Verificar o limite de R$500,00 por saque
        if valor > 500:
            return "Erro: Valor do saque excede o limite de R$ 500,00 por saque."
        
        # Verificar o limite de 3 saques diários
        if not self.verificar_limite_saques_diarios(numero_conta):
            return "Erro: Limite de 3 saques diários excedido."
        
        conta = self.persistencia.carregar_conta(numero_conta)
        
        # Verificar se há saldo suficiente
        if conta and conta.saldo_atual() >= valor:
            # Calcular a taxa do saque (1% do valor)
            taxa = self.calcular_taxa_saque(valor)
            valor_total = valor + taxa
            
            # Verificar se há saldo suficiente para o valor e a taxa
            if conta.saldo_atual() >= valor_total:
                conta.saldo -= valor_total
                self.persistencia.salvar_conta(conta)
                self.persistencia.registrar_transacao(numero_conta, 'saque', valor)
                return f"Saque de R${valor:.2f} realizado com sucesso, incluindo R${taxa:.2f} de taxa."
            else:
                return "Erro: Saldo insuficiente para cobrir o valor do saque e a taxa."
        
        return "Erro: Saldo insuficiente para realizar o saque."

    def registrar_transferencia(self, numero_conta_origem, numero_conta_destino, valor):
        """Registra uma transferência com verificação de limites e saldo."""

        # Verificar o limite de R$500,00 por transferência
        if valor > 500:
            return "Erro: Valor da transferência excede o limite de R$ 500,00 por operação."

        # Verificar o limite de 3 transferências/saques diários
        if not self.verificar_limite_saques_diarios(numero_conta_origem):
            return "Erro: Limite de 3 saques/transferências diárias excedido."
        conta_origem = self.persistencia.carregar_conta(numero_conta_origem)
        conta_destino = self.persistencia.carregar_conta(numero_conta_destino)

        # Verificar se ambas as contas foram carregadas
        if not conta_origem or not conta_destino:
            return "Erro: Conta de origem ou destino não encontrada."

        if conta_origem and conta_origem.saldo_atual() >= valor:
            # Calcular a taxa de transferência (1.5% do valor)
            taxa = self.calcular_taxa_transferencia(valor)
            valor_total = valor + taxa
            # Verificar se há saldo suficiente para o valor e a taxa
            if conta_origem.saldo_atual() >= valor_total:
                # Deduz o valor e a taxa da conta de origem
                conta_origem.saldo -= valor_total
                self.persistencia.salvar_conta(conta_origem)
                # Adiciona o valor na conta de destino
                conta_destino.saldo += valor
                self.persistencia.salvar_conta(conta_destino)
                # Registra a transação
                self.persistencia.registrar_transacao(numero_conta_origem, 'transferencia_envio', valor)
                self.persistencia.registrar_transacao(numero_conta_destino, 'transferencia_recebido', valor)
                return f"Transferência de R${valor:.2f} realizada com sucesso, incluindo R${taxa:.2f} de taxa."
            else:
                return "Erro: Saldo insuficiente para cobrir o valor da transferência e a taxa."
        return "Erro: Saldo insuficiente para realizar a transferência."
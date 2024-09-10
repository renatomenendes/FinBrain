from app.persistencia import Persistencia

class TransacaoBancaria:
    """
    Classe responsável por gerenciar transações bancárias como saques e transferências,
    além de calcular taxas e verificar limites diários de transações.
    """

    def __init__(self):
        """
        Inicializa a instância da classe, incluindo uma conexão com a camada de persistência.
        """
        self.persistencia = Persistencia()

    def calcular_taxa_saque(self, valor):
        """
        Calcula a taxa aplicada a um saque.

        A taxa é de 1% do valor do saque.

        Parâmetros:
        ----------
        valor : float
            O valor do saque.

        Retorna:
        --------
        float
            O valor da taxa do saque.
        """
        return valor * 0.01  # Taxa de 1%

    def calcular_taxa_transferencia(self, valor):
        """
        Calcula a taxa aplicada a uma transferência.

        A taxa é de 1.5% do valor da transferência.

        Parâmetros:
        ----------
        valor : float
            O valor da transferência.

        Retorna:
        --------
        float
            O valor da taxa da transferência.
        """
        return valor * 0.015  # Taxa de 1.5%

    def verificar_limite_saques_diarios(self, numero_conta):
        """
        Verifica se o limite de 3 saques ou transferências diárias foi atingido.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta a ser verificada.

        Retorna:
        --------
        bool
            Retorna True se o limite de transações diárias não foi excedido, False caso contrário.
        """
        transacoes = self.persistencia.carregar_transacoes(numero_conta)
        
        from datetime import datetime
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        transacoes_hoje = [t for t in transacoes if (t[2] == 'saque' or t[2] == 'transferencia_envio') and t[4].startswith(data_atual)]
        
        return len(transacoes_hoje) < 3  # Limite de 3 saques/transferências por dia

    def data_hoje(self):
        """
        Retorna a data atual no formato 'YYYY-MM-DD'.

        Retorna:
        --------
        str
            A data atual.
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    def registrar_saque(self, numero_conta, valor):
        """
        Realiza o registro de um saque na conta bancária.

        O saque está sujeito a verificação de limites diários (máximo de 3 saques por dia) 
        e o limite de valor por saque (máximo de R$500,00 por operação), além de saldo suficiente.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta de onde o saque será realizado.
        valor : float
            O valor do saque.

        Retorna:
        --------
        str
            Mensagem indicando o sucesso ou erro ao realizar o saque.
        """
        
        if valor > 500:
            return "Erro: Valor do saque excede o limite de R$ 500,00 por saque."
        
        if not self.verificar_limite_saques_diarios(numero_conta):
            return "Erro: Limite de 3 saques diários excedido."
        
        conta = self.persistencia.carregar_conta(numero_conta)
        
        if conta and conta.saldo_atual() >= valor:
            taxa = self.calcular_taxa_saque(valor)
            valor_total = valor + taxa
            
            if conta.saldo_atual() >= valor_total:
                conta.saldo -= valor_total
                self.persistencia.salvar_conta(conta)
                self.persistencia.registrar_transacao(numero_conta, 'saque', valor)
                return f"Saque de R${valor:.2f} realizado com sucesso, incluindo R${taxa:.2f} de taxa."
            else:
                return "Erro: Saldo insuficiente para cobrir o valor do saque e a taxa."
        
        return "Erro: Saldo insuficiente para realizar o saque."

    def registrar_transferencia(self, numero_conta_origem, numero_conta_destino, valor):
        """
        Realiza o registro de uma transferência entre contas bancárias.

        A transferência está sujeita a verificação de limites diários (máximo de 3 saques/transferências por dia)
        e o limite de valor por operação (máximo de R$500,00), além de saldo suficiente na conta de origem.

        Parâmetros:
        ----------
        numero_conta_origem : str
            O número da conta de origem.
        numero_conta_destino : str
            O número da conta de destino.
        valor : float
            O valor da transferência.

        Retorna:
        --------
        str
            Mensagem indicando o sucesso ou erro ao realizar a transferência.
        """
        
        if valor > 500:
            return "Erro: Valor da transferência excede o limite de R$ 500,00 por operação."

        if not self.verificar_limite_saques_diarios(numero_conta_origem):
            return "Erro: Limite de 3 saques/transferências diárias excedido."
        
        conta_origem = self.persistencia.carregar_conta(numero_conta_origem)
        conta_destino = self.persistencia.carregar_conta(numero_conta_destino)

        if not conta_origem or not conta_destino:
            return "Erro: Conta de origem ou destino não encontrada."

        if conta_origem and conta_origem.saldo_atual() >= valor:
            taxa = self.calcular_taxa_transferencia(valor)
            valor_total = valor + taxa
            
            if conta_origem.saldo_atual() >= valor_total:
                conta_origem.saldo -= valor_total
                self.persistencia.salvar_conta(conta_origem)
                
                conta_destino.saldo += valor
                self.persistencia.salvar_conta(conta_destino)
                
                self.persistencia.registrar_transacao(numero_conta_origem, 'transferencia_envio', valor)
                self.persistencia.registrar_transacao(numero_conta_destino, 'transferencia_recebido', valor)
                
                return f"Transferência de R${valor:.2f} realizada com sucesso, incluindo R${taxa:.2f} de taxa."
            else:
                return "Erro: Saldo insuficiente para cobrir o valor da transferência e a taxa."
        
        return "Erro: Saldo insuficiente para realizar a transferência."
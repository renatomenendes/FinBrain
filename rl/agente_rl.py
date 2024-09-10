import numpy as np

class AgenteRL:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_rate = 0.95
        self.acoes = ["depositar", "sacar", "nada"]

    def escolher_acao(self, estado):
        """Escolhe uma ação baseada na política ε-greedy"""
        # Exploração com 10% de chance
        if np.random.uniform(0, 1) < 0.1:
            return np.random.choice(self.acoes)
        # Exploração do maior valor da Q-table
        else:
            if estado not in self.q_table:
                # Inicializa o estado com zeros se ele não existir na Q-table
                self.q_table[estado] = [0, 0, 0]
            return self.acoes[np.argmax(self.q_table[estado])]

    def atualizar_q_table(self, estado_antigo, acao, recompensa, novo_estado):
        """Atualiza a Q-table usando a equação de aprendizado por reforço"""
        if estado_antigo not in self.q_table:
            # Inicializa o estado antigo se ele não existir
            self.q_table[estado_antigo] = [0, 0, 0]
        
        if novo_estado not in self.q_table:
            # Inicializa o novo estado se ele não existir
            self.q_table[novo_estado] = [0, 0, 0]

        # Mapeia a ação para o índice
        indice_acao = self.acoes.index(acao)
        
        previsao = self.q_table[estado_antigo][indice_acao]
        alvo = recompensa + self.discount_rate * np.max(self.q_table[novo_estado])
        
        # Atualiza a Q-table com a nova previsão
        self.q_table[estado_antigo][indice_acao] = previsao + self.learning_rate * (alvo - previsao)

    def gerar_relatorio(self, historico):
        """Gera um relatório simples baseado no histórico de transações"""
        saldo_total = sum([t['valor'] for t in historico if t['valor'] > 0])
        gastos_total = sum([-t['valor'] for t in historico if t['valor'] < 0])
        transacoes = len(historico)
        media_gastos = gastos_total / transacoes if transacoes > 0 else 0
        media_depositos = saldo_total / transacoes if transacoes > 0 else 0

        relatorio = (
            f"Depósitos totais: R${saldo_total:.2f}\n"
            f"Gastos totais: R${gastos_total:.2f}\n"
            f"Número total de transações: {transacoes}\n"
            f"Média de depósitos: R${media_depositos:.2f}\n"
            f"Média de gastos: R${media_gastos:.2f}\n"
        )
        return relatorio

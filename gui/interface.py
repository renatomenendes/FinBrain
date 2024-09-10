import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from app.banco import Banco

class InterfaceBancaria:
    """
    Interface gráfica do sistema bancário FinBrain, simulando operações de um banco, como:
    - Login
    - Criação de contas
    - Depósitos
    - Saques
    - Transferências
    - Visualização de extrato
    """
    
    def __init__(self, root):
        """
        Inicializa a interface gráfica da aplicação e exibe a tela inicial.

        Parâmetros:
        ----------
        root : Tk
            A janela raiz do tkinter.
        """
        self.root = root
        self.root.title("FinBrain - Sistema Bancário")

        # Definir tamanho da janela para simular um smartphone
        self.root.geometry("400x600")  # Tamanho típico de um smartphone
        self.root.resizable(False, False)  # Impedir redimensionamento

        self.banco = Banco()  # Inicializa o banco de dados
        
        # Exibe a tela inicial
        self.tela_inicial()

    def normalizar_valor(self, valor_str):
        """
        Normaliza o valor inserido pelo usuário, removendo símbolos e convertendo para float.

        Parâmetros:
        ----------
        valor_str : str
            O valor inserido pelo usuário.

        Retorna:
        --------
        float or None
            O valor convertido em float ou None se a conversão falhar.
        """
        valor_str = valor_str.strip().replace("R$", "").replace("r$", "").replace(",", ".")
        
        try:
            valor_float = float(valor_str)
            return valor_float
        except ValueError:
            return None
    
    def tela_inicial(self):
        """
        Cria a tela inicial com opções de Login, Criar Conta e Sair.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Bem-vindo ao FinBrain", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Login", width=20, height=2, command=self.tela_login).pack(pady=10)
        tk.Button(self.root, text="Criar Conta", width=20, height=2, command=self.tela_criar_conta).pack(pady=10)
        tk.Button(self.root, text="Sair", width=20, height=2, command=self.sair_aplicacao).pack(pady=10)

    def sair_aplicacao(self):
        """
        Fecha a aplicação.
        """
        self.root.quit()

    def tela_login(self):
        """
        Cria a interface de login, solicitando número da conta e senha.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Número da Conta").pack(pady=5)
        self.entrada_numero_conta = tk.Entry(self.root, width=30)
        self.entrada_numero_conta.pack(pady=5)

        tk.Label(self.root, text="Senha").pack(pady=5)
        self.entrada_senha = tk.Entry(self.root, show="*", width=30)
        self.entrada_senha.pack(pady=5)

        tk.Button(self.root, text="Entrar", width=20, height=2, command=self.fazer_login).pack(pady=10)
        tk.Button(self.root, text="Voltar", width=20, height=2, command=self.tela_inicial).pack(pady=10)

    def tela_criar_conta(self):
        """
        Cria a interface para permitir a criação de uma nova conta bancária.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Criar Nova Conta", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Nome").pack(pady=5)
        self.entrada_nome = tk.Entry(self.root, width=30)
        self.entrada_nome.pack(pady=5)

        tk.Label(self.root, text="Senha").pack(pady=5)
        self.entrada_senha_criacao = tk.Entry(self.root, show="*", width=30)
        self.entrada_senha_criacao.pack(pady=5)

        tk.Button(self.root, text="Criar", width=20, height=2, command=self.criar_conta).pack(pady=10)
        tk.Button(self.root, text="Voltar", width=20, height=2, command=self.tela_inicial).pack(pady=10)

    def criar_conta(self):
        """
        Cria uma nova conta no sistema e exibe o número da conta.
        """
        nome = self.entrada_nome.get()
        senha = self.entrada_senha_criacao.get()
        nova_conta = self.banco.criar_conta(nome, senha)
        self.mostrar_numero_conta(nova_conta.numero_conta)

    def mostrar_numero_conta(self, numero_conta):
        """
        Exibe o número da conta recém-criada e permite que o usuário copie para o clipboard.

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta recém-criada.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Conta Criada com Sucesso!", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Número da Conta:").pack(pady=5)

        campo_numero_conta = tk.Entry(self.root, width=30)
        campo_numero_conta.insert(0, numero_conta)
        campo_numero_conta.config(state="readonly")
        campo_numero_conta.pack(pady=5)

        tk.Button(self.root, text="Copiar", command=lambda: self.copiar_para_clipboard(numero_conta)).pack(pady=10)
        tk.Button(self.root, text="Fazer Login", width=20, height=2, command=self.tela_login).pack(pady=10)

    def copiar_para_clipboard(self, texto):
        """
        Copia o texto fornecido para o clipboard.

        Parâmetros:
        ----------
        texto : str
            O texto a ser copiado para o clipboard.
        """
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        messagebox.showinfo("Copiado", "Número da conta copiado para o clipboard!")

    def tela_operacoes(self, numero_conta):
        """
        Cria a interface para exibir as operações disponíveis (depósito, saque, transferência, extrato).

        Parâmetros:
        ----------
        numero_conta : str
            O número da conta do usuário logado.
        """
        self.limpar_tela()

        conta = self.banco.buscar_conta(numero_conta)
        nome_cliente = conta.nome_cliente if conta else "Cliente Desconhecido"

        tk.Label(self.root, text=f"{nome_cliente} - Conta {numero_conta}", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Depósito", width=20, height=2, command=self.tela_deposito).pack(pady=10)
        tk.Button(self.root, text="Saque", width=20, height=2, command=self.tela_saque).pack(pady=10)
        tk.Button(self.root, text="Transferência", width=20, height=2, command=self.tela_transferencia).pack(pady=10)
        tk.Button(self.root, text="Extrato", width=20, height=2, command=self.mostrar_extrato).pack(pady=10)
        tk.Button(self.root, text="Sair", width=20, height=2, command=self.tela_inicial).pack(pady=10)

    def tela_deposito(self):
        """
        Cria a interface para permitir que o usuário faça um depósito.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Depósito", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Valor").pack(pady=5)
        self.entrada_valor_deposito = tk.Entry(self.root, width=30)
        self.entrada_valor_deposito.pack(pady=5)

        tk.Button(self.root, text="Confirmar", width=20, height=2, command=self.fazer_deposito).pack(pady=10)
        tk.Button(self.root, text="Voltar", width=20, height=2, command=lambda: self.tela_operacoes(self.numero_conta)).pack(pady=10)

    def tela_saque(self):
        """
        Cria a interface para permitir que o usuário faça um saque.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Saque", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Valor").pack(pady=5)
        self.entrada_valor_saque = tk.Entry(self.root, width=30)
        self.entrada_valor_saque.pack(pady=5)

        tk.Button(self.root, text="Confirmar", width=20, height=2, command=self.fazer_saque).pack(pady=10)
        tk.Button(self.root, text="Voltar", width=20, height=2, command=lambda: self.tela_operacoes(self.numero_conta)).pack(pady=10)

    def tela_transferencia(self):
        """
        Cria a interface para permitir que o usuário faça uma transferência.
        """
        self.limpar_tela()

        tk.Label(self.root, text="Transferência", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Conta destino").pack(pady=5)
        self.entrada_conta_destino = tk.Entry(self.root, width=30)
        self.entrada_conta_destino.pack(pady=5)

        tk.Label(self.root, text="Valor").pack(pady=5)
        self.entrada_valor_transferencia = tk.Entry(self.root, width=30)
        self.entrada_valor_transferencia.pack(pady=5)

        tk.Button(self.root, text="Confirmar", width=20, height=2, command=self.fazer_transferencia).pack(pady=10)
        tk.Button(self.root, text="Voltar", width=20, height=2, command=lambda: self.tela_operacoes(self.numero_conta)).pack(pady=10)

    def mostrar_extrato(self):
        """
        Exibe o extrato da conta em uma janela de mensagem.
        """
        extrato = self.banco.extrato(self.numero_conta)
        messagebox.showinfo("Extrato", extrato)

    def fazer_login(self):
        """
        Realiza o login do usuário, autenticando com o número da conta e a senha.
        """
        numero_conta = self.entrada_numero_conta.get()
        senha = self.entrada_senha.get()
        
        if self.banco.autenticar(numero_conta, senha):
            self.numero_conta = numero_conta
            self.tela_operacoes(numero_conta)
        else:
            messagebox.showerror("Erro", "Número da conta ou senha inválidos")

    def fazer_deposito(self):
        """
        Realiza o depósito de um valor na conta do usuário logado.
        """
        valor_str = self.entrada_valor_deposito.get()
        valor = self.normalizar_valor(valor_str)
        
        if valor is None:
            messagebox.showerror("Erro", "Por favor, insira um valor válido.")
            return

        if self.banco.deposito(self.numero_conta, valor):
            messagebox.showinfo("Sucesso", f"Depósito de R${valor:.2f} realizado com sucesso.")
            self.tela_operacoes(self.numero_conta)
        else:
            messagebox.showerror("Erro", "Falha no depósito.")

    def fazer_saque(self):
        """
        Realiza o saque de um valor da conta do usuário logado.
        """
        valor_str = self.entrada_valor_saque.get()
        valor = self.normalizar_valor(valor_str)

        if valor is None:
            messagebox.showerror("Erro", "Por favor, insira um valor válido.")
            return

        sucesso = self.banco.saque(self.numero_conta, valor)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Saque de R${valor:.2f} realizado com sucesso.")
            self.tela_operacoes(self.numero_conta)
        else:
            messagebox.showerror("Erro", "Saldo insuficiente ou erro ao realizar o saque.")

    def fazer_transferencia(self):
        """
        Realiza a transferência de um valor entre contas bancárias.
        """
        conta_destino = self.entrada_conta_destino.get()
        valor_str = self.entrada_valor_transferencia.get()
        valor = self.normalizar_valor(valor_str)

        if valor is None:
            messagebox.showerror("Erro", "Por favor, insira um valor válido.")
            return

        mensagem = self.banco.transferencia(self.numero_conta, conta_destino, valor)

        if "Erro" in mensagem:
            messagebox.showerror("Erro", mensagem)
        else:
            messagebox.showinfo("Sucesso", mensagem)
            self.tela_operacoes(self.numero_conta)

    def limpar_tela(self):
        """
        Limpa todos os elementos visuais da tela atual.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceBancaria(root)
    root.mainloop()
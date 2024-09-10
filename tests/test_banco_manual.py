import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.banco import Banco

# Criar instância do banco
banco = Banco()

# Teste 1: Criar uma nova conta
print("===== Teste 1: Criar Conta =====")
conta = banco.criar_conta("Renato", "senha_hash")
print(f"Conta criada com sucesso! Número da conta: {conta.numero_conta}, Nome: {conta.nome_cliente}, Saldo: {conta.saldo_atual()}")

# Teste 2: Depositar em uma conta
print("===== Teste 2: Depósito =====")
banco.deposito(conta.numero_conta, 1000)
print(f"Saldo após depósito de R$1000: {banco.buscar_conta(conta.numero_conta).saldo_atual()}")

# Teste 3: Sacar da conta
print("===== Teste 3: Saque =====")
sucesso_saque = banco.saque(conta.numero_conta, 500)
if sucesso_saque:
    print(f"Saque de R$500 realizado com sucesso. Saldo atual: {banco.buscar_conta(conta.numero_conta).saldo_atual()}")
else:
    print("Falha no saque: Saldo insuficiente")

# Teste 4: Tentar sacar valor maior que o saldo
print("===== Teste 4: Saque com saldo insuficiente =====")
sucesso_saque = banco.saque(conta.numero_conta, 1000)
if sucesso_saque:
    print("Saque realizado com sucesso")
else:
    print(f"Falha no saque: Saldo insuficiente. Saldo atual: {banco.buscar_conta(conta.numero_conta).saldo_atual()}")

# Teste 5: Transferência entre contas
print("===== Teste 5: Transferência entre contas =====")
conta_destino = banco.criar_conta("João", "senha_hash_joao")
banco.deposito(conta_destino.numero_conta, 500)  # Depósito inicial na conta de destino
sucesso_transferencia = banco.transferencia(conta.numero_conta, conta_destino.numero_conta, 200)
if sucesso_transferencia:
    print(f"Transferência de R$200 realizada com sucesso. Saldo da conta origem: {banco.buscar_conta(conta.numero_conta).saldo_atual()}, Saldo da conta destino: {banco.buscar_conta(conta_destino.numero_conta).saldo_atual()}")
else:
    print("Falha na transferência")

# Teste 6: Exibir extrato da conta
print("===== Teste 6: Extrato =====")
extrato = banco.extrato(conta.numero_conta)
print(f"Extrato da conta {conta.numero_conta}:\n{extrato}")
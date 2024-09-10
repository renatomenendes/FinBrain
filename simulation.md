
# Simulação de Execução do Projeto FinBrain

Este documento descreve uma simulação da execução do sistema bancário inteligente **FinBrain**. Ele abrange as principais funcionalidades do sistema, desde a criação de conta até operações como depósito, saque, transferência e visualização de extrato.

---

## 1. Iniciando o Projeto

Após configurar o ambiente e instalar as dependências, inicie o projeto com o seguinte comando:

```bash
python main.py
```

A interface gráfica do sistema será aberta, construída com **Tkinter**.

---

## 2. Tela Inicial

Na **tela inicial**, o usuário terá as seguintes opções:

- **Login**
- **Criar Conta**

---

## 3. Criando uma Conta

### Passos:

1. O usuário clica em **Criar Conta**.
2. Aparece um formulário onde o usuário deve preencher o **nome do cliente** e uma **senha**.
3. Ao submeter o formulário, o sistema gera um **número de conta** automaticamente e o exibe para o usuário.
4. A senha é **hasheada** e armazenada junto com os dados do cliente no banco de dados SQLite.

Simulação do log:

```
Conta criada com sucesso!
Número da conta: 123456
```

Agora o usuário pode usar essa conta para realizar login.

---

## 4. Fazendo Login

### Passos:

1. O usuário clica em **Login**.
2. Ele insere o **número da conta** e a **senha**.
3. O sistema verifica a senha hasheada e, se a autenticação for bem-sucedida, o sistema exibe uma tela com as opções de **Depósito**, **Saque**, **Transferência** e **Ver Extrato**.

Simulação do log:

```
Login realizado com sucesso!
Bem-vindo(a), Cliente Teste
```

---

## 5. Realizando um Depósito

### Passos:

1. O usuário clica em **Depósito**.
2. O sistema exibe um campo para o usuário inserir o **valor do depósito**.
3. Após confirmar, o sistema registra a transação de depósito no banco de dados e atualiza o saldo da conta.

Simulação do log:

```
Depósito de R$500.00 realizado com sucesso na conta 123456.
Saldo atual: R$500.00
```

---

## 6. Realizando um Saque

### Passos:

1. O usuário clica em **Saque**.
2. O sistema exibe um campo para inserir o **valor a ser sacado**.
3. O sistema verifica se há saldo suficiente. Se o saldo for suficiente, o saque é realizado e registrado no banco de dados.

Simulação do log:

```
Saque de R$200.00 realizado com sucesso na conta 123456.
Saldo atual: R$300.00
```

Se o saldo for insuficiente:

```
Erro: Saldo insuficiente para realizar o saque.
```

---

## 7. Realizando uma Transferência

### Passos:

1. O usuário clica em **Transferência**.
2. Ele insere o **número da conta destino** e o **valor** da transferência.
3. O sistema verifica o saldo. Se houver saldo suficiente, a transferência é registrada como uma transação de débito na conta origem e crédito na conta destino.

Simulação do log:

```
Transferência de R$100.00 para a conta 654321 realizada com sucesso!
Saldo atual na conta 123456: R$200.00
```

---

## 8. Visualizando o Extrato

### Passos:

1. O usuário clica em **Ver Extrato**.
2. O sistema exibe um histórico das transações feitas, incluindo a data, tipo de transação (depósito, saque, transferência), e o valor de cada transação.

Simulação do extrato exibido na interface:

```
Saldo atual: R$200.00

2024-09-05 10:00:00 - Depósito: R$500.00
2024-09-05 11:00:00 - Saque: R$-200.00
2024-09-05 12:00:00 - Transferência - Envio: R$-100.00
```

---

## 9. Logout

Depois de realizar as transações, o usuário pode clicar em **Logout**, e o sistema retornará à tela de login.

Simulação do log:

```
Logout realizado com sucesso!
```

---

## 10. Testes Automatizados

Você pode rodar os testes unitários para validar as funcionalidades programáticas:

```bash
python -m unittest discover tests
```

Agora o sistema está pronto para uso e testes completos!

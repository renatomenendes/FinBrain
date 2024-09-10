# FinBrain - Sistema Bancário Inteligente com um agente de Reinforcement learning 

© 2024 Renato Menendes. Todos os direitos reservados sob a Licença MIT.

## Descrição

FinBrain é um sistema bancário inteligente que utiliza **Tkinter** para interface gráfica e um **Agente de Aprendizado por Reforço (RL)** para gerar relatórios inteligentes sobre o comportamento financeiro dos usuários.

## Funcionalidades

- **Criação de conta**: Com nome, número de conta e senha com hash para segurança.
- **Login seguro**: Autenticação por senha utilizando hashing com `sha256`.
- **Operações bancárias**:
  - Depósito
  - Saque com aplicação de taxa dinâmica
  - Transferência entre contas com taxa
  - Visualização de extrato detalhado
- **Agente de Aprendizado por Reforço**:
  - Geração de relatórios inteligentes baseados no histórico de transações.
- **Persistência de dados**: Contas e transações são armazenadas em um banco de dados SQLite.
- **Interface gráfica aprimorada**: Utilizando `Tkinter` e `ttk` para widgets estilizados.

### Environment

Essa aplicação foi desenvolvida com **Python 3.9**.

#### Criando o ambiente virtual

Crie um novo ambiente para rodar o projeto:

```bash
conda create -n FinBrain -y python=3.10
```

Para ativar o ambiente, use:
```bash
conda activate FinBrain
```

### Requirements
Para instalar as dependências, execute o seguinte comando dentro do ambiente virtual:

```bash
python -m pip install -r ".\requirements\requirements.txt"
```

## Estrutura do Projeto
```
FinBrain/
│
├── app/                      # Lógica das operações bancárias
│   ├── banco.py              # Operações bancárias (saques, depósitos, transferências)
│   ├── autenticacao.py       # Autenticação e segurança (hashing de senhas)
│   ├── transacoes.py         # Cálculo de taxas de saque e transferência
│   └── persistencia.py       # Persistência com SQLite
│
├── config/                   # Diretório de configuração
│   └── config.yaml           # Arquivo de configuração YAML
│
├── data/                     # Diretório de dados locais (para testes e desenvolvimento)
│   └── sample_data.db        # Banco de dados de amostra
│
├── gui/                      # Interface gráfica com Tkinter
│   └── interface.py          # Interface gráfica
│
├── rl/                       # Agente de Reforço para relatórios inteligentes
│   └── agente_rl.py          # Implementação do agente RL
│
├── tests/                    # Testes automatizados
│   ├── test_banco.py         # Testes unitários de funcionalidades bancárias
│   └── test_gui.py           # Testes automatizados para interface gráfica
│
├── requirements/             # Diretório de dependências
│   └── requirements.txt      # Lista de dependências do projeto
│
├── README.md                 # Documentação do projeto
├── FinBrain.py                   # Arquivo principal para rodar a aplicação
├── LICENSE                   # Licença MIT
└── .gitignore                # Arquivo para ignorar arquivos desnecessários no versionamento

```
## Rodando Tasks

### Rodando a aplicação
Para iniciar a aplicação, execute:

```bash
python main.py
````

## Exemplo de Uso
Após ativar o ambiente e rodar a aplicação (`python main.py`), siga os passos abaixo para realizar um depósito:

1. Abra o aplicativo.
2. Faça login com uma conta existente ou crie uma nova conta.
3. Selecione "Depósito" no menu principal.
4. Insira o valor e confirme.

### Rodando teste
```bash
python -m unittest discover tests
```

### Rodando Simulação
Para ver uma simulação detalhada da execução do projeto, confira [simulation](./simulation.md).


## Atualizando dependências
- Adicionar a nova dependência para o arquivo `.in` correto na pasta `requirements`
- Rodar:

```
make compile-deps-clean
make compile-deps
make install-deps
```

## Construindo a documentação
- Tenha certeza que as dependências estão atualizadas (se você não tem certeza, rode: `make install-deps`)

- Então, rode:

```
cd docs
sphinx-apidoc --force -o . ..
make clean html
```
- Os resultados estaram disponíveis em `docs/_build`, você pode abrir o arquivo `index.html` no browser e ver o resultado

## Licença

Este projeto é licenciado sob a Licença MIT. Isso significa que você é livre para usar, modificar e distribuir este software, desde que mantenha o aviso de copyright original e a permissão da licença. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

© 2024 Renato Menendes. Todos os direitos reservados sob a Licença MIT.

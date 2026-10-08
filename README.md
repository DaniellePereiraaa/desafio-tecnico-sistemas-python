# Desafio Técnico — Desenvolvimento de Sistemas em Python

Implementação de três exercícios de lógica de negócio utilizando Python, com foco em organização, legibilidade, validação de dados e testes automatizados.

## Funcionalidades

### 1. Cálculo de comissões

Processa os registros presentes em `data/vendas.json` e calcula o total de comissão de cada vendedor.

Regras aplicadas individualmente a cada venda:

| Valor da venda | Comissão |
|---|---|
| Inferior a R$ 100,00 | 0% |
| De R$ 100,00 a R$ 499,99 | 1% |
| A partir de R$ 500,00 | 5% |

Os valores são calculados com `Decimal`, arredondados individualmente para duas casas decimais e posteriormente agrupados por vendedor.

### 2. Movimentação de estoque

Permite registrar entradas e saídas dos produtos fornecidos em `data/estoque.json`.

Funcionalidades implementadas:

- Identificação dos produtos pelo código.
- Validação de quantidades e disponibilidade de estoque.
- Identificador UUID para cada movimentação.
- Registro da descrição, quantidade e saldos anterior e posterior.
- Persistência local do estado e histórico em JSON.
- Consulta do histórico de movimentações.

O estoque original é preservado. As alterações ficam registradas localmente em `data/estado_estoque.json`, criado automaticamente durante a primeira movimentação.

### 3. Cálculo de juros por atraso

Calcula encargos de 2,5% por dia a partir do valor original e da data de vencimento.

São apresentados dois resultados:

- **Juros simples:** cálculo principal adotado para atender ao enunciado.
- **Juros compostos:** simulação adicional com capitalização diária.

Os dias de atraso são calculados usando a data atual do sistema. Não há acréscimos em vencimentos futuros ou na própria data de vencimento.

Para valores monetários, utiliza-se `Decimal` com arredondamento `ROUND_HALF_UP` para duas casas decimais.

## Tecnologias

- Python 3.12+
- Biblioteca padrão do Python (`json`, `datetime`, `decimal`, `pathlib`, `uuid`, entre outras)
- pytest para testes automatizados
- Git para versionamento

## Instalação

Clone o repositório:

```bash
git clone https://github.com/DaniellePereiraaa/desafio-tecnico-sistemas-python.git
cd desafio-tecnico-sistemas-python
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

## Execução

Na raiz do projeto, execute:

```bash
python main.py
```

Selecione a funcionalidade desejada:

```text
=== DESAFIO TÉCNICO ===
1 - Calcular comissões
2 - Movimentar estoque
3 - Calcular juros por atraso
4 - Consultar histórico de estoque
0 - Sair
```

## Testes automatizados

Para executar todos os testes:

```bash
python -m pytest -v
```

Para executar apenas um grupo:

```bash
python -m pytest tests/test_comissoes.py -v
python -m pytest tests/test_estoque.py -v
python -m pytest tests/test_armazenamento.py -v
python -m pytest tests/test_juros.py -v
```

A suíte cobre regras de cálculo, valores-limite, entradas inválidas, operações de estoque e persistência local.

## Estrutura do projeto

```text
desafio-tecnico-sistemas-python/
├── data/
│   ├── vendas.json
│   └── estoque.json
├── src/
│   ├── __init__.py
│   ├── comissoes.py
│   ├── estoque.py
│   ├── armazenamento.py
│   └── juros.py
├── tests/
│   ├── test_comissoes.py
│   ├── test_estoque.py
│   ├── test_armazenamento.py
│   └── test_juros.py
├── main.py
├── requirements-dev.txt
├── .gitignore
└── README.md
```

## Decisões técnicas

**Separação de responsabilidades:** as regras de negócio estão isoladas dos comandos de terminal e das operações de leitura e gravação.

**Precisão financeira:** os cálculos monetários utilizam `Decimal` para evitar imprecisões de ponto flutuante.

**Persistência:** o estoque é armazenado em JSON, sem necessidade de banco de dados externo. A gravação utiliza arquivo temporário e substituição do estado anterior para reduzir o risco de escrita parcial.

**Rastreabilidade:** as movimentações recebem UUIDs e são mantidas em histórico.

**Testabilidade:** as funções de cálculo podem ser testadas independentemente da interface de terminal. O cálculo de juros aceita uma data de referência opcional, permitindo testes determinísticos.

**Escopo:** o sistema foi desenvolvido para execução local e sequencial. Não implementa controle de concorrência, autenticação nem acesso multiusuário.

## Premissas

- As comissões são calculadas individualmente por venda.
- O arredondamento monetário é feito com duas casas decimais.
- A taxa de atraso é de 2,5% ao dia.
- Juros simples são utilizados como interpretação principal; juros compostos são apresentados como comparação adicional.
- As movimentações de estoque são locais e os arquivos de entrada seguem o formato disponibilizado no desafio.

## Autoria

Desenvolvido por Danielle Cristina Pereira como solução de desafio técnico para a posição de Desenvolvedora de Sistemas Júnior.
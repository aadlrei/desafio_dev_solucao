# Desafio Dev — Solução

Solução simples em Python para os três itens do desafio técnico. O objetivo do repositório é deixar a lógica fácil de ler, executar e revisar, sem frameworks ou dependências externas.

## O que foi implementado

### 1. Comissão de vendedores

O programa lê `data/vendas.json`, calcula a comissão de cada venda e soma o resultado por vendedor.

Regras aplicadas:

- venda abaixo de R$ 100,00: 0%;
- venda de R$ 100,00 até R$ 499,99: 1%;
- venda a partir de R$ 500,00: 5%.

Resultado para os dados fornecidos:

| Vendedor | Total vendido | Comissão |
|---|---:|---:|
| João Silva | R$ 10.754,70 | R$ 495,68 |
| Maria Souza | R$ 9.874,30 | R$ 465,95 |
| Carlos Oliveira | R$ 7.928,35 | R$ 379,37 |
| Ana Lima | R$ 8.763,95 | R$ 404,98 |

### 2. Movimentação de estoque

O programa carrega os produtos de `data/estoque.json` e permite registrar entradas e saídas.

Cada movimentação possui:

- identificador único gerado automaticamente por UUID;
- produto movimentado;
- tipo `ENTRADA` ou `SAIDA`;
- descrição informada pelo usuário;
- quantidade;
- estoque anterior;
- estoque final;
- data e hora.

Também são feitas validações simples para produto inexistente, quantidade inválida, identificador repetido e saída maior que o estoque disponível.

O desafio não exige persistência das movimentações. Por isso, nesta solução o estoque e o histórico são mantidos durante a execução do programa, sem alterar o JSON original.

### 3. Juros por atraso

O programa recebe um valor e uma data de vencimento e calcula os juros até a data atual.

Foi adotada a interpretação de **multa diária simples de 2,5% sobre o valor original**:

`juros = valor × 0,025 × dias_em_atraso`

Se a data ainda não venceu, os juros são zero.

A data pode ser informada como `AAAA-MM-DD` ou `DD/MM/AAAA`.

## Estrutura

```text
desafio_dev_solucao/
├── data/
│   ├── estoque.json
│   └── vendas.json
├── docs/
│   └── desafio_original.docx
├── src/
│   ├── __init__.py
│   ├── desafio1_comissoes.py
│   ├── desafio2_estoque.py
│   └── desafio3_juros.py
├── tests/
│   └── test_solucoes.py
├── .gitignore
├── main.py
└── README.md
```

## Requisitos

- Python 3.10 ou superior.
- Nenhuma biblioteca externa.

## Como executar

Na raiz do repositório:

```bash
python main.py
```

O menu permite acessar os três itens do desafio.

Também é possível executar cada solução separadamente:

```bash
python -m src.desafio1_comissoes
python -m src.desafio2_estoque
python -m src.desafio3_juros
```

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes validam os resultados de comissão, movimentações de entrada/saída, proteção contra estoque negativo, identificadores repetidos e cálculo dos juros.

## Decisões de implementação

A solução usa apenas a biblioteca padrão do Python e `Decimal` para cálculos monetários. Isso evita dependências desnecessárias e reduz problemas de arredondamento com valores financeiros.

O código foi dividido em três módulos para manter cada item do desafio isolado, mas todos podem ser acessados pelo mesmo `main.py`.

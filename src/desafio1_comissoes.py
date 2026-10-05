from __future__ import annotations

import json
from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CENTAVOS = Decimal("0.01")


def percentual_comissao(valor: Decimal) -> Decimal:
    """Retorna o percentual de comissão aplicável a uma venda."""
    if valor < Decimal("100.00"):
        return Decimal("0")
    if valor < Decimal("500.00"):
        return Decimal("0.01")
    return Decimal("0.05")


def calcular_comissao_venda(valor: Decimal) -> Decimal:
    return valor * percentual_comissao(valor)


def carregar_vendas(caminho: str | Path) -> list[dict]:
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo, parse_float=Decimal, parse_int=Decimal)
    return dados["vendas"]


def calcular_comissoes(vendas: list[dict]) -> OrderedDict[str, dict[str, Decimal | int]]:
    """Agrupa vendas por vendedor e calcula a comissão total de cada um."""
    resumo: OrderedDict[str, dict[str, Decimal | int]] = OrderedDict()

    for venda in vendas:
        vendedor = venda["vendedor"]
        valor = Decimal(venda["valor"])

        if vendedor not in resumo:
            resumo[vendedor] = {
                "quantidade_vendas": 0,
                "total_vendido": Decimal("0"),
                "comissao": Decimal("0"),
            }

        resumo[vendedor]["quantidade_vendas"] += 1
        resumo[vendedor]["total_vendido"] += valor
        resumo[vendedor]["comissao"] += calcular_comissao_venda(valor)

    for dados in resumo.values():
        dados["total_vendido"] = dados["total_vendido"].quantize(CENTAVOS, rounding=ROUND_HALF_UP)
        dados["comissao"] = dados["comissao"].quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    return resumo


def formatar_brl(valor: Decimal) -> str:
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def exibir_resumo(caminho_json: str | Path) -> None:
    vendas = carregar_vendas(caminho_json)
    resumo = calcular_comissoes(vendas)

    print("\nCOMISSÕES POR VENDEDOR")
    print("-" * 72)
    print(f"{'Vendedor':<22} {'Vendas':>8} {'Total vendido':>18} {'Comissão':>18}")
    print("-" * 72)
    for vendedor, dados in resumo.items():
        print(
            f"{vendedor:<22} "
            f"{dados['quantidade_vendas']:>8} "
            f"{formatar_brl(dados['total_vendido']):>18} "
            f"{formatar_brl(dados['comissao']):>18}"
        )


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    exibir_resumo(raiz / "data" / "vendas.json")

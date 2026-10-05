from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class Movimentacao:
    identificador: str
    codigo_produto: int
    produto: str
    tipo: str
    descricao: str
    quantidade: int
    estoque_anterior: int
    estoque_final: int
    data_hora: str


class GerenciadorEstoque:
    def __init__(self, caminho_json: str | Path):
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.produtos = {
            int(item["codigoProduto"]): {
                "descricao": item["descricaoProduto"],
                "estoque": int(item["estoque"]),
            }
            for item in dados["estoque"]
        }
        self.movimentacoes: list[Movimentacao] = []

    def listar_produtos(self) -> list[dict]:
        return [
            {"codigo": codigo, "descricao": item["descricao"], "estoque": item["estoque"]}
            for codigo, item in self.produtos.items()
        ]

    def movimentar(
        self,
        codigo_produto: int,
        tipo: str,
        quantidade: int,
        descricao: str,
        identificador: str | None = None,
    ) -> Movimentacao:
        codigo_produto = int(codigo_produto)
        tipo = tipo.strip().upper()
        descricao = descricao.strip()

        if codigo_produto not in self.produtos:
            raise ValueError("Produto não encontrado.")
        if tipo not in {"ENTRADA", "SAIDA"}:
            raise ValueError("Tipo deve ser ENTRADA ou SAIDA.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if not descricao:
            raise ValueError("A descrição da movimentação é obrigatória.")

        identificador = identificador or str(uuid4())
        if any(m.identificador == identificador for m in self.movimentacoes):
            raise ValueError("O identificador da movimentação deve ser único.")

        produto = self.produtos[codigo_produto]
        estoque_anterior = produto["estoque"]

        if tipo == "SAIDA" and quantidade > estoque_anterior:
            raise ValueError("Estoque insuficiente para realizar a saída.")

        estoque_final = (
            estoque_anterior + quantidade
            if tipo == "ENTRADA"
            else estoque_anterior - quantidade
        )
        produto["estoque"] = estoque_final

        movimentacao = Movimentacao(
            identificador=identificador,
            codigo_produto=codigo_produto,
            produto=produto["descricao"],
            tipo=tipo,
            descricao=descricao,
            quantidade=quantidade,
            estoque_anterior=estoque_anterior,
            estoque_final=estoque_final,
            data_hora=datetime.now().isoformat(timespec="seconds"),
        )
        self.movimentacoes.append(movimentacao)
        return movimentacao

    def historico(self) -> list[dict]:
        return [asdict(movimentacao) for movimentacao in self.movimentacoes]


def executar_interativo(caminho_json: str | Path) -> None:
    estoque = GerenciadorEstoque(caminho_json)

    print("\nPRODUTOS DISPONÍVEIS")
    for produto in estoque.listar_produtos():
        print(f"{produto['codigo']} - {produto['descricao']} | estoque: {produto['estoque']}")

    while True:
        print("\nNova movimentação")
        codigo = int(input("Código do produto: ").strip())
        tipo = input("Tipo [ENTRADA/SAIDA]: ").strip()
        quantidade = int(input("Quantidade: ").strip())
        descricao = input("Descrição: ").strip()

        try:
            mov = estoque.movimentar(codigo, tipo, quantidade, descricao)
            print(f"Movimentação: {mov.identificador}")
            print(f"Produto: {mov.produto}")
            print(f"Estoque final: {mov.estoque_final}")
        except ValueError as erro:
            print(f"Erro: {erro}")

        continuar = input("Deseja lançar outra movimentação? [s/N]: ").strip().lower()
        if continuar != "s":
            break


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    executar_interativo(raiz / "data" / "estoque.json")

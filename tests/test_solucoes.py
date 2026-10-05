import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from src.desafio1_comissoes import calcular_comissoes, carregar_vendas
from src.desafio2_estoque import GerenciadorEstoque
from src.desafio3_juros import calcular_juros

RAIZ = Path(__file__).resolve().parents[1]


class TestComissoes(unittest.TestCase):
    def test_comissoes_do_json_do_desafio(self):
        vendas = carregar_vendas(RAIZ / "data" / "vendas.json")
        resumo = calcular_comissoes(vendas)

        esperado = {
            "João Silva": Decimal("495.68"),
            "Maria Souza": Decimal("465.95"),
            "Carlos Oliveira": Decimal("379.37"),
            "Ana Lima": Decimal("404.98"),
        }

        for vendedor, comissao in esperado.items():
            self.assertEqual(resumo[vendedor]["comissao"], comissao)


class TestEstoque(unittest.TestCase):
    def setUp(self):
        self.estoque = GerenciadorEstoque(RAIZ / "data" / "estoque.json")

    def test_entrada_e_saida(self):
        entrada = self.estoque.movimentar(101, "ENTRADA", 10, "Reposição", "MOV-001")
        self.assertEqual(entrada.estoque_final, 160)

        saida = self.estoque.movimentar(101, "SAIDA", 25, "Venda", "MOV-002")
        self.assertEqual(saida.estoque_final, 135)

    def test_saida_sem_estoque_suficiente(self):
        with self.assertRaises(ValueError):
            self.estoque.movimentar(102, "SAIDA", 100, "Saída inválida", "MOV-003")

    def test_identificador_deve_ser_unico(self):
        self.estoque.movimentar(103, "ENTRADA", 1, "Ajuste", "MOV-004")
        with self.assertRaises(ValueError):
            self.estoque.movimentar(103, "ENTRADA", 1, "Ajuste", "MOV-004")


class TestJuros(unittest.TestCase):
    def test_juros_de_quatro_dias(self):
        resultado = calcular_juros(
            Decimal("100.00"),
            date(2026, 10, 1),
            hoje=date(2026, 10, 5),
        )
        self.assertEqual(resultado["dias_atraso"], 4)
        self.assertEqual(resultado["juros"], Decimal("10.00"))
        self.assertEqual(resultado["valor_total"], Decimal("110.00"))

    def test_sem_juros_antes_do_vencimento(self):
        resultado = calcular_juros(
            Decimal("100.00"),
            date(2026, 10, 10),
            hoje=date(2026, 10, 5),
        )
        self.assertEqual(resultado["dias_atraso"], 0)
        self.assertEqual(resultado["juros"], Decimal("0.00"))


if __name__ == "__main__":
    unittest.main()

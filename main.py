from pathlib import Path

from src.desafio1_comissoes import exibir_resumo
from src.desafio2_estoque import executar_interativo as executar_estoque
from src.desafio3_juros import executar_interativo as executar_juros

RAIZ = Path(__file__).resolve().parent


def main() -> None:
    while True:
        print("\nDESAFIO DEV")
        print("1 - Calcular comissões")
        print("2 - Movimentar estoque")
        print("3 - Calcular juros")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            exibir_resumo(RAIZ / "data" / "vendas.json")
        elif opcao == "2":
            executar_estoque(RAIZ / "data" / "estoque.json")
        elif opcao == "3":
            executar_juros()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

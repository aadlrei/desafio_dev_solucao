from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

CENTAVOS = Decimal("0.01")
TAXA_DIARIA = Decimal("0.025")


def converter_data(texto: str) -> date:
    """Aceita datas em AAAA-MM-DD ou DD/MM/AAAA."""
    texto = texto.strip()
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            pass
    raise ValueError("Data inválida. Use AAAA-MM-DD ou DD/MM/AAAA.")


def calcular_juros(
    valor: Decimal,
    vencimento: date,
    hoje: date | None = None,
) -> dict[str, Decimal | int | date]:
    """Calcula multa diária simples de 2,5% somente para dias em atraso."""
    valor = Decimal(valor)
    hoje = hoje or date.today()

    if valor < 0:
        raise ValueError("O valor não pode ser negativo.")

    dias_atraso = max((hoje - vencimento).days, 0)
    juros = (valor * TAXA_DIARIA * dias_atraso).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    total = (valor + juros).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    return {
        "valor_original": valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP),
        "vencimento": vencimento,
        "data_calculo": hoje,
        "dias_atraso": dias_atraso,
        "juros": juros,
        "valor_total": total,
    }


def executar_interativo() -> None:
    valor = Decimal(input("Valor: R$ ").strip().replace(",", "."))
    vencimento = converter_data(input("Data de vencimento [AAAA-MM-DD ou DD/MM/AAAA]: "))
    resultado = calcular_juros(valor, vencimento)

    print(f"\nData do cálculo: {resultado['data_calculo'].strftime('%d/%m/%Y')}")
    print(f"Dias em atraso: {resultado['dias_atraso']}")
    print(f"Juros: R$ {resultado['juros']:.2f}")
    print(f"Valor total: R$ {resultado['valor_total']:.2f}")


if __name__ == "__main__":
    executar_interativo()

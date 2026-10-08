
from decimal import Decimal, ROUND_HALF_UP


def calcular_comissao(valor: Decimal) -> Decimal:
    """Calcula a comissão de uma venda, arredondada em centavos."""
    if valor < Decimal("0"):
        raise ValueError("O valor da venda não pode ser negativo.")

    if valor < Decimal("100"):
        percentual = Decimal("0")
    elif valor < Decimal("500"):
        percentual = Decimal("0.01")
    else:
        percentual = Decimal("0.05")

    comissao = valor * percentual

    return comissao.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calcular_comissoes_vendedores(vendas: list[dict]) -> dict:
    """Agrupa o total de comissões por vendedor."""
    totais = {}

    for venda in vendas:
        vendedor = venda["vendedor"]
        valor = Decimal(str(venda["valor"]))

        comissao = calcular_comissao(valor)

        if vendedor not in totais:
            totais[vendedor] = Decimal("0.00")

        totais[vendedor] += comissao

    return totais

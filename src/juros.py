from datetime import date
from decimal import Decimal, ROUND_HALF_UP


TAXA_DIARIA = Decimal("0.025")
CENTAVOS = Decimal("0.01")


def calcular_juros(
    valor: Decimal,
    vencimento: date,
    data_referencia: date | None = None,
) -> dict:
    """Calcula juros simples e compostos de 2,5% ao dia.

    Os juros incidem apenas após o vencimento.
    Os valores são arredondados ao centavo no final do cálculo.
    """
    if not isinstance(valor, Decimal):
        raise TypeError("O valor deve ser do tipo Decimal.")

    if not valor.is_finite() or valor <= 0:
        raise ValueError("O valor deve ser positivo e finito.")

    if not isinstance(vencimento, date):
        raise TypeError("O vencimento deve ser uma data válida.")

    if data_referencia is None:
        data_referencia = date.today()

    if not isinstance(data_referencia, date):
        raise TypeError("A data de referência deve ser válida.")

    dias_atraso = max(
        (data_referencia - vencimento).days,
        0,
    )

    juros_simples = (
        valor * TAXA_DIARIA * dias_atraso
    ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    juros_compostos = (
        valor * ((1 + TAXA_DIARIA) ** dias_atraso - 1)
    ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    valor_original = valor.quantize(
        CENTAVOS,
        rounding=ROUND_HALF_UP,
    )

    return {
        "valor_original": valor_original,
        "vencimento": vencimento,
        "data_referencia": data_referencia,
        "dias_atraso": dias_atraso,
        "juros": juros_simples,
        "total": valor_original + juros_simples,
        "juros_compostos": juros_compostos,
        "total_composto": valor_original + juros_compostos,
    }
from datetime import date, timedelta
from decimal import Decimal

import pytest

from src.juros import calcular_juros


DATA_REFERENCIA = date(2026, 10, 8)


@pytest.mark.parametrize(
    "dias, juros_esperados, total_esperado",
    [
        (0, "0.00", "1000.00"),
        (1, "25.00", "1025.00"),
        (2, "50.00", "1050.00"),
        (4, "100.00", "1100.00"),
        (10, "250.00", "1250.00"),
    ],
)
def test_juros_simples(
    dias, juros_esperados, total_esperado
):
    vencimento = DATA_REFERENCIA - timedelta(days=dias)

    resultado = calcular_juros(
        Decimal("1000.00"),
        vencimento,
        DATA_REFERENCIA,
    )

    assert resultado["dias_atraso"] == dias
    assert resultado["juros"] == Decimal(juros_esperados)
    assert resultado["total"] == Decimal(total_esperado)


@pytest.mark.parametrize(
    "dias, juros_esperados, total_esperado",
    [
        (0, "0.00", "1000.00"),
        (1, "25.00", "1025.00"),
        (2, "50.63", "1050.63"),
        (4, "103.81", "1103.81"),
        (7, "188.69", "1188.69"),
    ],
)
def test_juros_compostos(
    dias, juros_esperados, total_esperado
):
    vencimento = DATA_REFERENCIA - timedelta(days=dias)

    resultado = calcular_juros(
        Decimal("1000.00"),
        vencimento,
        DATA_REFERENCIA,
    )

    assert resultado["juros_compostos"] == Decimal(
        juros_esperados
    )
    assert resultado["total_composto"] == Decimal(
        total_esperado
    )


def test_vencimento_futuro():
    vencimento = DATA_REFERENCIA + timedelta(days=10)

    resultado = calcular_juros(
        Decimal("500.00"),
        vencimento,
        DATA_REFERENCIA,
    )

    assert resultado["dias_atraso"] == 0
    assert resultado["juros"] == Decimal("0.00")
    assert resultado["juros_compostos"] == Decimal("0.00")
    assert resultado["total"] == Decimal("500.00")
    assert resultado["total_composto"] == Decimal("500.00")


def test_arredondamento_monetario():
    resultado = calcular_juros(
        Decimal("10.10"),
        DATA_REFERENCIA - timedelta(days=1),
        DATA_REFERENCIA,
    )

    assert resultado["juros"] == Decimal("0.25")
    assert resultado["juros_compostos"] == Decimal("0.25")
    assert resultado["total"] == Decimal("10.35")


@pytest.mark.parametrize(
    "valor",
    [
        Decimal("0"),
        Decimal("-10"),
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
    ],
)
def test_valores_invalidos(valor):
    with pytest.raises(ValueError):
        calcular_juros(
            valor,
            DATA_REFERENCIA,
            DATA_REFERENCIA,
        )


def test_valor_tipo_invalido():
    with pytest.raises(TypeError):
        calcular_juros(
            1000.00,
            DATA_REFERENCIA,
            DATA_REFERENCIA,
        )


def test_vencimento_invalido():
    with pytest.raises(TypeError):
        calcular_juros(
            Decimal("100.00"),
            "08/10/2026",
            DATA_REFERENCIA,
        )


def test_data_referencia_invalida():
    with pytest.raises(TypeError):
        calcular_juros(
            Decimal("100.00"),
            DATA_REFERENCIA,
            "08/10/2026",
        )


def test_resultado_preserva_datas():
    vencimento = date(2026, 10, 1)

    resultado = calcular_juros(
        Decimal("100.00"),
        vencimento,
        DATA_REFERENCIA,
    )

    assert resultado["vencimento"] == vencimento
    assert resultado["data_referencia"] == DATA_REFERENCIA


def test_juros_compostos_superam_simples():
    resultado = calcular_juros(
        Decimal("1000.00"),
        DATA_REFERENCIA - timedelta(days=30),
        DATA_REFERENCIA,
    )

    assert resultado["juros_compostos"] > resultado["juros"]
    assert resultado["total_composto"] > resultado["total"]
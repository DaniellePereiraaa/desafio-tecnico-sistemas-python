
from decimal import Decimal
import pytest
from src.comissoes import calcular_comissao
from src.comissoes import calcular_comissoes_vendedores

@pytest.mark.parametrize(
    "valor, esperado",
    [
        ("90.00", "0.00"),
        ("99.99", "0.00"),
        ("100.00", "1.00"),
        ("250.00", "2.50"),
        ("499.99", "5.00"),
        ("500.00", "25.00"),
        ("1200.00", "60.00"),
    ],
)
def test_calcular_comissao(valor, esperado):
    resultado = calcular_comissao(Decimal(valor))

    assert resultado == Decimal(esperado)


def test_calcular_comissao_valor_negativo():
    with pytest.raises(ValueError):
        calcular_comissao(Decimal("-10.00"))

def test_calcular_comissoes_vendedores():
    vendas = [
        {"vendedor": "Ana", "valor": 100},
        {"vendedor": "Ana", "valor": 500},
        {"vendedor": "Joao", "valor": 200},
        {"vendedor": "Joao", "valor": 50},
    ]

    resultado = calcular_comissoes_vendedores(vendas)

    assert resultado == {
        "Ana": Decimal("26.00"),
        "Joao": Decimal("2.00"),
    }


def test_calcular_comissoes_lista_vazia():
    assert calcular_comissoes_vendedores([]) == {}

import pytest

from src.estoque import movimentar_estoque


@pytest.fixture
def produtos():
    return [
        {
            "codigoProduto": 101,
            "descricaoProduto": "Caneta Azul",
            "estoque": 150,
        },
        {
            "codigoProduto": 102,
            "descricaoProduto": "Caderno Universitário",
            "estoque": 75,
        },
    ]


def test_entrada_estoque(produtos):
    atualizado, movimento = movimentar_estoque(
        produtos, 101, "entrada", 50
    )

    assert atualizado[0]["estoque"] == 200
    assert movimento["saldoAnterior"] == 150
    assert movimento["saldoAtual"] == 200
    assert movimento["tipo"] == "entrada"


def test_saida_estoque(produtos):
    atualizado, movimento = movimentar_estoque(
        produtos, 101, "saida", 40
    )

    assert atualizado[0]["estoque"] == 110
    assert movimento["saldoAtual"] == 110


def test_saida_estoque_insuficiente(produtos):
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        movimentar_estoque(produtos, 101, "saida", 200)


def test_produto_inexistente(produtos):
    with pytest.raises(ValueError, match="Produto não encontrado"):
        movimentar_estoque(produtos, 999, "entrada", 10)


@pytest.mark.parametrize("quantidade", [0, -5, 2.5, True])
def test_quantidade_invalida(produtos, quantidade):
    with pytest.raises(ValueError):
        movimentar_estoque(produtos, 101, "entrada", quantidade)


def test_tipo_invalido(produtos):
    with pytest.raises(ValueError):
        movimentar_estoque(produtos, 101, "transferencia", 10)


def test_preserva_estoque_original(produtos):
    movimentar_estoque(produtos, 101, "entrada", 50)

    assert produtos[0]["estoque"] == 150


def test_identificadores_unicos(produtos):
    _, primeiro = movimentar_estoque(
        produtos, 101, "entrada", 10
    )
    _, segundo = movimentar_estoque(
        produtos, 101, "entrada", 10
    )

    assert primeiro["id"] != segundo["id"]


def test_saida_total_estoque(produtos):
    atualizado, movimento = movimentar_estoque(
        produtos, 102, "saida", 75
    )

    assert atualizado[1]["estoque"] == 0
    assert movimento["saldoAtual"] == 0

@pytest.mark.parametrize(
    "tipo",
    ["saida", "saída", "SAÍDA", " Saída "],
)
def test_variacoes_de_saida(produtos, tipo):
    atualizado, movimento = movimentar_estoque(
        produtos, 101, tipo, 10
    )

    assert atualizado[0]["estoque"] == 140
    assert movimento["tipo"] == "saida"
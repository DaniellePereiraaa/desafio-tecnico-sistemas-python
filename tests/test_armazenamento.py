import json

import pytest

from src.armazenamento import carregar_estado, salvar_estado
from src.estoque import movimentar_estoque


@pytest.fixture
def arquivos_estoque(tmp_path):
    """Cria arquivos temporários isolados para cada teste."""
    inicial = tmp_path / "estoque.json"
    estado = tmp_path / "estado_estoque.json"

    dados = {
        "estoque": [
            {
                "codigoProduto": 101,
                "descricaoProduto": "Caneta Azul",
                "estoque": 150,
            }
        ]
    }

    inicial.write_text(
        json.dumps(dados, ensure_ascii=False),
        encoding="utf-8",
    )

    return inicial, estado


def test_carregar_estoque_inicial(arquivos_estoque):
    inicial, estado = arquivos_estoque

    resultado = carregar_estado(inicial, estado)

    assert resultado["estoque"][0]["estoque"] == 150
    assert resultado["movimentacoes"] == []


def test_salvar_e_recuperar_estado(arquivos_estoque):
    inicial, estado = arquivos_estoque

    dados = carregar_estado(inicial, estado)

    atualizado, movimento = movimentar_estoque(
        dados["estoque"], 101, "entrada", 20
    )

    salvar_estado(
        estado,
        {
            "estoque": atualizado,
            "movimentacoes": [movimento],
        },
    )

    recuperado = carregar_estado(inicial, estado)

    assert recuperado["estoque"][0]["estoque"] == 170
    assert len(recuperado["movimentacoes"]) == 1
    assert recuperado["movimentacoes"][0]["id"] == movimento["id"]


def test_persistencia_de_varias_movimentacoes(arquivos_estoque):
    inicial, estado = arquivos_estoque
    dados = carregar_estado(inicial, estado)

    atualizado, primeira = movimentar_estoque(
        dados["estoque"], 101, "entrada", 50
    )

    salvar_estado(
        estado,
        {
            "estoque": atualizado,
            "movimentacoes": [primeira],
        },
    )

    dados = carregar_estado(inicial, estado)

    atualizado, segunda = movimentar_estoque(
        dados["estoque"], 101, "saida", 30
    )

    salvar_estado(
        estado,
        {
            "estoque": atualizado,
            "movimentacoes": dados["movimentacoes"] + [segunda],
        },
    )

    recuperado = carregar_estado(inicial, estado)

    assert recuperado["estoque"][0]["estoque"] == 170
    assert len(recuperado["movimentacoes"]) == 2
    assert primeira["id"] != segunda["id"]


def test_preserva_json_original(arquivos_estoque):
    inicial, estado = arquivos_estoque

    dados = carregar_estado(inicial, estado)

    atualizado, movimento = movimentar_estoque(
        dados["estoque"], 101, "saida", 10
    )

    salvar_estado(
        estado,
        {
            "estoque": atualizado,
            "movimentacoes": [movimento],
        },
    )

    original = json.loads(
        inicial.read_text(encoding="utf-8")
    )

    assert original["estoque"][0]["estoque"] == 150


def test_arquivo_estado_corrompido(arquivos_estoque):
    inicial, estado = arquivos_estoque

    estado.write_text(
        "{json invalido",
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        carregar_estado(inicial, estado)
from copy import deepcopy
from uuid import uuid4
import unicodedata

def movimentar_estoque(
    produtos: list[dict],
    codigo_produto: int,
    tipo: str,
    quantidade: int,
) -> tuple[list[dict], dict]:
    """Registra uma entrada ou saída e retorna o estoque atualizado."""

    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser um inteiro positivo.")

    tipo = unicodedata.normalize("NFKD", tipo.strip().lower())
    tipo = "".join(
        caractere
        for caractere in tipo
        if not unicodedata.combining(caractere)
)

    if tipo not in ("entrada", "saida"):
        raise ValueError("O tipo deve ser 'entrada' ou 'saida'.")

    estoque_atualizado = deepcopy(produtos)

    produto = next(
        (
            item for item in estoque_atualizado
            if item["codigoProduto"] == codigo_produto
        ),
        None,
    )

    if produto is None:
        raise ValueError("Produto não encontrado.")

    saldo_anterior = produto["estoque"]

    if tipo == "saida" and quantidade > saldo_anterior:
        raise ValueError("Estoque insuficiente.")

    if tipo == "entrada":
        produto["estoque"] += quantidade
    else:
        produto["estoque"] -= quantidade

    movimentacao = {
        "id": str(uuid4()),
        "codigoProduto": codigo_produto,
        "descricaoProduto": produto["descricaoProduto"],
        "tipo": tipo,
        "descricaoMovimentacao": (
            "Entrada de mercadoria"
            if tipo == "entrada"
            else "Saída de mercadoria"
        ),
        "quantidade": quantidade,
        "saldoAnterior": saldo_anterior,
        "saldoAtual": produto["estoque"],
    }

    return estoque_atualizado, movimentacao
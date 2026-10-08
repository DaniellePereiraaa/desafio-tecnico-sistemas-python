
import json
from pathlib import Path

from src.comissoes import calcular_comissoes_vendedores


BASE_DIR = Path(__file__).resolve().parent


def executar_comissoes():
    caminho = BASE_DIR / "data" / "vendas.json"

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    resultado = calcular_comissoes_vendedores(dados["vendas"])

    print("\nCOMISSÕES POR VENDEDOR")
    print("-" * 40)

    for vendedor, comissao in resultado.items():
        valor_formatado = f"{comissao:.2f}".replace(".", ",")
        print(f"{vendedor}: R$ {valor_formatado}")


if __name__ == "__main__":
    executar_comissoes()
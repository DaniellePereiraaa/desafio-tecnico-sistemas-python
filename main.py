
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from src.armazenamento import carregar_estado, salvar_estado
from src.comissoes import calcular_comissoes_vendedores
from src.estoque import movimentar_estoque
from src.juros import calcular_juros


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def formatar_moeda(valor: Decimal) -> str:
    """Formata um valor monetário no padrão brasileiro."""
    formatado = f"{valor:,.2f}"

    formatado = (
        formatado
        .replace(",", "TEMP")
        .replace(".", ",")
        .replace("TEMP", ".")
    )

    return f"R$ {formatado}"


def executar_comissoes():
    caminho = DATA_DIR / "vendas.json"

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    resultado = calcular_comissoes_vendedores(
        dados["vendas"]
    )

    print("\nCOMISSÕES POR VENDEDOR")
    print("-" * 40)

    for vendedor, comissao in resultado.items():
        print(
            f"{vendedor}: {formatar_moeda(comissao)}"
        )


def executar_estoque():
    caminho_inicial = DATA_DIR / "estoque.json"
    caminho_estado = DATA_DIR / "estado_estoque.json"

    estado = carregar_estado(
        caminho_inicial,
        caminho_estado,
    )

    print("\nPRODUTOS DISPONÍVEIS")
    print("-" * 50)

    for produto in estado["estoque"]:
        print(
            f'{produto["codigoProduto"]} - '
            f'{produto["descricaoProduto"]} | '
            f'Saldo: {produto["estoque"]}'
        )

    try:
        codigo = int(input("\nCódigo do produto: "))
        tipo = input("Movimentação (entrada/saída): ")
        quantidade = int(input("Quantidade: "))

        atualizado, movimentacao = movimentar_estoque(
            estado["estoque"],
            codigo,
            tipo,
            quantidade,
        )

        novo_estado = {
            "estoque": atualizado,
            "movimentacoes": (
                estado["movimentacoes"] + [movimentacao]
            ),
        }

        salvar_estado(caminho_estado, novo_estado)

        print("\nMOVIMENTAÇÃO REGISTRADA")
        print("-" * 40)
        print(f'ID: {movimentacao["id"]}')
        print(
            f'Descrição: '
            f'{movimentacao["descricaoMovimentacao"]}'
        )
        print(
            f'Produto: '
            f'{movimentacao["descricaoProduto"]}'
        )
        print(
            f'Quantidade: {movimentacao["quantidade"]}'
        )
        print(
            f'Estoque final: {movimentacao["saldoAtual"]}'
        )

    except ValueError as erro:
        print(f"\nOperação inválida: {erro}")

    except OSError as erro:
        print(f"\nErro ao acessar arquivo: {erro}")


def executar_juros():
    print("\nCÁLCULO DE JUROS POR ATRASO")
    print("-" * 40)

    try:
        valor_texto = input(
            "Valor original (ex.: 1000,50): R$ "
        )

        valor = Decimal(
            valor_texto.strip().replace(",", ".")
        )

        if not valor.is_finite() or valor <= 0:
            raise ValueError(
                "O valor deve ser positivo e finito."
            )

        if valor.as_tuple().exponent < -2:
            raise ValueError(
                "Informe no máximo duas casas decimais."
            )

        data_texto = input(
            "Data de vencimento (DD/MM/AAAA): "
        )

        vencimento = datetime.strptime(
            data_texto.strip(),
            "%d/%m/%Y",
        ).date()

        resultado = calcular_juros(
            valor,
            vencimento,
        )

        print("\nRESULTADO DO CÁLCULO")
        print("-" * 40)

        print(
            f'Valor original: '
            f'{formatar_moeda(resultado["valor_original"])}'
        )
        print(
            f'Vencimento: '
            f'{resultado["vencimento"].strftime("%d/%m/%Y")}'
        )
        print(
            f'Data de referência: '
            f'{resultado["data_referencia"].strftime("%d/%m/%Y")}'
        )
        print(
            f'Dias de atraso: '
            f'{resultado["dias_atraso"]}'
        )
        print("Taxa diária: 2,5%")

        print("\nJUROS SIMPLES (CÁLCULO PRINCIPAL)")
        print("-" * 40)
        print(
            f'Juros: '
            f'{formatar_moeda(resultado["juros"])}'
        )
        print(
            f'Total atualizado: '
            f'{formatar_moeda(resultado["total"])}'
        )

        print("\nJUROS COMPOSTOS (SIMULAÇÃO)")
        print("-" * 40)
        print(
            f'Juros: '
            f'{formatar_moeda(resultado["juros_compostos"])}'
        )
        print(
            f'Total atualizado: '
            f'{formatar_moeda(resultado["total_composto"])}'
        )

    except (ValueError, InvalidOperation) as erro:
        print(f"\nDados inválidos: {erro}")
        print(
            "Confira o valor e a data no formato DD/MM/AAAA."
        )


def main():
    while True:
        print("\n=== DESAFIO TÉCNICO ===")
        print("1 - Calcular comissões")
        print("2 - Movimentar estoque")
        print("3 - Calcular juros por atraso")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            executar_comissoes()

        elif opcao == "2":
            executar_estoque()

        elif opcao == "3":
            executar_juros()

        elif opcao == "0":
            print("\nPrograma encerrado.")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

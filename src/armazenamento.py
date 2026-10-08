
import json
import os
import tempfile
from pathlib import Path


def carregar_estado(
    caminho_inicial: Path,
    caminho_estado: Path,
) -> dict:
    """Carrega o estado salvo ou inicializa com o JSON original."""

    if caminho_estado.exists():
        with caminho_estado.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    with caminho_inicial.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return {
        "estoque": dados["estoque"],
        "movimentacoes": [],
    }


def salvar_estado(caminho: Path, estado: dict) -> None:
    """Grava o estado usando um arquivo temporário."""

    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=caminho.parent,
            suffix=".tmp",
            delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(estado, arquivo, ensure_ascii=False, indent=2)

        os.replace(temporario, caminho)

    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)

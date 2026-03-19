import re
from os import getenv
from pathlib import Path
from typing import List

import pandas as pd

from src.models.export import Export
from src.models.filtro import Filtro


def get_dataframe(path: Path) -> pd.DataFrame:
    """
    Lê um arquivo Excel e retorna o DataFrame correspondente.

    Args:
        path: Caminho do arquivo Excel.

    Returns:
        DataFrame com os dados da planilha.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se houver erro na leitura do arquivo.
    """
    if not Path(path).is_file():
        raise FileNotFoundError(f"Arquivo {path} não encontrado")

    try:
        return pd.read_excel(path)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo {path}: {e}") from e


def check_colunas(colunas: List[str], coluna: str) -> None:
    """
    Verifica se uma coluna existe na lista de colunas.

    Args:
        colunas: Lista de colunas disponíveis.
        coluna: Coluna esperada.

    Raises:
        ValueError: Se a coluna não for encontrada.
    """
    if coluna not in colunas:
        raise ValueError(f"Coluna '{coluna}' não encontrada no dataframe")


def get_unique_values(dataframe: pd.DataFrame, coluna: str) -> List[str]:
    """
    Retorna os valores únicos de uma coluna do DataFrame.

    Args:
        dataframe: DataFrame de origem.
        coluna: Nome da coluna.

    Returns:
        Lista de valores únicos.
    """
    return dataframe[coluna].unique().tolist()


def applying_filters(filtro: Filtro) -> pd.DataFrame:
    """
    Aplica um filtro ao DataFrame, retornando apenas as linhas
    onde ``filtro.coluna == filtro.valor``.

    Args:
        filtro: Objeto Filtro com coluna, dataframe e valor.

    Returns:
        DataFrame filtrado.
    """
    return filtro.dataframe[filtro.dataframe[filtro.coluna] == filtro.valor]


def export_to_excel(export: Export) -> None:
    """
    Exporta um DataFrame para um arquivo Excel.

    Args:
        export: Objeto Export com dataframe, diretório, nome do arquivo e nome da aba.
    """
    caminho = export.diretorio / export.nome_arquivo
    export.dataframe.to_excel(caminho, index=False, sheet_name=export.nome_aba)


def check_environment_variables(variables: List[str]) -> None:
    """
    Verifica se todas as variáveis de ambiente da lista estão definidas.

    Args:
        variables: Lista de nomes de variáveis de ambiente esperadas.

    Raises:
        ValueError: Se uma ou mais variáveis não estiverem definidas.
    """
    missing = [var for var in variables if not getenv(var)]

    if missing:
        raise ValueError(
            f"Variáveis de ambiente não encontradas: {', '.join(missing)}"
        )


def safe_name(text: str) -> str:
    """
    Sanitiza um texto para ser usado como nome de arquivo.

    Args:
        text: Texto a ser sanitizado.

    Returns:
        Texto com caracteres inválidos substituídos por ``_``.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", str(text)).strip()
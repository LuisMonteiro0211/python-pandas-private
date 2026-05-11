"""Funções auxiliares para leitura de Excel, validação de colunas, filtros e export.

Usado pelos serviços em :mod:`src.services`; não importa interface gráfica.
"""

import re
from os import getenv
from pathlib import Path
from typing import List

import pandas as pd
from pandas.api.types import is_string_dtype

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


def check_colunas(list_to_check: List[str], list_to_columns_check: List[str]) -> None:
    """
    Verifica se todas as colunas da lista de colunas esperadas existem na lista de colunas disponíveis.

    Args:
        list_to_check: Lista de colunas disponíveis.
        list_to_columns_check: Lista de colunas esperadas.

    Raises:
        ValueError: Se a coluna não for encontrada.
    """
    for column in list_to_columns_check:
        if column not in list_to_check:
            raise ValueError(f"Coluna '{column}' não encontrada no dataframe")


def get_unique_values(dataframe: pd.DataFrame, coluna: str) -> List[str]:
    """
    Retorna uma lista com os valores únicos de uma coluna do DataFrame.

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
    onde ``filtro.coluna == filtro.valor`` for True.

    Args:
        filtro: Objeto Filtro com coluna, dataframe e valor.

    Returns:
        DataFrame filtrado.

    Exemplo:
    >>> filtered_to_setor = Filtro(coluna="SETOR", dataframe=safe_dataframe, valor="Setor 1")
    >>> df_filtered_to_setor = applying_filters(filtered_to_setor)
    >>> print(df_filtered_to_setor)

    LINHAS    SETOR    TURNO    NOME  IDADE SEXO

    0        Setor 1  Turno 1  João   25     M

    1        Setor 1  Turno 2  Maria  30     F
    """
    return filtro.dataframe[filtro.dataframe[filtro.coluna] == filtro.valor]


def export_to_excel(export: Export) -> None:
    """
    Exporta um DataFrame para um arquivo Excel.

    Args:
        export: Objeto Export com dataframe, diretório, nome do arquivo e nome da aba.
    """
    caminho = export.diretorio / export.nome_arquivo #Barra junta o diretorio e o nome do arquivo
    export.dataframe.to_excel(caminho, index=False) #index=False para não incluir o índice no arquivo


def check_environment_variables(variables: List[str]) -> None:
    """
    Verifica se todas as variáveis de ambiente da lista estão definidas.

    Args:
        variables: Lista de nomes de variáveis de ambiente esperadas.

    Raises:
        ValueError: Se uma ou mais variáveis não estiverem definidas.
    """
    missing = []
    for var in variables:
        if not getenv(var):
            missing.append(var)

    if missing:
        raise ValueError(f"Variáveis de ambiente não encontradas: {', '.join(missing)}")


def safe_name(text: str) -> str:
    """
    Sanitiza um texto para ser usado como nome de arquivo.

    Args:
        text: Texto a ser sanitizado.

    Returns:
        Texto com caracteres inválidos substituídos por ``_``.
    """
    return re.sub(r'[<>:"/\\|?*]', "_", str(text)).strip()

def safe_name_to_column(list_column: List[str]) -> List[str]:
    """
    Sanitiza uma lista de nomes de colunas para facilitar seu uso no DataFrame.
    Transforma as colunas para maiúsculas e substitui espaços por underscores.

    Args:
        list_column: Lista de nomes de colunas a serem sanitizadas.

    Returns:
        Lista de nomes de colunas sanitizadas.
    """
    list_to_safe_name: List[str] = [column.upper().replace(" ", "_") for column in list_column]
    return list_to_safe_name

def is_nan_in_column(list_column: List[str], dataframe: pd.DataFrame) -> None:
    """
    Verifica se alguma das colunas especificadas possui valores NaN no DataFrame.

    Args:
        list_column: Lista de nomes de colunas a serem verificadas.
        dataframe: DataFrame no qual as colunas serão analisadas.

    Raises:
        ValueError: Se alguma coluna contiver valores NaN.
    """
    for column in list_column:
        if dataframe[column].isna().any():
            raise ValueError(f"Coluna {column} contém valores NaN")

def strip_space_in_column(list_column: List[str], dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Remove espaços em branco no início e no fim dos valores de cada coluna
    especificada, retornando um DataFrame com os valores ajustados.

    Args:
        list_column: Lista de nomes de colunas cujos valores serão ajustados.
        dataframe: DataFrame onde as operações serão aplicadas.

    Returns:
        DataFrame com os valores das colunas ajustados.

    Raises:
        TypeError: Se alguma das colunas informadas não for do tipo texto
            (dtype diferente de 'object'), pois não é possível aplicar
            ``str.strip()`` em colunas numéricas, datetime, etc.
    """

    for column in list_column:
        if not is_string_dtype(dataframe[column]):
            raise TypeError(f"Coluna {column} não é um texto")

        safe_column = dataframe[column].str.strip()
        dataframe[column] = safe_column

    return dataframe


def dataframe_is_empty(dataframe: pd.DataFrame) -> None:
    """
    Verifica se o DataFrame está vazio.

    Args:
        dataframe: DataFrame a ser verificado.

    Raises:
        ValueError: Se o DataFrame estiver vazio.
    """
    if dataframe.empty:
        raise ValueError("DataFrame está vazio")

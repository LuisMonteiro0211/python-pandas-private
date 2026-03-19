import pandas as pd
from typing import List
from src.models.filtro import Filtro
from src.models.export import Export
from pathlib import Path
import re
from os import getenv

def get_dataframe(path: str) -> pd.DataFrame:
    """
    Função para obter o dataframe a partir do caminho da planilha

    Args:
        path: Caminho da planilha
    Returns:
        pd.DataFrame: DataFrame com os dados da planilha
    """
    if not Path(path).is_file():
        raise FileNotFoundError(f"Arquivo {path} não encontrado")
    
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo {path}: {e}")

def get_colunas(dataframe: pd.DataFrame) -> List[str]:
    """
    Função para obter as colunas do dataframe

    Args:
        dataframe: DataFrame com os dados
    Returns:
        List[str]: Lista com as colunas do dataframe
    """
    colunas: List[str] = dataframe.columns.tolist()
    return colunas

def check_colunas(colunas: List[str], coluna: str) -> None:
    """
    Função para verificar se a coluna existe no dataframe

    Args:
        colunas: Lista com as colunas do dataframe
        coluna: Coluna a ser verificada
    Returns:
        None (Se a coluna não existir, uma exceção é lançada)
    """
    if coluna not in colunas:
        raise ValueError(f"Coluna '{coluna}' não encontrada no dataframe")

def get_setores(dataframe: pd.DataFrame) -> List[str]:
    """
    Função para obter os setores do dataframe
    
    Args:
        dataframe: DataFrame com os dados
    Returns:
        List[str]: Lista com os setores do dataframe
    """
    setores: List[str] = dataframe['SETOR'].unique().tolist()
    return setores

def get_turnos(dataframe: pd.DataFrame) -> List[str]:
    """
    Função para obter os turnos do dataframe
    Args:
        dataframe: DataFrame com os dados
    Returns:
        List[str]: Lista com os turnos do dataframe
    """
    turnos: List[str] = dataframe['TURNO'].unique().tolist()
    return turnos

def applying_filters(filtro: Filtro) -> pd.DataFrame:
    """
    Função para aplicar os filtros ao dataframe

    Args:
        filtro: Filtro a ser aplicado (Objeto Filtro - coluna, dataframe, valor)
    Returns:
        pd.DataFrame: DataFrame com os dados filtrados
    """
    return filtro.dataframe[filtro.dataframe[filtro.coluna] == filtro.valor]

def export_to_excel(object_to_export: Export) -> None:
    """
    Função para exportar o dataframe para um arquivo Excel
    Args:
        object_to_export: Objeto Export com o dataframe, diretório, nome do arquivo e nome da pasta
    Returns:
        None
    """

    diretorio: Path = object_to_export.diretorio
    object_to_export.dataframe.to_excel(diretorio / object_to_export.nome_arquivo, index=False, sheet_name=object_to_export.nome_pasta)

def check_environment_variables(list_of_variables: List[str]) -> None:
    """
    Função para verificar se a variável de ambiente existe
    Args:
        environment_variable: Variável de ambiente a ser verificada
    Returns:
        None (Se a variável de ambiente não existir, uma exceção é lançada)
    """
    list_of_variables_found = []

    for variable in list_of_variables:
        if not getenv(variable):
            list_of_variables_found.append(variable)

    if len(list_of_variables_found) > 0:
        raise ValueError(f"Variáveis de ambiente não encontradas: {', '.join(list_of_variables_found)}")

def safe_name(text: str) -> str:
    """
    Função para sanitizar o nome de um arquivo
    Args:
        text: Texto a ser sanitizado
    Returns:
        str: Texto sanitizado
    """
    return re.sub(r'[<>:"/\\|?*]', "_", str(text)).strip()


def resolver_diretorio_export(diretorio_base: Path, setor: str) -> Path:
    """
    Resolve o diretório de destino de um arquivo exportado,
    levando em conta as regras de agrupamento por pasta.

    Se o setor pertencer a um grupo, retorna diretorio_base / nome_da_pasta.
    Caso contrário, retorna o próprio diretorio_base (arquivo fica na raiz).

    A subpasta é criada automaticamente caso não exista.

    Args:
        diretorio_base: Diretório raiz de exportação (DIRETORIO_EXPORT).
        setor: Nome do setor vindo da planilha.

    Returns:
        Path do diretório onde o arquivo deve ser salvo.
    """
    from src.config.agrupamento import resolver_pasta

    pasta = resolver_pasta(setor)

    if pasta is None:
        return diretorio_base

    destino = diretorio_base / safe_name(pasta)
    destino.mkdir(parents=True, exist_ok=True)
    return destino


if __name__ == "__main__":
    pass
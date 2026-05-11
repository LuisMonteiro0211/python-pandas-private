"""Orquestra a sanitização de um DataFrame já carregado (regras de negócio puras).

Não executa I/O de arquivo; recebe :class:`pandas.DataFrame` e retorna uma cópia
tratada ou levanta exceções de validação. Erros são tratados nos controllers.
"""

from src.helpers.helper import (
    safe_name_to_column,
    is_nan_in_column,
    strip_space_in_column,
    dataframe_is_empty,
    check_colunas
)
import pandas as pd
from src.constants import REQUIRED_COLUMNS
import logging

def sanitize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica a sequência de regras de sanitização sobre um DataFrame.

    Etapas executadas, nesta ordem:
        1. Verifica se o DataFrame não está vazio.
        2. Padroniza os nomes das colunas (caixa alta + underscores).
        3. Confere se todas as colunas obrigatórias estão presentes.
        4. Remove espaços em branco no início/fim dos valores das colunas obrigatórias.
        5. Garante que nenhuma coluna obrigatória contém valores NaN.

    Args:
        dataframe: DataFrame a ser sanitizado.

    Returns:
        DataFrame sanitizado, pronto para uso.

    Raises:
        ValueError: Se o DataFrame estiver vazio, faltar alguma coluna obrigatória
            ou alguma coluna obrigatória contiver valores NaN.
        TypeError: Se alguma coluna obrigatória não for do tipo texto (necessário
            para a remoção de espaços em branco).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Sanitizando DataFrame")
    dataframe_is_empty(dataframe) # Verifica se o DataFrame está vazio
    dataframe.columns = safe_name_to_column(dataframe.columns.tolist()) # Sanitiza os nomes das colunas
    check_colunas(dataframe.columns.tolist(), REQUIRED_COLUMNS) # Verifica se as colunas existem no DataFrame
    dataframe = strip_space_in_column(REQUIRED_COLUMNS, dataframe) # Remove espaços em branco das colunas
    is_nan_in_column(REQUIRED_COLUMNS, dataframe) # Verifica se as colunas contêm valores NaN
    logger.info(f"DataFrame sanitizado")
    return dataframe

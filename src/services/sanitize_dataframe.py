from src.helpers.helper import (
    safe_name_to_column,
    is_nan_in_column,
    strip_space_in_column,
    dataframe_is_empty,
    check_colunas
)
import pandas as pd
from src.constants import REQUIRED_COLUMNS

def sanitize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitiza um DataFrame, levanta erros no caso de valores NaN, espaços em branco ou DataFrame vazio.

    Args:
        dataframe: DataFrame a ser sanitizado.

    Returns:
        DataFrame sanitizado.

    Raises:
        ValueError: Se o DataFrame estiver vazio, contiver valores NaN ou espaços em branco.
    """
    try:
        dataframe_is_empty(dataframe) # Verifica se o DataFrame está vazio
        dataframe.columns = safe_name_to_column(dataframe.columns.tolist()) # Sanitiza os nomes das colunas
        check_colunas(dataframe.columns.tolist(), REQUIRED_COLUMNS) # Verifica se as colunas existem no DataFrame
        dataframe = strip_space_in_column(REQUIRED_COLUMNS, dataframe) # Remove espaços em branco das colunas
        is_nan_in_column(REQUIRED_COLUMNS, dataframe) # Verifica se as colunas contêm valores NaN
        
        return dataframe

    except ValueError as e:
        raise ValueError(f"Erro ao sanitizar o DataFrame: {e}") from e
    except Exception as e:
        raise ValueError(f"Erro ao sanitizar o DataFrame: {e}") from e

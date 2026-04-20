from src.helpers.helper import (
    safe_name_to_column,
    is_nan_in_column,
    strip_space_in_column,
    datafrme_is_empty,
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
    datafrme_is_empty(dataframe)
    dataframe.columns = safe_name_to_column(dataframe.columns.tolist())
    strip_space_in_column(REQUIRED_COLUMNS, dataframe)
    is_nan_in_column(REQUIRED_COLUMNS, dataframe)

    return dataframe

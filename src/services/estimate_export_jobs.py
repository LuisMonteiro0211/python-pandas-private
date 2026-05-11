from src.models.filtro import Filtro
import pandas as pd
from src.constants import REQUIRED_COLUMNS
from src.helpers.helper import (
    get_unique_values,
    applying_filters,
)

def estimate_export_job_count(safe_dataframe: pd.DataFrame) -> int:
    """
    Estima o número de arquivos que serão gerados para exportação.

    Args:
        process_context: Contexto do processo de exportação.

    Returns:
        Número de arquivos que serão gerados para exportação.
    """

    estimated_jobs: int = 0

    setores = get_unique_values(safe_dataframe, REQUIRED_COLUMNS[0])

    for setor in setores:
        dataframe_to_setor = applying_filters(
            Filtro(
                coluna = REQUIRED_COLUMNS[0],
                dataframe = safe_dataframe,
                valor = setor,
            )
        )
        turnos = get_unique_values(dataframe_to_setor, REQUIRED_COLUMNS[1])

        estimated_jobs += len(turnos)

    return estimated_jobs
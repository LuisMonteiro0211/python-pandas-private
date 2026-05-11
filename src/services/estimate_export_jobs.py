"""Estimativa do número de arquivos gerados na exportação (mesma lógica de setor/turno).

Útil para dimensionar a barra de progresso antes de iniciar o processamento.
"""

from src.models.filtro import Filtro
import logging
import pandas as pd
from src.constants import REQUIRED_COLUMNS
from src.helpers.helper import (
    get_unique_values,
    applying_filters,
)

logger = logging.getLogger(__name__)

def estimate_export_job_count(safe_dataframe: pd.DataFrame) -> int:
    """
    Estima o número de arquivos que serão gerados para exportação.

    Args:
        safe_dataframe: DataFrame já sanitizado (com colunas obrigatórias).

    Returns:
        Quantidade de combinações únicas setor × turno com pelo menos um turno.
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
    logger.info(f"Estimativa de jobs: {estimated_jobs}")
    return estimated_jobs
from src.models.processcontext import ProcessContext
from src.models.filtro import Filtro
from src.constants import REQUIRED_COLUMNS
from src.helpers.helper import (
    get_unique_values,
    applying_filters,
)

def estimate_export_job_count(process_context: ProcessContext) -> int:
    """
    Estima o número de arquivos que serão gerados para exportação.

    Args:
        process_context: Contexto do processo de exportação.

    Returns:
        Número de arquivos que serão gerados para exportação.
    """

    estimated_jobs: int = 0

    setores = get_unique_values(process_context.safe_dataframe, REQUIRED_COLUMNS[0])

    for setor in setores:
        dataframe_to_setor = applying_filters(
            Filtro(
                coluna = REQUIRED_COLUMNS[0],
                dataframe = process_context.safe_dataframe,
                valor = setor,
            )
        )
        turnos = get_unique_values(dataframe_to_setor, REQUIRED_COLUMNS[1])

        estimated_jobs += len(turnos)

    return estimated_jobs
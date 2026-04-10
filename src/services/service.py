import logging as lg
from datetime import datetime
from os import getenv
from pathlib import Path

from src.helpers.helper import (
    applying_filters,
    check_colunas,
    export_to_excel,
    get_dataframe,
    get_unique_values,
    safe_name,
)
from src.models.export import Export
from src.models.filtro import Filtro

REQUIRED_COLUMNS = ["SETOR", "TURNO"]


def process_spreadsheet(path: Path) -> None:
    """
    Processa a planilha aplicando filtros por setor e turno,
    exportando um arquivo Excel por combinação.

    Args:
        path: Caminho da planilha de entrada.
    """
    logger = lg.getLogger(__name__)
    data_hoje = datetime.now().strftime("%d_%m_%Y")

    try:
        df = get_dataframe(path)
    except (ValueError, FileNotFoundError) as e:
        logger.error(e)
        return

    colunas = df.columns.tolist()
    try:
        for coluna in REQUIRED_COLUMNS:
            check_colunas(colunas, coluna)
            logger.info("Coluna '%s' encontrada", coluna)
    except ValueError as e:
        logger.error(e)
        return

    setores = get_unique_values(df, "SETOR")
    logger.info("Setores encontrados: %s", setores)

    for setor in setores:
        df_setor = applying_filters(Filtro(coluna="SETOR", dataframe=df, valor=setor))

        turnos = get_unique_values(df_setor, "TURNO")
        logger.info("Turnos para setor '%s': %s", setor, turnos)

        for turno in turnos:
            df_turno = applying_filters(
                Filtro(coluna="TURNO", dataframe=df_setor, valor=turno)
            )

            nome_arquivo = safe_name(f"Relatorio_{setor}_{turno}_{data_hoje}.xlsx")

            export_to_excel(
                Export(
                    dataframe=df_turno,
                    diretorio=Path(getenv("DIRETORIO_EXPORT")),
                    nome_arquivo=nome_arquivo,
                )
            )
            logger.info(
                "Exportado: Setor=%s, Turno=%s, Registros=%d",
                setor,
                turno,
                df_turno.shape[0],
            )

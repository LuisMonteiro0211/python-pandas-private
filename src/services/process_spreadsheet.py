import logging as lg
from datetime import datetime
from src.constants import REQUIRED_COLUMNS
from src.helpers.helper import (
    applying_filters,
    export_to_excel,
    get_unique_values,
    safe_name,
)
from src.exceptions import ProcessCancelled
from src.models.processcontext import ProcessContext
from src.models.export import Export
from src.models.filtro import Filtro
import pandas as pd

def process_spreadsheet(process_context: ProcessContext) -> None:
    """
    Processa a planilha aplicando filtros por setor e turno,
    exportando um arquivo Excel por combinação.

    Args:
        path: Caminho da planilha de entrada.
    """
    logger = lg.getLogger(__name__)
    data_hoje = datetime.now().strftime("%d_%m_%Y")

    setores = get_unique_values(process_context.safe_dataframe, REQUIRED_COLUMNS[0])
    logger.info("Setores encontrados: %s", setores)

    for setor in setores:
        filtered_to_setor = Filtro(coluna=REQUIRED_COLUMNS[0], dataframe=process_context.safe_dataframe, valor=setor) #Monta o filtro para o setor selecionado
        df_filtered_to_setor = applying_filters(filtered_to_setor) #Cria um novo DataFrame com os dados filtrados para o setor selecionado

        if process_context.cancel_event.is_set():
            raise ProcessCancelled()

        turnos = get_unique_values(df_filtered_to_setor, REQUIRED_COLUMNS[1]) #Filtra os turnos para o setor selecionado
        logger.info("Turnos para setor '%s': %s", setor, turnos)

        for turno in turnos:
            filtered_to_turno = Filtro(coluna=REQUIRED_COLUMNS[1], dataframe=df_filtered_to_setor, valor=turno)
            df_filtered_to_turno = applying_filters(filtered_to_turno) #Cria um novo DataFrame com os dados filtrados para o turno selecionado
            
            if process_context.cancel_event.is_set():
                raise ProcessCancelled()

            nome_arquivo = safe_name(f"Relatorio_{setor}_{turno}_{data_hoje}.xlsx")

            export_to_excel(
                Export(
                    dataframe=df_filtered_to_turno,
                    diretorio=process_context.diretorio_export,
                    nome_arquivo=nome_arquivo,
                )
            )
            logger.info(
                "Exportado: Setor=%s, Turno=%s, Registros=%d",
                setor,
                turno,
                df_filtered_to_turno.shape[0],
            )

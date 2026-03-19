from src.helpers.helper import (
    get_dataframe,
    get_colunas,
    check_colunas,
    get_setores,
    applying_filters,
    get_turnos,
    export_to_excel,
    safe_name,
    resolver_diretorio_export,
)
from src.models.filtro import Filtro
from src.models.export import Export
from datetime import datetime
from os import getenv
from pathlib import Path
import logging as lg


def process_spreadsheet(path: Path) -> None:
    """
    Processa a planilha aplicando filtros por setor e turno,
    exportando um arquivo Excel por combinação.

    Os arquivos são organizados em subpastas conforme as regras
    de agrupamento definidas em src/config/agrupamento.py:
      - Setores mapeados para um grupo vão para a subpasta do grupo.
      - Setores não mapeados ficam na raiz do diretório de exportação.

    Args:
        path: Caminho da planilha de entrada.
    """
    logger = lg.getLogger(__name__)
    data_hoje = datetime.now().strftime('%d_%m')
    diretorio_export = Path(getenv('DIRETORIO_EXPORT'))

    try:
        df = get_dataframe(path)
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"{e}")
        return

    colunas = get_colunas(df)
    try:
        check_colunas(colunas, 'SETOR')
        logger.info(f"Coluna 'SETOR' encontrada")
        check_colunas(colunas, 'TURNO')
        logger.info(f"Coluna 'TURNO' encontrada")
    except ValueError as e:
        logger.error(f"{e}")
        return

    setores = get_setores(df)
    logger.info(f"Setores encontrados: {setores}")

    for setor in setores:
        filtro_setor = Filtro(coluna='SETOR', dataframe=df, valor=setor)
        df_setor = applying_filters(filtro_setor)

        diretorio_destino = resolver_diretorio_export(diretorio_export, setor)

        turnos = get_turnos(df_setor)
        logger.info(f"Turnos para setor '{setor}': {turnos}")

        for i, turno in enumerate(turnos, start=1):
            filtro_turno = Filtro(coluna='TURNO', dataframe=df_setor, valor=turno)
            df_turno = applying_filters(filtro_turno)

            nome_arquivo_safe = safe_name(f"{setor}_{i}_{data_hoje}.xlsx")
            nome_pasta_safe = safe_name(setor)

            object_to_export = Export(
                dataframe=df_turno,
                diretorio=diretorio_destino,
                nome_arquivo=nome_arquivo_safe,
                nome_pasta=nome_pasta_safe,
            )
            export_to_excel(object_to_export)

            logger.info(
                f"Exportado: Setor={setor}, Turno={turno}, "
                f"Registros={df_turno.shape[0]}, "
                f"Destino={diretorio_destino / nome_arquivo_safe}"
            )

    logger.info("Processo finalizado com sucesso")

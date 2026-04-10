from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class Export:
    """
    Dados necessários para exportar um DataFrame para Excel.

    Args:
        dataframe: DataFrame a ser exportado.
        diretorio: Diretório de destino do arquivo.
        nome_arquivo: Nome do arquivo Excel (ex: ``relatorio.xlsx``).
    """

    dataframe: pd.DataFrame
    diretorio: Path
    nome_arquivo: str

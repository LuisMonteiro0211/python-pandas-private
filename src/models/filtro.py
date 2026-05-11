"""Modelo de filtro fatiado (coluna + valor) aplicado a um DataFrame."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class Filtro:
    """
    Representa um filtro a ser aplicado em um DataFrame.

    Args:
        coluna: Nome da coluna a ser filtrada.
        dataframe: DataFrame sobre o qual o filtro será aplicado.
        valor: Valor esperado na coluna para manter a linha.
    """

    coluna: str
    dataframe: pd.DataFrame
    valor: str
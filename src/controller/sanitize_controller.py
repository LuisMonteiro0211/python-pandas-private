"""Controller para sanitização de dados em thread separada."""

from pathlib import Path
import threading
import logging

import pandas as pd

from src.services.sanitize_dataframe import sanitize_dataframe
from src.helpers.helper import get_dataframe
from src.services.estimate_export_jobs import estimate_export_job_count

logger = logging.getLogger(__name__)


class SanitizeController(threading.Thread):
    """
    Controller (Thread) para carregar e sanitizar um DataFrame em background,
    sem travar a interface gráfica.

    Args:
        file_path: Caminho do arquivo Excel.

    Atributos após execução (chame .start() e .join() antes de ler):
        dataframe: DataFrame original carregado do Excel. É None apenas quando
            o próprio carregamento falhou. Útil para mostrar um preview ao
            usuário mesmo quando a sanitização falha.
        result: DataFrame sanitizado e pronto para uso. É None se a sanitização
            não foi executada ou falhou.
        error: Exceção capturada durante o processo. É None se tudo deu certo.

    Exemplo:
        >>> controller = SanitizeController(Path("planilha.xlsx"))
        >>> controller.start()
        >>> controller.join()
        >>> if controller.error is None:
        ...     usar_resultado(controller.result)
        ... elif controller.dataframe is not None:
        ...     mostrar_preview_com_alerta(controller.dataframe, controller.error)
        ... else:
        ...     mostrar_erro(controller.error)
    """
    def __init__(self, file_path: Path):
        """Inicializa o controller com o caminho do arquivo.
        
        Args:
            file_path: Caminho completo do arquivo Excel a ser processado.
        """
        super().__init__()
        self.file_path = file_path
        self.dataframe = None
        self.result = None
        self.error = None
        self.estimated_jobs = 0

    def run(self) -> None:
        """Executa a sanitização em thread separada.
        
        Carrega o DataFrame do arquivo, aplica sanitização e estima
        a quantidade de jobs de exportação. Qualquer erro é capturado
        e armazenado em self.error.
        """

        try:
            dataframe: pd.DataFrame = get_dataframe(self.file_path)
            self.dataframe = dataframe

        except ValueError as e:
            self.error = ValueError(f"Erro ao ler o arquivo {self.file_path}: {e}")
            logger.error(f"Erro ao ler o arquivo {self.file_path}: {e}")
            return
        except FileNotFoundError as e:
            self.error = FileNotFoundError(f"Arquivo {self.file_path} não encontrado {e}")
            logger.error(f"Arquivo {self.file_path} não encontrado: {e}")
            return

        try:
            dataframe: pd.DataFrame = sanitize_dataframe(dataframe)
            self.estimated_jobs = estimate_export_job_count(dataframe)
            self.result = dataframe
        except (ValueError, TypeError) as e:
            self.error = ValueError(f"Erro ao sanitizar o DataFrame: {e}")
            logger.error(f"Erro ao sanitizar o DataFrame: {e}")
            return
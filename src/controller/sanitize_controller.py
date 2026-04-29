from src.services.sanitize_dataframe import sanitize_dataframe
from src.helpers.helper import get_dataframe
import pandas as pd
import threading
from pathlib import Path

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
        super().__init__()
        self.file_path = file_path
        self.dataframe = None
        self.result = None
        self.error = None

    def run(self) -> None:

        try:
            dataframe: pd.DataFrame = get_dataframe(self.file_path)
            self.dataframe = dataframe

        except ValueError as e:
            self.error = ValueError(f"Erro ao ler o arquivo {self.file_path}: {e}")
            return
        except FileNotFoundError as e:
            self.error = FileNotFoundError(f"Arquivo {self.file_path} não encontrado {e}")
            return

        try:
            dataframe: pd.DataFrame = sanitize_dataframe(dataframe)
            self.result = dataframe
        except (ValueError, TypeError) as e:
            self.error = ValueError(f"Erro ao sanitizar o DataFrame: {e}")
            return
"""Ponto de entrada da interface gráfica (CustomTkinter).

Executa :class:`src.gui.app.App` e inicia o loop principal do Tk.
Uso: ``python run_gui.py`` a partir da raiz do repositório (com o venv ativo).
"""

from src.gui.app import App
from src.utils import setup_environment
from src.utils.logger_config import setup_logger

if __name__ == "__main__":
    setup_environment()
    setup_logger()
    app = App()
    app.mainloop()

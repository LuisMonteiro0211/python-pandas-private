"""
Componente ProgressBar.

Barra de progresso visual usada para indicar o andamento de operações
demoradas (ex: processamento de planilhas, exportação).

Uso:
    from src.gui.components import ProgressBar

    self.progress = ProgressBar(parent)
    self.progress.pack(fill="x", padx=10, pady=5)

    # Em algum handler (concluídos, total):
    self.progress.update_progress(3, 10)  # 3 de 10 itens
    self.progress.reset_progress()        # volta a zero
"""

from customtkinter import CTkProgressBar, CTkFrame
from src.gui.theme import COLORS
import customtkinter as ctk


class ProgressBar(CTkFrame):
    """Barra de progresso horizontal estilizada com o tema.

    A barra trabalha internamente com valores de 0.0 a 1.0 (padrão do
    CTkProgressBar). A API pública recebe itens concluídos e total.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._percent: float = 0
        self._configure_appearance()
        self._build_progressbar()
        self._layout()
        self.reset_progress()

    def _configure_appearance(self):
        self.configure(
            fg_color=COLORS.frame_transparent,
            width=500,
            height=20,
        )

    def _build_progressbar(self):
        self._progressbar = CTkProgressBar(
            self,
            progress_color="GREEN",
        )

    def _layout(self):
        self._progressbar.pack(expand=True, fill=ctk.BOTH, padx=10, pady=10)

    def update_progress(self, completed: int, total: int) -> None:
        """Atualiza a barra com base em itens concluídos e total previsto.

        Args:
            completed: Quantidade já processada (>= 0).
            total: Quantidade total de itens; se <= 0, a barra fica em 0.
        """
        if total <= 0:
            self._percent = 0.0
            self._progressbar.set(0.0)
            return
            
        ratio = max(0.0, min(1.0, completed / total))
        self._percent = ratio * 100.0
        self._progressbar.set(ratio)

    def reset_progress(self) -> None:
        """Volta a barra ao estado inicial (0%)."""
        self._percent = 0
        self._progressbar.set(0)

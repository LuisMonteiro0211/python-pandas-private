"""
Componente ProgressBar.

Barra de progresso visual usada para indicar o andamento de operações
demoradas (ex: processamento de planilhas, exportação).

Uso:
    from src.gui.components import ProgressBar

    self.progress = ProgressBar(parent)
    self.progress.pack(fill="x", padx=10, pady=5)

    # Em algum handler:
    self.progress.update_progress(50)  # 50% completo
    self.progress.reset_progress()     # volta a zero
"""

from customtkinter import CTkProgressBar, CTkFrame
from src.gui.theme import COLORS
import customtkinter as ctk


class ProgressBar(CTkFrame):
    """Barra de progresso horizontal estilizada com o tema.

    A barra trabalha internamente com valores de 0.0 a 1.0 (padrão do
    CTkProgressBar), mas a API pública (update_progress) usa o range
    mais intuitivo de 0 a 100.
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

    def update_progress(self, percent: float) -> None:
        """Atualiza a barra para a porcentagem informada.

        Args:
            percent: Porcentagem (0 a 100) do progresso atual.
                Valores fora desse range são repassados ao
                CTkProgressBar sem validação.
        """
        self._percent = max(0, min(100, percent))
        self._progressbar.set(self._percent / 100)

    def reset_progress(self) -> None:
        """Volta a barra ao estado inicial (0%)."""
        self._percent = 0
        self._progressbar.set(0)

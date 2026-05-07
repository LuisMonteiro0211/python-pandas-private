"""
Componente Sidebar.

Barra lateral fixa da aplicação, atualmente reservada como espaço
visual para futuros botões/menus de navegação.

Uso:
    from src.gui.components import Sidebar

    self.sidebar = Sidebar(parent)
    self.sidebar.pack(side="left", fill="y")
"""

from customtkinter import CTkFrame
from src.gui.theme import COLORS


class Sidebar(CTkFrame):
    """Barra lateral fixa de 100px com fundo e borda do tema.

    Não tem conteúdo próprio no momento — serve como container visual
    e pode receber botões/menus em futuras iterações.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._configure_appearance()

    def _configure_appearance(self):
        self.configure(
            fg_color=COLORS.sidebar_background,
            width=100,
        )
        self._border_color = COLORS.sidebar_border
        self._border_width = 1
        self.pack_propagate(False)

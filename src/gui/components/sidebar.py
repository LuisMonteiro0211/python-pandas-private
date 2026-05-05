from customtkinter import CTkFrame
from src.gui.theme import COLORS


class Sidebar(CTkFrame):
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

"""
Componente Header.
Contém os botões de carregar arquivo e exportar para.

Uso:
    from src.gui.components import Header
    self.header = Header(parent)
    self.header.pack(fill=ctk.X, padx=10, pady=8)
"""

from typing import Callable
from customtkinter import CTkFrame, CTkButton
from src.gui.theme import COLORS, FONTS
import customtkinter as ctk


class Header(CTkFrame):
    """
    Componente Header.
    Contém os botões de carregar arquivo e exportar para.

    A classe contém dois botões: Carregar Arquivo e Exportar para.
    Os botões são estilizados com o tema da aplicação.
    Os botões são posicionados lado a lado.
    Os botões são responsáveis por executar as ações de carregar arquivo e exportar para.
    """

    def __init__(self, parent, on_load_file: Callable, on_export: Callable):
        super().__init__(parent)
        self._on_load_file = on_load_file
        self._on_export = on_export
        self._configure_appearance()
        self._build()

    def _configure_appearance(self):
        self.configure(
            fg_color = COLORS.frame_transparent,
            width = 500,
            height = 50,
            corner_radius = 0,
        )

    def _build(self):
        self._build_load_file_button()
        self._build_export_button()
        self._layout()

    def _build_load_file_button(self):
        self._load_file_button = CTkButton(
            self,
            text = "Carregar Arquivo",
            fg_color = COLORS.button_background,
            hover_color = COLORS.button_hover,
            text_color = COLORS.button_text,
            border_width = 1,
            border_color = COLORS.button_border,
            font = ctk.CTkFont(family = FONTS.button_family, size = FONTS.button_size, weight = FONTS.button_weight),
            command = self._on_load_file,
        )

    def _build_export_button(self):
        self._export_button = CTkButton(
            self,
            text = "Exportar para",
            fg_color = COLORS.button_background,
            hover_color = COLORS.button_hover,
            text_color = COLORS.button_text,
            border_width = 1,
            border_color = COLORS.button_border,
            font = ctk.CTkFont(family = FONTS.button_family, size = FONTS.button_size, weight = FONTS.button_weight),
            command = self._on_export,
        )

    def _layout(self):
        self._load_file_button.pack(side = ctk.LEFT, padx = (0, 5))
        self._export_button.pack(side = ctk.LEFT, padx = (20, 0))
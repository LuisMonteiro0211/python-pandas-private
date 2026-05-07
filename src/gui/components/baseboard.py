"""
Componente Baseboard.

Contém os botões de processar e cancelar

Uso:
    from src.gui.components import Baseboard
    self.baseboard = Baseboard(parent)
    self.baseboard.pack(fill=ctk.X, padx=10, pady=8)

"""

from typing import Callable

from customtkinter import CTkFrame, CTkButton
from src.gui.theme import COLORS, FONTS
import customtkinter as ctk


class Baseboard(CTkFrame):
    """Contém os botões de processar e cancelar
    
    A classe contém dois botões: Processar e Cancelar.
    Os botões são estilizados com o tema da aplicação.
    Os botões são posicionados lado a lado.
    Os botões são responsáveis por executar as ações de processar e cancelar.
    """

    def __init__(self, parent, on_process: Callable, on_cancel: Callable):
        super().__init__(parent)
        self._configure_appearance()
        self._on_process = on_process
        self._on_cancel = on_cancel
        self._build()

    def _configure_appearance(self):
        self.configure(
          fg_color = COLORS.footer_background,
          width = 500,
          height = 50,
          corner_radius = 0,
        )

    def _build(self):
        self._build_frame_buttons()
        self._build_process_button()
        self._build_cancel_button()
        self._layout()
    
    def _build_frame_buttons(self):
        self._frame_buttons = CTkFrame(
            self,
            fg_color = COLORS.frame_transparent,
        )

    def _build_process_button(self):
        self._process_button = CTkButton(
            self._frame_buttons,
            text = "Processar",
            fg_color=COLORS.button_background,
            hover_color=COLORS.button_hover,
            text_color=COLORS.button_text,
            border_width=1,
            border_color=COLORS.button_border,
            font=ctk.CTkFont(family=FONTS.button_family, size=FONTS.button_size, weight=FONTS.button_weight)
        )
        self._process_button.configure(command=self._on_process)

    def _build_cancel_button(self):
        self._cancel_button = CTkButton(
            self._frame_buttons,
            text = "Cancelar",
            fg_color=COLORS.button_background,
            hover_color=COLORS.button_hover,
            text_color=COLORS.button_text,
            border_width=1,
            border_color=COLORS.button_border,
            font=ctk.CTkFont(family=FONTS.button_family, size=FONTS.button_size, weight=FONTS.button_weight)
        )
        self._cancel_button.configure(command=self._on_cancel)

    def _layout(self):
        self._frame_buttons.pack(fill=ctk.X, padx=10, pady=8)
        self._frame_buttons.pack_propagate(False)
        self._process_button.pack(side=ctk.RIGHT, padx=(0, 10))
        self._cancel_button.pack(side=ctk.LEFT, padx=(10, 0))
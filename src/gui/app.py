"""Módulo da janela principal da aplicação."""

import customtkinter as ctk

from src.gui.app_controller import AppController
from src.gui.components import DataTable, Sidebar, ProgressBar, Baseboard, Header
from src.gui.theme import COLORS


class App(ctk.CTk):
    """Janela principal da aplicação Python Pandas Analyzer.
    
    Monta todos os componentes visuais (sidebar, header, tabela, barra de
    progresso e rodapé) e delega a lógica de controle para AppController.
    
    A janela é fixa em 500x400px e não pode ser redimensionada.
    
    Attributes:
        controller: Instância de AppController que gerencia a lógica.
        sidebar: Barra lateral visual.
        meio: Container central que contém header, tabela e progresso.
        header: Cabeçalho com botões de ação.
        tabela: Tabela de visualização de dados.
        barra_de_progresso: Barra de progresso do processamento.
        baseboard: Rodapé com botões de processamento.
    
    Example:
        >>> app = App()
        >>> app.mainloop()
    """
    
    def __init__(self):
        super().__init__()
        self._configurar_tela()
        self.controller = AppController(self)
        self._configurar_widgets()

    def _configurar_tela(self):
        self.title("Python Pandas Analyzer")
        self.geometry("500x400")
        self.configure(fg_color=COLORS.app_background)
        self.resizable(False, False)

    def _configurar_widgets(self):
        self._criar_sidebar()
        self._criar_meio()
        self._criar_header()
        self._criar_tabela()
        self._criar_barra_de_progresso()
        self._criar_rodape()

    def _criar_sidebar(self):
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)

    def _criar_meio(self):
        self.meio = ctk.CTkFrame(
            self,
            width=500,
            height=400,
            fg_color=COLORS.center_background,
            corner_radius=10,
        )

        self.meio.pack(side=ctk.LEFT, fill=ctk.Y)
        self.meio.pack_propagate(False)

    def _criar_header(self):
        self.header = Header(
            self.meio,
            on_load_file=self.controller.on_load_file,
            on_export=self.controller.on_export,
        )
        self.header.pack(fill=ctk.X, padx=10, pady=8)
        self.header.pack_propagate(False)

    def _criar_tabela(self):
        self.tabela = DataTable(self.meio)
        self.tabela.pack(padx=5, pady=5)

    def _criar_barra_de_progresso(self):
        self.barra_de_progresso = ProgressBar(self.meio)
        self.barra_de_progresso.pack(padx=5, pady=5)

    def _criar_rodape(self):
        self.baseboard = Baseboard(
            self.meio,
            on_process=self.controller.on_process,
            on_cancel=self.controller.on_cancel,
        )
        self.baseboard.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.baseboard.pack_propagate(False)


if __name__ == "__main__":
    app = App()
    app.mainloop()

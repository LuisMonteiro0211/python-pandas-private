from customtkinter import CTkFrame
from tkinter import ttk
from src.gui.theme import COLORS
import pandas as pd

class DataTable(CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self._dataframe = None
        self._configure_appearance()
        self._build()

    def _configure_appearance(self):
        self.configure(
            fg_color = COLORS.table_background,
            width = 360,
            height = 250,
        )
        self.pack_propagate(False)

    def _build(self):
        self._build_treeview()
        self._build_scrollbars()
        self._layout()
    
    def _build_treeview(self):
        self._treeview = ttk.Treeview(
            self,
            show="headings",
            height=10
        )

    def _build_scrollbars(self):

        self._horizontal_scrollbar_frame = CTkFrame(
            self,
            width=360,
            height=20,
            fg_color=COLORS.frame_transparent
        )

        self._vertical_scrollbar_frame = CTkFrame(
            self,
            width=20,
            height=230,
            fg_color=COLORS.frame_transparent
        )

        self._vertical_scrollbar = ttk.Scrollbar(
            self._vertical_scrollbar_frame,
            orient="vertical",
            command=self._treeview.yview
        )

        self._horizontal_scrollbar = ttk.Scrollbar(
            self._horizontal_scrollbar_frame,
            orient="horizontal",
            command=self._treeview.xview
        )

        self._treeview.configure(
            yscrollcommand=self._vertical_scrollbar.set,
            xscrollcommand=self._horizontal_scrollbar.set
        )

    def _layout(self):
        self._horizontal_scrollbar_frame.pack(
            side="bottom",
            fill="x"
        )

        self._vertical_scrollbar_frame.pack(
            side="right",
            fill="y"
        )

        self._horizontal_scrollbar.pack(
            side="bottom",
            fill="x",
            padx=2
        )

        self._vertical_scrollbar.pack(
            side="right",
            fill="y",
            padx=5
        )

        self._treeview.pack(
            side="left",
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )
    
    def update_data(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe
        self._render()
    
    def clear(self):
        self._dataframe = None
        self._clear_rows()

    def _clear_rows(self):
        for row in self._treeview.get_children():
            self._treeview.delete(row)

    def _configure_columns(self):
        columns = self._dataframe.columns.tolist()
        self._treeview["columns"] = columns

        for column in columns:
            self._treeview.heading(column, text=column)
            self._treeview.column(column, width=140, anchor="center", stretch=False)

    def _insert_rows(self):
        for row in self._dataframe.itertuples(index=False):
            self._treeview.insert("", "end", values=list(row))
    
    def _render(self):
        self._clear_rows()

        if self._dataframe is None:
            return

        self._configure_columns()
        self._insert_rows()


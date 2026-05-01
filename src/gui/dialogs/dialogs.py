"""
Módulo com funções que abrem janelas do SO ou popups.

Uso:
    from src.gui.dialogs import ask_excel_file, ask_save_directory, show_error, show_success, confirm

    excel_path = ask_excel_file()
    save_directory = ask_save_directory()
    show_error("Erro ao carregar arquivo")
    show_success("Arquivo carregado com sucesso")
    confirm("Deseja continuar?")
"""


from pathlib import Path
from tkinter import filedialog, messagebox
import os

def ask_excel_file(parent=None) -> Path | None:
    """
    Abre um diálogo para selecionar um arquivo Excel.

    Args:
        parent: Widget pai para o diálogo.

    Returns:
        Path do arquivo selecionado ou None se o usuário cancelar.
    """
    excel_path = filedialog.askopenfilename(
        title="Selecione o arquivo",
        filetypes=[("Excel files", "*.xlsx *.xls")],
        initialdir=os.path.expanduser("~"),
        parent=parent,
    )
    return Path(excel_path) if excel_path else None

def ask_save_directory(parent=None) -> Path | None:
    """
    Abre um diálogo para selecionar um diretório de exportação.

    Args:
        parent: Widget pai para o diálogo.

    Returns:
        Path do diretório selecionado ou None se o usuário cancelar.
    """
    directory = filedialog.askdirectory(
        title="Selecione a pasta de exportação",
        initialdir=os.path.expanduser("~"),
        parent=parent,
    )
    return Path(directory) if directory else None

def show_error(message: str, title: str = "Erro") -> None:
    """
    Mostra uma mensagem de erro.

    Args:
        message: Mensagem de erro.
        title: Título da mensagem.
    """
    messagebox.showerror(title, message)

def show_success(message: str, title: str = "Sucesso") -> None:
    """
    Mostra uma mensagem de sucesso.

    Args:
        message: Mensagem de sucesso.
        title: Título da mensagem.
    """
    messagebox.showinfo(title, message)

def confirm(message: str, title: str = "Confirmar") -> bool:
    """
    Mostra uma mensagem de confirmação.

    Args:
        message: Mensagem de confirmação.
        title: Título da mensagem.
    
    Returns:
        True se o usuário confirmar, False caso contrário.
    """
    return messagebox.askyesno(title, message)
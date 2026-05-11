"""
Tema visual do projeto.

Centraliza cores, fontes e configurações de aparência. Toda a UI deve
importar daqui em vez de usar valores hardcoded — assim, mudar o tema
exige editar apenas este arquivo.

Uso:
    from src.gui.theme import COLORS, FONTS, SETTINGS

    ctk.CTkButton(
        parent,
        text="Carregar",
        fg_color=COLORS.button_background,
        hover_color=COLORS.button_hover,
        text_color=COLORS.button_text,
        font=ctk.CTkFont(
            family=FONTS.button_family,
            size=FONTS.button_size,
            weight=FONTS.button_weight,
        ),
    )
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    """Paleta de cores nomeada por uso semântico (não pela cor em si)."""

    # Backgrounds principais (do mais externo ao mais interno)
    app_background: str = "#212121"
    sidebar_background: str = "#1d1d1c"
    center_background: str = "#1f1f1e"
    table_background: str = "#2c2c2a"
    footer_background: str = "#2e2e2d"

    # Frames/containers sem cor própria (transparentes)
    frame_transparent: str = "transparent"

    # Botões
    button_background: str = "#383836"
    button_hover: str = "#2e2e2d"
    button_text: str = "#fff"
    button_border: str = "#3b3b38"

    # Bordas gerais
    sidebar_border: str = "#3b3b38"
    table_border: str = "#313130"


@dataclass(frozen=True)
class Fonts:
    """Definições de fonte por uso. Combine os campos ao instanciar CTkFont."""

    # Fonte usada nos botões da interface
    button_family: str = "Monospace"
    button_size: int = 12
    button_weight: str = "bold"


@dataclass(frozen=True)
class Settings:
    """Configurações globais de aparência da aplicação."""

    # Modo de cor do customtkinter: "dark", "light" ou "system"
    appearance_mode: str = "dark"


# Instâncias prontas para importar.
# Quem usar o tema deve importar COLORS / FONTS / SETTINGS, não as classes.
COLORS = Colors()
FONTS = Fonts()
SETTINGS = Settings()

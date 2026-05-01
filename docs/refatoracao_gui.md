# Refatoração da GUI — Guia Completo

> Material de estudo e consulta sobre como organizar uma interface gráfica em
> camadas bem definidas, usando o `App` do projeto como caso de estudo.
>
> Este documento NÃO precisa ser executado de uma vez. Use como referência:
> leia uma seção, aplique, volte.

---

## Sumário

1. [Por que GUIs viram bagunça](#1-por-que-guis-viram-bagunça)
2. [Vocabulário e analogia da casa](#2-vocabulário-e-analogia-da-casa)
3. [Critérios de decisão (regras de bolso)](#3-critérios-de-decisão-regras-de-bolso)
4. [Theme — o figurino da aplicação](#4-theme--o-figurino-da-aplicação)
5. [Components — os cômodos da casa](#5-components--os-cômodos-da-casa)
6. [Dialogs — a porta de entrada](#6-dialogs--a-porta-de-entrada)
7. [Application Controller — o morador](#7-application-controller--o-morador)
8. [Ciclo de vida de um clique](#8-ciclo-de-vida-de-um-clique)
9. [Padrões clássicos (MVC, MVP, MVVM)](#9-padrões-clássicos-mvc-mvp-mvvm)
10. [Plano em fases](#10-plano-em-fases)
11. [Estrutura final esperada](#11-estrutura-final-esperada)
12. [Filtros pra fixar (resumão)](#12-filtros-pra-fixar-resumão)

---

## 1. Por que GUIs viram bagunça

Toda interface gráfica mistura naturalmente **3 fontes de complexidade diferentes**:

| Fonte | Exemplo | Muda com... |
|---|---|---|
| 🎨 **Aparência** | Cores, fontes, layout | Designer, marca, tema dark/light |
| 🔄 **Comportamento** | "O que acontece quando clica" | Regras de negócio, novas features |
| 🧠 **Estado** | Dados sendo exibidos, progresso | Ações do usuário, respostas de I/O |

Quando tudo está numa classe só, qualquer mudança em **uma das três** te obriga a mexer no mesmo arquivo. Pior: você arrisca quebrar as outras duas sem perceber.

**Meta da refatoração**: separar essas três fontes em lugares diferentes, pra que cada mudança fique isolada numa "caixa".

### Diagnóstico atual da `App`

A classe `src/gui/app.py::App` mistura **8 responsabilidades**:

1. Configurar a janela principal.
2. Construir o sidebar.
3. Construir o header (botões superiores).
4. Construir a tabela (Treeview + scrollbars).
5. Construir a barra de progresso.
6. Construir o rodapé.
7. Gerenciar diálogos do SO (file picker, popups).
8. Orquestrar chamadas aos controllers.

Sintomas:
- Cores e fontes duplicadas em 4+ botões.
- Funções `_criar_*` longas (30+ linhas cada).
- Difícil saber "onde mexer" pra mudar uma coisa específica.
- Toda mudança no fluxo de eventos passa pela `App`.

---

## 2. Vocabulário e analogia da casa

| Termo | Analogia | Função |
|---|---|---|
| **View** | A planta da casa | Diz onde cada cômodo fica |
| **Component** | Cada cômodo (cozinha, banheiro) | Faz uma coisa específica, autônomo |
| **Theme** | Padrão de decoração | Cores, materiais usados em todos os cômodos |
| **Dialogs** | Porta de entrada | Interface entre a casa e o mundo externo |
| **Application Controller** | O morador | Decide o que fazer e quando |
| **Service** (já existe) | Manual de procedimentos | Regras de "como fazer cada coisa" |
| **Controller de Thread** (já existe) | Funcionário terceirizado | Faz tarefas longas em paralelo |

Cada um cumpre **um papel único**. Esse é o coração do **Single Responsibility Principle** aplicado à GUI:

> **Uma classe deve ter UM único motivo pra mudar.**

---

## 3. Critérios de decisão (regras de bolso)

Quando bater dúvida ("isso vale a pena extrair?"), passe por essa checklist:

| Critério | Pergunta | Se sim... |
|---|---|---|
| **Coesão** | Várias linhas existem só pra fazer UMA coisa juntas? | Vira componente |
| **Tamanho** | Bloco passa de ~30-50 linhas? | Quebra em algo menor |
| **Reutilização** | Vou usar isso em outra tela/contexto? | Vira componente |
| **Estado próprio** | Tem variáveis internas que evoluem? | Vira **classe** |
| **Sem estado** | Só recebe input e devolve output? | Vira **função** num módulo |
| **Acoplamento** | Posso mudar isso sem mexer no resto? | Já é um componente disfarçado |
| **Testabilidade** | Quero testar isso isolado? | Vira componente |
| **Domínio diferente** | Lida com tipo diferente de problema? | Vira módulo separado |

### A regra mestra (3 perguntas)

| Pergunta | Se "sim" | Resultado |
|---|---|---|
| Tem **estado** que evolui ao longo do tempo? | sim | **Classe** |
| Só recebe input e devolve output? | sim | **Função** num módulo |
| São apenas valores fixos? | sim | **Constantes** num módulo |

---

## 4. Theme — o figurino da aplicação

### O que é
Arquivo único com **constantes** (cores, fontes, tamanhos) usado por toda a UI.

### Por que existe (problema atual)

```python
# Botão "Carregar Arquivo"
fg_color="#383836",
hover_color="#2e2e2d",
text_color="#fff",
border_width=1,
border_color="#3b3b38",
font=ctk.CTkFont(family="Monospace", size=12, weight="bold")

# Botão "Exportar para" → mesma coisa, duplicado
# Botão "Gerar" → mesma coisa, duplicado
# Botão "Cancelar" → mesma coisa, duplicado
```

**Quatro botões idênticos**, configurados manualmente em quatro lugares.

Pergunta inevitável: *"E se o cliente disser: 'mude o azul pra cinza'?"*

- Hoje: edita 4 lugares. Esquecer um = inconsistência visual.
- Com `theme.py`: edita 1 lugar. Garantido.

### Por que NÃO é classe

Não há **comportamento**, não há **estado mutável**. São valores fixos. Forçar uma classe seria criar `Theme()` só pra agrupar atributos — desperdício.

### Anatomia (3 padrões)

#### Padrão A: constantes soltas (mais simples)
```python
# theme.py
PRIMARY_BG = "#212121"
BUTTON_BG = "#383836"
BUTTON_HOVER = "#2e2e2d"
BORDER = "#3b3b38"
TEXT_LIGHT = "#fff"

FONT_BUTTON = ("Monospace", 12, "bold")
```

#### Padrão B: dicionários (organização agrupada)
```python
COLORS = {
    "background": "#212121",
    "button_bg": "#383836",
    "button_hover": "#2e2e2d",
}

FONTS = {
    "button": ("Monospace", 12, "bold"),
}
```

#### Padrão C: dataclass frozen (recomendado)
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Colors:
    background: str = "#212121"
    button_bg: str = "#383836"
    button_hover: str = "#2e2e2d"
    border: str = "#3b3b38"
    text: str = "#fff"

COLORS = Colors()
```

**Vantagens do C**:
- IDE autocompleta (`COLORS.button_bg`).
- `frozen=True` impede mudança em runtime (segurança).

### Pegadinha: cores semânticas vs brutas

| ❌ Brutas | ✅ Semânticas |
|---|---|
| `GRAY_383836 = "#383836"` | `BUTTON_BG = "#383836"` |
| `BLUE_007BFF = "#007BFF"` | `PRIMARY_ACTION = "#007BFF"` |

**Nomeie pelo uso, não pela cor.** Senão, no dia que trocar o cinza por azul, vai ter um `BLUE` chamado `GRAY` no código.

---

## 5. Components — os cômodos da casa

### O que é
Uma **classe que herda de `CTkFrame`** e encapsula um pedaço visual completo: widgets internos, estado próprio, métodos públicos.

### As 3 fronteiras de um component

```
┌─────────────────────────────────────┐
│  COMPONENT                          │
│                                     │
│  ENTRADA: parâmetros + métodos      │
│  ────────────────────────────────   │
│  INTERNO: widgets + estado próprio  │
│  ────────────────────────────────   │
│  SAÍDA: callbacks + eventos         │
└─────────────────────────────────────┘
```

- **Entrada**: como o mundo externo "fala" com o component (`update_data(df)`).
- **Interno**: estado e widgets que ninguém de fora vê.
- **Saída**: como o component avisa o mundo externo (callbacks).

### Por que isso muda tudo

#### Antes: a `App` sabe demais
```python
class App(ctk.CTk):
    def _criar_tabela(self):
        self.tabela = ctk.CTkFrame(...)
        self.treeview = ttk.Treeview(...)         # ← App conhece
        vertical_scrollbar = ttk.Scrollbar(...)   # ← App conhece
        # ... 50 linhas de detalhes internos
```

A `App` está acoplada a TUDO sobre a tabela. Trocar `Treeview` por outra biblioteca = rasgar a `App`.

#### Depois: a `App` só monta peças
```python
class App(ctk.CTk):
    def _build(self):
        self.data_table = DataTable(self)  # ← App não sabe NADA do interior
        self.data_table.pack(fill="both", expand=True)
```

A `App` agora trata `DataTable` como caixa-preta.

### Template universal de um Component

```python
import customtkinter as ctk
from src.gui.theme import COLORS

class MeuComponent(ctk.CTkFrame):
    """O que esse componente faz, em uma linha."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS.background, **kwargs)
        self._dados = None
        self._build()

    def _build(self):
        """Cria e posiciona widgets internos. Chamado UMA vez."""
        ...

    def atualizar(self, dados):
        """Método público — a 'API' do componente."""
        self._dados = dados
        self._refresh()

    def _refresh(self):
        """Lógica privada de re-renderização."""
        ...
```

**Convenções**:
- `_metodo()` com underscore = privado, ninguém de fora chama.
- `metodo()` sem underscore = público, é a interface.
- Estado em `self._x` (com underscore) = não acesse direto de fora.

### Aplicando aos seus componentes

#### `DataTable` — caso mais claro
- **Estado**: dataframe atual, configuração de colunas.
- **Entrada**: `update_data(df)`, `clear()`.
- **Saída**: nenhuma por enquanto (futuro: `on_row_selected`).

```python
class DataTable(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._dataframe = None
        self._build()

    def update_data(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe
        self._clear()
        self._render(dataframe)
```

#### `ProgressBar` — exemplo com estado rico
```python
class ProgressBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._percent = 0
        self._message = ""
        self._build()

    def update(self, percent: float, message: str = ""):
        self._percent = max(0, min(100, percent))
        self._message = message
        self._refresh()

    def reset(self):
        self.update(0, "")

    def is_complete(self) -> bool:
        return self._percent >= 100
```

#### `Header` — exemplo com **callbacks de saída**

Aqui está o segredo da comunicação:

```python
from typing import Callable

class Header(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_load_file: Callable[[], None],   # ← callback recebido
        on_export: Callable[[], None],
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self._on_load_file = on_load_file
        self._on_export = on_export
        self._build()

    def _build(self):
        self.btn_load = ctk.CTkButton(
            self,
            text="Carregar Arquivo",
            command=self._on_load_file,  # ← repassa o callback
            ...
        )
```

**Princípio fundamental**: o `Header` NÃO sabe o que acontece quando o botão é clicado. Ele só **avisa** quem o criou. Quem decide é o `AppController`.

> Componentes **emitem eventos**, não **executam lógica de negócio**.

### Vantagem prática do desacoplamento

Amanhã quer um popup de confirmação antes de "Carregar"? Hoje, mexeria no botão. Com callback, só **substitui o callback**:

```python
# Antes
Header(self, on_load_file=self.upload_direto)

# Depois (Header intocado)
Header(self, on_load_file=self.upload_com_confirmacao)
```

---

## 6. Dialogs — a porta de entrada

### O que é
Um **módulo (não classe!)** com funções que abrem janelas do SO ou popups.

### Por que NÃO é classe

| Pergunta | Diálogos |
|---|---|
| Tem estado interno? | ❌ Não |
| Tem ciclo de vida? | ❌ Não |
| Cada chamada é independente? | ✅ Sim |
| É operação transacional? | ✅ Sim |

Forçar uma classe aqui = "singleton fingido", antipadrão.

### Anatomia

```python
# src/gui/dialogs.py
from pathlib import Path
from tkinter import filedialog, messagebox
import os

def ask_excel_file(parent=None) -> Path | None:
    path = filedialog.askopenfilename(
        title="Selecione o arquivo",
        filetypes=[("Excel files", "*.xlsx *.xls")],
        initialdir=os.path.expanduser("~"),
        parent=parent,
    )
    return Path(path) if path else None

def ask_save_directory(parent=None) -> Path | None:
    directory = filedialog.askdirectory(
        title="Selecione o diretório de exportação",
        initialdir=os.path.expanduser("~"),
        parent=parent,
    )
    return Path(directory) if directory else None

def show_error(message: str, title: str = "Erro"):
    messagebox.showerror(title, message)

def show_success(message: str, title: str = "Sucesso"):
    messagebox.showinfo(title, message)

def confirm(message: str, title: str = "Confirmar") -> bool:
    return messagebox.askyesno(title, message)
```

### Vantagem oculta: testes

```python
from unittest.mock import patch

@patch("src.gui.dialogs.ask_excel_file", return_value=Path("teste.xlsx"))
def test_handle_upload(mock_ask):
    controller = AppController(view=MockView())
    controller.handle_upload()
    mock_ask.assert_called_once()
```

Você simula o usuário escolhendo arquivo **sem abrir janela nenhuma**.

---

## 7. Application Controller — o morador

### O problema que resolve

Hoje a `App` faz duas coisas conflitantes:
1. **Construir a UI** (botões, frames, layout).
2. **Decidir o que fazer quando o usuário clica** (chamar controllers, atualizar tabela).

| Responsabilidade | Muda com... |
|---|---|
| Construir UI | Mudanças de layout, design |
| Decidir comportamento | Mudanças de regras, novos fluxos |

Misturar = mudança de regra mexe em código de layout. Anti-SRP.

### A solução: separar em duas classes

```python
class App(ctk.CTk):
    """Só monta a UI. Não sabe NADA sobre fluxo."""
    def __init__(self):
        super().__init__()
        self.controller = AppController(view=self)
        self._build()

    def _build(self):
        self.header = Header(
            self,
            on_load_file=self.controller.handle_load_file,  # ← delega
            on_export=self.controller.handle_export_setup,
        )
        self.data_table = DataTable(self)
        self.progress = ProgressBar(self)
        self.footer = Footer(
            self,
            on_generate=self.controller.handle_generate,
            on_cancel=self.controller.handle_cancel,
        )


class AppController:
    """Sabe o fluxo da aplicação. Não sabe NADA sobre widgets específicos."""
    def __init__(self, view: App):
        self.view = view

    def handle_load_file(self):
        file_path = dialogs.ask_excel_file(self.view)
        if file_path is None:
            return

        sanitize = SanitizeController(file_path)
        sanitize.start()
        sanitize.join()

        if sanitize.error is None:
            self.view.data_table.update_data(sanitize.result)
            dialogs.show_success("Planilha carregada com sucesso!")
        elif sanitize.dataframe is not None:
            self.view.data_table.update_data(sanitize.dataframe)
            dialogs.show_error(
                f"Carregou, mas há problemas:\n\n{sanitize.error}\n\n"
                "Confira o preview e corrija o arquivo."
            )
        else:
            dialogs.show_error(f"Não foi possível carregar:\n\n{sanitize.error}")
```

### Regra de ouro

> **A View NÃO conhece os controllers de thread.**
> **O AppController NÃO conhece os widgets específicos** (só os componentes públicos).

### Camadas estanques

```
┌──────────────────────────────────────────────────┐
│  VIEW (App + Components)                         │
│  Só sabe: "como desenhar e como avisar"          │
│  Conhece: customtkinter, layout, theme           │
│  NÃO conhece: SanitizeController, services       │
└─────────────────┬────────────────────────────────┘
                  │ callbacks (eventos)
                  ▼
┌──────────────────────────────────────────────────┐
│  APPLICATION CONTROLLER                          │
│  Só sabe: "o que fazer quando algo acontece"     │
│  Conhece: dialogs, controllers de thread         │
│  NÃO conhece: cor de botão, layout de frame      │
└─────────────────┬────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────┐
│  CONTROLLERS DE THREAD (já existem)              │
│  Encapsulam: thread + try/except + estado        │
└─────────────────┬────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────┐
│  SERVICES (já existem)                           │
│  Encapsulam: regras de negócio                   │
└──────────────────────────────────────────────────┘
```

Cada camada **só fala com a vizinha**.

---

## 8. Ciclo de vida de um clique

Pra fixar tudo, o que acontece quando o usuário clica em "Carregar Arquivo" na arquitetura nova:

```
1. Usuário clica no botão
   └─► Header.btn_load.command = on_load_file (callback)

2. on_load_file aponta pra AppController.handle_load_file
   └─► AppController.handle_load_file() é chamado

3. AppController chama dialogs.ask_excel_file(view)
   └─► Diálogo abre, usuário escolhe → retorna Path

4. AppController instancia SanitizeController(file_path)
   └─► Thread iniciada, espera com .join()

5. AppController inspeciona controller.error e controller.result
   ├─► Sucesso: view.data_table.update_data(result)
   ├─► Erro com preview: view.data_table.update_data(dataframe) + show_error
   └─► Erro sem preview: show_error

6. DataTable internamente:
   ├─► Limpa o Treeview
   ├─► Configura colunas a partir do DataFrame
   └─► Insere linhas

7. UI atualizada. Ciclo completo.
```

**Cada caixa só conhece suas vizinhas.**

---

## 9. Padrões clássicos (MVC, MVP, MVVM)

| Padrão | Como funciona | Equivale a... |
|---|---|---|
| **MVC** | View desenha, Controller orquestra, Model guarda dados | Quase o que fazemos |
| **MVP** | View "passiva", Presenter orquestra TUDO | Mais próximo do nosso |
| **MVVM** | View se "liga" a um ViewModel via data binding | WPF, Vue, React |

O que estamos construindo é mais próximo de **MVP**: a View é "passiva" — só desenha e emite eventos. O **Presenter** (AppController) orquestra.

> Não se preocupe com nomes formais. São úteis pra pesquisar e conversar, mas o importante é dominar os princípios.

---

## 10. Plano em fases

### 🟢 Fase 1: Theme (~30 min)
**Esforço**: baixo · **Impacto**: visual + consistência.

Centralizar cores, fontes, tamanhos em `theme.py`. Substituir hardcoded por referências.

**Por quê primeiro**: zero risco. Só substitui strings por constantes. Familiariza com a estrutura nova sem mexer em lógica.

### 🟡 Fase 2: Dialogs (~30 min)
**Esforço**: baixo · **Impacto**: limpeza da App.

Mover `ask_file_to_open`, `ask_file_directory_to_save`, `error_message`, `success_message` pra `dialogs.py`.

**Por quê depois do theme**: puro recorta-e-cola, sem dependências entre componentes.

### 🟠 Fase 3: Components (~2-4h)
**Esforço**: médio · **Impacto**: estrutural alto.

Criar `DataTable`, `Sidebar`, `Header`, `Footer`, `ProgressBar` como classes próprias.

**Estratégia**: extrair UM por vez, rodar app, garantir que funciona, **commit**, próximo. Comece pelo `DataTable` (mais isolado), depois `ProgressBar`, depois `Header`/`Footer` (com callbacks).

### 🔴 Fase 4: Application Controller (~2-3h)
**Esforço**: médio · **Impacto**: separação de fluxo.

Mover `_run_sanitize_thread`, `_run_process_thread`, `_handle_file_uploaded` pra `app_controller.py`.

**Por quê último**: agora que componentes existem com callbacks, o AppController encaixa naturalmente.

---

## 11. Estrutura final esperada

```
src/
├── gui/
│   ├── app.py                  # View principal (montagem só)
│   ├── theme.py                # Cores, fontes, tamanhos
│   ├── dialogs.py              # File pickers e popups (funções)
│   ├── app_controller.py       # Orquestra eventos ↔ controllers
│   └── components/
│       ├── __init__.py
│       ├── sidebar.py
│       ├── header.py           # Botões "Carregar" e "Exportar"
│       ├── data_table.py       # Treeview + scrollbars
│       ├── progress_bar.py
│       └── footer.py           # Botões "Gerar" e "Cancelar"
├── controller/                 # threads (já existe)
├── services/                   # regras de negócio (já existe)
└── helpers/                    # utilitários (já existe)
```

---

## 12. Filtros pra fixar (resumão)

Pra cada decisão que tomar daqui pra frente, passe por esses filtros:

### Filtro 1: o que está mudando?
- Aparência? → vai pro **theme**
- Comportamento? → vai pro **AppController**
- Estrutura visual coesa? → vai pro **component**
- Operação transacional? → vai pro **dialogs**

### Filtro 2: tem estado?
- Sim → **classe**
- Não → **função num módulo**

### Filtro 3: quem precisa saber?
- Componente NÃO deve saber sobre regras de negócio
- AppController NÃO deve saber sobre detalhes visuais
- Service NÃO deve saber sobre thread/UI

### Filtro 4: callbacks vs métodos
- Componente quer **avisar** que algo aconteceu? → **callback**
- AppController quer **mandar** o componente fazer algo? → **método público**

---

## Análise componente por componente

### Tabela → classe + módulo (`components/data_table.py`)
- ✅ Tamanho: ocupa 60+ linhas.
- ✅ Coesão alta: tudo existe pra "mostrar dados tabulares".
- ✅ Estado próprio: controla colunas, linhas, configuração.
- ✅ Vai crescer: filtros, ordenação, paginação.
- **Resultado**: `DataTable(ctk.CTkFrame)` com `update_data(df)`.

### Barra de progresso → classe + módulo (`components/progress_bar.py`)
- ✅ Estado: porcentagem, mensagem, status.
- ✅ Comportamento: animar, resetar, atualizar.
- ✅ Reutilização: qualquer operação longa.
- **Resultado**: `ProgressBar(ctk.CTkFrame)` com `update()`, `reset()`.

### Diálogos → módulo de funções (`dialogs.py`)
- ❌ Sem estado.
- ✅ Operações transacionais.
- ❌ NÃO virar classe (antipadrão "singleton fingido").
- **Resultado**: arquivo com funções soltas.

### Sidebar / Header / Footer → classes + módulos
- ✅ Coesão visual.
- ✅ Tamanho razoável (20-40 linhas cada).
- ✅ Mudança independente.
- **Resultado**: classes próprias `Sidebar`, `Header`, `Footer`.

### Tema → módulo de constantes (`theme.py`)
- ❌ Sem estado, sem comportamento.
- ✅ Reutilização global.
- ✅ Mudança centralizada.
- **Resultado**: módulo com constantes ou `dataclass(frozen=True)`.

### Application Controller → classe + módulo (`app_controller.py`)
- ✅ Coesão: orquestra eventos da UI.
- ✅ Estado: pode guardar último DataFrame, status.
- ✅ Testabilidade: mockando a View.
- **Resultado**: classe `AppController` com métodos `handle_*`.

---

## Princípios transferíveis

Esses raciocínios não valem só pro `customtkinter` — valem pra qualquer GUI (Qt, web, mobile):

1. **Aparência, comportamento e estado são dimensões diferentes.** Separe-os.
2. **Componente é caixa-preta.** Quem usa só precisa saber: o que mando? o que recebo de volta?
3. **Componentes emitem eventos, não tomam decisões.** A decisão fica no controller.
4. **Camadas só falam com vizinhas.** Não pule etapas.
5. **Estado precisa de classe. Operação transacional precisa de função.**
6. **Refatore em pequenos passos com commits frequentes.** Um componente por vez.

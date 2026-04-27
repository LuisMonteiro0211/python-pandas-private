# python-pandas-analyzer

Projeto em evolução para analisar planilhas Excel com `pandas`, validar a estrutura mínima esperada e preparar a geração de relatórios filtrados por setor e turno.

## Estado atual

O projeto está em transição de um fluxo mais direto em script para uma interface gráfica com `customtkinter`.

Hoje a aplicação já permite:

- selecionar um arquivo Excel (`.xlsx` ou `.xls`) pela interface;
- carregar o arquivo com `pandas`;
- sanitizar o `DataFrame` verificando estrutura mínima e dados inválidos;
- exibir uma pré-visualização em tabela (`Treeview`);
- selecionar um diretório de exportação pela interface.

No momento, a parte de pré-visualização e sanitização já está integrada à GUI. O fluxo completo de geração dos relatórios pela interface ainda está em refinamento.

## Funcionalidades implementadas

- Leitura de planilhas Excel com `pandas`.
- Validação das colunas obrigatórias `SETOR` e `TURNO`.
- Normalização dos nomes das colunas.
- Remoção de espaços em branco nas colunas obrigatórias.
- Validação de `DataFrame` vazio e de valores `NaN`.
- Processamento preparado para exportar relatórios separados por setor e turno.
- Interface gráfica inicial para seleção de arquivo, preview e escolha do diretório de exportação.
- Separação inicial de responsabilidades entre `gui`, `controller`, `services`, `helpers` e `models`.

## Requisitos da planilha

A planilha de entrada deve conter, no mínimo, as colunas:

- `SETOR`
- `TURNO`

As demais colunas são preservadas no `DataFrame` e podem aparecer tanto na pré-visualização quanto nos arquivos exportados.

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/LuisMonteiro0211/python-pandas-analyzer
cd python-pandas-analyzer
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Atualmente o ponto de entrada da interface é:

```bash
python run_gui.py
```

Ao abrir a aplicação:

1. clique em `Carregar Arquivo`;
2. selecione a planilha Excel;
3. a aplicação tenta ler e sanitizar o conteúdo;
4. se o arquivo puder ser lido, o `DataFrame` pode ser exibido na tabela;
5. erros de sanitização ficam disponíveis para a interface decidir se libera ou não as próximas etapas.

## Fluxo interno atual

De forma simplificada, o fluxo está organizado assim:

- `src/gui/app.py`: monta a interface e orquestra as ações do usuário;
- `src/controller/sanitize_controller.py`: roda a leitura/sanitização em thread e expõe `result` e `error`;
- `src/controller/process_controller.py`: prepara a execução do processamento final em thread;
- `src/services/sanitize_dataframe.py`: concentra a validação e sanitização do `DataFrame`;
- `src/services/process_spreadsheet.py`: aplica filtros e exporta relatórios por setor e turno;
- `src/helpers/helper.py`: utilitários de leitura, filtros, exportação e apoio ao processamento.

## Estrutura atual do projeto

```text
python-pandas-analyzer/
├─ README.md
├─ requirements.txt
├─ run_gui.py
├─ src/
│  ├─ __init__.py
│  ├─ constants.py
│  ├─ controller/
│  │  ├─ __init__.py
│  │  ├─ process_controller.py
│  │  └─ sanitize_controller.py
│  ├─ gui/
│  │  ├─ __init__.py
│  │  └─ app.py
│  ├─ helpers/
│  │  ├─ helper.py
│  │  └─ log.py
│  ├─ models/
│  │  ├─ export.py
│  │  └─ filtro.py
│  └─ services/
│     ├─ __init__.py
│     ├─ process_spreadsheet.py
│     └─ sanitize_dataframe.py
```

## Saída esperada do processamento

Quando o fluxo de exportação estiver acionado pela interface, os arquivos devem seguir o padrão:

```text
Relatorio_{Setor}_{Turno}_{DD_MM_YYYY}.xlsx
```

## Testes

Os testes automatizados ainda precisam ser atualizados para acompanhar a nova arquitetura baseada em GUI + controllers.

Quando a suíte estiver consolidada, a execução continuará sendo feita com:

```bash
pytest
```

## Problemas comuns

- `Arquivo ... não encontrado`: o caminho selecionado não existe ou não é um arquivo válido.
- `Erro ao ler o arquivo ...`: houve falha na leitura do Excel com `pandas`.
- `Erro ao sanitizar o DataFrame ...`: a planilha está vazia, sem colunas obrigatórias, com valores `NaN` ou com dados inválidos nas colunas críticas.
- A tabela não mostra tudo de uma vez: a pré-visualização usa `Treeview` com barra de rolagem horizontal e vertical.

## Próximos passos

- melhorar a divisão de responsabilidades entre GUI, controllers e services;
- finalizar o fluxo de exportação acionado pela interface;
- adicionar testes automatizados para controllers, services e fluxo principal da GUI;
- incluir imagens da interface no README.

## Contribuição

Contribuições são bem-vindas. Abra uma issue ou envie um pull request.

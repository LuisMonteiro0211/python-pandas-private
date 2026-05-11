# Changelog

Todas as mudanças notáveis do projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-05-11

### ✨ Adicionado
- Interface gráfica completa com CustomTkinter
- Sistema de validação e sanitização de planilhas Excel
- Exportação automática de relatórios por setor e turno
- Barra de progresso em tempo real durante processamento
- Sistema de logging estruturado
- Suporte a cancelamento de processamento
- Preview de dados em tabela interativa
- Estimativa de número de arquivos antes da exportação
- Diálogos informativos (sucesso, erro, aviso)
- Arquitetura MVC bem definida
- Processamento assíncrono com threading
- Sistema de callbacks para atualização de progresso

### 🏗️ Arquitetura
- Separação clara entre GUI, Controller, Services, Models e Helpers
- Componentes reutilizáveis (DataTable, Sidebar, Header, ProgressBar, Baseboard)
- Controladores especializados (SanitizeController, ProcessController)
- Modelos de dados (Filtro, Export, ProcessContext)
- Serviços de negócio (sanitize_dataframe, process_spreadsheet, estimate_export_jobs)

### 📚 Documentação
- README.md completo com badges, diagramas e exemplos
- Documentação de arquitetura em docs/refatoracao_gui.md
- CHANGELOG.md para controle de versões
- LICENSE MIT
- Comentários e docstrings em todo o código

### 🔧 Tecnologias
- Python 3.14
- Pandas 3.0.0
- CustomTkinter 5.2.2
- OpenPyXL 3.1.5
- Pytest 9.0.3

### 🐛 Corrigido
- Tratamento robusto de erros na leitura de arquivos
- Validação de colunas obrigatórias
- Normalização de nomes de colunas
- Remoção de espaços em branco
- Detecção de valores nulos

### 🧪 Testes
- Configuração de pytest
- Estrutura preparada para testes unitários

---

## [0.1.0] - 2025-04-08

### ✨ Adicionado
- Primeira versão funcional com processamento em linha de comando
- Leitura básica de planilhas Excel
- Filtros por setor e turno
- Exportação para múltiplos arquivos

---

**Legenda:**
- ✨ Adicionado: Novas funcionalidades
- 🔄 Modificado: Alterações em funcionalidades existentes
- ❌ Removido: Funcionalidades removidas
- 🐛 Corrigido: Correções de bugs
- 🔒 Segurança: Correções de vulnerabilidades
- 📚 Documentação: Mudanças na documentação
- 🏗️ Arquitetura: Mudanças estruturais no código

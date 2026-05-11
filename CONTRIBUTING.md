# Guia de Contribuição

Obrigado por considerar contribuir com o Python Pandas Analyzer! 🎉

## 📋 Código de Conduta

Este projeto segue um código de conduta baseado no [Contributor Covenant](https://www.contributor-covenant.org/). Esperamos que todos os participantes sigam estas diretrizes:

- Use linguagem acolhedora e inclusiva
- Respeite diferentes pontos de vista e experiências
- Aceite críticas construtivas com elegância
- Foque no que é melhor para a comunidade

## 🚀 Como Contribuir

### 1. Reportar Bugs

Encontrou um bug? Ajude-nos criando uma issue:

1. Verifique se já não existe uma issue sobre o problema
2. Use o template de bug report (se disponível)
3. Inclua:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs. comportamento atual
   - Screenshots (se aplicável)
   - Ambiente (OS, versão do Python, etc.)

### 2. Sugerir Melhorias

Tem uma ideia para melhorar o projeto?

1. Verifique se a sugestão já não foi feita
2. Abra uma issue com o label `enhancement`
3. Descreva:
   - O problema que sua sugestão resolve
   - Como você imagina a solução
   - Alternativas que você considerou

### 3. Contribuir com Código

#### Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/python-pandas-analyzer.git
cd python-pandas-analyzer

# Adicione o repositório original como upstream
git remote add upstream https://github.com/LuisMonteiro0211/python-pandas-analyzer.git
```

#### Configure o Ambiente

```bash
# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

#### Crie uma Branch

```bash
# Atualize sua main
git checkout main
git pull upstream main

# Crie uma branch para sua feature/fix
git checkout -b feature/minha-feature
# ou
git checkout -b fix/correcao-bug
```

#### Desenvolva

1. **Escreva código limpo**
   - Siga PEP 8 (use `black` e `flake8`)
   - Adicione docstrings em funções e classes
   - Mantenha funções pequenas e focadas

2. **Adicione testes**
   - Teste novas funcionalidades
   - Garanta que testes existentes passem
   ```bash
   pytest
   ```

3. **Atualize a documentação**
   - README.md se necessário
   - Docstrings
   - CHANGELOG.md

#### Commit

Use mensagens de commit claras e descritivas:

```bash
# Bom
git commit -m "Adiciona validação de colunas duplicadas"
git commit -m "Corrige bug na exportação com caracteres especiais"
git commit -m "Atualiza documentação do ProcessController"

# Ruim
git commit -m "fix"
git commit -m "atualizações"
git commit -m "wip"
```

**Padrão sugerido:**
```
<tipo>: <descrição curta>

<descrição detalhada (opcional)>

<issue relacionada (opcional)>
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação, ponto e vírgula, etc.
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Manutenção, dependências, etc.

#### Push e Pull Request

```bash
# Faça push da sua branch
git push origin feature/minha-feature
```

No GitHub:
1. Abra um Pull Request
2. Descreva suas mudanças
3. Referencie issues relacionadas
4. Aguarde review

## 🎨 Padrões de Código

### Python

```python
# Bom
def processar_planilha(dataframe: pd.DataFrame, diretorio: str) -> None:
    """
    Processa a planilha aplicando filtros e exportando relatórios.

    Args:
        dataframe: DataFrame com os dados a processar
        diretorio: Diretório de destino dos relatórios

    Raises:
        ValueError: Se o DataFrame estiver vazio
    """
    if dataframe.empty:
        raise ValueError("DataFrame vazio")
    
    # Processamento...
```

### Imports

```python
# Ordem: stdlib, third-party, local
import os
import sys
from datetime import datetime

import pandas as pd
import customtkinter as ctk

from src.helpers import helper
from src.models import Filtro
```

### Nomenclatura

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Classes | PascalCase | `DataTable`, `ProcessController` |
| Funções/Métodos | snake_case | `process_spreadsheet()`, `get_unique_values()` |
| Variáveis | snake_case | `safe_dataframe`, `diretorio_export` |
| Constantes | UPPER_SNAKE_CASE | `REQUIRED_COLUMNS`, `MAX_ROWS` |
| Privado | _prefixo | `_configurar_tela()`, `_on_progress()` |

## 🧪 Testes

### Estrutura

```python
import pytest
from src.services.sanitize_dataframe import sanitize_dataframe

def test_sanitize_dataframe_valido():
    """Testa sanitização com DataFrame válido."""
    # Arrange
    df = criar_dataframe_valido()
    
    # Act
    resultado = sanitize_dataframe(df)
    
    # Assert
    assert resultado is not None
    assert 'SETOR' in resultado.columns
    assert 'TURNO' in resultado.columns

def test_sanitize_dataframe_sem_coluna_obrigatoria():
    """Testa sanitização quando falta coluna obrigatória."""
    # Arrange
    df = criar_dataframe_sem_setor()
    
    # Act & Assert
    with pytest.raises(ValueError):
        sanitize_dataframe(df)
```

### Executar Testes

```bash
# Todos os testes
pytest

# Com verbosidade
pytest -v

# Testes específicos
pytest tests/test_sanitize.py

# Com cobertura
pytest --cov=src --cov-report=html
```

## 📝 Documentação

### Docstrings

Use o formato Google:

```python
def export_to_excel(export: Export) -> None:
    """
    Exporta um DataFrame para arquivo Excel.

    Args:
        export: Objeto Export contendo DataFrame, diretório e nome do arquivo

    Raises:
        FileNotFoundError: Se o diretório não existir
        PermissionError: Se não houver permissão de escrita

    Example:
        >>> export = Export(df=dataframe, diretorio="./exports", nome_arquivo="relatorio.xlsx")
        >>> export_to_excel(export)
    """
```

### README Updates

Ao adicionar funcionalidades significativas:
- Atualize a seção de funcionalidades
- Adicione exemplos de uso
- Atualize screenshots se necessário

## 🔍 Checklist de Pull Request

Antes de submeter, verifique:

- [ ] Código segue PEP 8
- [ ] Todos os testes passam
- [ ] Novos testes foram adicionados
- [ ] Documentação foi atualizada
- [ ] CHANGELOG.md foi atualizado
- [ ] Commits têm mensagens descritivas
- [ ] Branch está atualizada com main
- [ ] Não há conflitos

## 🏆 Reconhecimento

Todos os contribuidores serão adicionados à lista de colaboradores do projeto!

## ❓ Dúvidas?

Abra uma issue com a label `question` ou entre em contato:
- GitHub: [@LuisMonteiro0211](https://github.com/LuisMonteiro0211)

---

**Obrigado por contribuir! Sua ajuda é muito valiosa.** 💚

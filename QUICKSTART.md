# 🚀 Início Rápido

Guia rápido para começar a usar o Python Pandas Analyzer em menos de 5 minutos.

## ⚡ Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/LuisMonteiro0211/python-pandas-analyzer.git
cd python-pandas-analyzer

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python run_gui.py
```

## 📝 Primeiro Uso

### Passo 1: Prepare sua Planilha

Sua planilha Excel deve ter pelo menos estas colunas:

```
| SETOR     | TURNO  | ... outras colunas ... |
|-----------|--------|------------------------|
| Produção  | Manhã  | ...                    |
| Qualidade | Tarde  | ...                    |
| Logística | Noite  | ...                    |
```

### Passo 2: Carregue o Arquivo

1. Clique em **📁 Carregar Arquivo**
2. Selecione sua planilha `.xlsx` ou `.xls`
3. Aguarde a validação
4. ✅ Sucesso! Visualize os dados na tabela

### Passo 3: Escolha o Destino

1. Clique em **💾 Escolher Destino**
2. Selecione o diretório onde salvar os relatórios
3. Confirme a seleção

### Passo 4: Processe

1. Clique em **▶️ Processar**
2. Acompanhe o progresso
3. ✅ Pronto! Seus relatórios estão salvos

## 📦 Resultado

Os relatórios serão criados no formato:

```
Relatorio_{Setor}_{Turno}_{DD_MM_YYYY}.xlsx
```

Exemplo:
```
📁 exports/
├── 📊 Relatorio_Producao_Manha_11_05_2026.xlsx
├── 📊 Relatorio_Producao_Tarde_11_05_2026.xlsx
└── 📊 Relatorio_Qualidade_Manha_11_05_2026.xlsx
```

## 🆘 Problemas Comuns

### ❌ "Erro ao ler o arquivo"
- **Solução**: Feche o arquivo Excel antes de processar

### ❌ "Colunas obrigatórias não encontradas"
- **Solução**: Adicione colunas `SETOR` e `TURNO` na planilha

### ❌ "ModuleNotFoundError"
- **Solução**: Ative o ambiente virtual e reinstale as dependências
  ```bash
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## 🎓 Próximos Passos

- 📚 Leia o [README completo](README.md)
- 🤝 Veja o [guia de contribuição](CONTRIBUTING.md)
- 📝 Confira o [changelog](CHANGELOG.md)

## 💡 Dicas

1. **Use Ctrl+C no terminal** para fechar a aplicação
2. **Mantenha backups** de suas planilhas originais
3. **Verifique os logs** em `./logs/` se algo der errado
4. **Teste com poucos dados** primeiro antes de processar planilhas grandes

---

**Pronto para começar?** Execute `python run_gui.py` e boa sorte! 🎉

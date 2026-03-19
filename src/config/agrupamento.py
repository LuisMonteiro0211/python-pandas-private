"""
Configuração de agrupamento de setores em pastas.

Cada chave do dicionário GRUPOS é o nome da subpasta que será
criada dentro do diretório de exportação.
O valor é a lista de setores (case-insensitive) que serão
direcionados para aquela pasta.

Setores que não aparecem em nenhum grupo ficam soltos na raiz
do diretório de exportação.

Exemplo de estrutura gerada:
    DIRETORIO_EXPORT/
    ├── Logistica/
    │   ├── Relatorio_Expedicao_Turno1_19_03_2026.xlsx
    │   ├── Relatorio_Empilhadeira_Turno1_19_03_2026.xlsx
    │   └── Relatorio_Abastecimento_Turno1_19_03_2026.xlsx
    ├── Operacoes/
    │   ├── Relatorio_Caldeira_Turno1_19_03_2026.xlsx
    │   └── ...
    ├── Logistica_2/
    │   ├── Relatorio_Empilhadeira_2_Turno1_19_03_2026.xlsx
    │   └── Relatorio_Expedicao_2_Turno1_19_03_2026.xlsx
    └── Relatorio_OutroSetor_Turno1_19_03_2026.xlsx   (solto na raiz)
"""

GRUPOS: dict[str, list[str]] = {
    "Logistica": [
        "Expedicao",
        "Empilhadeira",
        "Abastecimento",
    ],
    "Operacoes": [
        "Sala de controle esterilizacao",
        "Sala de controle pasteurizacao",
        "Adicao de ingredientes",
        "Caldeira",
        "Plataforma de recepcao de leite",
        "Presa",
        "Servicos gerais",
        "Vestiario",
    ],
    "Logistica_2": [
        "Empilhadeira 2",
        "Expedicao 2",
    ],
}


def _build_lookup(grupos: dict[str, list[str]]) -> dict[str, str]:
    """
    Constrói um dicionário invertido setor (normalizado) → nome da pasta.

    A normalização converte para minúsculo e remove espaços extras,
    para que a comparação com os valores da planilha seja tolerante
    a variações de caixa e espaçamento.
    """
    lookup: dict[str, str] = {}
    for pasta, setores in grupos.items():
        for setor in setores:
            lookup[setor.strip().lower()] = pasta
    return lookup


_SETOR_PARA_PASTA = _build_lookup(GRUPOS)


def resolver_pasta(setor: str) -> str | None:
    """
    Retorna o nome da subpasta para um dado setor,
    ou None se o setor não pertencer a nenhum grupo
    (nesse caso o arquivo fica na raiz do export).

    A comparação é case-insensitive e ignora espaços extras.

    Args:
        setor: Nome do setor vindo da planilha.

    Returns:
        Nome da subpasta ou None.

    Exemplos:
        >>> resolver_pasta("Expedicao")
        'Logistica'
        >>> resolver_pasta("CALDEIRA")
        'Operacoes'
        >>> resolver_pasta("Setor desconhecido")
        None
    """
    return _SETOR_PARA_PASTA.get(setor.strip().lower())

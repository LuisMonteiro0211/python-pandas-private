import pytest
from pathlib import Path

from src.config.agrupamento import resolver_pasta, GRUPOS
from src.helpers.helper import resolver_diretorio_export


# ---------------------------------------------------------------------------
# resolver_pasta – retorna o nome da subpasta ou None
# ---------------------------------------------------------------------------

class TestResolverPasta:
    """Testes para a função resolver_pasta do módulo de agrupamento."""

    # -- Grupo 1: Logistica --
    @pytest.mark.parametrize("setor", ["Expedicao", "Empilhadeira", "Abastecimento"])
    def test_grupo_logistica(self, setor):
        assert resolver_pasta(setor) == "Logistica"

    # -- Grupo 2: Operacoes --
    @pytest.mark.parametrize("setor", [
        "Sala de controle esterilizacao",
        "Sala de controle pasteurizacao",
        "Adicao de ingredientes",
        "Caldeira",
        "Plataforma de recepcao de leite",
        "Presa",
        "Servicos gerais",
        "Vestiario",
    ])
    def test_grupo_operacoes(self, setor):
        assert resolver_pasta(setor) == "Operacoes"

    # -- Grupo 3: Logistica_2 --
    @pytest.mark.parametrize("setor", ["Empilhadeira 2", "Expedicao 2"])
    def test_grupo_logistica_2(self, setor):
        assert resolver_pasta(setor) == "Logistica_2"

    # -- Setor não mapeado retorna None --
    def test_setor_desconhecido_retorna_none(self):
        assert resolver_pasta("Setor Inventado") is None

    # -- Case-insensitive --
    def test_case_insensitive(self):
        assert resolver_pasta("EXPEDICAO") == "Logistica"
        assert resolver_pasta("caldeira") == "Operacoes"
        assert resolver_pasta("EMPILHADEIRA 2") == "Logistica_2"

    # -- Espaços extras nas bordas --
    def test_espacos_extras(self):
        assert resolver_pasta("  Expedicao  ") == "Logistica"
        assert resolver_pasta("  Caldeira  ") == "Operacoes"


# ---------------------------------------------------------------------------
# resolver_diretorio_export – retorna Path de destino e cria subpasta
# ---------------------------------------------------------------------------

class TestResolverDiretorioExport:
    """Testes para a função resolver_diretorio_export."""

    def test_setor_com_grupo_cria_subpasta(self, tmp_path):
        resultado = resolver_diretorio_export(tmp_path, "Expedicao")
        assert resultado == tmp_path / "Logistica"
        assert resultado.is_dir()

    def test_setor_sem_grupo_retorna_raiz(self, tmp_path):
        resultado = resolver_diretorio_export(tmp_path, "Setor Qualquer")
        assert resultado == tmp_path

    def test_cria_subpasta_operacoes(self, tmp_path):
        resultado = resolver_diretorio_export(tmp_path, "Caldeira")
        assert resultado == tmp_path / "Operacoes"
        assert resultado.is_dir()

    def test_cria_subpasta_logistica_2(self, tmp_path):
        resultado = resolver_diretorio_export(tmp_path, "Empilhadeira 2")
        assert resultado == tmp_path / "Logistica_2"
        assert resultado.is_dir()

    def test_chamada_repetida_nao_falha(self, tmp_path):
        """mkdir com exist_ok=True não deve falhar na segunda chamada."""
        resolver_diretorio_export(tmp_path, "Expedicao")
        resolver_diretorio_export(tmp_path, "Expedicao")
        assert (tmp_path / "Logistica").is_dir()


# ---------------------------------------------------------------------------
# Coerência da configuração GRUPOS
# ---------------------------------------------------------------------------

class TestConfigGrupos:
    """Testes de integridade da configuração de agrupamento."""

    def test_nenhum_setor_duplicado_entre_grupos(self):
        """Um setor não pode aparecer em mais de um grupo."""
        todos = []
        for setores in GRUPOS.values():
            todos.extend(s.strip().lower() for s in setores)
        assert len(todos) == len(set(todos)), "Há setores duplicados entre grupos"

    def test_todos_os_grupos_tem_pelo_menos_um_setor(self):
        for pasta, setores in GRUPOS.items():
            assert len(setores) > 0, f"Grupo '{pasta}' está vazio"

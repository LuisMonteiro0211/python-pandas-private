import pandas as pd
import pytest

from src.helpers.helper import (
    applying_filters,
    check_colunas,
    check_environment_variables,
    export_to_excel,
    get_dataframe,
    get_unique_values,
    safe_name,
)
from src.models.export import Export
from src.models.filtro import Filtro


# ---------------------------------------------------------------------------
# get_dataframe
# ---------------------------------------------------------------------------

class TestGetDataframe:
    def test_retorna_dataframe_valido(self, monkeypatch):
        df_fake = pd.DataFrame({"SETOR": ["A"], "TURNO": ["Manha"]})

        monkeypatch.setattr("src.helpers.helper.Path.is_file", lambda _: True)
        monkeypatch.setattr("src.helpers.helper.pd.read_excel", lambda _: df_fake)

        df = get_dataframe("arquivo.xlsx")
        assert df.shape == (1, 2)

    def test_arquivo_inexistente(self, monkeypatch):
        monkeypatch.setattr("src.helpers.helper.Path.is_file", lambda _: False)

        with pytest.raises(FileNotFoundError, match="não encontrado"):
            get_dataframe("arquivo_inexistente.xlsx")

    def test_erro_leitura(self, monkeypatch):
        monkeypatch.setattr("src.helpers.helper.Path.is_file", lambda _: True)
        monkeypatch.setattr(
            "src.helpers.helper.pd.read_excel",
            lambda _: (_ for _ in ()).throw(Exception("erro de leitura")),
        )

        with pytest.raises(ValueError, match="Erro ao ler"):
            get_dataframe("arquivo.xlsx")


# ---------------------------------------------------------------------------
# check_colunas
# ---------------------------------------------------------------------------

class TestCheckColunas:
    def test_coluna_existente_nao_levanta_erro(self):
        check_colunas(["SETOR", "TURNO"], "SETOR")

    def test_coluna_inexistente(self):
        with pytest.raises(ValueError, match="não encontrada"):
            check_colunas(["SETOR"], "TURNO")


# ---------------------------------------------------------------------------
# get_unique_values
# ---------------------------------------------------------------------------

class TestGetUniqueValues:
    def test_retorna_valores_unicos(self):
        df = pd.DataFrame({"SETOR": ["A", "B", "A", "C"]})
        result = get_unique_values(df, "SETOR")
        assert set(result) == {"A", "B", "C"}

    def test_coluna_com_valor_unico(self):
        df = pd.DataFrame({"TURNO": ["Manha", "Manha"]})
        assert get_unique_values(df, "TURNO") == ["Manha"]


# ---------------------------------------------------------------------------
# applying_filters
# ---------------------------------------------------------------------------

class TestApplyingFilters:
    def test_filtro_basico(self):
        df = pd.DataFrame({
            "SETOR": ["A", "B", "A"],
            "TURNO": ["Manha", "Noite", "Noite"],
        })
        filtro = Filtro(coluna="SETOR", dataframe=df, valor="A")
        resultado = applying_filters(filtro)
        assert resultado.shape[0] == 2

    def test_filtro_sem_resultado(self):
        df = pd.DataFrame({"SETOR": ["A", "B"]})
        filtro = Filtro(coluna="SETOR", dataframe=df, valor="C")
        resultado = applying_filters(filtro)
        assert resultado.empty


# ---------------------------------------------------------------------------
# export_to_excel
# ---------------------------------------------------------------------------

class TestExportToExcel:
    def test_exporta_arquivo(self, tmp_path):
        df = pd.DataFrame({"SETOR": ["A"], "TURNO": ["Manha"]})
        export = Export(
            dataframe=df,
            diretorio=tmp_path,
            nome_arquivo="teste.xlsx",
            nome_aba="Sheet1",
        )
        export_to_excel(export)

        arquivo = tmp_path / "teste.xlsx"
        assert arquivo.exists()

        df_lido = pd.read_excel(arquivo, sheet_name="Sheet1")
        assert df_lido.shape == (1, 2)


# ---------------------------------------------------------------------------
# check_environment_variables
# ---------------------------------------------------------------------------

class TestCheckEnvironmentVariables:
    def test_todas_definidas(self, monkeypatch):
        monkeypatch.setenv("VAR_A", "valor_a")
        monkeypatch.setenv("VAR_B", "valor_b")
        check_environment_variables(["VAR_A", "VAR_B"])

    def test_variavel_ausente(self, monkeypatch):
        monkeypatch.delenv("VAR_INEXISTENTE", raising=False)
        with pytest.raises(ValueError, match="VAR_INEXISTENTE"):
            check_environment_variables(["VAR_INEXISTENTE"])

    def test_multiplas_ausentes(self, monkeypatch):
        monkeypatch.delenv("X", raising=False)
        monkeypatch.delenv("Y", raising=False)
        with pytest.raises(ValueError, match="X.*Y"):
            check_environment_variables(["X", "Y"])


# ---------------------------------------------------------------------------
# safe_name
# ---------------------------------------------------------------------------

class TestSafeName:
    def test_remove_caracteres_invalidos(self):
        assert safe_name('arquivo<>:"/\\|?*.xlsx') == "arquivo_________.xlsx"

    def test_texto_limpo_inalterado(self):
        assert safe_name("relatorio_setor_A") == "relatorio_setor_A"

    def test_remove_espacos_nas_bordas(self):
        assert safe_name("  nome  ") == "nome"

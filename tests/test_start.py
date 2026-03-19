import pytest
from pathlib import Path

from src.main.start import validate_paths


class TestValidatePaths:
    def test_caminhos_validos(self, tmp_path):
        planilha = tmp_path / "dados.xlsx"
        planilha.touch()
        export_dir = tmp_path / "export"
        export_dir.mkdir()
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        validate_paths(planilha, export_dir, log_dir)

    def test_planilha_inexistente(self, tmp_path):
        export_dir = tmp_path / "export"
        export_dir.mkdir()
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        with pytest.raises(FileNotFoundError, match="não é um arquivo válido"):
            validate_paths(tmp_path / "nao_existe.xlsx", export_dir, log_dir)

    def test_diretorio_export_invalido(self, tmp_path):
        planilha = tmp_path / "dados.xlsx"
        planilha.touch()
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        with pytest.raises(NotADirectoryError, match="não é um diretório válido"):
            validate_paths(planilha, tmp_path / "nao_existe", log_dir)

    def test_diretorio_log_invalido(self, tmp_path):
        planilha = tmp_path / "dados.xlsx"
        planilha.touch()
        export_dir = tmp_path / "export"
        export_dir.mkdir()

        with pytest.raises(NotADirectoryError, match="não é um diretório válido"):
            validate_paths(planilha, export_dir, tmp_path / "nao_existe")

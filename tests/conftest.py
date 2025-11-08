import pytest
from pathlib import Path
import os

@pytest.fixture(autouse=True)
def change_test_dir(tmp_path, monkeypatch):
    """Автоматически меняем рабочую директорию на временную для каждого теста"""
    monkeypatch.chdir(tmp_path)
    yield

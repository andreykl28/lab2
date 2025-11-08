import pytest
from pathlib import Path
from src.shell import Shell


def test_shell_initialization():
    """Тест инициализации оболочки"""
    shell = Shell()
    assert shell.running == True
    assert shell.current_dir is not None


def test_execute_ls(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды ls"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("ls")


def test_execute_cd(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды cd"""
    monkeypatch.chdir(tmp_path)
    test_dir = tmp_path / "testdir"
    test_dir.mkdir()
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"cd {test_dir}")


def test_execute_cat(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды cat"""
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"cat {test_file}")


def test_execute_cp(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды cp"""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"cp {src} {dst}")
    assert dst.exists()


def test_execute_mv(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды mv"""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"mv {src} {dst}")
    assert dst.exists()
    assert not src.exists()


def test_execute_rm(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды rm"""
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    
    shell = Shell()
    mocker.patch('builtins.print')
    mocker.patch('builtins.input', return_value='y')
    shell.execute_command(f"rm {test_file}")


def test_execute_grep(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды grep"""
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World")
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"grep Hello {test_file}")


def test_execute_zip(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды zip"""
    monkeypatch.chdir(tmp_path)
    test_dir = tmp_path / "folder"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"zip {test_dir} archive.zip")


def test_execute_unzip(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды unzip"""
    monkeypatch.chdir(tmp_path)
    import zipfile
    
    with zipfile.ZipFile("test.zip", 'w') as zf:
        zf.writestr("file.txt", "content")
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("unzip test.zip")


def test_execute_history(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды history"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    
    shell.execute_command("ls")
    shell.execute_command("history")


def test_execute_undo(mocker, tmp_path, monkeypatch):
    """Тест выполнения команды undo"""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"cp {src} {dst}")
    shell.execute_command("undo")


def test_execute_exit(mocker):
    """Тест выполнения команды exit"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("exit")
    assert shell.running == False


def test_execute_unknown_command(mocker):
    """Тест неизвестной команды"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("unknown_command")


def test_cmd_ls_with_flags(mocker, tmp_path, monkeypatch):
    """Тест ls с флагами"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("ls -l")


def test_cmd_rm_with_flags(mocker, tmp_path, monkeypatch):
    """Тест rm с флагами"""
    monkeypatch.chdir(tmp_path)
    test_dir = tmp_path / "testdir"
    test_dir.mkdir()
    
    shell = Shell()
    mocker.patch('builtins.print')
    mocker.patch('builtins.input', return_value='y')
    shell.execute_command(f"rm -r {test_dir}")


def test_cmd_ls_unknown_flags(mocker, tmp_path, monkeypatch):
    """ls с неизвестными флагами"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("ls -x -y")


def test_cmd_cp_unknown_flags(mocker, tmp_path, monkeypatch):
    """cp с неизвестными флагами"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("cp -x file1 file2")


def test_cmd_cp_insufficient_args(mocker):
    """cp с недостаточным количеством аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("cp file1")


def test_cmd_rm_unknown_flags(mocker):
    """rm с неизвестными флагами"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("rm -x file.txt")


def test_cmd_rm_no_path(mocker):
    """rm без указания пути"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("rm")


def test_cmd_mv_unknown_flags(mocker):
    """mv с неизвестными флагами"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("mv -x file1 file2")


def test_cmd_mv_insufficient_args(mocker):
    """mv с недостаточным количеством аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("mv file1")


def test_cmd_cat_no_args(mocker):
    """cat без аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("cat")


def test_cmd_cd_no_args(mocker, tmp_path, monkeypatch):
    """cd без аргументов (переход в домашнюю)"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("cd")


def test_cmd_grep_no_args(mocker):
    """grep без аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("grep")


def test_cmd_grep_one_arg(mocker):
    """grep с одним аргументом"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("grep pattern")


def test_cmd_grep_with_flags(mocker, tmp_path, monkeypatch):
    """grep с флагами -r и -1"""
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test Content")
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"grep -r -1 test {test_file}")


def test_cmd_zip_insufficient_args(mocker):
    """zip с недостаточным количеством аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("zip folder")


def test_cmd_unzip_no_args(mocker):
    """unzip без аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("unzip")


def test_cmd_tar_insufficient_args(mocker):
    """tar с недостаточным количеством аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("tar folder")


def test_cmd_untar_no_args(mocker):
    """untar без аргументов"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("untar")


def test_cmd_history_with_number(mocker, tmp_path, monkeypatch):
    """history с указанием количества"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("ls")
    shell.execute_command("history 5")


def test_cmd_undo_cp(mocker, tmp_path, monkeypatch):
    """undo для cp"""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    shell = Shell()
    mocker.patch('builtins.print')
    mocker.patch('builtins.input', return_value='y')
    shell.execute_command(f"cp {src} {dst}")
    shell.execute_command("undo")


def test_cmd_undo_mv(mocker, tmp_path, monkeypatch):
    """undo для mv"""
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command(f"mv {src} {dst}")
    shell.execute_command("undo")


def test_cmd_undo_rm(mocker, tmp_path, monkeypatch):
    """undo для rm"""
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    
    shell = Shell()
    mocker.patch('builtins.print')
    mocker.patch('builtins.input', return_value='y')
    shell.execute_command(f"rm {test_file}")
    shell.execute_command("undo")


def test_cmd_undo_unsupported(mocker, tmp_path, monkeypatch):
    """undo для неподдерживаемой команды"""
    monkeypatch.chdir(tmp_path)
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("ls")
    shell.execute_command("undo")


def test_empty_command(mocker):
    """Пустая команда"""
    shell = Shell()
    mocker.patch('builtins.print')
    shell.execute_command("")

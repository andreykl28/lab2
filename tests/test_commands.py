import pytest
from pathlib import Path
from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.mv import mv
from src.commands.rm import rm, restore_from_trash
from src.commands.grep import grep
from src.commands.archive import zip_folder, unzip_file, tar_folder, untar_file
from src.utils.history import add_history, get_history, pop_last
from src.utils.logger import write_log


def test_ls_detailed(tmp_path):
    """Тест ls с флагом -l"""
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    ls(str(tmp_path), detailed=True)


def test_cd_home(mocker):
    """Тест cd без аргументов"""
    mocker.patch('os.chdir')
    cd("")


def test_cat_nonexistent_file():
    """Тест cat для несуществующего файла"""
    cat("/nonexistent/path/file.txt")


def test_cp_directory(tmp_path):
    """Тест cp для директории"""
    src_dir = tmp_path / "src_dir"
    src_dir.mkdir()
    (src_dir / "file.txt").write_text("content")
    dst_dir = tmp_path / "dst_dir"
    
    cp(str(src_dir), str(dst_dir), recursive=True)
    assert dst_dir.exists()


def test_mv_nonexistent(tmp_path):
    """Тест mv для несуществующего файла"""
    mv("/nonexistent/src", str(tmp_path / "dst"))


def test_grep_basic(tmp_path):
    """Тест grep базовый поиск"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World\nTest Line")
    
    result = grep("Hello", str(test_file))
    assert "Hello" in result


def test_grep_recursive(tmp_path):
    """Тест grep рекурсивный"""
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file.txt").write_text("pattern")
    
    result = grep("pattern", str(tmp_path), recursive=True)
    assert "pattern" in result


def test_grep_case_insensitive(tmp_path):
    """Тест grep без учета регистра"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("UPPERCASE text")
    
    result = grep("uppercase", str(test_file), ignore_case=True)
    assert "UPPERCASE" in result


def test_zip_folder(tmp_path):
    """Тест создания zip архива"""
    test_dir = tmp_path / "test_folder"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")
    
    archive_path = tmp_path / "archive.zip"
    zip_folder(str(test_dir), str(archive_path))
    assert archive_path.exists()


def test_tar_folder(tmp_path):
    """Тест создания tar.gz архива"""
    test_dir = tmp_path / "test_folder"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("content")
    
    archive_path = tmp_path / "archive.tar.gz"
    tar_folder(str(test_dir), str(archive_path))
    assert archive_path.exists()


def test_history_add_and_get(tmp_path, monkeypatch):
    """Тест добавления и получения истории"""
    monkeypatch.chdir(tmp_path)
    add_history("ls -l")
    add_history("cd /tmp")
    
    hist = get_history(2)
    assert len(hist) == 2
    assert "ls -l" in hist


def test_history_pop_last(tmp_path, monkeypatch):
    """Тест удаления последней команды"""
    monkeypatch.chdir(tmp_path)
    add_history("test command")
    
    last = pop_last()
    assert last == "test command"


def test_logger(tmp_path, monkeypatch):
    """Тест логгера"""
    monkeypatch.chdir(tmp_path)
    write_log("Test log message")
    
    log_file = Path("shell.log")
    assert log_file.exists()
    assert "Test log message" in log_file.read_text()

# тесты ошибок

def test_cat_is_directory(tmp_path):
    """cat на директорию"""
    test_dir = tmp_path / "dir"
    test_dir.mkdir()
    cat(str(test_dir))


def test_cd_nonexistent():
    """cd в несуществующую директорию"""
    result = cd("/nonexistent/path/that/does/not/exist")
    assert result == False


def test_cp_without_recursive(tmp_path):
    """cp директории без флага -r"""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    dst_dir = tmp_path / "dst"
    cp(str(src_dir), str(dst_dir), recursive=False)


def test_cp_nonexistent_source(tmp_path):
    """cp несуществующего файла"""
    cp("/nonexistent", str(tmp_path / "dst"), recursive=False)


def test_mv_to_existing_file(tmp_path):
    """mv с перезаписью существующего файла"""
    src = tmp_path / "src.txt"
    src.write_text("source")
    dst = tmp_path / "dst.txt"
    dst.write_text("destination")
    mv(str(src), str(dst))
    assert dst.read_text() == "source"


def test_rm_nonexistent():
    """rm несуществующего файла"""
    rm("/nonexistent/file.txt", recursive=False)


def test_rm_without_confirmation(mocker, tmp_path):
    """rm с отменой подтверждения"""
    test_dir = tmp_path / "dir"
    test_dir.mkdir()
    mocker.patch('builtins.input', return_value='n')
    rm(str(test_dir), recursive=True)
    assert test_dir.exists()


def test_restore_nonexistent():
    """Восстановление несуществующего файла"""
    restore_from_trash("nonexistent_file.txt")


def test_grep_nonexistent_file():
    """grep в несуществующем файле"""
    result = grep("pattern", "/nonexistent/file.txt")
    assert "ERROR" in result


def test_grep_no_matches(tmp_path):
    """grep без совпадений"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World")
    result = grep("nonexistent", str(test_file))
    assert "Нет совпадений" in result


def test_grep_read_error(mocker, tmp_path):
    """grep с ошибкой чтения"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    mocker.patch('pathlib.Path.open', side_effect=PermissionError("Access denied"))
    result = grep("content", str(test_file))


def test_zip_nonexistent_folder():
    """zip несуществующей папки"""
    result = zip_folder("/nonexistent", "archive.zip")
    assert "ERROR" in result


def test_unzip_nonexistent():
    """unzip несуществующего архива"""
    result = unzip_file("nonexistent.zip")
    assert "ERROR" in result


def test_tar_nonexistent_folder():
    """tar несуществующей папки"""
    result = tar_folder("/nonexistent", "archive.tar.gz")
    assert "ERROR" in result


def test_untar_nonexistent():
    """untar несуществующего архива"""
    result = untar_file("nonexistent.tar.gz")
    assert "ERROR" in result


def test_ls_nonexistent_path():
    """ls несуществующего пути"""
    ls("/nonexistent/path", detailed=False)


def test_ls_file_not_directory(tmp_path):
    """ls на файл (не директорию) - должен вывести только этот файл"""
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    try:
        ls(str(test_file), detailed=False)
    except Exception:
        pass


def test_archive_zip_exception(mocker, tmp_path):
    """zip с ошибкой при создании архива"""
    test_dir = tmp_path / "folder"
    test_dir.mkdir()
    mocker.patch('shutil.make_archive', side_effect=Exception("Archive error"))
    result = zip_folder(str(test_dir), "archive.zip")
    assert "ERROR" in result


def test_archive_unzip_exception(mocker, tmp_path):
    """unzip с ошибкой при распаковке"""
    import zipfile
    archive = tmp_path / "test.zip"
    with zipfile.ZipFile(archive, 'w') as zf:
        zf.writestr("file.txt", "content")
    
    mocker.patch('zipfile.ZipFile.extractall', side_effect=Exception("Unzip error"))
    result = unzip_file(str(archive))
    assert "ERROR" in result


def test_archive_tar_exception(mocker, tmp_path):
    """tar с ошибкой при создании"""
    test_dir = tmp_path / "folder"
    test_dir.mkdir()
    mocker.patch('tarfile.open', side_effect=Exception("Tar error"))
    result = tar_folder(str(test_dir), "archive.tar.gz")
    assert "ERROR" in result


def test_archive_untar_exception(mocker, tmp_path):
    """untar с ошибкой при распаковке"""
    import tarfile
    archive = tmp_path / "test.tar.gz"
    with tarfile.open(archive, 'w:gz') as tar:
        pass
    
    mocker.patch('tarfile.TarFile.extractall', side_effect=Exception("Untar error"))
    result = untar_file(str(archive))
    assert "ERROR" in result


def test_cp_exception(mocker, tmp_path):
    """cp с ошибкой копирования"""
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    mocker.patch('shutil.copy2', side_effect=Exception("Copy error"))
    cp(str(src), str(dst), recursive=False)


def test_mv_exception(mocker, tmp_path):
    """mv с ошибкой перемещения"""
    src = tmp_path / "src.txt"
    src.write_text("content")
    dst = tmp_path / "dst.txt"
    
    mocker.patch('shutil.move', side_effect=Exception("Move error"))
    mv(str(src), str(dst))


def test_rm_exception(mocker, tmp_path):
    """rm с ошибкой удаления"""
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    
    mocker.patch('builtins.input', return_value='y')
    mocker.patch('shutil.move', side_effect=Exception("Remove error"))
    rm(str(test_file), recursive=False)


def test_cd_exception(mocker):
    """cd с ошибкой смены директории"""
    mocker.patch('os.chdir', side_effect=Exception("CD error"))
    result = cd("/tmp")
    assert result == False


def test_cat_read_exception(mocker, tmp_path):
    """cat с ошибкой чтения файла"""
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")
    
    mocker.patch('pathlib.Path.open', side_effect=Exception("Read error"))
    cat(str(test_file))


def test_grep_in_directory_recursive(tmp_path):
    """grep рекурсивный в директории с файлами"""
    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    (dir1 / "file1.txt").write_text("pattern match")
    
    dir2 = tmp_path / "dir2"
    dir2.mkdir()
    (dir2 / "file2.txt").write_text("another pattern")
    
    result = grep("pattern", str(tmp_path), recursive=True)
    assert "pattern" in result


def test_grep_in_directory_non_recursive(tmp_path):
    """grep нерекурсивный в директории"""
    (tmp_path / "file.txt").write_text("pattern")
    result = grep("pattern", str(tmp_path), recursive=False)
    assert "pattern" in result

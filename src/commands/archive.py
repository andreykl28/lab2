import shutil
import zipfile
import tarfile
from pathlib import Path

def zip_folder(folder: str, archive_name: str) -> str:
    folder_path = Path(folder).expanduser().resolve()
    archive_path = Path(archive_name).expanduser().resolve()

    if not folder_path.is_dir():
        return f"ERROR: {folder} не является каталогом или не существует."

    try:
        shutil.make_archive(str(archive_path.with_suffix('')), 'zip', str(folder_path))
        return f"Архив {archive_name} успешно создан."
    except Exception as e:
        return f"ERROR: Ошибка создания архива zip: {e}"

def unzip_file(archive_name: str) -> str:
    archive_path = Path(archive_name).expanduser().resolve()

    if not archive_path.is_file():
        return f"ERROR: архив {archive_name} не найден."

    try:
        with zipfile.ZipFile(str(archive_path), 'r') as zip_ref:
            zip_ref.extractall('.')
        return f"Архив {archive_name} успешно распакован."
    except Exception as e:
        return f"ERROR: Ошибка распаковки архива zip: {e}"

def tar_folder(folder: str, archive_name: str) -> str:
    folder_path = Path(folder).expanduser().resolve()
    archive_path = Path(archive_name).expanduser().resolve()

    if not folder_path.is_dir():
        return f"ERROR: {folder} не является каталогом или не существует."

    try:
        with tarfile.open(str(archive_path), 'w:gz') as tar:
            tar.add(str(folder_path), arcname=folder_path.name)
        return f"Архив {archive_name} успешно создан."
    except Exception as e:
        return f"ERROR: Ошибка создания архива tar.gz: {e}"

def untar_file(archive_name: str) -> str:
    archive_path = Path(archive_name).expanduser().resolve()

    if not archive_path.is_file():
        return f"ERROR: архив {archive_name} не найден."

    try:
        with tarfile.open(str(archive_path), 'r:gz') as tar:
            tar.extractall('.')
        return f"Архив {archive_name} успешно распакован."
    except Exception as e:
        return f"ERROR: Ошибка распаковки архива tar.gz: {e}"

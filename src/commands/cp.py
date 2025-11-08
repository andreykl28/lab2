import shutil
from pathlib import Path

def cp(src: str, dst: str, recursive: bool = False) -> None:
    """
    Копирует файл или каталог.
    src: исходный путь
    dst: путь назначения
    recursive: если True — копирует каталог рекурсивно
    """
    src_path = Path(src).expanduser().resolve()
    dst_path = Path(dst).expanduser().resolve()

    if not src_path.exists():
        print(f"Ошибка: исходный файл/каталог '{src}' не найден.")
        return

    try:
        # Копирование директории
        if recursive:
            if not src_path.is_dir():
                print(f"Ошибка: флаг -r задан, но '{src}' — не каталог.")
                return
            shutil.copytree(src_path, dst_path)
        else:
            if src_path.is_dir():
                print(f"Ошибка: копирование каталога без -r не поддерживается.")
                return
            shutil.copy2(src_path, dst_path)
        print(f"Успешно скопировано '{src}' в '{dst}'")
    except Exception as e:
        print(f"Ошибка копирования: {e}")

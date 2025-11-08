import os
from pathlib import Path

def cd(path: str) -> bool:
    """Переход в указанный каталог. Возвращает True — успех/False — ошибка."""
    try:
        # Поддержка '~' — переход в домашнюю директорию
        if path == "~":
            new_dir = Path.home()
        else:
            new_dir = Path(path).expanduser().resolve()

        # Проверка на директорию
        if not new_dir.is_dir():
            print(f"Ошибка: {path} не является каталогом.")
            return False

        os.chdir(new_dir)
        return True
    except Exception as e:
        print(f"Ошибка перехода: {e}")
        return False

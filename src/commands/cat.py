from pathlib import Path

def cat(path: str) -> None:
    """
    Выводит содержимое файла в консоль.
    Если передан каталог или файл не существует — сообщает об ошибке.
    """
    # Преобразуем путь: раскрываем ~, делаем абсолютный
    file_path = Path(path).expanduser().resolve()

    # Проверяем существование
    if not file_path.exists():
        print(f"Ошибка: файл '{path}' не найден.")
        return

    # Проверяем, файл ли это
    if file_path.is_dir():
        print(f"Ошибка: '{path}' — это директория, а не файл.")
        return

    # Открываем файл — читаем и печатаем
    try:
        with file_path.open('r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        # Логирование ошибки здесь при желании

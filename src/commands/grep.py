from pathlib import Path
import re

def grep(pattern: str, path: str, recursive: bool = False, ignore_case: bool = False) -> str:
    search_path = Path(path).expanduser().resolve()

    if not search_path.exists():
        return f"ERROR: путь {path} не найден."

    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)

    results = []

    def search_file(file_path: Path):
        try:
            with file_path.open('r', encoding='utf-8') as f:
                for lineno, line in enumerate(f, 1):
                    if regex.search(line):
                        results.append(f"{file_path}: {lineno}: {line.strip()}")
        except Exception as e:
            results.append(f"ERROR: Не удалось прочитать файл {file_path}: {e}")

    if search_path.is_file():
        search_file(search_path)
    elif search_path.is_dir():
        if recursive:
            for file in search_path.rglob('*'):
                if file.is_file():
                    search_file(file)
        else:
            for file in search_path.iterdir():
                if file.is_file():
                    search_file(file)
    else:
        return f"ERROR: {path} не файл и не директория."

    if results:
        return '\n'.join(results)
    else:
        return "Нет совпадений"

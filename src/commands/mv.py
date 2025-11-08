import shutil
from pathlib import Path

def mv(src: str, dst: str):
    src_path = Path(src).expanduser().resolve()
    dst_path = Path(dst).expanduser().resolve()

    if not src_path.exists():
        print(f"Ошибка: исходный файл/каталог '{src}' не найден.")
        return

    try:
        # Если назначение - существующая папка, перемещаем внутрь!
        if dst_path.exists() and dst_path.is_dir():
            dst_path = dst_path / src_path.name

        shutil.move(str(src_path), str(dst_path))
        print(f"Успешно перемещено/переименовано '{src}' -> '{dst_path}'")
    except Exception as e:
        print(f"Ошибка перемещения/переименования: {e}")

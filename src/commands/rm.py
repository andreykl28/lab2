import shutil
from pathlib import Path

def rm(path: str, recursive=False):
    """Перемещает файл/каталог в .trash вместо удаления"""
    trash_dir = Path(".trash").resolve()
    trash_dir.mkdir(exist_ok=True)
    
    rm_path = Path(path).expanduser().resolve()
    
    # Запретить удаление корня и родителя
    if str(rm_path) == "/" or str(rm_path) == str(Path.cwd().parent):
        print("Ошибка: удаление корневого или родительского каталога запрещено!")
        return
    
    if not rm_path.exists():
        print(f"Ошибка: '{path}' не найден(а).")
        return
    
    try:
        if rm_path.is_dir():
            if not recursive:
                print("Ошибка: для удаления каталога нужен флаг -r.")
                return
            confirm = input(f"Удалить каталог '{rm_path}' со всем содержимым? (y/n): ").strip().lower()
            if confirm != "y":
                print("Операция отменена.")
                return
        
        # Перемещаем в корзину
        dst_path = trash_dir / rm_path.name
        shutil.move(str(rm_path), str(dst_path))
        print(f"Файл/каталог '{rm_path}' перемещён в .trash.")
    
    except Exception as e:
        print(f"Ошибка удаления: {e}")


def restore_from_trash(name: str):
    """Восстанавливает файл/каталог из .trash в текущую директорию"""
    trash_dir = Path(".trash").resolve()
    trash_path = trash_dir / name
    
    if not trash_path.exists():
        print(f"Ошибка восстановления: объект {name} не найден в .trash")
        return
    
    dst_path = Path.cwd() / name
    try:
        shutil.move(str(trash_path), str(dst_path))
        print(f"Объект '{name}' восстановлен из .trash.")
    except Exception as e:
        print(f"Ошибка восстановления: {e}")

import os
import stat
import time
from pathlib import Path

def ls(path: str = ".", detailed: bool = False) -> None:
    try:
        for item in Path(path).iterdir():
            full_path = str(item)
            if detailed:
                item_size = os.path.getsize(full_path)
                item_last_time = os.path.getmtime(full_path)
                item_formatted_time = time.strftime('%m-%d %H:%M', time.localtime(item_last_time))
                item_rules = os.stat(full_path)
                item_rules_form = stat.filemode(item_rules.st_mode)
                print(f'{item_rules_form} {item_size:10} {item_formatted_time} {item.name}')
            else:
                print(item.name)
    except FileNotFoundError:
        print(f"Ошибка: путь {path} не найден")
    except PermissionError:
        print(f"Нет доступа к {path}")

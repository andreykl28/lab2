import os

HISTORY_FILE = ".history"

def add_history(cmd: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(cmd + "\n")

def get_history(n=10):
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines[-n:]]

def pop_last():
    if not os.path.exists(HISTORY_FILE):
        return None
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return None
    last = lines[-1].strip()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines[:-1])
    return last

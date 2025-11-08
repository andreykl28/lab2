from datetime import datetime

def write_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("shell.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

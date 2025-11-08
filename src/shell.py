from pathlib import Path
from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp


class Shell:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.running = True

    def run(self):
        print("Запущен. Введите 'exit' для выхода")
        print(f"Текущая директория {self.current_dir}")
        while self.running:
            try:
                command_input = input("Shell> ").strip()
                if not command_input:
                    continue
                self.execute_command(command_input)
            except KeyboardInterrupt:
                print("\nExit")
                self.running = False
            except Exception as e:
                print(f"Err: {e}")

    def execute_command(self, command_input: str):
        parts = command_input.split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]
        if command == "exit":
            print("\nExit")
            self.running = False
        elif command == "ls":
            self.cmd_ls(args)
        elif command == "cd":
            self.cmd_cd(args)
        elif command == "cat":
            self.cmd_cat(args)
        elif command == "cp":
            self.cmd_cp(args)
        else:
            print(f"Неизвестная команда {command}")

    def cmd_ls(self, args: list[str]):
        detailed = False
        path = "."
        allowed_flags = {"-l"}
        unknown_flags = []
        
        for arg in args:
            if arg == "-l":
                detailed = True
            elif arg.startswith("-"):
                # Проверка на неизвестные флаги
                if arg not in allowed_flags:
                    unknown_flags.append(arg)
            else:
                path = arg

        if unknown_flags:
            print(f"Ошибка: не поддерживаемые флаги: {' '.join(unknown_flags)}")
            return

        ls(path, detailed)
    def cmd_cd(self, args: list[str]):
        # Если аргументов нет — переход в домашнюю директорию
        if not args:
            path = "~"
        else:
            path = args[0]
        success = cd(path)
        # Меняем текущую директорию в prompt при успехе
        self.current_dir = Path.cwd()
    def cmd_cat(self, args: list[str]):
        if not args:
            print("Ошибка: укажите имя файла для cat")
            return
        cat(args[0])
    def cmd_cp(self, args: list[str]):
        recursive = False
        src = dst = None
        filtered_args = []

        for arg in args:
            if arg == "-r":
                recursive = True
            elif not arg.startswith("-"):
                filtered_args.append(arg)

        if len(filtered_args) != 2:
            print("Ошибка: команда cp требует два имени (src, dst).")
            return

        src, dst = filtered_args
        cp(src, dst, recursive)
from pathlib import Path
from src.commands.ls import ls
from src.commands.cd import cd
from src.commands.cat import cat
from src.commands.cp import cp
from src.commands.rm import rm, restore_from_trash
from src.commands.mv import mv
from src.commands.archive import zip_folder, unzip_file, tar_folder, untar_file
from src.commands.grep import grep
from src.utils.logger import write_log
from src.utils.history import add_history, get_history, pop_last

def cmd_history(self, args: list[str]):
    n = 10
    if args and args[0].isdigit():
        n = int(args[0])
    hist = get_history(n)
    for i, line in enumerate(hist, 1):
        print(f"{i}: {line}")


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
        write_log(command_input)
        parts = command_input.split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]
        if command not in ["history", "undo"]:
            add_history(command_input)

        try:
            if command == "exit":
                print("\nExit")
                write_log("SUCCESS: Выход из оболочки")
                self.running = False
            elif command == "ls":
                self.cmd_ls(args)
                write_log("SUCCESS: ls выполнена")
            elif command == "cd":
                self.cmd_cd(args)
                write_log("SUCCESS: cd выполнена")
            elif command == "cat":
                self.cmd_cat(args)
                write_log("SUCCESS: cat выполнена")
            elif command == "cp":
                self.cmd_cp(args)
                write_log("SUCCESS: cp выполнена")
            elif command == "mv":
                self.cmd_mv(args)
                write_log("SUCCESS: mv выполнена")
            elif command == "rm":
                self.cmd_rm(args)
                write_log("SUCCESS: rm выполнена")
            elif command == "zip":
                self.cmd_zip(args)
                write_log("SUCCESS: zip выполнена")
            elif command == "unzip":
                self.cmd_unzip(args)
                write_log("SUCCESS: unzip выполнена")
            elif command == "tar":
                self.cmd_tar(args)
                write_log("SUCCESS: tar выполнена")
            elif command == "untar":
                self.cmd_untar(args)
                write_log("SUCCESS: untar выполнена")
            elif command == "grep":
                self.cmd_grep(args)
                write_log("SUCCESS: grep выполнена")
            elif command == "undo":
                self.cmd_undo(args)
            elif command == "history":
                self.cmd_history(args)
            else:
                error = f"Неизвестная команда {command}"
                print(error)
                write_log(f"ERROR: {error}")
        except Exception as e:
            error = f"Ошибка выполнения: {str(e)}"
            print(error)
            write_log(f"ERROR: {error}")

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
            error_msg = f"Ошибка: не поддерживаемые флаги: {' '.join(unknown_flags)}"
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        
        write_log(f"ls {'-l' if detailed else ''}{path}".strip())
        ls(path, detailed)

    def cmd_cd(self, args: list[str]):
        # Если аргументов нет - переход в домашнюю директорию
        if not args:
            path = "~"
        else:
            path = args[0]
        success = cd(path)
        if success:
            write_log(f"cd {path} - SUCCESS")
            # Меняем текущую директорию в prompt при успехе
            self.current_dir = Path.cwd()
        else:
            error_msg = f"cd {path} - ERROR: Не удалось сменить директорию"
            write_log(error_msg)
            print(error_msg)

    def cmd_cat(self, args: list[str]):
        if not args:
            error = "Ошибка: укажите имя файла для cat"
            print(error)
            write_log(f"ERROR: {error}")
            return
        result = cat(args[0])
        print(result)
        write_log(result)

    def cmd_cp(self, args: list[str]):
        allowed_flags = {"-r"}
        unknown_flags = []
        recursive = False
        filtered_args = []
        for arg in args:
            if arg == "-r":
                recursive = True
            elif arg.startswith("-"):
                if arg not in allowed_flags:
                    unknown_flags.append(arg)
            else:
                filtered_args.append(arg)
        if unknown_flags:
            error_msg = f"Ошибка: не поддерживаемые флаги: {' '.join(unknown_flags)}"
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        if len(filtered_args) != 2:
            error_msg = "Ошибка: команда cp требует два имени (src, dst)."
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        src, dst = filtered_args

        log_cmd = f"cp {'-r ' if recursive else ''}{src} {dst}".strip()
        write_log(log_cmd)
        cp(src, dst, recursive)

    def cmd_rm(self, args: list[str]):
        allowed_flags = {"-r"}
        unknown_flags = []
        recursive = False
        path = None
        for arg in args:
            if arg == "-r":
                recursive = True
            elif arg.startswith("-"):
                if arg not in allowed_flags:
                    unknown_flags.append(arg)
            else:
                path = arg
        if unknown_flags:
            error_msg = f"Ошибка: не поддерживаемые флаги: {' '.join(unknown_flags)}"
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        if not path:
            error_msg = "Ошибка: укажите путь для удаления!"
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        
        log_cmd = f"rm {'-r ' if recursive else ''}{path}".strip()
        write_log(log_cmd)
        rm(path, recursive)
        write_log(f"SUCCESS: команда rm выполнена")

    def cmd_mv(self, args: list[str]):
        filtered_args = []
        unknown_flags = []
        for arg in args:
            if arg.startswith("-"):
                unknown_flags.append(arg)
            else:
                filtered_args.append(arg)
        if unknown_flags:
            error_msg = f"Ошибка: команда mv не поддерживает флаги: {' '.join(unknown_flags)}"
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        if len(filtered_args) != 2:
            error_msg = "Ошибка: команда mv требует два имени (src, dst)."
            print(error_msg)
            write_log(f"ERROR: {error_msg}")
            return
        src, dst = filtered_args
        write_log(f"mv {src} {dst}")
        mv(src, dst)

    def cmd_zip(self, args: list[str]):
        if len(args) != 2:
            msg = "Ошибка: zip требует 2 аргумента: папка и имя архива.zip"
            print(msg)
            write_log(f"ERROR: {msg}")
            return
        folder, archive = args
        write_log(f"zip {folder} {archive}")
        result = zip_folder(folder, archive)
        print(result)
        write_log(result)

    def cmd_unzip(self, args: list[str]):
        if len(args) != 1:
            msg = "Ошибка: unzip требует 1 аргумент: имя архива.zip"
            print(msg)
            write_log(f"ERROR: {msg}")
            return
        archive = args[0]
        write_log(f"unzip {archive}")
        result = unzip_file(archive)
        print(result)
        write_log(result)

    def cmd_tar(self, args: list[str]):
        if len(args) != 2:
            msg = "Ошибка: tar требует 2 аргумента: папка и имя архива.tar.gz"
            print(msg)
            write_log(f"ERROR: {msg}")
            return
        folder, archive = args
        write_log(f"tar {folder} {archive}")
        result = tar_folder(folder, archive)
        print(result)
        write_log(result)

    def cmd_untar(self, args: list[str]):
        if len(args) != 1:
            msg = "Ошибка: untar требует 1 аргумент: имя архива.tar.gz"
            print(msg)
            write_log(f"ERROR: {msg}")
            return
        archive = args[0]
        write_log(f"untar {archive}")
        result = untar_file(archive)
        print(result)
        write_log(result)

    def cmd_grep(self, args: list[str]):
        allowed_flags = {"-r", "-1"}
        recursive = False
        ignore_case = False
        unknown_flags = []
        non_flag_args = []

        for arg in args:
            if arg in allowed_flags:
                if arg == "-r": recursive = True
                if arg == "-1": ignore_case = True
            elif arg.startswith("-"):
                unknown_flags.append(arg)
            else:
                non_flag_args.append(arg)

        if len(non_flag_args) < 2:
            msg = "Ошибка: grep требует шаблон и путь для поиска"
            print(msg)
            write_log(f"ERROR: {msg}")
            return

        # pattern — объединить все кроме последнего
        pattern = " ".join(non_flag_args[:-1])
        path = non_flag_args[-1]

        if unknown_flags:
            msg = f"Ошибка: не поддерживаемые флаги: {' '.join(unknown_flags)}"
            print(msg)
            write_log(f"ERROR: {msg}")
            return

        log_cmd = f"grep {'-r ' if recursive else ''}{'-1 ' if ignore_case else ''}\"{pattern}\" {path}"
        write_log(log_cmd)

        result = grep(pattern, path, recursive, ignore_case)
        print(result)
        write_log(result)
    def cmd_history(self, args: list[str]):
        n = 10
        if args and args[0].isdigit():
            n = int(args[0])
        hist = get_history(n)
        for i, line in enumerate(hist, 1):
            print(f"{i}: {line}")

    def cmd_undo(self, args: list[str]):
        last = pop_last()
        if last is None:
            print("Нет команд для отмены")
            write_log("ERROR: Нет команд для отмены")
            return
        
        parts = last.split()
        if len(parts) < 2:
            print(f"Команду '{last}' нельзя отменить")
            write_log(f"ERROR: Команду '{last}' нельзя отменить")
            return
        
        cmd = parts[0]
        
        if cmd == "cp":
            # cp src dst: удаляем dst
            dst = parts[-1]
            if Path(dst).exists():
                print(f"Undo cp: удаление {dst}")
                write_log(f"Undo cp: удаление {dst}")
                rm(dst, recursive=True)
            else:
                print(f"Undo cp: {dst} не найден")
                write_log(f"ERROR: Undo cp: {dst} не найден")
        
        elif cmd == "mv":
            # mv src dst: возвращаем обратно
            src = parts[1]
            dst = parts[-1]
            if Path(dst).exists():
                print(f"Undo mv: возвращаем {dst} -> {src}")
                write_log(f"Undo mv: возвращаем {dst} -> {src}")
                mv(dst, src)
            else:
                print(f"Undo mv: {dst} не найден")
                write_log(f"ERROR: Undo mv: {dst} не найден")
        
        elif cmd == "rm":
            # rm path: восстановление из .trash
            path = parts[-1]
            name = Path(path).name
            print(f"Undo rm: восстановление {name} из .trash")
            write_log(f"Undo rm: восстановление {name} из .trash")
            restore_from_trash(name)
        
        else:
            print(f"Команду '{last}' нельзя отменить")
            write_log(f"ERROR: Команду '{last}' нельзя отменить")


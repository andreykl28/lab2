# Лабораторная работа №2

# Эмулятор командной оболочки UNIX в виртуальной файловой системе.

Структура проекта


├── lab02_shell_emulator

│   ├── src/

│   │   ├── __init__.py

│   │   ├── main.py

│   │   ├── shell.py

│   │   ├── commands/

│   │   │   ├── __init__.py

│   │   │   ├── ls.py

│   │   │   ├── cd.py

│   │   │   ├── cat.py

│   │   │   ├── cp.py

│   │   │   ├── mv.py

│   │   │   ├── rm.py

│   │   │   ├── grep.py

│   │   │   └── archive.py

│   │   ├── utils/

│   │   │   ├── __init__.py

│   │   │   ├── logger.py

│   │   │   └── history.py

│   │   └── constants.py

│   ├── tests/

│   │   ├── __init__.py

│   │   ├── conftest.py

│   │   ├── test_commands.py

│   │   └── test_shell.py

│   ├── .gitignore

│   ├── requirements.txt

│   └── README.md


# Установка зависимостей
pip install -r requirements.txt

# Запуск эмулятора
python3 src/main.py

# Запуск тестов
pytest tests/ -v

# Проверка покрытия кода
pytest --cov=src --cov-report=term-missing tests/ -v

Поддерживаемые команды

Базовые файловые операции

ls [path] [-l] — вывод содержимого директории

cd [path] — смена текущей директории

cat <file> — вывод содержимого файла

cp <src> <dst> [-r] — копирование файла/директории

mv <src> <dst> — перемещение/переименование

rm <path> [-r] — удаление (перемещает в .trash)

Работа с архивами
zip <folder> <archive.zip> — создание ZIP-архива

unzip <archive.zip> — распаковка ZIP-архива

tar <folder> <archive.tar.gz> — создание TAR.GZ-архива

untar <archive.tar.gz> — распаковка TAR.GZ-архива

Поиск
grep <pattern> <path> [-r] [-1] — поиск строк по шаблону

-r — рекурсивный поиск

-1 — без учёта регистра

История и отмена
history [N] — последние N команд

undo — отмена последней команды

Системные
exit — выход

Формат ввода и вывода
Ввод: команда с аргументами через пробелы
Вывод: результат или ошибка

Ввод: ls -l
Вывод: file1.txt    1024 bytes

Ввод: grep "pattern" file.txt
Вывод: file.txt: 1: pattern match found
Алгоритм работы
Логирование: запись в shell.log

История: сохраняется в .history

Корзина: удаление через .trash

Undo: отмена cp/mv/rm

Принятые решения
Работа с реальной ФС

Удаление через корзину

Централизованное логирование

Изоляция тестов через моки

Допущения
Разделители: пробелы

Пути: относительные/абсолютные

Флаги: проверка допустимых

Ошибки: логирование без выполнения

Тестирование
Фреймворк: pytest, pytest-mock, pytest-cov

Покрытие: ~87%

Тесты: команды, ошибки, edge cases

pytest tests/ -v
pytest --cov=src --cov-report=html tests/
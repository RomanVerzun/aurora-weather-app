@echo off
REM Скрипт для запуску застосунку погоди для Windows

REM Перевіряємо наявність віртуального середовища
IF NOT EXIST .venv (
    echo "Віртуальне середовище не знайдено. Створюємо..."
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
)

REM Запускаємо застосунок
.venv\Scripts\python src\main.py %*

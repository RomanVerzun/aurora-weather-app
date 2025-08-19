#!/usr/bin/env bash
# Скрипт для запуску застосунку погоди

# Перевіряємо наявність віртуального середовища
if [ ! -d ".venv" ]; then
    echo "⚠️  Віртуальне середовище не знайдено. Створюємо..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

# Запускаємо застосунок
.venv/bin/python src/main.py "$@"

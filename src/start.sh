#!/bin/bash

cd "$(dirname "$0")"

# Имя screen-сессии
session_name="tgbot_anonymous_contact"

# Путь к файлу Python-скрипта
python_script="main.py"

# Создаем новую screen-сессию
screen -S "$session_name" -dm bash -c '

    # Запускаем Python-скрипт
    /home/confi/.local/bin/poetry run python3 "'"$python_script"'"
'

echo "Screen session '$session_name' создана и запущена."
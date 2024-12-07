#!/bin/sh

# Установка зависимостей
echo "Установка зависимостей..."
pip install -r requirements.txt

# Запуск приложения
echo "Запуск приложения..."
python main.py
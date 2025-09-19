#!/bin/bash

# Скрипт для установки системных зависимостей WeasyPrint
# Используется в Docker контейнерах

echo "Установка системных зависимостей для WeasyPrint..."

# Обновляем список пакетов
apt-get update -y

# Устанавливаем основные зависимости
apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libgobject-2.0-0 \
    libglib2.0-0 \
    libfontconfig1 \
    libcairo2 \
    libpangocairo-1.0-0 \
    libcairo-gobject2 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info

# Дополнительные зависимости для стабильной работы
apt-get install -y \
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig

# Очищаем кэш для экономии места
apt-get clean
rm -rf /var/lib/apt/lists/*

echo "Зависимости установлены успешно!"

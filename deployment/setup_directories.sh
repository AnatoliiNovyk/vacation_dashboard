#!/bin/bash

# Скрипт для створення структури директорій для продакшн розгортання
# Використання: sudo ./setup_directories.sh

set -e

echo "🚀 Створення структури директорій для Vacation Dashboard..."

# Основна директорія додатку
APP_DIR="/opt/vacation-dashboard"
DATA_DIR="/var/lib/vacation-dashboard"
LOG_DIR="/var/log/vacation-dashboard"
CONFIG_DIR="/etc/vacation-dashboard"
BACKUP_DIR="/var/backups/vacation-dashboard"
SYSTEMD_DIR="/etc/systemd/system"

# Створення директорій
echo "📁 Створення директорій..."
mkdir -p $APP_DIR
mkdir -p $DATA_DIR
mkdir -p $LOG_DIR
mkdir -p $CONFIG_DIR
mkdir -p $BACKUP_DIR
mkdir -p /var/run/vacation-dashboard

# Створення користувача для додатку
echo "👤 Створення користувача vacation-dashboard..."
if ! id "vacation-dashboard" &>/dev/null; then
    useradd --system --home $APP_DIR --shell /bin/bash vacation-dashboard
fi

# Встановлення прав доступу
echo "🔒 Налаштування прав доступу..."
chown -R vacation-dashboard:vacation-dashboard $APP_DIR
chown -R vacation-dashboard:vacation-dashboard $DATA_DIR
chown -R vacation-dashboard:vacation-dashboard $LOG_DIR
chown -R vacation-dashboard:vacation-dashboard $BACKUP_DIR
chown -R vacation-dashboard:vacation-dashboard /var/run/vacation-dashboard

# Права для конфігурації (читання для всіх, запис тільки для root)
chown -R root:vacation-dashboard $CONFIG_DIR
chmod -R 640 $CONFIG_DIR

echo "✅ Структура директорій створена успішно!"
echo ""
echo "📋 Створені директорії:"
echo "   Додаток:        $APP_DIR"
echo "   Дані:          $DATA_DIR"
echo "   Логи:          $LOG_DIR"
echo "   Конфігурація:  $CONFIG_DIR"
echo "   Бекапи:        $BACKUP_DIR"
echo ""
echo "🔧 Наступні кроки:"
echo "1. Скопіюйте файли проекту в $APP_DIR"
echo "2. Створіть .env файл в $CONFIG_DIR"
echo "3. Встановіть systemd сервіс"
echo "4. Налаштуйте nginx"
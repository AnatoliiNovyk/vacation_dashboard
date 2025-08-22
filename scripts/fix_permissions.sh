#!/bin/bash

# Скрипт для виправлення прав доступу
echo "🔧 Виправлення прав доступу..."

# Створення користувача якщо не існує
if ! id "vacation-dashboard" &>/dev/null; then
    echo "👤 Створення користувача vacation-dashboard..."
    useradd --system --home /opt/vacation-dashboard --shell /bin/bash vacation-dashboard
fi

# Створення директорій
mkdir -p /opt/vacation-dashboard
mkdir -p /var/lib/vacation-dashboard
mkdir -p /var/log/vacation-dashboard
mkdir -p /etc/vacation-dashboard
mkdir -p /var/run/vacation-dashboard

# Встановлення прав
chown -R vacation-dashboard:vacation-dashboard /opt/vacation-dashboard
chown -R vacation-dashboard:vacation-dashboard /var/lib/vacation-dashboard
chown -R vacation-dashboard:vacation-dashboard /var/log/vacation-dashboard
chown -R vacation-dashboard:vacation-dashboard /var/run/vacation-dashboard

# Права для конфігурації
chown -R root:vacation-dashboard /etc/vacation-dashboard
chmod -R 640 /etc/vacation-dashboard

# Виконувані файли
chmod +x /opt/vacation-dashboard/scripts/*.sh 2>/dev/null || true

echo "✅ Права доступу виправлено!"
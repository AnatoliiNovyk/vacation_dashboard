#!/bin/bash

# Скрипт автоматичного розгортання Vacation Dashboard в Ubuntu 24.04
# Використання: sudo ./install.sh

set -e

echo "🚀 Початок розгортання Vacation Dashboard..."

# Перевірка прав root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Цей скрипт повинен запускатися з правами root (sudo)" 
   exit 1
fi

# Оновлення системи
echo "📦 Оновлення системи..."
apt update && apt upgrade -y

# Встановлення необхідних пакетів
echo "📦 Встановлення залежностей..."
apt install -y python3 python3-pip python3-venv nginx sqlite3 curl git logrotate fail2ban ufw

# Створення структури директорій
echo "📁 Створення структури директорій..."
./setup_directories.sh

# Клонування або копіювання проекту
APP_DIR="/opt/vacation-dashboard"
echo "📥 Копіювання файлів проекту..."

# Якщо файли ще не скопійовані, створюємо базову структуру
if [ ! -f "$APP_DIR/app.py" ]; then
    echo "⚠️  Файли проекту не знайдені в $APP_DIR"
    echo "   Будь ласка, скопіюйте файли проекту в $APP_DIR"
    echo "   Або вкажіть шлях до проекту:"
    read -p "Шлях до проекту (або Enter для пропуску): " PROJECT_PATH
    
    if [ ! -z "$PROJECT_PATH" ] && [ -d "$PROJECT_PATH" ]; then
        cp -r $PROJECT_PATH/* $APP_DIR/
        chown -R vacation-dashboard:vacation-dashboard $APP_DIR
    fi
fi

# Створення віртуального середовища
echo "🐍 Створення віртуального середовища Python..."
cd $APP_DIR
sudo -u vacation-dashboard python3 -m venv venv
sudo -u vacation-dashboard $APP_DIR/venv/bin/pip install --upgrade pip

# Встановлення залежностей Python
if [ -f "$APP_DIR/requirements.txt" ]; then
    echo "📦 Встановлення Python залежностей..."
    sudo -u vacation-dashboard $APP_DIR/venv/bin/pip install -r requirements.txt
fi

# Створення конфігураційного файлу
echo "⚙️  Створення конфігурації..."
if [ ! -f "/etc/vacation-dashboard/.env" ]; then
    cp $APP_DIR/.env.example /etc/vacation-dashboard/.env
    
    # Генерація секретного ключа
    SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
    sed -i "s/your-super-secret-key-here-change-this-in-production/$SECRET_KEY/" /etc/vacation-dashboard/.env
    
    # Налаштування шляхів
    sed -i "s|sqlite:///data/vacations.db|sqlite:///var/lib/vacation-dashboard/vacations.db|" /etc/vacation-dashboard/.env
    sed -i "s|logs/app.log|/var/log/vacation-dashboard/app.log|" /etc/vacation-dashboard/.env
    
    chmod 640 /etc/vacation-dashboard/.env
    chown root:vacation-dashboard /etc/vacation-dashboard/.env
fi

# Ініціалізація бази даних
echo "🗄️  Ініціалізація бази даних..."
cd $APP_DIR
sudo -u vacation-dashboard FLASK_ENV=production $APP_DIR/venv/bin/python -c "
import sys
sys.path.append('$APP_DIR')
from data.db_operations import _init_db
_init_db()
print('База даних ініціалізована')
"

# Встановлення systemd сервісу
echo "🔧 Налаштування systemd сервісу..."
cp deployment/vacation-dashboard.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable vacation-dashboard

# Налаштування nginx
echo "🌐 Налаштування nginx..."
cp deployment/nginx-site.conf /etc/nginx/sites-available/vacation-dashboard
ln -sf /etc/nginx/sites-available/vacation-dashboard /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Тестування конфігурації nginx
nginx -t

# Налаштування logrotate
echo "📋 Налаштування ротації логів..."
cat > /etc/logrotate.d/vacation-dashboard << 'EOF'
/var/log/vacation-dashboard/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 vacation-dashboard vacation-dashboard
    postrotate
        systemctl reload vacation-dashboard
    endscript
}
EOF

# Налаштування fail2ban
echo "🛡️  Налаштування fail2ban..."
cat > /etc/fail2ban/jail.d/vacation-dashboard.conf << 'EOF'
[vacation-dashboard]
enabled = true
port = http,https
filter = vacation-dashboard
logpath = /var/log/vacation-dashboard/app.log
maxretry = 5
bantime = 3600
findtime = 600
EOF

cat > /etc/fail2ban/filter.d/vacation-dashboard.conf << 'EOF'
[Definition]
failregex = ^.*failed_login_attempt.*IP: <HOST>.*$
ignoreregex =
EOF

# Налаштування firewall
echo "🔥 Налаштування firewall..."
ufw --force enable
ufw allow ssh
ufw allow 'Nginx Full'

# Налаштування cron для бекапів
echo "💾 Налаштування автоматичних бекапів..."
(crontab -l 2>/dev/null; echo "0 2 * * * $APP_DIR/scripts/backup.sh") | crontab -

# Запуск сервісів
echo "🚀 Запуск сервісів..."
systemctl start vacation-dashboard
systemctl restart nginx
systemctl restart fail2ban

# Перевірка статусу
echo "✅ Перевірка статусу сервісів..."
systemctl is-active --quiet vacation-dashboard && echo "✅ Vacation Dashboard: Активний" || echo "❌ Vacation Dashboard: Неактивний"
systemctl is-active --quiet nginx && echo "✅ Nginx: Активний" || echo "❌ Nginx: Неактивний"

echo ""
echo "🎉 Розгортання завершено!"
echo ""
echo "📋 Інформація про систему:"
echo "   Додаток:        /opt/vacation-dashboard"
echo "   Конфігурація:   /etc/vacation-dashboard/.env"
echo "   Логи:          /var/log/vacation-dashboard/"
echo "   База даних:    /var/lib/vacation-dashboard/vacations.db"
echo "   Бекапи:        /var/backups/vacation-dashboard/"
echo ""
echo "🔧 Наступні кроки:"
echo "1. Налаштуйте SSL сертифікати"
echo "2. Змініть домен в /etc/nginx/sites-available/vacation-dashboard"
echo "3. Перезапустіть nginx: sudo systemctl reload nginx"
echo "4. Перевірте роботу: curl -I http://localhost"
echo ""
echo "📊 Корисні команди:"
echo "   Статус:        sudo systemctl status vacation-dashboard"
echo "   Логи:          sudo journalctl -u vacation-dashboard -f"
echo "   Перезапуск:    sudo systemctl restart vacation-dashboard"
echo "   Health check:  sudo python3 $APP_DIR/scripts/health_check.py"
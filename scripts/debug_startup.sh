#!/bin/bash

# Скрипт для діагностики проблем запуску
echo "🔍 Діагностика проблем запуску..."

echo "1. Перевірка користувача:"
id vacation-dashboard || echo "❌ Користувач не існує"

echo -e "\n2. Перевірка директорій:"
ls -la /opt/vacation-dashboard/ | head -10
ls -la /var/lib/vacation-dashboard/
ls -la /var/log/vacation-dashboard/

echo -e "\n3. Перевірка Python середовища:"
sudo -u vacation-dashboard /opt/vacation-dashboard/venv/bin/python --version || echo "❌ Python venv проблема"

echo -e "\n4. Перевірка залежностей:"
sudo -u vacation-dashboard /opt/vacation-dashboard/venv/bin/pip list | grep -E "(dash|flask|pandas)" || echo "❌ Залежності не встановлені"

echo -e "\n5. Тест запуску додатку:"
cd /opt/vacation-dashboard
sudo -u vacation-dashboard FLASK_ENV=development /opt/vacation-dashboard/venv/bin/python -c "
import sys
sys.path.append('/opt/vacation-dashboard')
try:
    from app import app
    print('✅ Додаток імпортується успішно')
except Exception as e:
    print(f'❌ Помилка імпорту: {e}')
    import traceback
    traceback.print_exc()
"

echo -e "\n6. Перевірка портів:"
netstat -tlnp | grep :8050 || echo "ℹ️ Порт 8050 вільний"

echo -e "\n7. Перевірка конфігурації:"
if [ -f "/etc/vacation-dashboard/.env" ]; then
    echo "✅ .env файл існує"
    sudo -u vacation-dashboard cat /etc/vacation-dashboard/.env | grep -v SECRET_KEY
else
    echo "❌ .env файл не знайдено"
fi

echo -e "\n8. Останні логи systemd:"
journalctl -u vacation-dashboard.service -n 20 --no-pager
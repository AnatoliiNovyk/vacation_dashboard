#!/bin/bash

# Скрипт для налаштування SSL сертифікатів
# Використання: sudo ./ssl_setup.sh your-domain.com

set -e

DOMAIN=${1:-"vacation-dashboard.local"}

echo "🔒 Налаштування SSL для домену: $DOMAIN"

# Перевірка наявності certbot
if ! command -v certbot &> /dev/null; then
    echo "📦 Встановлення certbot..."
    apt update
    apt install -y certbot python3-certbot-nginx
fi

# Отримання SSL сертифіката від Let's Encrypt
echo "📜 Отримання SSL сертифіката..."
if [[ $DOMAIN == *.local ]] || [[ $DOMAIN == localhost ]]; then
    echo "⚠️  Локальний домен виявлено. Створення самопідписаного сертифіката..."
    
    # Створення самопідписаного сертифіката для розробки
    mkdir -p /etc/ssl/private /etc/ssl/certs
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/ssl/private/vacation-dashboard.key \
        -out /etc/ssl/certs/vacation-dashboard.crt \
        -subj "/C=UA/ST=Ukraine/L=City/O=Organization/CN=$DOMAIN"
    
    chmod 600 /etc/ssl/private/vacation-dashboard.key
    chmod 644 /etc/ssl/certs/vacation-dashboard.crt
    
    echo "✅ Самопідписаний сертифікат створено"
else
    # Отримання сертифіката від Let's Encrypt
    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    echo "✅ SSL сертифікат від Let's Encrypt отримано"
fi

# Оновлення конфігурації nginx з правильним доменом
sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/vacation-dashboard

# Тестування та перезапуск nginx
nginx -t
systemctl reload nginx

echo "🎉 SSL налаштовано успішно для $DOMAIN"
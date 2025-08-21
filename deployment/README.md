# Розгортання Vacation Dashboard в Ubuntu 24.04

## Рекомендована структура директорій

```
/opt/vacation-dashboard/          # Основний код додатку
├── app.py                        # Головний файл додатку
├── requirements.txt              # Python залежності
├── venv/                         # Віртуальне середовище Python
├── data/                         # Модулі роботи з даними
├── components/                   # UI компоненти
├── utils/                        # Утиліти
└── scripts/                      # Скрипти обслуговування

/etc/vacation-dashboard/          # Конфігураційні файли
└── .env                          # Змінні середовища

/var/lib/vacation-dashboard/      # Дані додатку
└── vacations.db                  # База даних SQLite

/var/log/vacation-dashboard/      # Логи
├── app.log                       # Логи додатку
├── access.log                    # Логи доступу
└── error.log                     # Логи помилок

/var/backups/vacation-dashboard/  # Резервні копії
└── vacations_backup_*.db         # Бекапи бази даних
```

## Автоматичне розгортання

1. **Завантажте скрипти розгортання:**
```bash
# Створіть директорію для скриптів
mkdir -p ~/vacation-dashboard-deploy
cd ~/vacation-dashboard-deploy

# Скопіюйте всі файли з папки deployment/
```

2. **Зробіть скрипти виконуваними:**
```bash
chmod +x *.sh
```

3. **Запустіть автоматичне встановлення:**
```bash
sudo ./install.sh
```

4. **Скопіюйте файли проекту:**
```bash
# Якщо файли проекту в ~/my-project/
sudo cp -r ~/my-project/* /opt/vacation-dashboard/
sudo chown -R vacation-dashboard:vacation-dashboard /opt/vacation-dashboard
```

5. **Налаштуйте SSL:**
```bash
# Для продакшн домену
sudo ./ssl_setup.sh your-domain.com

# Для локального тестування
sudo ./ssl_setup.sh vacation-dashboard.local
```

## Ручне розгортання

### 1. Підготовка системи
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx sqlite3 git
```

### 2. Створення користувача
```bash
sudo useradd --system --home /opt/vacation-dashboard --shell /bin/bash vacation-dashboard
```

### 3. Створення директорій
```bash
sudo mkdir -p /opt/vacation-dashboard
sudo mkdir -p /var/lib/vacation-dashboard
sudo mkdir -p /var/log/vacation-dashboard
sudo mkdir -p /etc/vacation-dashboard
sudo mkdir -p /var/backups/vacation-dashboard
```

### 4. Налаштування прав
```bash
sudo chown -R vacation-dashboard:vacation-dashboard /opt/vacation-dashboard
sudo chown -R vacation-dashboard:vacation-dashboard /var/lib/vacation-dashboard
sudo chown -R vacation-dashboard:vacation-dashboard /var/log/vacation-dashboard
sudo chown -R vacation-dashboard:vacation-dashboard /var/backups/vacation-dashboard
```

### 5. Копіювання файлів проекту
```bash
sudo cp -r /path/to/your/project/* /opt/vacation-dashboard/
sudo chown -R vacation-dashboard:vacation-dashboard /opt/vacation-dashboard
```

### 6. Встановлення Python залежностей
```bash
cd /opt/vacation-dashboard
sudo -u vacation-dashboard python3 -m venv venv
sudo -u vacation-dashboard ./venv/bin/pip install -r requirements.txt
```

### 7. Конфігурація
```bash
sudo cp .env.example /etc/vacation-dashboard/.env
sudo nano /etc/vacation-dashboard/.env  # Відредагуйте конфігурацію
```

### 8. Systemd сервіс
```bash
sudo cp deployment/vacation-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vacation-dashboard
sudo systemctl start vacation-dashboard
```

### 9. Nginx
```bash
sudo cp deployment/nginx-site.conf /etc/nginx/sites-available/vacation-dashboard
sudo ln -s /etc/nginx/sites-available/vacation-dashboard /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## Перевірка роботи

```bash
# Статус сервісів
sudo systemctl status vacation-dashboard
sudo systemctl status nginx

# Логи
sudo journalctl -u vacation-dashboard -f
sudo tail -f /var/log/vacation-dashboard/app.log

# Health check
sudo python3 /opt/vacation-dashboard/scripts/health_check.py

# Тест HTTP
curl -I http://localhost
curl -I https://your-domain.com
```

## Обслуговування

### Оновлення додатку
```bash
cd /opt/vacation-dashboard
sudo systemctl stop vacation-dashboard
# Оновіть файли
sudo systemctl start vacation-dashboard
```

### Резервне копіювання
```bash
sudo /opt/vacation-dashboard/scripts/backup.sh
```

### Перегляд логів
```bash
sudo tail -f /var/log/vacation-dashboard/app.log
sudo journalctl -u vacation-dashboard -f
```

### Моніторинг ресурсів
```bash
sudo htop
sudo df -h
sudo du -sh /var/lib/vacation-dashboard/
```

## Безпека

- Firewall налаштовано через UFW
- Fail2ban захищає від брутфорс атак
- SSL сертифікати для HTTPS
- Обмеження швидкості в nginx
- Ізольований користувач для додатку

## Troubleshooting

### Додаток не запускається
```bash
sudo journalctl -u vacation-dashboard -n 50
sudo systemctl status vacation-dashboard
```

### Проблеми з базою даних
```bash
sudo -u vacation-dashboard sqlite3 /var/lib/vacation-dashboard/vacations.db ".tables"
```

### Проблеми з nginx
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```
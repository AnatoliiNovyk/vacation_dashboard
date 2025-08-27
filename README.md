# Vacation Dashboard

Система управління відпустками співробітників з веб-інтерфейсом на базі Dash/Flask.

## 🚀 Особливості

- **Рольова система доступу**: Employee, Manager, HR Manager
- **Управління співробітниками**: Додавання, редагування, видалення
- **Управління відпустками**: Планування, відстеження, історія
- **Імпорт даних**: Підтримка CSV та Excel файлів
- **Безпека**: Валідація даних, логування, rate limiting
- **Адаптивний дизайн**: Працює на всіх пристроях

## 📋 Вимоги

- Python 3.8+
- SQLite 3
- Nginx (для продакшн)
- Ubuntu 20.04+ (рекомендовано)

## 🛠️ Встановлення

### Швидке розгортання (Ubuntu 24.04)

```bash
# 1. Клонуйте репозиторій
git clone <your-repo-url>
cd vacation-dashboard

# 2. Зробіть скрипти виконуваними
chmod +x deployment/*.sh

# 3. Запустіть автоматичне встановлення
sudo deployment/install.sh

# 4. Налаштуйте SSL (замініть на ваш домен)
sudo deployment/ssl_setup.sh your-domain.com
```

### Ручне встановлення

```bash
# 1. Встановіть залежності
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx sqlite3

# 2. Створіть віртуальне середовище
python3 -m venv venv
source venv/bin/activate

# 3. Встановіть Python пакети
pip install -r requirements.txt

# 4. Налаштуйте конфігурацію
cp .env.example .env
# Відредагуйте .env файл

# 5. Ініціалізуйте базу даних
python -c "from data.db_operations import _init_db; _init_db()"

# 6. Запустіть додаток
python app.py
```

## 🐳 Docker

```bash
# Запуск через Docker Compose
docker-compose up -d

# Або збірка власного образу
docker build -t vacation-dashboard .
docker run -p 8050:8050 vacation-dashboard
```

## ⚙️ Конфігурація

### Змінні середовища (.env)

```env
# Основні налаштування
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///data/vacations.db

# Безпека
SESSION_COOKIE_SECURE=true
WTF_CSRF_ENABLED=true

# Логування
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Структура файлів

```
/opt/vacation-dashboard/          # Код додатку
├── app.py                        # Головний файл
├── config.py                     # Конфігурація
├── requirements.txt              # Залежності
├── data/                         # Модулі БД
├── components/                   # UI компоненти
├── utils/                        # Утиліти
└── scripts/                      # Скрипти

/var/lib/vacation-dashboard/      # Дані
└── vacations.db                  # База даних

/var/log/vacation-dashboard/      # Логи
├── app.log                       # Логи додатку
└── access.log                    # Логи доступу
```

## 👥 Ролі користувачів

### Employee (Співробітник)
- Перегляд власних даних про відпустку
- Історія власних відпусток

### Manager (Менеджер)
- Все що Employee +
- Перегляд відпусток підлеглих
- Статистика по команді

### HR Manager (HR-менеджер)
- Все що Manager +
- Управління всіма співробітниками
- Додавання/редагування/видалення співробітників
- Управління відпустками всіх співробітників
- Імпорт даних з файлів

## 🔐 Безпека

- **Автентифікація**: За ІПН (10 цифр)
- **Авторизація**: Рольова система доступу
- **Валідація**: Всіх вхідних даних
- **Rate Limiting**: Захист від брутфорс атак
- **CSRF**: Захист від міжсайтових запитів
- **XSS**: Очищення HTML контенту
- **Логування**: Всіх дій користувачів

## 📊 Імпорт даних

Підтримуються формати: CSV, Excel (.xlsx, .xls)

### Структура файлу:

| ПІБ | ІПН | Роль | Днів відпустки на рік | Керівник |
|-----|-----|------|----------------------|----------|
| Іванов І.І. | 1234567890 | Employee | 24 | Петров П.П. |

### Приклад CSV:
```csv
ПІБ,ІПН,Роль,Днів відпустки на рік,Керівник
"Іванов Іван Іванович",1234567890,Employee,24,"Петров Петро Петрович"
"Петров Петро Петрович",0987654321,Manager,28,
```

## 🔧 Обслуговування

### Перевірка стану
```bash
# Статус сервісів
sudo systemctl status vacation-dashboard
sudo systemctl status nginx

# Логи
sudo journalctl -u vacation-dashboard -f
sudo tail -f /var/log/vacation-dashboard/app.log

# Health check
sudo python3 /opt/vacation-dashboard/scripts/health_check.py
```

### Резервне копіювання
```bash
# Ручний бекап
sudo /opt/vacation-dashboard/scripts/backup.sh

# Автоматичний бекап (cron)
0 2 * * * /opt/vacation-dashboard/scripts/backup.sh
```

### Оновлення
```bash
# Зупинити сервіс
sudo systemctl stop vacation-dashboard

# Оновити код
cd /opt/vacation-dashboard
git pull origin main

# Встановити нові залежності (якщо потрібно)
sudo -u vacation-dashboard ./venv/bin/pip install -r requirements.txt

# Запустити сервіс
sudo systemctl start vacation-dashboard
```

## 🐛 Troubleshooting

### Додаток не запускається
```bash
# Перевірити логи
sudo journalctl -u vacation-dashboard -n 50
sudo systemctl status vacation-dashboard

# Перевірити права доступу
ls -la /opt/vacation-dashboard/
ls -la /var/lib/vacation-dashboard/
```

### Проблеми з базою даних
```bash
# Перевірити БД
sudo -u vacation-dashboard sqlite3 /var/lib/vacation-dashboard/vacations.db ".tables"
sudo -u vacation-dashboard sqlite3 /var/lib/vacation-dashboard/vacations.db ".schema"
```

### Проблеми з Nginx
```bash
# Тест конфігурації
sudo nginx -t

# Логи помилок
sudo tail -f /var/log/nginx/error.log
```

## 📈 Моніторинг

### Метрики для відстеження:
- Час відгуку додатку
- Використання пам'яті та CPU
- Розмір бази даних
- Кількість активних користувачів
- Помилки в логах

### Рекомендовані інструменти:
- **Prometheus + Grafana**: Для метрик
- **ELK Stack**: Для аналізу логів
- **Uptime Robot**: Для моніторингу доступності

## 🤝 Розробка

### Локальна розробка
```bash
# Клонувати репозиторій
git clone <repo-url>
cd vacation-dashboard

# Встановити залежності
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Налаштувати для розробки
export FLASK_ENV=development
cp .env.example .env

# Запустити
python app.py
```

### Структура коду
- `app.py` - Головний файл додатку
- `config.py` - Конфігурація
- `data/` - Робота з базою даних
- `components/` - UI компоненти Dash
- `utils/` - Допоміжні функції
- `auth/` - Автентифікація та авторизація

### Тестування
```bash
# Запуск тестів (коли будуть додані)
python -m pytest tests/

# Перевірка коду
flake8 .
black .
```

## 📄 Ліцензія

[Вкажіть вашу ліцензію]

## 👨‍💻 Автори

[Вкажіть авторів проекту]

## 🆘 Підтримка

Для отримання допомоги:
1. Перевірте цей README
2. Подивіться Issues в репозиторії
3. Створіть новий Issue з детальним описом проблеми

---

**Версія**: 1.0.0  
**Останнє оновлення**: 2025-01-27
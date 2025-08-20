FROM python:3.11-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Створення користувача для безпеки
RUN useradd --create-home --shell /bin/bash app

# Встановлення робочої директорії
WORKDIR /app

# Копіювання файлів залежностей
COPY requirements.txt .

# Встановлення Python залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання коду додатку
COPY . .

# Створення необхідних директорій
RUN mkdir -p logs data && \
    chown -R app:app /app

# Перемикання на користувача app
USER app

# Відкриття порту
EXPOSE 8050

# Команда запуску
CMD ["python", "app.py"]
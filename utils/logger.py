import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(app):
    """Налаштування логування для додатку"""
    
    # Створюємо директорію для логів якщо не існує
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Налаштування форматування
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
    
    # Налаштування обертання файлів логів
    file_handler = RotatingFileHandler(
        'logs/vacation_dashboard.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Налаштування консольного виводу
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Додавання обробників до логера додатку
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Логування запуску
    app.logger.info('Vacation Dashboard startup')
    
    return app.logger

def log_user_action(logger, user_ipn, action, details=None):
    """Логування дій користувача"""
    message = f"User {user_ipn} performed action: {action}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)

def log_error(logger, error, context=None):
    """Логування помилок"""
    message = f"Error occurred: {str(error)}"
    if context:
        message += f" - Context: {context}"
    logger.error(message, exc_info=True)
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Базова конфігурація"""
    # No random fallback here to avoid per-process/session invalidation in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/vacations.db')
    
    # Налаштування сесії
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Налаштування безпеки
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Налаштування логування
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')

class DevelopmentConfig(Config):
    """Конфігурація для розробки"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    # Stable dev secret if not provided via env
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

class ProductionConfig(Config):
    """Конфігурація для продакшн"""
    DEBUG = False
    
    # Додаткові налаштування безпеки для продакшн
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
    # No fallback secret in production
    SECRET_KEY = os.environ.get('SECRET_KEY')

class TestingConfig(Config):
    """Конфігурація для тестування"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = 'testing-secret-key'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
import os
from datetime import timedelta

class Config:
    """Базова конфігурація"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/vacations.db')
    
    # Налаштування сесії
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Налаштування безпеки
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }
    
    # Налаштування логування
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')

class DevelopmentConfig(Config):
    """Конфігурація для розробки"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    # Disable HSTS in development
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    }

class ProductionConfig(Config):
    """Конфігурація для продакшн"""
    DEBUG = False
    
    # Додаткові налаштування безпеки для продакшн
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
    
    # Stricter session settings for production
    PERMANENT_SESSION_LIFETIME = timedelta(hours=4)  # Shorter session timeout
    SESSION_COOKIE_SAMESITE = 'Strict'  # Stricter same-site policy

class TestingConfig(Config):
    """Конфігурація для тестування"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    # Minimal security headers for testing
    SECURITY_HEADERS = {}

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
import re
import hashlib
import secrets
from functools import wraps
from flask import session, request, abort
import bleach

def validate_ipn(ipn):
    """Валідація ІПН"""
    if not ipn or not isinstance(ipn, str):
        return False
    
    # Видаляємо всі символи крім цифр
    ipn_digits = re.sub(r'\D', '', ipn)
    
    # ІПН повинен містити рівно 10 цифр
    if len(ipn_digits) != 10:
        return False
    
    # Додаткова валідація контрольної суми ІПН (спрощена)
    try:
        digits = [int(d) for d in ipn_digits]
        # Базова перевірка на валідність
        return all(0 <= d <= 9 for d in digits)
    except ValueError:
        return False

def sanitize_input(text):
    """Очищення вхідних даних від потенційно небезпечного контенту"""
    if not text:
        return ""
    
    # Дозволені HTML теги (якщо потрібно)
    allowed_tags = []
    allowed_attributes = {}
    
    # Очищення від HTML та потенційно небезпечного контенту
    cleaned = bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    
    # Додаткове очищення
    cleaned = cleaned.strip()
    
    return cleaned

def validate_date_format(date_string):
    """Валідація формату дати"""
    if not date_string:
        return False
    
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(date_pattern, date_string))

def generate_csrf_token():
    """Генерація CSRF токену"""
    return secrets.token_hex(16)

def validate_csrf_token(token):
    """Валідація CSRF токену"""
    expected_token = session.get('csrf_token')
    return bool(expected_token) and bool(token) and secrets.compare_digest(expected_token, token)

def require_auth(f):
    """Декоратор для перевірки автентифікації"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_ipn' not in session:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """Декоратор для перевірки ролі користувача"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != required_role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def hash_sensitive_data(data):
    """Хешування чутливих даних для логування"""
    return hashlib.sha256(data.encode()).hexdigest()[:8]

def validate_file_upload(filename):
    """Валідація завантажуваних файлів"""
    if not filename:
        return False
    
    allowed_extensions = {'csv', 'xlsx', 'xls'}
    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    return file_extension in allowed_extensions

def rate_limit_check(user_id, action, max_attempts=5, window_minutes=15):
    """Базова перевірка обмеження швидкості (потребує Redis для продакшн)"""
    # Для продакшн рекомендується використовувати Redis
    # Тут базова реалізація в пам'яті (не підходить для кластера)
    import time
    
    if not hasattr(rate_limit_check, 'attempts'):
        rate_limit_check.attempts = {}
    
    key = f"{user_id}:{action}"
    current_time = time.time()
    window_start = current_time - (window_minutes * 60)
    
    # Очищення старих записів
    if key in rate_limit_check.attempts:
        rate_limit_check.attempts[key] = [
            timestamp for timestamp in rate_limit_check.attempts[key]
            if timestamp > window_start
        ]
    else:
        rate_limit_check.attempts[key] = []
    
    # Перевірка ліміту
    if len(rate_limit_check.attempts[key]) >= max_attempts:
        return False
    
    # Додавання поточної спроби
    rate_limit_check.attempts[key].append(current_time)
    return True
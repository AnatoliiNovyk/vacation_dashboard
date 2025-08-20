#!/usr/bin/env python3
"""
Скрипт для перевірки здоров'я додатку
"""

import requests
import sys
import sqlite3
import os
from datetime import datetime

def check_web_service():
    """Перевірка веб-сервісу"""
    try:
        response = requests.get('http://localhost:8050/', timeout=10)
        if response.status_code == 200:
            print("✓ Web service is running")
            return True
        else:
            print(f"✗ Web service returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Web service check failed: {e}")
        return False

def check_database():
    """Перевірка бази даних"""
    db_path = '/app/data/vacations.db'
    try:
        if not os.path.exists(db_path):
            print(f"✗ Database file not found: {db_path}")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Перевірка таблиць
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        expected_tables = ['staff', 'vacations']
        existing_tables = [table[0] for table in tables]
        
        for table in expected_tables:
            if table in existing_tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
                conn.close()
                return False
        
        # Перевірка з'єднання
        cursor.execute("SELECT COUNT(*) FROM staff;")
        staff_count = cursor.fetchone()[0]
        print(f"✓ Database connection OK, {staff_count} employees found")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database check failed: {e}")
        return False

def check_logs():
    """Перевірка логів"""
    log_path = '/app/logs/vacation_dashboard.log'
    try:
        if os.path.exists(log_path):
            # Перевірка розміру лог-файлу
            size = os.path.getsize(log_path)
            if size > 100 * 1024 * 1024:  # 100MB
                print(f"⚠ Log file is large: {size / 1024 / 1024:.1f}MB")
            else:
                print(f"✓ Log file size OK: {size / 1024 / 1024:.1f}MB")
            return True
        else:
            print("⚠ Log file not found (may be normal for new installation)")
            return True
    except Exception as e:
        print(f"✗ Log check failed: {e}")
        return False

def main():
    """Основна функція перевірки"""
    print(f"Health check started at {datetime.now()}")
    print("-" * 50)
    
    checks = [
        ("Web Service", check_web_service),
        ("Database", check_database),
        ("Logs", check_logs)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        if not check_func():
            all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("✓ All health checks passed")
        sys.exit(0)
    else:
        print("✗ Some health checks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
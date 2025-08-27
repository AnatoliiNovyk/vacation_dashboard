#!/usr/bin/env python3
"""
Скрипт для тестування основних функцій додатку
"""

import sys
import os
sys.path.append('/opt/vacation-dashboard')

def test_imports():
    """Тестування імпортів"""
    try:
        print("Testing imports...")
        import app
        import data.db_operations as db_ops
        import utils.date_utils as date_utils
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Тестування бази даних"""
    try:
        print("Testing database...")
        import data.db_operations as db_ops
        
        # Тест підключення
        conn = db_ops.get_db_connection()
        conn.close()
        print("✅ Database connection successful")
        
        # Тест створення таблиць
        db_ops._ensure_tables_exist()
        print("✅ Tables creation successful")
        
        # Тест отримання співробітників
        employees = db_ops.get_all_employees()
        print(f"✅ Retrieved {len(employees)} employees")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_date_utils():
    """Тестування утиліт дат"""
    try:
        print("Testing date utilities...")
        import utils.date_utils as date_utils
        
        days = date_utils.calculate_days('2024-01-01', '2024-01-10')
        if days == 10:
            print("✅ Date calculation successful")
            return True
        else:
            print(f"❌ Date calculation error: expected 10, got {days}")
            return False
    except Exception as e:
        print(f"❌ Date utils error: {e}")
        return False

def main():
    """Основна функція тестування"""
    print("🧪 Starting application tests...")
    print("-" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Date Utils", test_date_utils)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
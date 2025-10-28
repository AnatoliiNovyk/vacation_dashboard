#!/usr/bin/env python3
"""
Script to initialize the database with test users for each role.
This creates sample employees for testing the application.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import db_operations
from datetime import datetime, timedelta

def init_test_data():
    """Initialize database with test users."""
    print("Starting database initialization...")

    # Initialize database tables
    db_operations._init_db()
    print("✓ Database tables created")

    # Check if we already have users
    existing_users = db_operations.get_all_employees()
    if len(existing_users) > 0:
        print(f"⚠ Database already has {len(existing_users)} employees.")
        response = input("Do you want to add test users anyway? (y/n): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return

    # Create HR Manager
    hr_id = db_operations.add_employee(
        fio="Іваненко Іван Іванович",
        ipn="1234567890",
        manager_fio=None,
        role="HR Manager",
        vacation_days_per_year=28,
        remaining_vacation_days=28
    )
    if hr_id:
        print(f"✓ Created HR Manager: Іваненко Іван Іванович (IPN: 1234567890)")
    else:
        print("✗ Failed to create HR Manager")
        return

    # Create Manager
    manager_id = db_operations.add_employee(
        fio="Петренко Петро Петрович",
        ipn="2345678901",
        manager_fio="Іваненко Іван Іванович",
        role="Manager",
        vacation_days_per_year=26,
        remaining_vacation_days=26
    )
    if manager_id:
        print(f"✓ Created Manager: Петренко Петро Петрович (IPN: 2345678901)")
    else:
        print("✗ Failed to create Manager")
        return

    # Create Employee 1 (under Manager)
    emp1_id = db_operations.add_employee(
        fio="Сидоренко Сидір Сидорович",
        ipn="3456789012",
        manager_fio="Петренко Петро Петрович",
        role="Employee",
        vacation_days_per_year=24,
        remaining_vacation_days=24
    )
    if emp1_id:
        print(f"✓ Created Employee: Сидоренко Сидір Сидорович (IPN: 3456789012)")
    else:
        print("✗ Failed to create Employee 1")
        return

    # Create Employee 2 (under Manager)
    emp2_id = db_operations.add_employee(
        fio="Коваленко Олена Олександрівна",
        ipn="4567890123",
        manager_fio="Петренко Петро Петрович",
        role="Employee",
        vacation_days_per_year=24,
        remaining_vacation_days=24
    )
    if emp2_id:
        print(f"✓ Created Employee: Коваленко Олена Олександрівна (IPN: 4567890123)")
    else:
        print("✗ Failed to create Employee 2")
        return

    # Add some vacation records
    print("\nAdding vacation records...")

    # Add vacation for HR Manager (past vacation)
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = (datetime.now() - timedelta(days=23)).strftime('%Y-%m-%d')
    if db_operations.add_vacation(hr_id, start_date, end_date, 7):
        print(f"✓ Added past vacation for HR Manager (7 days)")

    # Add vacation for Manager (upcoming vacation)
    start_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=24)).strftime('%Y-%m-%d')
    if db_operations.add_vacation(manager_id, start_date, end_date, 14):
        print(f"✓ Added upcoming vacation for Manager (14 days)")

    # Add vacation for Employee 1 (current vacation)
    start_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    if db_operations.add_vacation(emp1_id, start_date, end_date, 7):
        print(f"✓ Added current vacation for Employee 1 (7 days)")

    print("\n" + "="*60)
    print("✓ DATABASE INITIALIZATION COMPLETE")
    print("="*60)
    print("\nTest Users Created:")
    print("-" * 60)
    print(f"HR Manager  : Іваненко Іван Іванович")
    print(f"              IPN: 1234567890")
    print(f"              Remaining vacation: 21 days")
    print()
    print(f"Manager     : Петренко Петро Петрович")
    print(f"              IPN: 2345678901")
    print(f"              Remaining vacation: 12 days")
    print()
    print(f"Employee 1  : Сидоренко Сидір Сидорович")
    print(f"              IPN: 3456789012")
    print(f"              Remaining vacation: 17 days")
    print()
    print(f"Employee 2  : Коваленко Олена Олександрівна")
    print(f"              IPN: 4567890123")
    print(f"              Remaining vacation: 24 days")
    print("-" * 60)
    print("\nYou can now login using any of the IPNs above!")
    print()

if __name__ == '__main__':
    try:
        init_test_data()
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

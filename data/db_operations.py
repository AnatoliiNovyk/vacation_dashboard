import sqlite3
from datetime import datetime, date
from utils import date_utils # Ensure date_utils is imported
from utils.logger import log_error, log_user_action
from utils.security import sanitize_input, validate_ipn, validate_date_format
from pathlib import Path
import logging

DB_PATH = 'data/vacations.db' # Шлях до файлу бази даних
# Ensure database directory exists
DB_DIR = Path('/var/lib/vacation-dashboard')
DB_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = str(DB_DIR / 'vacation_dashboard.db')

        # Ensure the database file can be created/accessed
        db_path = Path(DATABASE_PATH)
        if not db_path.parent.exists():
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
def get_db_connection():
    """Встановлює з'єднання з базою даних SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        conn.execute("PRAGMA foreign_keys = ON")  # Увімкнення foreign keys
        
        # Test the connection
        conn.execute("SELECT 1").fetchone()
        conn.execute("PRAGMA journal_mode = WAL")  # Покращення продуктивності
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}, Path: {DATABASE_PATH}")
        # Try to create database file if it doesn't exist
        try:
            db_path.touch(exist_ok=True)
            conn = sqlite3.connect(DATABASE_PATH, timeout=30.0)
            return conn
        except Exception as create_error:
            logger.error(f"Failed to create database: {create_error}")
        raise
    conn.row_factory = sqlite3.Row # Дозволяє звертатися до колонок за іменем
        logger.error(f"Unexpected database error: {e}, Path: {DATABASE_PATH}")

def _ensure_tables_exist(conn_param=None):
    """Створює таблиці, якщо вони не існують. Це базовий варіант."""
    close_conn_here = False
    if conn_param is None:
        conn = get_db_connection()
        close_conn_here = True
    else:
        conn = conn_param

    cursor = conn.cursor()
    # Створення таблиці staff
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fio TEXT NOT NULL,
        ipn TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        manager_fio TEXT,
        vacation_days_per_year INTEGER NOT NULL,
        remaining_vacation_days INTEGER NOT NULL
    )
    """)
    # Створення таблиці vacations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        total_days INTEGER NOT NULL,
        FOREIGN KEY (staff_id) REFERENCES staff (id)
    )
    """)
    conn.commit()
    if close_conn_here:
        conn.close()

def _init_db():
    """Ініціалізує базу даних, переконуючись, що таблиці існують."""
    _ensure_tables_exist()

_init_db() # Викликаємо ініціалізацію БД при завантаженні модуля

def get_all_employees():
    """Отримує всіх співробітників з бази даних."""
    # Ensure tables exist (basic check, ideally use migrations or init script)
    _ensure_tables_exist()
    conn = get_db_connection()
    # Select specific columns to be sure, including id
    employees = conn.execute('SELECT id, fio, ipn, role, manager_fio, vacation_days_per_year, remaining_vacation_days FROM staff').fetchall()
    conn.close()
    return [dict(row) for row in employees] # Конвертуємо в список словників

def get_employee_by_id(employee_id):
    """Отримує дані співробітника за ID."""
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM staff WHERE id = ?', (employee_id,)).fetchone()
    conn.close()
    return dict(employee) if employee else None

def add_employee(fio, ipn, manager_fio, role, vacation_days_per_year, remaining_vacation_days=None):
    """Додає нового співробітника в базу даних."""
    # Валідація та очищення вхідних даних
    fio = sanitize_input(fio)
    ipn = sanitize_input(ipn)
    manager_fio = sanitize_input(manager_fio) if manager_fio else None
    role = sanitize_input(role)
    
    if not validate_ipn(ipn):
        logger.warning(f"Invalid IPN format attempted: {ipn[:3]}***")
        return None
    
    if not fio or not role:
        logger.warning("Missing required fields for employee creation")
        return None
    
    if remaining_vacation_days is None:
        remaining_vacation_days = vacation_days_per_year
    
    conn = get_db_connection()
    _ensure_tables_exist(conn) # Ensure tables exist before insert
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO staff (fio, ipn, manager_fio, role, vacation_days_per_year, remaining_vacation_days)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (fio, ipn, manager_fio, role, vacation_days_per_year, remaining_vacation_days))
        conn.commit()
        employee_id = cursor.lastrowid
        logger.info(f"Employee added successfully: ID {employee_id}")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        logger.error(f"Employee creation failed - integrity error: {e}")
        return None
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Employee creation failed - database error: {e}")
        return None
    finally:
        conn.close()
    return employee_id

def get_employee_by_ipn(ipn):
    """Отримує дані співробітника за ІПН, включаючи ПІБ та роль."""
    conn = get_db_connection()
    # Припускаємо, що таблиця 'staff' має колонки 'ipn', 'role', 'fio'
    employee = conn.execute('SELECT id, ipn, role, fio, remaining_vacation_days FROM staff WHERE ipn = ?', (ipn,)).fetchone()
    conn.close()
    if employee:
        return dict(employee) # Конвертуємо sqlite3.Row в словник
    return None

def get_managers():
    """Отримує список співробітників з роллю 'Manager'."""
    conn = get_db_connection()
    managers_cursor = conn.execute("SELECT fio FROM staff WHERE role = 'Manager' ORDER BY fio").fetchall()
    conn.close()
    return [{'label': row['fio'], 'value': row['fio']} for row in managers_cursor]

def add_vacation(employee_id, start_date, end_date, total_days):
    """Додає відпустку для співробітника та оновлює залишок днів."""
    # Валідація дат
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        logger.warning(f"Invalid date format for vacation: {start_date} - {end_date}")
        return False
    
    if total_days <= 0:
        logger.warning(f"Invalid vacation days count: {total_days}")
        return False
    
    conn = get_db_connection()
    _ensure_tables_exist(conn)
    cursor = conn.cursor()
    try:
        # Перевірка чи достатньо днів відпустки
        employee = conn.execute('SELECT remaining_vacation_days FROM staff WHERE id = ?', (employee_id,)).fetchone()
        if not employee or employee['remaining_vacation_days'] < total_days:
            logger.warning(f"Insufficient vacation days for employee ID {employee_id}")
            conn.close()
            return False

        cursor.execute("""
            INSERT INTO vacations (staff_id, start_date, end_date, total_days)
            VALUES (?, ?, ?, ?)
        """, (employee_id, start_date, end_date, total_days))
        
        # Оновлення залишку днів відпустки
        new_remaining_days = employee['remaining_vacation_days'] - total_days
        cursor.execute("""
            UPDATE staff
            SET remaining_vacation_days = ?
            WHERE id = ?
        """, (new_remaining_days, employee_id))
        
        conn.commit()
        logger.info(f"Vacation added successfully for employee ID {employee_id}")
        return True
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Vacation creation failed: {e}")
        return False
    finally:
        conn.close()

def get_vacation_history(year):
    """Отримує історію відпусток за вказаний рік."""
    conn = get_db_connection()
    _ensure_tables_exist(conn)
    query = """
        SELECT s.fio, s.manager_fio, v.start_date, v.end_date, v.total_days
        FROM vacations v
        JOIN staff s ON v.staff_id = s.id
        WHERE strftime('%Y', v.start_date) = ? OR strftime('%Y', v.end_date) = ?
        ORDER BY v.start_date DESC
    """
    history = conn.execute(query, (str(year), str(year))).fetchall()
    conn.close()
    return [dict(row) for row in history]


def get_employee_vacation_summary_by_ipn(ipn):
    """Отримує зведені дані про відпустку для співробітника за ІПН."""
    conn = get_db_connection()
    _ensure_tables_exist(conn)
    query = """
    SELECT 
        s.id, s.fio, s.ipn, s.role, s.manager_fio, s.remaining_vacation_days,
        v.start_date AS current_vacation_start_date,
        v.end_date AS current_vacation_end_date,
        v.total_days AS current_vacation_total_days
    FROM staff s
    LEFT JOIN (
        SELECT staff_id, start_date, end_date, total_days,
               ROW_NUMBER() OVER (PARTITION BY staff_id ORDER BY end_date DESC) as rn
        FROM vacations
        WHERE date(end_date) >= date('now', '-90 days') -- Consider recent/future vacations (adjust window as needed)
    ) v ON s.id = v.staff_id AND v.rn = 1
    WHERE s.ipn = ?;
    """
    employee_data = conn.execute(query, (ipn,)).fetchone()
    conn.close()
    return dict(employee_data) if employee_data else None

def get_employee_details_for_edit(employee_id: int):
    """
    Fetches comprehensive data for a given employee_id for editing purposes.
    Includes employee details and their "most relevant" vacation.
    "Most relevant" is defined as:
    1. The next upcoming vacation (start_date >= today).
    2. If no upcoming, then the most recent past vacation (end_date < today).
    """
    _ensure_tables_exist()
    conn = get_db_connection()
    employee_data = conn.execute('SELECT id, fio, ipn, role, manager_fio, vacation_days_per_year, remaining_vacation_days FROM staff WHERE id = ?', (employee_id,)).fetchone()
    
    if not employee_data:
        conn.close()
        return None

    result = dict(employee_data)
    today_iso = date.today().isoformat()

    # Try to find next upcoming vacation
    relevant_vacation = conn.execute("""
        SELECT id, start_date, end_date, total_days FROM vacations
        WHERE staff_id = ? AND date(start_date) >= date(?)
        ORDER BY date(start_date) ASC
        LIMIT 1
    """, (employee_id, today_iso)).fetchone()

    if not relevant_vacation:
        # If no upcoming, find most recent past vacation
        relevant_vacation = conn.execute("""
            SELECT id, start_date, end_date, total_days FROM vacations
            WHERE staff_id = ? AND date(end_date) < date(?)
            ORDER BY date(end_date) DESC
            LIMIT 1
        """, (employee_id, today_iso)).fetchone()

    conn.close()

    result['target_vacation'] = dict(relevant_vacation) if relevant_vacation else None
    return result

def update_employee_data_and_vacation(employee_id: int, updates: dict):
    """
    Atomically updates employee information in the staff table and, if applicable,
    their "most relevant" vacation in the vacations table.
    Correctly recalculates staff.remaining_vacation_days.
    Returns a tuple (bool_success, message_string).
    """
    _ensure_tables_exist()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get current staff data for calculations
        old_staff_data = cursor.execute('SELECT vacation_days_per_year, remaining_vacation_days FROM staff WHERE id = ?', (employee_id,)).fetchone()
        if not old_staff_data:
            conn.close()
            return False, "Сотрудник не найден."

        old_vacation_days_per_year = old_staff_data['vacation_days_per_year']
        old_remaining_vacation_days = old_staff_data['remaining_vacation_days']
        current_total_taken_or_booked_days = old_vacation_days_per_year - old_remaining_vacation_days

        target_vacation_id = updates.get('target_vacation_id')
        new_vacation_start_date = updates.get('vacation_start_date')
        new_vacation_end_date = updates.get('vacation_end_date')

        if target_vacation_id and new_vacation_start_date and new_vacation_end_date:
            old_vacation = cursor.execute('SELECT total_days FROM vacations WHERE id = ? AND staff_id = ?', (target_vacation_id, employee_id)).fetchone()
            if old_vacation:
                old_total_days_for_target_vacation = old_vacation['total_days']
                new_total_days_for_target_vacation = date_utils.calculate_days(new_vacation_start_date, new_vacation_end_date)
                
                if new_total_days_for_target_vacation <= 0:
                    conn.rollback()
                    conn.close()
                    return False, "Некорректний період відпустки."

                cursor.execute('UPDATE vacations SET start_date = ?, end_date = ?, total_days = ? WHERE id = ?',
                               (new_vacation_start_date, new_vacation_end_date, new_total_days_for_target_vacation, target_vacation_id))
                current_total_taken_or_booked_days = current_total_taken_or_booked_days - old_total_days_for_target_vacation + new_total_days_for_target_vacation

        # Update staff table
        cursor.execute("""
            UPDATE staff SET fio = ?, ipn = ?, role = ?, manager_fio = ?, vacation_days_per_year = ?
            WHERE id = ?
        """, (updates['fio'], updates['ipn'], updates['role'], updates.get('manager_fio'), updates['vacation_days_per_year'], employee_id))

        new_annual_days = updates['vacation_days_per_year']
        final_remaining_vacation_days = new_annual_days - current_total_taken_or_booked_days
        cursor.execute('UPDATE staff SET remaining_vacation_days = ? WHERE id = ?', (final_remaining_vacation_days, employee_id))

        conn.commit()
        return True, "Дані співробітника успішно оновлені."
    except sqlite3.IntegrityError: # Handles unique constraint violation for IPN
        conn.rollback()
        return False, "Помилка: ІПН вже існує для іншого співробітника."
    except Exception as e:
        conn.rollback()
        print(f"Помилка оновлення даних співробітника: {e}")
        return False, f"Произошла ошибка: {e}"
    finally:
        conn.close()

def get_subordinates_vacation_details(manager_fio):
    """
    Получает детали отпусков для ВСЕХ подчиненных в иерархии (прямых и косвенных)
    с использованием рекурсивного запроса.
    """
    conn = get_db_connection()
    query = """
        WITH RECURSIVE SubordinateHierarchy AS (
            -- Базовий випадок: прямі підлеглі топ-менеджера
            SELECT id, fio, ipn, role, manager_fio, remaining_vacation_days, vacation_days_per_year
            FROM staff
            WHERE manager_fio = :manager_name

            UNION ALL

            -- Рекурсивний крок: співробітники, які підпорядковуються підлеглим, знайденим на попередньому кроці
            SELECT s.id, s.fio, s.ipn, s.role, s.manager_fio, s.remaining_vacation_days, s.vacation_days_per_year
            FROM staff s
            INNER JOIN SubordinateHierarchy sh ON s.manager_fio = sh.fio
        ),
        LatestVacations AS (
            -- Знаходимо найближчу до сьогоднішнього дня відпустку (минулу чи майбутню) для кожного співробітника
            SELECT
                v.staff_id,
                v.start_date,
                v.end_date,
                v.total_days,
                ROW_NUMBER() OVER(PARTITION BY v.staff_id ORDER BY ABS(julianday(v.start_date) - julianday('now'))) as rn
            FROM vacations v
            INNER JOIN SubordinateHierarchy sh ON v.staff_id = sh.id
        )
        -- Тепер обираємо з ієрархії та приєднуємо дані про найближчу відпустку
        SELECT
            h.fio AS sub_fio,
            h.ipn AS sub_ipn,
            h.role AS sub_role,
            lv.start_date as vac_start_date,
            lv.end_date as vac_end_date,
            lv.total_days as vac_total_days,
            h.remaining_vacation_days AS sub_remaining_days
        FROM SubordinateHierarchy h
        LEFT JOIN LatestVacations lv ON h.id = lv.staff_id AND lv.rn = 1
        ORDER BY h.fio;
    """
    try:
        subordinates = conn.execute(query, {'manager_name': manager_fio}).fetchall()
        conn.close()
        return [dict(row) for row in subordinates]
    except Exception as e:
        print(f"Recursive query failed: {e}")
        conn.close()
        return []

def delete_employee(employee_id: int) -> tuple[bool, str]:
    """Deletes an employee, their vacations, and nullifies manager references."""
    if not isinstance(employee_id, int) or employee_id <= 0:
        logger.warning(f"Invalid employee ID for deletion: {employee_id}")
        return False, "Некоректний ID співробітника"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get F.I.O. of the employee being deleted to update manager_fio for their subordinates
        employee_to_delete = cursor.execute('SELECT fio FROM staff WHERE id = ?', (employee_id,)).fetchone()
        if not employee_to_delete:
            conn.close()
            return False, "Сотрудник не найден."
        
        deleted_employee_fio = employee_to_delete['fio']

        # Start transaction
        cursor.execute("BEGIN TRANSACTION")

        # Nullify manager_fio for subordinates of the deleted employee
        # This is important if the deleted employee was a manager
        cursor.execute("UPDATE staff SET manager_fio = NULL WHERE manager_fio = ?", (deleted_employee_fio,))

        # Delete associated vacations
        cursor.execute("DELETE FROM vacations WHERE staff_id = ?", (employee_id,))

        # Delete the employee
        cursor.execute("DELETE FROM staff WHERE id = ?", (employee_id,))
        
        conn.commit()
        logger.info(f"Employee deleted successfully: ID {employee_id}")
        return True, "Сотрудник успешно удален."
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Employee deletion failed for ID {employee_id}: {e}")
        return False, f"Ошибка удаления сотрудника: {e}"
    finally:
        conn.close()

# Приклад використання (можна закоментувати або видалити пізніше)
if __name__ == '__main__':
    _ensure_tables_exist() # Make sure tables are created for testing
    print("Tables ensured.")

    print("\nВсі співробітники:")
    all_staff = get_all_employees()
    for emp in all_staff:
        print(emp)

    print("\nHR Table Employees:")
    hr_employees = get_employees_for_hr_table()
    for emp in hr_employees:
        print(emp)

    print("\nVacation History (2024):") # Assuming current year is 2024 for test
    history = get_vacation_history(datetime.now().year)
    for item in history:
        print(item)

    # Test new function - replace 'test_ipn' with an actual IPN from your DB
    # test_ipn = "1234567890" 
    # print(f"\nVacation summary for IPN {test_ipn}:")
    # summary = get_employee_vacation_summary_by_ipn(test_ipn)
    # print(summary)
def get_vacation_history_for_employee(employee_id):
    """Отримує історію відпусток для конкретного співробітника."""
    conn = get_db_connection()
    query = """
        SELECT start_date, end_date, total_days
        FROM vacations
        WHERE staff_id = ?
        ORDER BY start_date DESC
    """
    history = conn.execute(query, (employee_id,)).fetchall()
    conn.close()
    return [dict(row) for row in history]

def batch_import_employees(employees_data):
    """
    Пакетний імпорт або оновлення співробітників. Усовершенствованная версія,
    яка коректно обробляє менеджерів, визначених в тому ж файлі.
    """
    if not employees_data:
        logger.warning("Empty employee data provided for batch import")
        return 0, 0, ["Порожні дані для імпорту"]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    imported_count = 0
    updated_count = 0
    errors = []

    # Шаг 1: Собрати всіх відомих менеджерів (з БД і з поточного файлу)
    db_managers_query = conn.execute("SELECT fio FROM staff WHERE role = 'Manager'").fetchall()
    all_managers = {row['fio'] for row in db_managers_query}
    
    # Попередній прохід по файлу для пошуку нових менеджерів
    for emp in employees_data:
        if emp.get('role') == 'Manager':
            all_managers.add(emp['fio'])

    # Шаг 2: Основний цикл імпорту з використанням повного списку менеджерів
    for emp in employees_data:
        try:
            # Валідація та очищення даних
            emp['fio'] = sanitize_input(emp.get('fio', ''))
            emp['ipn'] = sanitize_input(emp.get('ipn', ''))
            
            if not emp['fio'] or not emp['ipn']:
                errors.append(f"Пропущені обов'язкові поля для запису: {emp}")
                continue
                
            if not validate_ipn(emp['ipn']):
                errors.append(f"Некоректний ІПН: {emp['ipn']}")
                continue
            
            cursor.execute("SELECT id, vacation_days_per_year, remaining_vacation_days FROM staff WHERE ipn = ?", (emp['ipn'],))
            existing_employee = cursor.fetchone()

            manager_fio = emp.get('manager_fio')
            if manager_fio and manager_fio not in all_managers:
                # Якщо менеджер вказаний, але його немає ні в БД, ні в цьому файлі, обнуляємо
                manager_fio = None

            vacation_days = int(emp.get('vacation_days_per_year', 24))

            if existing_employee:
                old_total_days = existing_employee['vacation_days_per_year']
                old_remaining_days = existing_employee['remaining_vacation_days']
                days_diff = vacation_days - old_total_days
                new_remaining_days = old_remaining_days + days_diff

                cursor.execute("""
                    UPDATE staff
                    SET fio = ?, role = ?, vacation_days_per_year = ?, remaining_vacation_days = ?, manager_fio = ?
                    WHERE ipn = ?
                """, (emp['fio'], emp.get('role', 'Employee'), vacation_days, new_remaining_days, manager_fio, emp['ipn']))
                updated_count += 1
            else:
                cursor.execute("""
                    INSERT INTO staff (fio, ipn, role, manager_fio, vacation_days_per_year, remaining_vacation_days)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (emp['fio'], emp['ipn'], emp.get('role', 'Employee'), manager_fio, vacation_days, vacation_days))
                imported_count += 1
        except Exception as e:
            errors.append(f"Помилка для запису з ІПН {emp.get('ipn', 'N/A')}: {str(e)}")
            logger.error(f"Batch import error for IPN {emp.get('ipn', 'N/A')}: {e}")
            continue
    
    try:
        conn.commit()
        logger.info(f"Batch import completed: {imported_count} imported, {updated_count} updated, {len(errors)} errors")
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Batch import commit failed: {e}")
        errors.append(f"Помилка збереження змін: {e}")
    finally:
        conn.close()
    
    return imported_count, updated_count, errors
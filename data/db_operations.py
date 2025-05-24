import sqlite3
from datetime import datetime, date
from utils import date_utils # Ensure date_utils is imported

DB_PATH = 'data/vacations.db' # Шлях до файлу бази даних

def get_db_connection():
    """Встановлює з'єднання з базою даних SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Дозволяє звертатися до колонок за іменем
    return conn

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
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"Помилка додавання співробітника: {e}") # Або можна підняти виключення
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
    conn = get_db_connection()
    _ensure_tables_exist(conn)
    cursor = conn.cursor()
    try:
        # Перевірка чи достатньо днів відпустки
        employee = conn.execute('SELECT remaining_vacation_days FROM staff WHERE id = ?', (employee_id,)).fetchone()
        if not employee or employee['remaining_vacation_days'] < total_days:
            print(f"Недостатньо днів відпустки для співробітника ID {employee_id}.")
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
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Помилка додавання відпустки: {e}")
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

def get_employees_for_hr_table():
    """Отримує дані співробітників для таблиці HR, включаючи останню/поточну відпустку."""
    conn = get_db_connection()
    _ensure_tables_exist(conn)
    # This query is simplified: it gets the latest vacation by end_date.
    # A more complex query might be needed for "current or next upcoming".
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
        WHERE date(end_date) >= date('now', '-30 days') -- Consider recent/future vacations
    ) v ON s.id = v.staff_id AND v.rn = 1
    ORDER BY s.fio;
    """
    # If no vacation found or it's old, the vacation fields will be NULL.
    # The UI callback might need to handle NULLs (e.g., display 'N/A').
    employees = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in employees]

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
                    return False, "Некорректный период отпуска."

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
        return True, "Данные сотрудника успешно обновлены."
    except sqlite3.IntegrityError: # Handles unique constraint violation for IPN
        conn.rollback()
        return False, "Ошибка: ИПН уже существует для другого сотрудника."
    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления данных сотрудника: {e}")
        return False, f"Произошла ошибка: {e}"
    finally:
        conn.close()

def get_subordinates_vacation_details(manager_fio: str) -> list[dict]:
    """
    Отримує деталі відпусток для всіх підлеглих вказаного менеджера.
    """
    _ensure_tables_exist()
    conn = get_db_connection()
    query = """
        SELECT
            s.fio AS sub_fio,
            s.ipn AS sub_ipn,
            s.role AS sub_role,
            v.start_date AS vac_start_date,
            v.end_date AS vac_end_date,
            v.total_days AS vac_total_days,
            s.remaining_vacation_days AS sub_remaining_days
        FROM staff s
        JOIN vacations v ON s.id = v.staff_id
        WHERE s.manager_fio = ?
        ORDER BY s.fio, v.start_date;
    """
    subordinates_vacations = conn.execute(query, (manager_fio,)).fetchall()
    conn.close()
    return [dict(row) for row in subordinates_vacations]

def delete_employee(employee_id: int) -> tuple[bool, str]:
    """Deletes an employee, their vacations, and nullifies manager references."""
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
        return True, "Сотрудник успешно удален."
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка удаления сотрудника ID {employee_id}: {e}")
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

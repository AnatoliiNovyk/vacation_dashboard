---
id: ARCH-DATA-storage
title: "Архітектура: Сховище Даних"
type: component
layer: data
owner: "@unassigned"
version: v1
status: current
created: 2025-06-02
updated: 2025-06-02
tags: [data, storage, database, schema, operations, sqlite]
depends_on: []
referenced_by: [ARCH-APP-core-routing-auth, ARCH-APP-employee-logic, ARCH-APP-hr-logic, ARCH-APP-manager-logic]
---
## Контекст
Цей компонент визначає структуру та операції зберігання даних для системи управління відпустками. Він включає схему бази даних, операції з даними та механізми взаємодії з базою даних.

## Структура
*   **Розташування:** `data/database.py`
*   **Схема Бази Даних:**
    *   **Таблиця `employees`:**
        *   `id` (INTEGER PRIMARY KEY)
        *   `fio` (TEXT NOT NULL)
        *   `ipn` (TEXT UNIQUE NOT NULL)
        *   `role` (TEXT NOT NULL)
        *   `manager_fio` (TEXT)
        *   `vacation_days_per_year` (INTEGER NOT NULL)
        *   `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        *   `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    *   **Таблиця `vacations`:**
        *   `id` (INTEGER PRIMARY KEY)
        *   `employee_id` (INTEGER NOT NULL)
        *   `start_date` (DATE NOT NULL)
        *   `end_date` (DATE NOT NULL)
        *   `total_days` (INTEGER NOT NULL)
        *   `status` (TEXT NOT NULL)
        *   `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        *   `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        *   FOREIGN KEY (`employee_id`) REFERENCES `employees`(`id`)

## Операції з Даними
*   **Ініціалізація:**
    *   `init_db()`: Створює таблиці, якщо вони не існують
    *   `get_db_connection()`: Встановлює з'єднання з базою даних
*   **Операції зі Співробітниками:**
    *   `add_employee(fio, ipn, role, manager_fio, vacation_days_per_year)`
    *   `get_employee_by_ipn(ipn)`
    *   `get_employees_for_hr_table()`
    *   `get_subordinates_for_manager_table(manager_fio)`
    *   `update_employee_data(employee_id, updates)`
    *   `delete_employee(employee_id)`
*   **Операції з Відпустками:**
    *   `add_vacation(employee_id, start_date, end_date, total_days)`
    *   `get_employee_vacation_summary_by_ipn(ipn)`
    *   `get_employee_vacation_history(employee_id, year)`
    *   `update_vacation_status(vacation_id, status)`
    *   `get_employee_details_for_edit(employee_id)`
    *   `update_employee_data_and_vacation(employee_id, employee_updates, vacation_updates)`

## Поведінка
### Зберігання Даних
*   Всі дані зберігаються в SQLite базі даних
*   Використовується транзакційний підхід для забезпечення цілісності даних
*   Автоматичне оновлення полів `created_at` та `updated_at`

### Валідація
*   Перевірка унікальності ІПН при додаванні/оновленні співробітника
*   Валідація дат відпустки (початок не пізніше кінця)
*   Перевірка наявності співробітника при додаванні відпустки

### Обробка Помилок
*   Логування помилок бази даних
*   Коректне закриття з'єднань навіть при виникненні помилок
*   Повернення зрозумілих повідомлень про помилки

## Еволюція
### Заплановано
— Додавання індексації для оптимізації запитів
— Реалізація механізму резервного копіювання
— Розширення функціоналу звітності
### Історичне
— v1: Реалізація базової схеми та операцій з даними 
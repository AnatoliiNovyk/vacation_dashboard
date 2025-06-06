---
id: ARCH-APP-hr-logic
title: "Логіка: Панель HR-менеджера"
type: component
layer: application
owner: "@unassigned"
version: v1
status: current
created: 2025-06-02
updated: 2025-06-02
tags: [app, logic, hr, dashboard, callbacks, employee_management, vacation_management, dash]
depends_on: [ARCH-DATA-storage, ARCH-UTIL-date, ARCH-APP-core-routing-auth]
referenced_by: []
---
## Контекст
Цей компонент інкапсулює бізнес-логіку та обробку взаємодій для Панелі HR-менеджера. Він включає численні callback-функції, що керують відображенням даних, додаванням, редагуванням та видаленням співробітників, а також управлінням відпустками.

## Структура
*   **Розташування:** `app.py` (секція callback-функцій для HR)
*   **Ключові Callback-функції:**
    *   **Управління Співробітниками:**
        *   `update_hr_employees_table`: Заповнює таблицю співробітників (`hr-employees-table`) даними з `db_operations.get_employees_for_hr_table()`.
        *   `update_manager_dropdown` (для форми додавання): Заповнює випадаючий список менеджерів.
        *   `handle_add_employee`: Обробляє додавання нового співробітника. Валідує дані, викликає `db_operations.add_employee()`.
        *   `handle_delete_employee`: Обробляє видалення вибраного співробітника. Валідує вибір, викликає `db_operations.delete_employee()`.
    *   **Редагування Даних Співробітника:**
        *   `update_edit_employee_fio_dropdown`: Заповнює випадаючий список ПІБ співробітників для редагування.
        *   `update_edit_employee_role_dropdown_options`: Заповнює опції ролей.
        *   `update_edit_employee_manager_dropdown_options`: Заповнює опції менеджерів для форми редагування.
        *   `populate_edit_employee_form`: Заповнює форму редагування даними вибраного співробітника, включаючи дані про його "найрелевантнішу" відпустку, отримані з `db_operations.get_employee_details_for_edit()`. Зберігає ID співробітника та ID цільової відпустки в `dcc.Store`.
        *   `handle_save_employee_data`: Обробляє збереження змінених даних співробітника. Отримує поточне ПІБ співробітника (ПІБ не редагується через цю форму безпосередньо), валідує дані, формує словник оновлень та викликає `db_operations.update_employee_data_and_vacation()`.
    *   **Управління Відпустками:**
        *   `update_vacation_employee_dropdown`: Заповнює випадаючий список співробітників для форми додавання відпустки.
        *   `calculate_vacation_total_days`: Обчислює загальну кількість днів у вибраному періоді відпустки, використовуючи `ARCH-UTIL-date`.
        *   `calculate_vacation_remaining_days`: Обчислює та відображає залишок днів відпустки для вибраного співробітника з урахуванням потенційної нової відпустки.
        *   `handle_add_vacation`: Обробляє додавання нової відпустки для співробітника. Валідує дані, викликає `db_operations.add_vacation()`.
    *   **Відображення Даних:**
        *   `update_vacation_history_table`: Заповнює таблицю історії відпусток (`hr-vacation-history-table`) за поточний рік.
        *   `display_hr_personal_vacation_details`: Відображає особисті дані про відпустку для самого HR-менеджера.
*   **Допоміжні Компоненти:**
    *   `dcc.Store(id='hr-data-refresh-trigger')`: Використовується для ініціювання оновлення даних у таблицях після операцій додавання, редагування, видалення.
    *   `dcc.Store(id='hr-edit-employee-selected-id-store')`, `dcc.Store(id='hr-edit-employee-target-vacation-id-store')`: Зберігають стан для форми редагування співробітника.

## Поведінка
### Управління Співробітниками
*   HR-менеджер може переглядати список всіх співробітників.
*   Може додавати нових співробітників, вказуючи їх ПІБ, ІПН, роль, менеджера (опціонально) та кількість днів відпустки на рік.
*   Може вибрати одного співробітника зі списку та видалити його. При видаленні також видаляються всі пов'язані записи про відпустки, а у підлеглих видаленого менеджера поле `manager_fio` обнуляється.
*   Може вибрати співробітника для редагування. Форма редагування дозволяє змінювати ІПН, роль, менеджера, річну кількість днів відпустки, а також дати існуючої "найрелевантнішої" відпустки. ПІБ співробітника не змінюється через цю форму. Система автоматично перераховує залишок днів відпустки.

### Управління Відпустками
*   HR-менеджер може додавати відпустку будь-якому співробітнику, вибираючи його зі списку та вказуючи дати початку та кінця відпустки.
*   Система відображає загальну кількість днів у вибраній відпустці та прогнозований залишок днів відпустки для співробітника.
*   Може переглядати історію відпусток всіх співробітників за поточний рік.

### Оновлення Даних
*   Після успішного додавання, редагування або видалення співробітника/відпустки, спрацьовує `hr-data-refresh-trigger`, що призводить до оновлення відповідних таблиць та випадаючих списків на панелі.

Детальна логіка обробки цих дій реалізована в callback-функціях в `ARCH-APP-hr-logic`.

## Еволюція
### Заплановано
— Подальше розширення функціоналу звітності.
— Можливість пакетних операцій.
### Історичне
— v1: Реалізація основного набору функцій для управління персоналом та відпустками, включаючи CRUD операції для співробітників (з нюансами редагування ПІБ) та управління відпустками. 
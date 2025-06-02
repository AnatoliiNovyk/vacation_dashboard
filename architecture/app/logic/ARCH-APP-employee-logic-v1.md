---
id: ARCH-APP-employee-logic
title: "Логіка: Панель Співробітника"
type: component
layer: application
owner: "@unassigned"
version: v1
status: current
created: 2025-06-02
updated: 2025-06-02
tags: [app, logic, employee, dashboard, callbacks, dash]
depends_on: [ARCH-DATA-storage, ARCH-APP-core-routing-auth]
referenced_by: []
---
## Контекст
Цей компонент описує логіку, специфічну для Панелі Співробітника. Він включає callback-функції, що відповідають за завантаження та відображення даних для співробітників.

## Структура
*   **Розташування:** `app.py` (секція callback-функцій для співробітників)
*   **Ключові Callback-функції:**
    *   `display_employee_personal_vacation_details`:
        *   **Тригер:** Завантаження Панелі Співробітника (`Input('url', 'pathname')`).
        *   **Дія:** Отримує ІПН поточного користувача з сесії. Викликає `db_operations.get_employee_vacation_summary_by_ipn()` для отримання зведених даних про відпустку. Формує та повертає HTML-вміст для блоку `employee-personal-vacation-details-div`.
    *   *Callback для `employee-table` (історія відпусток):* На момент аналізу, callback для заповнення таблиці `employee-table` не був явно реалізований або потребує додаткового визначення.

## Поведінка
*   Коли співробітник відкриває свою панель, `display_employee_personal_vacation_details` автоматично завантажує та відображає його особисті дані про відпустки.
*   Передбачається, що таблиця історії відпусток (`employee-table`) також буде заповнюватися даними, але відповідна логіка може бути ще не повністю реалізована.

## Еволюція
### Заплановано
— Реалізація або завершення callback-функції для заповнення таблиці `employee-table` історією відпусток співробітника.
### Історичне
— v1: Початкова реалізація логіки для відображення особистих даних про відпустку співробітника. 
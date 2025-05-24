# Refactoring/Design Plan: HR Dashboard Enhancements and Employee Data Management Adjustments

## 1. Executive Summary & Goals
This plan outlines the architectural changes required to enhance the HR Dashboard functionality within the vacation management project. The primary objective is to implement an employee deletion feature and refine the employee data editing process.

**Key Goals:**
1.  Enable HR Managers to delete employees from the system via the "СОТРУДНИКИ" (Employees) table.
2.  Streamline the "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" (Edit Employee Data) form by removing the direct F.I.O. editing field.
3.  Ensure all changes are robust, maintain data integrity, and adhere to existing coding standards.

## 2. Current Situation Analysis
The existing system features an HR Dashboard (`components/hr_dashboard.py`) allowing HR Managers to view, add, and edit employee information, as well as manage vacations. Employee data is stored in an SQLite database, accessed via `data/db_operations.py`. Callbacks in `app.py` handle the application logic.

**Relevant components for this task:**
*   `components/hr_dashboard.py`: Contains the UI for the "СОТРУДНИКИ" table and the "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" form.
*   `app.py`: Contains callbacks that populate these UI elements and handle form submissions.
*   `data/db_operations.py`: Contains functions for database interactions, which will need a new employee deletion function and potentially minor adjustments to the update function's usage.

**Key pain points/limitations addressed:**
*   No functionality to delete employees.
*   The "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" form includes a field for "Новое Ф.И.О.", which is redundant or undesirable as F.I.O. is primarily an identifier selected via a dropdown and typically not changed in this context.

## 3. Proposed Solution / Refactoring Strategy

### 3.1. High-Level Design / Architectural Overview
The proposed solution involves modifications across the UI, application logic, and data access layers.

1.  **Employee Deletion:**
    *   The "СОТРУДНИКИ" table (`hr-employees-table`) will be modified to use `row_selectable='multi'`, which adds a checkbox column for selection.
    *   A "УДАЛИТЬ" (DELETE) button will be added below this table.
    *   A new callback in `app.py` will handle the button click, retrieve the selected employee ID(s), validate that only one employee is selected, and call a new database function to perform the deletion.
    *   The database function `delete_employee` in `db_operations.py` will remove the employee and their associated vacation records. It will also nullify references to this employee if they were a manager to others.
2.  **F.I.O. Edit Field Removal:**
    *   The "Новое Ф.И.О. (если меняется)" input field (`hr-edit-employee-fio-input`) will be removed from the "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" form in `components/hr_dashboard.py`.
    *   The corresponding Dash callbacks in `app.py` (`populate_edit_employee_form` and `handle_save_employee_data`) will be updated to reflect this removal. The employee's F.I.O. will be treated as non-editable through this form; the existing F.I.O. will be preserved during updates of other fields.

### 3.2. Key Components / Modules

*   **`components/hr_dashboard.py` (UI Layer):**
    *   **`hr-employees-table` (DataTable):** Will be modified to include a selection checkbox column and allow row selection.
    *   **New "УДАЛИТЬ" Button:** Will be added to trigger the deletion process.
    *   **New Notification Area:** For displaying results of the delete operation.
    *   **"ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" Form:** The `hr-edit-employee-fio-input` field will be removed.
*   **`app.py` (Application Logic Layer):**
    *   **New Callback for Employee Deletion:** Will handle the logic for deleting an employee, including input validation, calling the database operation, and providing user feedback.
    *   **Modified `populate_edit_employee_form` Callback:** Will no longer attempt to populate the removed F.I.O. input field.
    *   **Modified `handle_save_employee_data` Callback:** Will no longer take the new F.I.O. as input. It will fetch the employee's current F.I.O. from the database to ensure it's preserved when updating other employee details.
    *   **Modified `update_hr_employees_table` Callback:** Ensure `row_ids` are correctly supplied to `hr-employees-table` using the employee's database ID to support `selected_row_ids`.
*   **`data/db_operations.py` (Data Access Layer):**
    *   **New `delete_employee(employee_id)` function:** Will handle the database operations for deleting an employee, their vacations, and updating manager references.
    *   The `update_employee_data_and_vacation` function will not change its signature but will be called with the original F.I.O.

### 3.3. Detailed Action Plan / Phases

#### Phase 1: Implement Employee Deletion Feature

*   **Objective(s):** Enable HR Managers to select and delete an employee from the "СОТРУДНИКИ" table.
*   **Priority:** High

*   **Task 1.1: Define Database Operation for Employee Deletion**
    *   **Rationale/Goal:** Create a robust function to remove an employee and their related data from the database.
    *   **Actions:**
        1.  In `data/db_operations.py`, create a new function `delete_employee(employee_id: int) -> tuple[bool, str]`.
        2.  Inside the function:
            a.  Establish a database connection and start a transaction.
            b.  Retrieve the F.I.O. of the employee being deleted (e.g., `deleted_employee_fio`).
            c.  Update the `staff` table: set `manager_fio = NULL` for any employees where `manager_fio` matches `deleted_employee_fio`.
            d.  Delete all records from the `vacations` table where `staff_id` matches `employee_id`.
            e.  Delete the employee record from the `staff` table where `id` matches `employee_id`.
            f.  Commit the transaction. If any step fails, roll back.
            g.  Return a tuple `(True, "Сотрудник успешно удален.")` on success, or `(False, "Ошибка удаления сотрудника: ...")` on failure.
    *   **Estimated Effort:** M
    *   **Deliverable/Criteria for Completion:** `delete_employee` function implemented, unit tested (if possible), and handles foreign key relationships correctly by cleaning up `vacations` and `manager_fio` references.

*   **Task 1.2: Update HR Dashboard UI for Employee Deletion**
    *   **Rationale/Goal:** Modify the "СОТРУДНИКИ" table to allow selection and add a delete button.
    *   **Actions:**
        1.  In `components/hr_dashboard.py`, locate the `hr-employees-table` DataTable definition within the "СОТРУДНИКИ" card.
        2.  Change `row_selectable='single'` to `row_selectable='multi'`. This will add a checkbox column at the beginning of the table.
        3.  Ensure the `id` property of the DataTable itself is `hr-employees-table`.
        4.  Below the `dash_table.DataTable(...)` component for `hr-employees-table`, add:
            ```python
            dbc.Button("УДАЛИТЬ", id='hr-delete-employee-button', color="danger", className="mt-2 me-2"),
            html.Div(id='hr-delete-employee-notification', className="mt-2")
            ```
    *   **Estimated Effort:** S
    *   **Deliverable/Criteria for Completion:** UI changes applied in `hr_dashboard.py`. The table shows checkboxes, and the "УДАЛИТЬ" button is visible.

*   **Task 1.3: Implement Callback Logic for Employee Deletion**
    *   **Rationale/Goal:** Connect the UI elements to the database operation for deleting an employee.
    *   **Actions:**
        1.  In `app.py`, create a new callback:
            ```python
            @app.callback(
                [Output('hr-delete-employee-notification', 'children'),
                 Output('hr-data-refresh-trigger', 'data', allow_duplicate=True)],
                [Input('hr-delete-employee-button', 'n_clicks')],
                [State('hr-employees-table', 'selected_row_ids')], # Requires row_ids in table data
                prevent_initial_call=True
            )
            def handle_delete_employee(n_clicks, selected_row_ids):
                if not n_clicks or not selected_row_ids:
                    raise PreventUpdate

                if len(selected_row_ids) != 1:
                    return dbc.Alert("Пожалуйста, выберите одного сотрудника для удаления.", color="warning"), dash.no_update

                employee_id_to_delete = selected_row_ids[0]
                
                # Ensure employee_id_to_delete is an integer if it comes as string
                try:
                    employee_id_to_delete = int(employee_id_to_delete)
                except ValueError:
                    return dbc.Alert("Некорректный ID сотрудника.", color="danger"), dash.no_update

                success, message = db_operations.delete_employee(employee_id_to_delete)

                if success:
                    alert_message = dbc.Alert(message, color="success")
                    # Trigger data refresh for tables
                    return alert_message, {'timestamp': datetime.now().timestamp()} 
                else:
                    alert_message = dbc.Alert(message, color="danger")
                    return alert_message, dash.no_update
            ```
        2.  Ensure the `update_hr_employees_table` callback provides `row_ids` to the `hr-employees-table`. The `data` prop for `dash_table.DataTable` should be a list of dictionaries, where each dictionary has an `id` key set to the employee's unique database ID. The `get_employees_for_hr_table` function in `db_operations.py` already returns `s.id`, so this should be straightforward to map in the callback.
            Example in `update_hr_employees_table` callback:
            `employees_data = db_operations.get_employees_for_hr_table()`
            `# Ensure 'id' key is used for row_ids, it should be present from get_employees_for_hr_table`
            `return columns, employees_data` (The `hr-employees-table` component in `hr_dashboard.py` will use these `id`s if its `data` prop receives them and no explicit `row_id` prop is set on the table component itself).
    *   **Estimated Effort:** M
    *   **Deliverable/Criteria for Completion:** Callback implemented. HR Manager can select one employee using the checkbox and delete them. Feedback is provided, and the table refreshes.

#### Phase 2: Modify "Edit Employee Data" Form

*   **Objective(s):** Remove the direct F.I.O. editing field from the employee edit form.
*   **Priority:** High

*   **Task 2.1: Update HR Dashboard UI for Edit Form**
    *   **Rationale/Goal:** Remove the redundant F.I.O. input field from the UI.
    *   **Actions:**
        1.  In `components/hr_dashboard.py`, navigate to the "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" `dbc.Card`.
        2.  Remove the following line:
            `dbc.Input(id='hr-edit-employee-fio-input', type='text', placeholder='Новое Ф.И.О. (если меняется)', className="mb-2"),`
    *   **Estimated Effort:** S
    *   **Deliverable/Criteria for Completion:** The specified input field is removed from the "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" form.

*   **Task 2.2: Adjust Callbacks for Edit Form**
    *   **Rationale/Goal:** Update backend logic to reflect UI changes and ensure F.I.O. is preserved during edits of other fields.
    *   **Actions:**
        1.  In `app.py`, modify the `populate_edit_employee_form` callback:
            *   Remove `Output('hr-edit-employee-fio-input', 'value')` from the list of outputs.
            *   Adjust the `return` statement tuple accordingly (remove the value that was intended for this output). The F.I.O. is already part of `employee_details` and displayed in the selection dropdown.
        2.  In `app.py`, modify the `handle_save_employee_data` callback:
            *   Remove `State('hr-edit-employee-fio-input', 'value')` from the list of states.
            *   Remove the corresponding `fio` parameter from the callback function definition.
            *   Inside the callback, before constructing the `updates` dictionary, fetch the current employee's data to get their F.I.O.:
                ```python
                # employee_id is from State('hr-edit-employee-selected-id-store', 'data')
                current_employee_data = db_operations.get_employee_by_id(employee_id)
                if not current_employee_data:
                    return dbc.Alert("Ошибка: Сотрудник для редактирования не найден.", color="danger"), dash.no_update
                original_fio = current_employee_data['fio']
                ```
            *   When constructing the `updates` dictionary, use this `original_fio`:
                `updates = { 'fio': original_fio, ... }`
    *   **Estimated Effort:** M
    *   **Deliverable/Criteria for Completion:** Callbacks updated. Editing an employee's data (other than F.I.O.) works correctly, and the F.I.O. remains unchanged. The application runs without errors related to the removed field.

### 3.4. Data Model Changes
No changes to the database schema (table structures or columns) are required. However, data integrity rules for deletion will be enforced programmatically (e.g., deleting associated vacations, nullifying manager references).

### 3.5. API Design / Interface Changes
*   **`data/db_operations.py`:**
    *   **New function:** `delete_employee(employee_id: int) -> tuple[bool, str]`
        *   **Input:** `employee_id` (integer)
        *   **Output:** Tuple containing a boolean success status and a message string.
        *   **Side effects:** Deletes employee, their vacations, and nullifies `manager_fio` references in `staff` table.

## 4. Key Considerations & Risk Mitigation

### 4.1. Technical Risks & Challenges
*   **Employee Deletion Cascade:** Ensuring all related data (vacations, manager references) is handled correctly upon employee deletion.
    *   **Mitigation:** The `delete_employee` function in `db_operations.py` will explicitly handle these cases within a transaction.
*   **Selection Logic in DataTable:** The user requested a "чекбокс (radiobutton)". `row_selectable='multi'` provides checkboxes. The callback will enforce single selection for deletion. If true radio button behavior (UI automatically deselects others) is strictly needed, it would require more complex client-side callbacks or custom component work.
    *   **Mitigation:** Start with `row_selectable='multi'` and server-side validation. Clarify with the user if this meets their needs.
*   **Concurrency:** Low risk for this application scale, but if multiple HR users could operate simultaneously, race conditions on delete/edit are theoretically possible.
    *   **Mitigation:** Current SQLite setup is typically single-writer. For larger systems, row-level locking or optimistic concurrency control would be considered. Not in scope for now.

### 4.2. Dependencies
*   **Internal:**
    *   Task 1.3 (Callback for Deletion) depends on Task 1.1 (DB Deletion Function) and Task 1.2 (UI for Deletion).
    *   Task 2.2 (Callback Adjustments for Edit) depends on Task 2.1 (UI for Edit Form).
*   **External:** None identified for this scope.

### 4.3. Non-Functional Requirements (NFRs) Addressed
*   **Usability:**
    *   Improved by providing a clear mechanism to delete employees.
    *   Streamlined edit form by removing a potentially confusing field.
*   **Maintainability:**
    *   Code changes will follow existing structure.
    *   Database operations are encapsulated in `db_operations.py`.
*   **Data Integrity:**
    *   The `delete_employee` function is designed to handle related data (vacations, manager references) to prevent orphaned records or inconsistencies. Transactions will be used for atomic operations.
*   **Security:**
    *   Deletion is a privileged operation, assumed to be restricted to HR Managers by the existing role-based access control (handled by `auth_middleware.py` and page routing). No new security vulnerabilities are introduced by these changes if existing auth is sound.

## 5. Success Metrics / Validation Criteria
*   **Employee Deletion:**
    *   HR Manager can select a single employee in the "СОТРУДНИКИ" table using the new checkbox column.
    *   Clicking "УДАЛИТЬ" successfully removes the employee from the table and the database.
    *   Associated vacation records for the deleted employee are also removed.
    *   If the deleted employee was a manager, their subordinates' `manager_fio` field is set to NULL.
    *   Appropriate success or error messages are displayed to the user.
    *   Attempting to delete without selection or with multiple selections results in a user-friendly warning.
*   **F.I.O. Edit Field Removal:**
    *   The "Новое Ф.И.О. (если меняется)" field is no longer visible in the "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА" form.
    *   Editing other details of an employee (e.g., IPN, role, vacation days) and saving them preserves the employee's original F.I.O.
    *   The application functions correctly without errors related to the removed field and its associated logic.

## 6. Assumptions Made
*   The existing authentication and authorization mechanism correctly restricts access to the HR Dashboard and its functionalities to users with the 'HR Manager' role.
*   The `hr-employees-table` data source (`get_employees_for_hr_table`) can reliably provide a unique `id` for each employee row, which will be used for `selected_row_ids`. (This is confirmed by inspecting `get_employees_for_hr_table` which selects `s.id`).
*   The user's request for "чекбокс (radiobutton)" in the first column is satisfied by a standard checkbox column (from `row_selectable='multi'`) with server-side validation to ensure only one employee is selected for deletion.
*   It is acceptable to set `manager_fio` to `NULL` for subordinates of a deleted manager. No automatic reassignment of subordinates is required.

## 7. Open Questions / Areas for Further Investigation
*   **Manager Deletion Policy:** Confirm if setting `manager_fio` to `NULL` for subordinates is the desired behavior. Are there scenarios where deletion of a manager should be prevented or trigger a different workflow (e.g., reassigning subordinates)? (The plan currently implements setting to `NULL`).
*   **User Experience for Selection:** Is the checkbox column (`row_selectable='multi'`) with server-side single-selection enforcement for deletion acceptable, or is a UI that behaves strictly like radio buttons (only one selectable at a time visually) a hard requirement? The latter would be more complex to implement.
*   **Error Handling for `delete_employee`:** What specific error messages or codes should be returned or logged if, for example, an employee to be deleted is not found, or if there's a database constraint violation not anticipated? (The plan suggests generic success/failure messages).

**Key discussion points for the team before finalizing or starting implementation:**
*   Review the proposed handling of `manager_fio` upon employee deletion.
*   Confirm the interpretation of "чекбокс (radiobutton)" and the planned implementation using `row_selectable='multi'` with validation.
```
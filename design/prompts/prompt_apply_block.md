# Refactoring/Design Plan: Manager Dashboard - Subordinate Vacations Block

## 1. Executive Summary & Goals
The primary objective of this plan is to enhance the Manager dashboard by adding a dedicated block at the top to display vacation information for the manager's direct subordinates. This block will provide a quick, read-only overview of subordinate vacations.

**Key Goals:**
1.  **Implement "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" Block:** Add a new, non-editable table displaying specified vacation details of subordinates.
2.  **Correct Placement:** Ensure this new block is prominently displayed at the top of the Manager dashboard.
3.  **Data Accuracy & Scope:** Fetch and display correct vacation data, scoped to the subordinates of the currently logged-in manager.

## 2. Current Situation Analysis
The existing `components/manager_dashboard.py` file includes a section titled `html.H3('Отпуска подчинённых сотрудников')` followed by a `dash_table.DataTable(id='subordinates-table', ...)`. This existing structure is semantically very similar to the requested "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block.

The current `manager_dashboard.py` layout is:
1.  Dashboard Title (`H2`)
2.  Manager's Personal Vacation Details (`dbc.Row` with `dbc.Card`)
3.  Manager's Own Vacation History (`H3` and `DataTable` with `id='manager-table'`)
4.  Subordinates' Vacations (`H3` and `DataTable` with `id='subordinates-table'`)

The `data/db_operations.py` file contains functions for database interactions but currently lacks a specific function to retrieve vacation details for all subordinates of a given manager in the format required.
The `app.py` file handles routing, authentication, and callbacks for populating dashboard components.

The request to add a block "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" at the top of the dashboard can be efficiently met by restructuring and enhancing the existing "Отпуска подчинённых сотрудников" section.

## 3. Proposed Solution / Refactoring Strategy

### 3.1. High-Level Design / Architectural Overview
The solution involves modifications in three main areas:
1.  **Backend (`data/db_operations.py`):** A new Python function will be created to fetch vacation data for a manager's subordinates. This function will query the `staff` and `vacations` tables.
2.  **Frontend UI (`components/manager_dashboard.py`):** The layout of the Manager dashboard will be updated. The existing "Отпуска подчинённых сотрудников" section (H3 and DataTable with `id='subordinates-table'`) will be wrapped in a `dbc.Card`, styled appropriately, and moved to the top of the dashboard. The DataTable within this card will be configured to display the required columns.
3.  **Application Logic (`app.py`):** A Dash callback will be implemented (or an existing one modified if one already populates `subordinates-table`) to use the new backend function and populate the `subordinates-table` with data specific to the logged-in manager.

Data Flow:
`Manager Dashboard View (Browser)` <- `app.py (Callback)` <- `db_operations.py (Data Fetching)` <- `SQLite DB`

### 3.2. Key Components / Modules

*   **`components/manager_dashboard.py`:**
    *   **Responsibility:** Define the visual structure of the Manager dashboard.
    *   **Modifications:**
        *   The existing `html.H3('Отпуска подчинённых сотрудников')` and `dash_table.DataTable(id='subordinates-table')` will be moved.
        *   They will be wrapped within a `dbc.Card` component. The `H3` content will become the `dbc.CardHeader`.
        *   This new `dbc.Card` will be positioned directly after the main `html.H2('Manager Dashboard')` and `html.Br()` elements, making it the first content block.
        *   The `subordinates-table` DataTable will be configured via a callback to display the specified columns.

*   **`data/db_operations.py`:**
    *   **Responsibility:** Handle all database interactions.
    *   **Modifications:**
        *   A new function `get_subordinates_vacation_details(manager_fio: str) -> list[dict]` will be added.
        *   This function will execute an SQL query to retrieve F.И.О., ИПН, Роль, Начало отпуска, Окончание отпуска, Всего дней отпуска, and Осталось дней отпуска for all employees who report to the given `manager_fio`.
        *   It will join `staff` and `vacations` tables.

*   **`app.py`:**
    *   **Responsibility:** Manage application state, routing, and callbacks.
    *   **Modifications:**
        *   A new Dash callback will be created (or an existing one for `subordinates-table` adapted).
        *   **Trigger:** `Input('url', 'pathname')` (when the manager dashboard is loaded).
        *   **Logic:**
            *   Verify the user is on the Manager dashboard and is a 'Manager'.
            *   Retrieve the logged-in manager's FIO from the `session` (e.g., `session.get('user_fio')`).
            *   Call `db_operations.get_subordinates_vacation_details()` with the manager's FIO.
            *   Return the columns definition and the fetched data.
        *   **Output:** `Output('subordinates-table', 'columns')` and `Output('subordinates-table', 'data')`.

### 3.3. Detailed Action Plan / Phases

#### **Phase 1: Backend Implementation**
*   Objective(s): Create the data retrieval logic for subordinate vacations.
*   **Priority:** High
*   **Task 1.1:** Define and implement `get_subordinates_vacation_details(manager_fio)` in `data/db_operations.py`.
    *   **Rationale/Goal:** To provide a structured way to fetch all necessary vacation data for a manager's subordinates.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:**
        *   Function is created in `db_operations.py`.
        *   The function accepts `manager_fio` as an argument.
        *   The function executes an SQL query joining `staff` and `vacations` tables, filtering by `manager_fio`.
        *   The SQL query selects the following fields with specified aliases:
            *   `s.fio AS sub_fio`
            *   `s.ipn AS sub_ipn`
            *   `s.role AS sub_role`
            *   `v.start_date AS vac_start_date`
            *   `v.end_date AS vac_end_date`
            *   `v.total_days AS vac_total_days`
            *   `s.remaining_vacation_days AS sub_remaining_days`
        *   The function returns a list of dictionaries, where each dictionary represents a row with keys matching the aliases.
        *   Basic unit tests for the function (e.g., with a test manager FIO and expected subordinate vacation data).

#### **Phase 2: Frontend and Application Logic Implementation**
*   Objective(s): Update the Manager dashboard UI and integrate the backend logic.
*   **Priority:** High (dependent on Phase 1)
*   **Task 2.1:** Modify `components/manager_dashboard.py` layout.
    *   **Rationale/Goal:** To create the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block and place it at the top of the dashboard.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:**
        *   A `dbc.Card` is added at the top of the `html.Div` layout, after `html.H2` and `html.Br`.
        *   The `dbc.CardHeader` contains `html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")`.
        *   The `dbc.CardBody` contains the `dash_table.DataTable` with `id='subordinates-table'`.
        *   The original `html.H3('Отпуска подчинённых сотрудников')` and its following `dash_table.DataTable(id='subordinates-table')` are removed from their old position.
        *   The `DataTable` properties `page_size`, `style_cell`, `style_header` are maintained or set as appropriate. `columns` and `data` attributes will be initially empty, to be populated by the callback.

*   **Task 2.2:** Implement the Dash callback in `app.py` to populate the `subordinates-table`.
    *   **Rationale/Goal:** To dynamically load and display subordinate vacation data based on the logged-in manager.
    *   **Estimated Effort (Optional):** M
    *   **Deliverable/Criteria for Completion:**
        *   A new callback is defined in `app.py`.
        *   Inputs: `Input('url', 'pathname')`.
        *   Outputs: `Output('subordinates-table', 'columns')`, `Output('subordinates-table', 'data')`.
        *   The callback checks if `pathname` corresponds to the manager's dashboard URL and if the logged-in user's role is 'Manager'.
        *   It retrieves `manager_fio` from `session`.
        *   It calls `db_operations.get_subordinates_vacation_details(manager_fio)`.
        *   It defines the `columns` structure for the DataTable as per user requirements:
            ```python
            columns = [
                {"name": "Ф.И.О.", "id": "sub_fio"},
                {"name": "ИПН", "id": "sub_ipn"},
                {"name": "Роль", "id": "sub_role"},
                {"name": "Начало", "id": "vac_start_date"},
                {"name": "Окончание", "id": "vac_end_date"},
                {"name": "Всего", "id": "vac_total_days"},
                {"name": "Осталось", "id": "sub_remaining_days"}
            ]
            ```
        *   The callback returns the `columns` and the fetched data.
        *   Handles cases where no data is found or `manager_fio` is not available by returning empty lists or appropriate messages.

#### **Phase 3: Testing and Validation**
*   Objective(s): Ensure the new feature works as expected and doesn't break existing functionality.
*   **Priority:** High (dependent on Phase 2)
*   **Task 3.1:** Manual testing of the Manager dashboard.
    *   **Rationale/Goal:** To verify functionality and UI from a user perspective.
    *   **Estimated Effort (Optional):** S
    *   **Deliverable/Criteria for Completion:**
        *   Log in as a Manager.
        *   Verify the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block appears at the top.
        *   Verify the table columns are correct as specified.
        *   Verify the data in the table accurately reflects the vacations of the manager's subordinates from the database.
        *   Verify the table is read-only.
        *   Verify other sections of the Manager dashboard (personal vacation details, own vacation history) are still functional.
        *   Test with a manager who has subordinates with vacations, a manager with subordinates without vacations (table should be empty or show a message), and a manager with no subordinates (table should be empty).

### 3.4. Data Model Changes
No changes to the existing database schema (`staff` and `vacations` tables) are required. Only a new SQL query will be introduced to fetch data.

### 3.5. API Design / Interface Changes
*   **Internal Function Signature (Python):**
    *   `db_operations.get_subordinates_vacation_details(manager_fio: str) -> list[dict]`
        *   Input: `manager_fio` (string) - The F.И.О. of the manager.
        *   Output: A list of dictionaries. Each dictionary represents one vacation record for a subordinate and should contain keys: `sub_fio`, `sub_ipn`, `sub_role`, `vac_start_date`, `vac_end_date`, `vac_total_days`, `sub_remaining_days`.

## 4. Key Considerations & Risk Mitigation

### 4.1. Technical Risks & Challenges
*   **Data Volume/Performance:** If a manager has a very large number of subordinates, each with many vacations, the query and table rendering might be slow.
    *   **Mitigation:** The current SQLite setup is likely sufficient for typical company sizes. If performance becomes an issue, consider pagination in the SQL query (if supported and necessary), optimizing the query, or indexing on `staff.manager_fio` and `vacations.staff_id`. For now, standard Dash DataTable pagination will handle the display.
*   **Accuracy of `manager_fio`:** The system relies on `staff.manager_fio` being correctly populated and `session['user_fio']` accurately reflecting the logged-in manager's FIO.
    *   **Mitigation:** This is an existing system dependency. Ensure data integrity practices for `manager_fio` are in place. The login mechanism must reliably set `session['user_fio']`.
*   **Timezone/Date Formatting:** Ensure date display is consistent and clear.
    *   **Mitigation:** Dates are stored as text 'YYYY-MM-DD'. Dash DataTable will display them as is, which is generally acceptable.

### 4.2. Dependencies
*   **Internal:**
    *   Task 2.1 (UI change) depends on the conceptual final structure.
    *   Task 2.2 (Callback) depends on Task 1.1 (DB function) and Task 2.1 (Table ID).
    *   Phase 3 (Testing) depends on Phase 1 and Phase 2.
*   **External:**
    *   Relies on the existing authentication mechanism to provide `session['user_fio']` and `session['user_role']`.

### 4.3. Non-Functional Requirements (NFRs) Addressed
*   **Usability:** The new block is placed at the top for high visibility. The table provides a clear, structured view of subordinate vacations.
*   **Performance:** The SQL query uses a standard JOIN, which is efficient for indexed columns on typical data sizes. DataTable pagination will handle large result sets on the client-side.
*   **Maintainability:**
    *   Changes are localized to `manager_dashboard.py`, `db_operations.py`, and `app.py`.
    *   The new database function `get_subordinates_vacation_details` encapsulates data retrieval logic, promoting separation of concerns.
    *   Adherence to "Код повинен бути чітко структурований та написаний згідно всіх необхідних стандартів" (User Rule) by using clear naming, modular functions, and Dash best practices.
*   **Security:** Data access is scoped by `manager_fio`, ensuring managers only see their own subordinates' data. This relies on the security of the session management.
*   **Reliability:** The feature's reliability depends on the correctness of the database query and the data in the `staff` and `vacations` tables.

## 5. Success Metrics / Validation Criteria
*   The "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block is present at the top of the Manager dashboard upon login for users with the 'Manager' role.
*   The table within the block correctly lists all vacations for the direct subordinates of the logged-in manager.
*   The table displays all seven specified columns: "Ф.И.О.", "ИПН", "Роль", "Начало", "Окончание", "Всего", "Осталось".
*   The data presented in the table is accurate and matches the information in the database.
*   The table is non-editable (view-only).
*   All other existing functionalities on the Manager dashboard remain operational.
*   The code changes are well-structured, commented where necessary, and follow project coding standards.

## 6. Assumptions Made
*   The `staff.manager_fio` field correctly links employees to their managers using the manager's F.И.О.
*   The `session['user_fio']` variable reliably contains the F.И.О. of the logged-in manager.
*   The `session['user_role']` variable correctly identifies if the user is a 'Manager'.
*   Displaying all vacations (past, current, future) for subordinates is the desired behavior. If specific filtering (e.g., by current year) is needed, the DB query will require adjustment.
*   The term "вверху дашборда" means it should be the first primary content block after the main dashboard title.
*   The existing `dash_table.DataTable` with `id='subordinates-table'` and its associated `H3` heading is the component to be enhanced and moved, rather than creating an entirely new, parallel table.

## 7. Open Questions / Areas for Further Investigation
*   **Vacation Timeframe:** Should the table display all historical, current, and future vacations, or only those within a specific timeframe (e.g., current calendar year, upcoming vacations)?
    *   **Current Plan:** Assumes all vacations linked to a subordinate are shown. If filtering is required, `get_subordinates_vacation_details` and its SQL query will need modification.
*   **Behavior for No Subordinates / No Vacations:** What should be displayed if a manager has no subordinates, or if subordinates have no recorded vacations?
    *   **Current Plan:** The table will appear empty. A "No data" message is default for Dash DataTable. This is generally acceptable.
*   **Sorting:** Should any default sorting be applied to the table (e.g., by subordinate name, then by vacation start date)?
    *   **Current Plan:** The SQL query sorts by `s.fio, v.start_date`. The DataTable itself also allows user-driven sorting.
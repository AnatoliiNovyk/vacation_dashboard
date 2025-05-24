## ROLE & PRIMARY GOAL:
You are a "Robotic Senior Software Engineer AI". Your mission is to meticulously analyze the user's coding request (`User Task`), strictly adhere to `Guiding Principles` and `User Rules`, comprehend the existing `File Structure`, and then generate a precise set of code changes. Your *sole and exclusive output* must be a single `git diff` formatted text. Zero tolerance for any deviation from the specified output format.

---

## INPUT SECTIONS OVERVIEW:
1.  `User Task`: The user's coding problem or feature request.
2.  `Guiding Principles`: Your core operational directives as a senior developer.
3.  `User Rules`: Task-specific constraints from the user, overriding `Guiding Principles` in case of conflict.
4.  `Output Format & Constraints`: Strict rules for your *only* output: the `git diff` text.
5.  `File Structure Format Description`: How the provided project files are structured in this prompt.
6.  `File Structure`: The current state of the project's files.

---

## 1. User Task
Ми прийняли решение внести некоторые правки в архитектуру нашего проекта. Правки будут делаться в дашборде Manager.
Вот они.
Сделай.
---
# Refactoring Plan: Manager Dashboard Layout Adjustment

## 1. Executive Summary & Goals
   - **Primary Objective:** To refactor the layout of the Manager Dashboard in the `vacation_dashboard` project to meet new user interface requirements.
   - **Key Goals:**
      1.  Position the "Мои личные данные отпуска" (My personal vacation data) block to the right of the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" (Subordinates' Vacations) block, ensuring they are on the same horizontal level.
      2.  Remove the textual heading "История моих отпусков" (History of my vacations).
      3.  Ensure all existing data displays and functionalities within the Manager Dashboard remain intact and operational.

## 2. Current Situation Analysis
The current layout of the Manager Dashboard (`components/manager_dashboard.py`) is structured as follows:
1.  A main title "Manager Dashboard".
2.  A `dbc.Card` component displaying "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ". This card currently occupies the full width available to it before any `dbc.Row` structuring for side-by-side elements.
3.  A `dbc.Row` containing two `dbc.Col` elements:
    *   The first `dbc.Col` (with `md=6`) houses the `dbc.Card` for "Мои личные данные отпуска".
    *   The second `dbc.Col` (with `md=6`) is currently a placeholder.
4.  An `html.H3` element with the text "История моих отпусков".
5.  A `dash_table.DataTable` (ID: `manager-table`) intended for displaying the manager's own vacation history.

This structure results in the "Мои личные данные отпуска" block appearing *below* the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block, not side-by-side.

## 3. Proposed Solution / Refactoring Strategy

### 3.1. High-Level Design / Architectural Overview
The refactoring will involve modifying the `layout` definition within the `components/manager_dashboard.py` file. The core idea is to use a single `dbc.Row` to contain both the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" card and the "Мои личные данные отпуска" card. Each of these cards will be wrapped in a `dbc.Col` component to manage their width and placement within the row. The specified `html.H3` heading will be removed.

**Textual Layout Comparison:**

**Current Layout (Simplified Snippet from `manager_dashboard.py`):**
```python
# ...
    # Block for Subordinates' Vacations
    dbc.Card([
        dbc.CardHeader(html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")),
        # ...
    ], className="mb-3"),

    # Row for Personal Vacation Data
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                # ...
            ], className="mb-3"),
        ], md=6),
        dbc.Col(md=6) # Placeholder
    ]),

    html.H3('История моих отпусков'), # To be removed
    dash_table.DataTable(id='manager-table', ...)
# ...
```

**Target Layout (Simplified Snippet for `manager_dashboard.py`):**
```python
# ...
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")),
                # ...
            ], className="mb-3")
        ], md=6), # Example width, adjust as needed

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                # ...
            ], className="mb-3")
        ], md=6)  # Example width, adjust as needed
    ]),

    dash_table.DataTable(id='manager-table', ...) # Manager's own vacation list, H3 removed
# ...
```

### 3.2. Key Components / Modules
-   **`components/manager_dashboard.py`**: This is the sole file requiring modification. The changes will be applied to its `layout` variable.

### 3.3. Detailed Action Plan / Phases

#### **Phase 1: Manager Dashboard UI Refactoring**
   - **Objective(s) for this phase:** Implement the requested layout changes in `components/manager_dashboard.py` to achieve the desired side-by-side block placement and text removal.
   - **Priority:** High
   - **Task 1.1:** Restructure blocks into a single `dbc.Row`.
      - **Rationale/Goal:** To place the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" card and the "Мои личные данные отпуска" card on the same horizontal level.
      - **Estimated Effort (Optional):** S
      - **Deliverable/Criteria for Completion:**
         - The `dbc.Card` for "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" is moved from being a direct child of the main `html.Div` (or its current container) into a new `dbc.Col`.
         - This new `dbc.Col` (containing the subordinates' card) and the existing `dbc.Col` (containing the personal data card) are placed as children of a *single, new* `dbc.Row`.
         - The original `dbc.Row` that only contained the personal data card and a placeholder is removed or its structure is adapted into the new single `dbc.Row`.
   - **Task 1.2:** Adjust Column Widths.
      - **Rationale/Goal:** To ensure both blocks ("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" and "Мои личные данные отпуска") share the row space appropriately. A 50%-50% split (e.g., `md=6` for each `dbc.Col`) is a common starting point.
      - **Estimated Effort (Optional):** S
      - **Deliverable/Criteria for Completion:** The two blocks are visually balanced side-by-side. Column width properties (e.g., `md=6`, `lg=6`) are correctly applied to the `dbc.Col` components.
   - **Task 1.3:** Remove "История моих отпусков" heading.
      - **Rationale/Goal:** To fulfill the user requirement of deleting this specific text from the dashboard.
      - **Estimated Effort (Optional):** S
      - **Deliverable/Criteria for Completion:** The `html.H3('История моих отпусков')` Python code line is deleted from the `layout` definition in `components/manager_dashboard.py`. The heading is no longer rendered on the page.
   - **Task 1.4:** Code Cleanup and Verification.
      - **Rationale/Goal:** Ensure the modified code is clean, well-structured, and that all functionalities (data loading, display) of the Manager Dashboard remain operational.
      - **Estimated Effort (Optional):** S
      - **Deliverable/Criteria for Completion:**
         - The `components/manager_dashboard.py` file reflects the new layout structure cleanly.
         - The Manager Dashboard loads without any Dash errors.
         - Data for subordinates' vacations, manager's personal vacation details, and manager's own vacation list table are correctly displayed.
         - The layout is responsive and appears correctly on various screen sizes (desktop, tablet).

### 3.4. Data Model Changes (if applicable)
   - N/A. This task involves UI layout changes only.

### 3.5. API Design / Interface Changes (if applicable)
   - N/A. No backend API changes are required for this UI refactoring.

## 4. Key Considerations & Risk Mitigation
   ### 4.1. Technical Risks & Challenges
      - **Layout Issues:** Incorrect nesting or configuration of `dbc.Row` and `dbc.Col` components could lead to unexpected visual output.
         - **Mitigation:** Careful implementation, adherence to Dash Bootstrap Components documentation, and iterative testing of the layout.
      - **Responsiveness:** The new two-column layout must adapt gracefully to different screen sizes.
         - **Mitigation:** Use responsive grid attributes (e.g., `md`, `lg`, `sm`) provided by Dash Bootstrap Components. Test on various viewport sizes. Default behavior of `md=6` columns is to stack on smaller screens, which is generally acceptable.
   ### 4.2. Dependencies
      - **Internal:** Tasks within Phase 1 are sequential or closely related. Task 1.4 (Verification) depends on the completion of Tasks 1.1, 1.2, and 1.3.
      - **External:** No new external library dependencies are introduced. Relies on existing `dash` and `dash-bootstrap-components`.
   ### 4.3. Non-Functional Requirements (NFRs) Addressed
      - **Usability:** The primary NFR addressed is usability, by restructuring the interface to match the user's preferred layout.
      - **Maintainability:** The code changes are localized to one component's layout definition. The resulting code should be as, or more, maintainable due to a potentially clearer row structure, adhering to the user rule: "Код повинен бути чітко структурований та написаний згідно всіх необхідних стандартів."

## 5. Success Metrics / Validation Criteria
1.  **Visual Confirmation (Layout Change):** The "Мои личные данные отпуска" block is rendered to the right of the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block, on the same horizontal level, when viewed on medium to large screens.
2.  **Visual Confirmation (Text Removal):** The text "История моих отпусков" is no longer visible anywhere on the Manager Dashboard.
3.  **Functional Integrity:** All data previously displayed in the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block, the "Мои личные данные отпуска" block, and the manager's own vacation history table (`manager-table`) continues to load and display correctly without errors.
4.  **Code Quality:** The changes in `components/manager_dashboard.py` are reviewed and deemed clean, readable, and correctly utilizing Dash Bootstrap Components.
5.  **Responsiveness:** The layout adapts appropriately on smaller screens (e.g., blocks stack vertically).

## 6. Assumptions Made
1.  The `dash_table.DataTable(id='manager-table')`, which displays the manager's own vacation history, should remain in the layout, positioned after the new two-column row containing the two cards. The request was to remove its preceding heading, not the table itself.
2.  An equal width split (e.g., `md=6` for each `dbc.Col`) for the "ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ" block and the "Мои личные данные отпуска" block is the desired initial configuration. This can be fine-tuned during implementation if specific proportions are preferred.
3.  The existing Dash callbacks associated with elements within `manager_dashboard.py` (e.g., populating `subordinates-table`, `manager-personal-vacation-details-div`, `manager-table`) will not require modification, as the IDs of these components are preserved.

## 7. Open Questions / Areas for Further Investigation
1.  **Specific Column Widths:** While `md=6` for each column is assumed for a 50/50 split, are there preferences for different proportions (e.g., `md=7` and `md=5`) or different behavior on larger/smaller screens (e.g., using `lg`, `sm` attributes)? (This plan proceeds with `md=6` as a default).
2.  **Title for Manager's Vacation Table:** With the "История моих отпусков" heading removed, should the `dash_table.DataTable(id='manager-table')` have any new descriptive title, or should it appear without any specific heading? (This plan assumes no new heading is required).

---

## 2. Guiding Principles (Your Senior Developer Logic)

### A. Analysis & Planning (Internal Thought Process - Do NOT output this part):
1.  **Deconstruct Request:** Deeply understand the `User Task` – its explicit requirements, implicit goals, and success criteria.
2.  **Identify Impact Zone:** Determine precisely which files/modules/functions will be affected.
3.  **Risk Assessment:** Anticipate edge cases, potential errors, performance impacts, and security considerations.
4.  **Assume with Reason:** If ambiguities exist in `User Task`, make well-founded assumptions based on best practices and existing code context. Document these assumptions internally if complex.
5.  **Optimal Solution Path:** Briefly evaluate alternative solutions, selecting the one that best balances simplicity, maintainability, readability, and consistency with existing project patterns.
6.  **Plan Changes:** Before generating diffs, mentally (or internally) outline the specific changes needed for each affected file.

### B. Code Generation & Standards:
*   **Simplicity & Idiomatic Code:** Prioritize the simplest, most direct solution. Write code that is idiomatic for the language and aligns with project conventions (inferred from `File Structure`). Avoid over-engineering.
*   **Respect Existing Architecture:** Strictly follow the established project structure, naming conventions, and coding style.
*   **Type Safety:** Employ type hints/annotations as appropriate for the language.
*   **Modularity:** Design changes to be modular and reusable where sensible.
*   **Documentation:**
    *   Add concise docstrings/comments for new public APIs, complex logic, or non-obvious decisions.
    *   Update existing documentation if changes render it inaccurate.
*   **Logging:** Introduce logging for critical operations or error states if consistent with the project's logging strategy.
*   **No New Dependencies:** Do NOT introduce external libraries/dependencies unless explicitly stated in `User Task` or `User Rules`.
*   **Atomicity of Changes (Hunks):** Each distinct change block (hunk in the diff output) should represent a small, logically coherent modification.
*   **Testability:** Design changes to be testable. If a testing framework is evident in `File Structure` or mentioned in `User Rules`, ensure new code is compatible.

---

## 3. User Rules
Код повинен бути чітко структурований та написаний згідно всіх необхідних стандартів.
*(These are user-provided, project-specific rules or task constraints. They take precedence over `Guiding Principles`.)*

---

## 4. Output Format & Constraints (MANDATORY & STRICT)

Your **ONLY** output will be a single, valid `git diff` formatted text, specifically in the **unified diff format**. No other text, explanations, or apologies are permitted.

### Git Diff Format Structure:
*   If no changes are required, output an empty string.
*   For each modified, newly created, or deleted file, include a diff block. Multiple file diffs are concatenated directly.

### File Diff Block Structure:
A typical diff block for a modified file looks like this:
```diff
diff --git a/relative/path/to/file.ext b/relative/path/to/file.ext
index <hash_old>..<hash_new> <mode>
--- a/relative/path/to/file.ext
+++ b/relative/path/to/file.ext
@@ -START_OLD,LINES_OLD +START_NEW,LINES_NEW @@
 context line (unchanged)
-old line to be removed
+new line to be added
 another context line (unchanged)
```

*   **`diff --git a/path b/path` line:**
    *   Indicates the start of a diff for a specific file.
    *   `a/path/to/file.ext` is the path in the "original" version.
    *   `b/path/to/file.ext` is the path in the "new" version. Paths are project-root-relative, using forward slashes (`/`).
*   **`index <hash_old>..<hash_new> <mode>` line (Optional Detail):**
    *   This line provides metadata about the change. While standard in `git diff`, if generating precise hashes and modes is overly complex for your internal model, you may omit this line or use placeholder values (e.g., `index 0000000..0000000 100644`). The `---`, `+++`, and `@@` lines are the most critical for applying the patch.
*   **`--- a/path/to/file.ext` line:**
    *   Specifies the original file. For **newly created files**, this should be `--- /dev/null`.
*   **`+++ b/path/to/file.ext` line:**
    *   Specifies the new file. For **deleted files**, this should be `+++ /dev/null`. For **newly created files**, this is `+++ b/path/to/new_file.ext`.
*   **Hunk Header (`@@ -START_OLD,LINES_OLD +START_NEW,LINES_NEW @@`):**
    *   `START_OLD,LINES_OLD`: 1-based start line and number of lines from the original file affected by this hunk.
        *   For **newly created files**, this is `0,0`.
        *   For hunks that **only add lines** (no deletions from original), `LINES_OLD` is `0`. (e.g., `@@ -50,0 +51,5 @@` means 5 lines added after original line 50).
    *   `START_NEW,LINES_NEW`: 1-based start line and number of lines in the new file version affected by this hunk.
        *   For **deleted files** (where the entire file is deleted), this is `0,0` for the `+++ /dev/null` part.
        *   For hunks that **only delete lines** (no additions), `LINES_NEW` is `0`. (e.g., `@@ -25,3 +25,0 @@` means 3 lines deleted starting from original line 25).
*   **Hunk Content:**
    *   Lines prefixed with a space (` `) are context lines (unchanged).
    *   Lines prefixed with a minus (`-`) are lines removed from the original file.
    *   Lines prefixed with a plus (`+`) are lines added to the new file.
    *   Include at least 3 lines of unchanged context around changes, where available. If changes are at the very beginning or end of a file, or if hunks are very close, fewer context lines are acceptable as per standard unified diff practice.

### Specific Cases:
*   **Newly Created Files:**
    ```diff
    diff --git a/relative/path/to/new_file.ext b/relative/path/to/new_file.ext
    new file mode 100644
    index 0000000..<hash_new_placeholder>
    --- /dev/null
    +++ b/relative/path/to/new_file.ext
    @@ -0,0 +1,LINES_IN_NEW_FILE @@
    +line 1 of new file
    +line 2 of new file
    ...
    ```
    *(The `new file mode` and `index` lines should be included. Use `100644` for regular files. For the hash in the `index` line, a placeholder like `abcdef0` is acceptable if the actual hash cannot be computed.)*

*   **Deleted Files:**
    ```diff
    diff --git a/relative/path/to/deleted_file.ext b/relative/path/to/deleted_file.ext
    deleted file mode <mode_old_placeholder>
    index <hash_old_placeholder>..0000000
    --- a/relative/path/to/deleted_file.ext
    +++ /dev/null
    @@ -1,LINES_IN_OLD_FILE +0,0 @@
    -line 1 of old file
    -line 2 of old file
    ...
    ```
    *(The `deleted file mode` and `index` lines should be included. Use a placeholder like `100644` for mode and `abcdef0` for hash if actual values are unknown.)*

*   **Untouched Files:** Do NOT include any diff output for files that have no changes.

### General Constraints on Generated Code:
*   **Minimal & Precise Changes:** Generate the smallest, most targeted diff that correctly implements the `User Task` per all rules.
*   **Preserve Integrity:** Do not break existing functionality unless the `User Task` explicitly requires it. The codebase should remain buildable/runnable.
*   **Leverage Existing Code:** Prefer modifying existing files over creating new ones, unless a new file is architecturally justified or required by `User Task` or `User Rules`.

---

## 5. File Structure Format Description
The `File Structure` (provided in the next section) is formatted as follows:
1.  An initial project directory tree structure (e.g., generated by `tree` or similar).
2.  Followed by the content of each file, using an XML-like structure:
    <file path="RELATIVE/PATH/TO/FILE">
    (File content here)
    </file>
    The `path` attribute contains the project-root-relative path, using forward slashes (`/`).
    File content is the raw text of the file. Each file block is separated by a newline.

---

## 6. File Structure
vacation_dashboard\
├── auth
│   └── auth_middleware.py
├── components
│   ├── __init__.py
│   ├── auth_form.py
│   ├── employee_dashboard.py
│   ├── hr_dashboard.py
│   └── manager_dashboard.py
├── data
│   └── db_operations.py
├── design
│   └── architecture.md
├── utils
│   ├── date_utils.py
│   └── excel_handler.py
├── app.py
├── README.md
└── requirements.txt

<file path="auth/auth_middleware.py">
def role_check_middleware(app):
    def middleware(environ, start_response):
        # Здесь можно сделать проверку cookie / session
        return app(environ, start_response)
    return middleware

</file>
<file path="components/__init__.py">
 
</file>
<file path="components/auth_form.py">
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H2("Авторизація", className="text-center mt-5"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dbc.Form([
                        dbc.Label("Ім'я користувача", html_for="username-input"),
                        dbc.Input(type="text", id="username-input", placeholder="Введіть ім'я користувача", className="mb-3"),
                        dbc.Label("Пароль", html_for="password-input"),
                        dbc.Input(type="password", id="password-input", placeholder="Введіть пароль", className="mb-3"),
                        dbc.Button("Увійти", id="login-button", color="primary", className="w-100")
                    ])
                ])
            ]),
            width=6,
            lg=4,
            className="mx-auto mt-4"
        )
    ])
], fluid=True) 
</file>
<file path="components/employee_dashboard.py">
from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Employee Dashboard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='employee-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6), # Adjust width as needed
        dbc.Col(md=6) # Placeholder for other content or to balance layout
    ]),
    html.H3("История моих отпусков"),
    dash_table.DataTable( # This table can list all of the employee's own vacations
        id='employee-table', # This ID is kept from original structure
        columns=[], # To be populated by a new callback
        data=[],    # To be populated by a new callback
        page_size=10
    ),
])

</file>
<file path="components/hr_dashboard.py">
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dcc.Store(id='hr-data-refresh-trigger'), # Used to trigger data refreshes
    dcc.Store(id='hr-edit-employee-selected-id-store'),
    dcc.Store(id='hr-edit-employee-target-vacation-id-store'),
    html.H2('HR Manager Dashboard'),
    html.Br(),
    # Блок списка сотрудников "СОТРУДНИКИ"
    dbc.Card([
        dbc.CardHeader(html.H4("СОТРУДНИКИ")),
        dbc.CardBody([
            dash_table.DataTable(
                id='hr-employees-table',
                columns=[], # Populated by callback
                data=[],    # Populated by callback
                row_selectable='single', # Changed to 'single' for radio button selection
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            ),
            dbc.Button("УДАЛИТЬ", id='hr-delete-employee-button', color="danger", className="mt-2 me-2"),
            html.Div(id='hr-delete-employee-notification', className="mt-2"
            )
        ])
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(md=4, children=[
            # Блок добавления нового сотрудника "ДОБАВИТЬ СОТРУДНИКА"
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ СОТРУДНИКА")),
                dbc.CardBody([
                    dbc.Input(id='hr-add-employee-fio-input', type='text', placeholder='Ф.И.О.', className="mb-2"),
                    dbc.Input(id='hr-add-employee-ipn-input', type='text', placeholder='ИПН (10 цифр)', className="mb-2", maxLength=10),
                    dcc.Dropdown(id='hr-add-employee-role-dropdown', options=[
                        {'label': 'Employee', 'value': 'Employee'},
                        {'label': 'Manager', 'value': 'Manager'},
                        {'label': 'HR Manager', 'value': 'HR Manager'}
                    ], placeholder='Роль', className="mb-2"),
                    dcc.Dropdown(id='hr-add-employee-manager-dropdown', options=[], placeholder='Менеджер', className="mb-2"), # Populated by callback
                    dbc.Input(id='hr-add-employee-vacation-days-input', type='number', placeholder='Отпуск в текущем году (дней)', className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-employee-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-employee-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ]),

        dbc.Col(md=4, children=[
            # Новый блок "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА"
            dbc.Card([
                dbc.CardHeader(html.H4("ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-edit-employee-fio-dropdown', placeholder='Ф.И.О. сотрудника', className="mb-2"),
                    dbc.Input(id='hr-edit-employee-ipn-input', type='text', placeholder='ИПН (10 цифр)', className="mb-2", maxLength=10),
                    dcc.Dropdown(id='hr-edit-employee-role-dropdown', placeholder='Роль', className="mb-2"),
                    dcc.Dropdown(id='hr-edit-employee-manager-dropdown', placeholder='Менеджер', className="mb-2", clearable=True),
                    dbc.Input(id='hr-edit-employee-annual-vacation-days-input', type='number', placeholder='Отпуск в этом году (дней)', className="mb-2"),
                    html.P("Даты отпуска (редактирование существующего):", className="mb-1 mt-2"),
                    dcc.DatePickerSingle(id='hr-edit-employee-vacation-start-date-picker', placeholder='Начало отпуска', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    dcc.DatePickerSingle(id='hr-edit-employee-vacation-end-date-picker', placeholder='Конец отпуска', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    dbc.Label("Остаток отпуска (дней):", className="mt-2"),
                    dbc.Input(id='hr-edit-employee-remaining-vacation-days-output', type='text', disabled=True, className="mb-2"),
                    dbc.Button("ЗАПИСАТЬ", id='hr-edit-employee-save-button', color="success", className="w-100"),
                    html.Div(id='hr-edit-employee-notification-div', className="mt-2")
                ])
            ], className="mb-3"),
        ]),

        dbc.Col(md=4, children=[
            # Блок добавления отпуска сотрудника "ДОБАВИТЬ ОТПУСК"
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ ОТПУСК")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-add-vacation-employee-dropdown', options=[], placeholder='Ф.И.О. сотрудника', className="mb-2"), # Populated by callback
                    html.P("Дата начала отпуска:", className="mb-1"),
                    dcc.DatePickerSingle(id='hr-add-vacation-start-date', placeholder='С', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    html.P("Дата окончания отпуска:", className="mb-1"),
                    dcc.DatePickerSingle(id='hr-add-vacation-end-date', placeholder='До', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    html.Div(id='hr-add-vacation-total-days-output', children="Всего дней: -", className="mb-2"),
                    html.Div(id='hr-add-vacation-remaining-days-output', children="Остаток дней: -", className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-vacation-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-vacation-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            # Блок истории отгулянных отпусков "ИСТОРИЯ ОТПУСКОВ"
            dbc.Card([
                dbc.CardHeader(html.H4("ИСТОРИЯ ОТПУСКОВ (текущий год)")),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='hr-vacation-history-table',
                        columns=[], # Populated by callback
                        data=[],    # Populated by callback
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    )
                ])
            ], className="mb-3"),
        ], md=6),

        dbc.Col([
            # Блок пользователя "Личные данные отпуска сотрудника"
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='hr-selected-employee-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6)
    ]),
])

</file>
<file path="components/manager_dashboard.py">
from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Manager Dashboard'),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")),
        dbc.CardBody([
            dash_table.DataTable(
                id='subordinates-table',
                columns=[], # Populated by callback
                data=[],    # Populated by callback
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6), # Adjust width as needed
        dbc.Col(md=6) # Placeholder for other content or to balance layout
    ]),
    html.H3('История моих отпусков'),
    dash_table.DataTable(id='manager-table', columns=[], data=[], page_size=10) # For manager's own vacation list
])

</file>
<file path="data/db_operations.py">
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

</file>
<file path="design/architecture.md">
vacation_dashboard\
├── auth
│   └── auth_middleware.py
├── components
│   ├── __init__.py
│   ├── auth_form.py
│   ├── employee_dashboard.py
│   ├── hr_dashboard.py
│   └── manager_dashboard.py
├── data
│   └── db_operations.py
├── design
│   └── architecture.md
├── utils
│   ├── date_utils.py
│   └── excel_handler.py
├── app.py
├── README.md
└── requirements.txt

<file path="auth/auth_middleware.py">
def role_check_middleware(app):
    def middleware(environ, start_response):
        # Здесь можно сделать проверку cookie / session
        return app(environ, start_response)
    return middleware

</file>
<file path="components/__init__.py">
 
</file>
<file path="components/auth_form.py">
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H2("Авторизація", className="text-center mt-5"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dbc.Form([
                        dbc.Label("Ім'я користувача", html_for="username-input"),
                        dbc.Input(type="text", id="username-input", placeholder="Введіть ім'я користувача", className="mb-3"),
                        dbc.Label("Пароль", html_for="password-input"),
                        dbc.Input(type="password", id="password-input", placeholder="Введіть пароль", className="mb-3"),
                        dbc.Button("Увійти", id="login-button", color="primary", className="w-100")
                    ])
                ])
            ]),
            width=6,
            lg=4,
            className="mx-auto mt-4"
        )
    ])
], fluid=True) 
</file>
<file path="components/employee_dashboard.py">
from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Employee Dashboard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='employee-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6), # Adjust width as needed
        dbc.Col(md=6) # Placeholder for other content or to balance layout
    ]),
    html.H3("История моих отпусков"),
    dash_table.DataTable( # This table can list all of the employee's own vacations
        id='employee-table', # This ID is kept from original structure
        columns=[], # To be populated by a new callback
        data=[],    # To be populated by a new callback
        page_size=10
    ),
])

</file>
<file path="components/hr_dashboard.py">
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dcc.Store(id='hr-data-refresh-trigger'), # Used to trigger data refreshes
    dcc.Store(id='hr-edit-employee-selected-id-store'),
    dcc.Store(id='hr-edit-employee-target-vacation-id-store'),
    html.H2('HR Manager Dashboard'),
    html.Br(),
    # Блок списка сотрудников "СОТРУДНИКИ"
    dbc.Card([
        dbc.CardHeader(html.H4("СОТРУДНИКИ")),
        dbc.CardBody([
            dash_table.DataTable(
                id='hr-employees-table',
                columns=[], # Populated by callback
                data=[],    # Populated by callback
                row_selectable='single', # Changed to 'single' for radio button selection
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            ),
            dbc.Button("УДАЛИТЬ", id='hr-delete-employee-button', color="danger", className="mt-2 me-2"),
            html.Div(id='hr-delete-employee-notification', className="mt-2"
            )
        ])
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(md=4, children=[
            # Блок добавления нового сотрудника "ДОБАВИТЬ СОТРУДНИКА"
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ СОТРУДНИКА")),
                dbc.CardBody([
                    dbc.Input(id='hr-add-employee-fio-input', type='text', placeholder='Ф.И.О.', className="mb-2"),
                    dbc.Input(id='hr-add-employee-ipn-input', type='text', placeholder='ИПН (10 цифр)', className="mb-2", maxLength=10),
                    dcc.Dropdown(id='hr-add-employee-role-dropdown', options=[
                        {'label': 'Employee', 'value': 'Employee'},
                        {'label': 'Manager', 'value': 'Manager'},
                        {'label': 'HR Manager', 'value': 'HR Manager'}
                    ], placeholder='Роль', className="mb-2"),
                    dcc.Dropdown(id='hr-add-employee-manager-dropdown', options=[], placeholder='Менеджер', className="mb-2"), # Populated by callback
                    dbc.Input(id='hr-add-employee-vacation-days-input', type='number', placeholder='Отпуск в текущем году (дней)', className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-employee-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-employee-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ]),

        dbc.Col(md=4, children=[
            # Новый блок "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА"
            dbc.Card([
                dbc.CardHeader(html.H4("ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-edit-employee-fio-dropdown', placeholder='Ф.И.О. сотрудника', className="mb-2"),
                    dbc.Input(id='hr-edit-employee-ipn-input', type='text', placeholder='ИПН (10 цифр)', className="mb-2", maxLength=10),
                    dcc.Dropdown(id='hr-edit-employee-role-dropdown', placeholder='Роль', className="mb-2"),
                    dcc.Dropdown(id='hr-edit-employee-manager-dropdown', placeholder='Менеджер', className="mb-2", clearable=True),
                    dbc.Input(id='hr-edit-employee-annual-vacation-days-input', type='number', placeholder='Отпуск в этом году (дней)', className="mb-2"),
                    html.P("Даты отпуска (редактирование существующего):", className="mb-1 mt-2"),
                    dcc.DatePickerSingle(id='hr-edit-employee-vacation-start-date-picker', placeholder='Начало отпуска', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    dcc.DatePickerSingle(id='hr-edit-employee-vacation-end-date-picker', placeholder='Конец отпуска', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    dbc.Label("Остаток отпуска (дней):", className="mt-2"),
                    dbc.Input(id='hr-edit-employee-remaining-vacation-days-output', type='text', disabled=True, className="mb-2"),
                    dbc.Button("ЗАПИСАТЬ", id='hr-edit-employee-save-button', color="success", className="w-100"),
                    html.Div(id='hr-edit-employee-notification-div', className="mt-2")
                ])
            ], className="mb-3"),
        ]),

        dbc.Col(md=4, children=[
            # Блок добавления отпуска сотрудника "ДОБАВИТЬ ОТПУСК"
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ ОТПУСК")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-add-vacation-employee-dropdown', options=[], placeholder='Ф.И.О. сотрудника', className="mb-2"), # Populated by callback
                    html.P("Дата начала отпуска:", className="mb-1"),
                    dcc.DatePickerSingle(id='hr-add-vacation-start-date', placeholder='С', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    html.P("Дата окончания отпуска:", className="mb-1"),
                    dcc.DatePickerSingle(id='hr-add-vacation-end-date', placeholder='До', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    html.Div(id='hr-add-vacation-total-days-output', children="Всего дней: -", className="mb-2"),
                    html.Div(id='hr-add-vacation-remaining-days-output', children="Остаток дней: -", className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-vacation-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-vacation-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            # Блок истории отгулянных отпусков "ИСТОРИЯ ОТПУСКОВ"
            dbc.Card([
                dbc.CardHeader(html.H4("ИСТОРИЯ ОТПУСКОВ (текущий год)")),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='hr-vacation-history-table',
                        columns=[], # Populated by callback
                        data=[],    # Populated by callback
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    )
                ])
            ], className="mb-3"),
        ], md=6),

        dbc.Col([
            # Блок пользователя "Личные данные отпуска сотрудника"
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='hr-selected-employee-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6)
    ]),
])

</file>
<file path="components/manager_dashboard.py">
from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Manager Dashboard'),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")),
        dbc.CardBody([
            dash_table.DataTable(
                id='subordinates-table',
                columns=[], # Populated by callback
                data=[],    # Populated by callback
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ])
    ], className="mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6), # Adjust width as needed
        dbc.Col(md=6) # Placeholder for other content or to balance layout
    ]),
    html.H3('История моих отпусков'),
    dash_table.DataTable(id='manager-table', columns=[], data=[], page_size=10) # For manager's own vacation list
])

</file>
<file path="data/db_operations.py">
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

</file>
<file path="design/architecture.md">
vacation_dashboard\
├── auth
│   └── auth_middleware.py
├── components
│   ├── __init__.py
│   ├── auth_form.py
│   ├── employee_dashboard.py
│   ├── hr_dashboard.py
│   └── manager_dashboard.py
├── data
│   └── db_operations.py
├── utils
│   ├── date_utils.py
│   └── excel_handler.py
├── app.py
├── README.md
└── requirements.txt

<file path="auth/auth_middleware.py">
def role_check_middleware(app):
    def middleware(environ, start_response):
        # Здесь можно сделать проверку cookie / session
        return app(environ, start_response)
    return middleware

</file>
<file path="components/__init__.py">
 
</file>
<file path="components/auth_form.py">
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H2("Авторизація", className="text-center mt-5"),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dbc.Form([
                        dbc.Label("Ім'я користувача", html_for="username-input"),
                        dbc.Input(type="text", id="username-input", placeholder="Введіть ім'я користувача", className="mb-3"),
                        dbc.Label("Пароль", html_for="password-input"),
                        dbc.Input(type="password", id="password-input", placeholder="Введіть пароль", className="mb-3"),
                        dbc.Button("Увійти", id="login-button", color="primary", className="w-100")
                    ])
                ])
            ]),
            width=6,
            lg=4,
            className="mx-auto mt-4"
        )
    ])
], fluid=True) 
</file>
<file path="components/employee_dashboard.py">
from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Employee Dashboard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='employee-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6), # Adjust width as needed
        dbc.Col(md=6) # Placeholder for other content or to balance layout
    ]),
    html.H3("История моих отпусков"),
    dash_table.DataTable( # This table can list all of the employee's own vacations
        id='employee-table', # This ID is kept from original structure
        columns=[], # To be populated by a new callback
        data=[],    # To be populated by a new callback
        page_size=10
    ),
])

</file>
<file path="components/hr_dashboard.py">
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dcc.Store(id='hr-data-refresh-trigger'), # Used to trigger data refreshes
    dcc.Store(id='hr-edit-employee-selected-id-store'),
    dcc.Store(id='hr-edit-employee-target-vacation-id-store'),
    html.H2('HR Manager Dashboard'),
    html.Br(),
    # Блок списка сотрудников "СОТРУДНИКИ"
    dbc.Card([
        dbc.CardHeader(html.H4("СОТРУДНИКИ")),
        dbc.CardBody([
            dash_table.DataTable(
                id='hr-employees-table',
                columns=[], # Populated by callback
                data=[],    # Populated by callback
                row_selectable='single',
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ])
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(md=4, children=[
            # Блок добавления нового сотрудника "ДОБАВИТЬ СОТРУДНИКА"
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ СОТРУДНИКА")),
                dbc.CardBody([
                    dbc.Input(id='hr-add-employee-fio-input', type='text', placeholder='Ф.И.О.', className="mb-2"),
                    dbc.Input(id='hr-add-employee-ipn-input', type='text', placeholder='ИПН (10 цифр)', className="mb-2", maxLength=10),
                    dcc.Dropdown(id='hr-add-employee-role-dropdown', options=[
                        {'label': 'Employee', 'value': 'Employee'},
                        {'label': 'Manager', 'value': 'Manager'},
                        {'label': 'HR Manager', 'value': 'HR Manager'}
                    ], placeholder='Роль', className="mb-2"),
                    dcc.Dropdown(id='hr-add-employee-manager-dropdown', options=[], placeholder='Менеджер', className="mb-2"), # Populated by callback
                    dbc.Input(id='hr-add-employee-vacation-days-input', type='number', placeholder='Отпуск в текущем году (дней)', className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-employee-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-employee-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ]),

        dbc.Col(md=4, children=[
            # Новый блок "ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА"
            dbc.Card([
                dbc.CardHeader(html.H4("ИЗМЕНИТЬ ДАННЫЕ СОТРУДНИКА")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-edit-employee-fio-dropdown', placeholder='Ф.И.О. сотрудника', className="mb-2"),
                    dbc.Input(id='hr-edit-employee-fio-input', type='text', placeholder='Новое Ф.И.О. (если меняется)', className="mb-2"), # Added for FIO edit
                    dbc.Input(id='hr-edit-employee-ipn-input', type='text', placeholder='ИПН (10 цифр)', className="mb-2", maxLength=10),
                    dcc.Dropdown(id='hr-edit-employee-role-dropdown', placeholder='Роль', className="mb-2"),
                    dcc.Dropdown(id='hr-edit-employee-manager-dropdown', placeholder='Менеджер', className="mb-2", clearable=True),
                    dbc.Input(id='hr-edit-employee-annual-vacation-days-input', type='number', placeholder='Отпуск в этом году (дней)', className="mb-2"),
                    html.P("Даты отпуска (редактирование существующего):", className="mb-1 mt-2"),
                    dcc.DatePickerSingle(id='hr-edit-employee-vacation-start-date-picker', placeholder='Начало отпуска', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    dcc.DatePickerSingle(id='hr-edit-employee-vacation-end-date-picker', placeholder='Конец отпуска', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    dbc.Label("Остаток отпуска (дней):", className="mt-2"),
                    dbc.Input(id='hr-edit-employee-remaining-vacation-days-output', type='text', disabled=True, className="mb-2"),
                    dbc.Button("ЗАПИСАТЬ", id='hr-edit-employee-save-button', color="success", className="w-100"),
                    html.Div(id='hr-edit-employee-notification-div', className="mt-2")
                ])
            ], className="mb-3"),
        ]),

        dbc.Col(md=4, children=[
            # Блок добавления отпуска сотрудника "ДОБАВИТЬ ОТПУСК"
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ ОТПУСК")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-add-vacation-employee-dropdown', options=[], placeholder='Ф.И.О. сотрудника', className="mb-2"), # Populated by callback
                    html.P("Дата начала отпуска:", className="mb-1"),
                    dcc.DatePickerSingle(id='hr-add-vacation-start-date', placeholder='С', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    html.P("Дата окончания отпуска:", className="mb-1"),
                    dcc.DatePickerSingle(id='hr-add-vacation-end-date', placeholder='До', display_format='YYYY-MM-DD', className="mb-2 d-block"),
                    html.Div(id='hr-add-vacation-total-days-output', children="Всего дней: -", className="mb-2"),
                    html.Div(id='hr-add-vacation-remaining-days-output', children="Остаток дней: -", className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-vacation-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-vacation-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            # Блок истории отгулянных отпусков "ИСТОРИЯ ОТПУСКОВ"
            dbc.Card([
                dbc.CardHeader(html.H4("ИСТОРИЯ ОТПУСКОВ (текущий год)")),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='hr-vacation-history-table',
                        columns=[], # Populated by callback
                        data=[],    # Populated by callback
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    )
                ])
            ], className="mb-3"),
        ], md=6),

        dbc.Col([
            # Блок пользователя "Личные данные отпуска сотрудника"
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='hr-selected-employee-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6)
    ]),
])

</file>
<file path="components/manager_dashboard.py">
from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Manager Dashboard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6), # Adjust width as needed
        dbc.Col(md=6) # Placeholder for other content or to balance layout
    ]),
    html.H3('История моих отпусков'),
    dash_table.DataTable(id='manager-table', columns=[], data=[], page_size=10), # For manager's own vacation list
    html.H3('Отпуска подчинённых сотрудников'),
    dash_table.DataTable(id='subordinates-table', columns=[], data=[], page_size=10) # For subordinates' vacation list
])

</file>
<file path="data/db_operations.py">
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

</file>
<file path="utils/date_utils.py">
from datetime import datetime

def calculate_days(start_date, end_date):
    d1 = datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.strptime(end_date, '%Y-%m-%d')
    return (d2 - d1).days + 1

</file>
<file path="utils/excel_handler.py">

</file>
<file path="app.py">
from dash import Dash, dcc, html, Input, Output, State
from flask import Flask, session, redirect, request
import dash
from dash.exceptions import PreventUpdate
from auth.auth_middleware import role_check_middleware
from components import employee_dashboard, manager_dashboard, hr_dashboard
from data import db_operations # Import db_operations
from utils import date_utils
import dash_bootstrap_components as dbc
import os # For secret key generation
from datetime import datetime

server = Flask(__name__)
# Use a secure secret key, e.g., from environment variable or generated
server.secret_key = os.urandom(24) # Generate a random secret key

app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server.wsgi_app = role_check_middleware(server.wsgi_app) # Middleware can remain, it's a pass-through

# Login page layout function
def login_page_layout():
    return dbc.Row(dbc.Col([
        html.H2("Авторизація Співробітника"),
        html.P("Будь ласка, введіть ваш ІПН для входу."),
        dcc.Input(id="login-ipn-input", type="text", placeholder="ІПН", className="mb-2", style={'width': '300px'}, n_submit=0),
        html.Br(),
        html.Button("Увійти", id="login-button", n_clicks=0, className="btn btn-primary"),
        html.Div(id="login-output-message", className="mt-2")
    ], width={'size': 6, 'offset': 3}, className="text-center mt-5"))

# Role to path/layout mapping
ROLE_DASHBOARDS = {
    'Employee': employee_dashboard.layout,
    'Manager': manager_dashboard.layout,
    'HR Manager': hr_dashboard.layout
}
ROLE_PATHS = {
    'Employee': '/employee',
    'Manager': '/manager',
    'HR Manager': '/hr'
}

# Main app layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='user-status-header'), # For user info and logout link
    html.Div(id='page-content')
], fluid=True)


# Callback to update header with user info and logout link
@app.callback(
    Output('user-status-header', 'children'),
    Input('url', 'pathname') # Trigger on URL change to update header
)
def update_user_header(pathname):
    if 'user_ipn' in session:
        user_fio = session.get('user_fio', session.get('user_ipn')) # Use FIO if available
        user_role = session.get('user_role', 'Невідома роль')
        
        header_content = [
            html.Span(f"Користувач: {user_fio} (Роль: {user_role})"),
            dcc.Link("Вийти", href="/logout", style={'marginLeft': '20px', 'color': 'red'})
        ]
        return html.Div(header_content, style={'padding': '10px', 'backgroundColor': '#f0f0f0', 'borderBottom': '1px solid #ccc', 'marginBottom': '15px'})
    return None # No header if not logged in


# Callback to handle login
@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('login-output-message', 'children')],
    [Input('login-button', 'n_clicks'),
     Input('login-ipn-input', 'n_submit')],
    [State('login-ipn-input', 'value')],
    prevent_initial_call=True
)
def process_login(n_clicks_login_btn, n_submit_ipn_field, ipn):
    if not ipn:
        return dash.no_update, dbc.Alert("Будь ласка, введіть ІПН.", color="warning")

    employee = db_operations.get_employee_by_ipn(ipn)

    if employee: # User found, IPN is effectively the password
        session['user_ipn'] = employee['ipn']
        session['user_role'] = employee['role']
        session['user_fio'] = employee.get('fio', employee['ipn']) # Store FIO if available

        redirect_path = ROLE_PATHS.get(employee['role'])
        if redirect_path:
            return redirect_path, dbc.Alert(f"Успішний вхід. Перенаправлення...", color="success", duration=2000)
        else:
            session.clear() 
            return dash.no_update, dbc.Alert("Помилка: Роль користувача не налаштована для перенаправлення.", color="danger")
    else: # User not found or IPN incorrect
        return dash.no_update, dbc.Alert("Помилка: Співробітника з таким ІПН не знайдено.", color="danger")


# Main callback to display pages and handle routing/auth
@app.callback(
    [Output('page-content', 'children'),
     Output('url', 'pathname', allow_duplicate=True)], # allow_duplicate because url.pathname is Input and Output
    [Input('url', 'pathname')],
    prevent_initial_call=True # Avoid initial call issues with redirects
)
def display_page_content(pathname):
    authenticated_ipn = session.get('user_ipn')
    authenticated_role = session.get('user_role')

    if pathname == '/logout':
        session.clear()
        return login_page_layout(), '/login'

    if authenticated_ipn: # User is logged in
        user_dashboard_path = ROLE_PATHS.get(authenticated_role)

        if pathname == '/login' or pathname == '/':
            return dash.no_update, user_dashboard_path if user_dashboard_path else '/'

        if pathname in ROLE_PATHS.values():
            if pathname == user_dashboard_path:
                return ROLE_DASHBOARDS[authenticated_role], dash.no_update
            else: # Trying to access a dashboard not matching their role
                return dash.no_update, user_dashboard_path
        
        # For any other path when logged in, redirect to their dashboard
        return dash.no_update, user_dashboard_path if user_dashboard_path else '/'

    else: # User is NOT logged in
        if pathname == '/login':
            return login_page_layout(), dash.no_update
        # For any other path (including dashboards or root), redirect to login
        return login_page_layout(), '/login'

# --- HR Dashboard Callbacks ---
@app.callback(
    Output('hr-employees-table', 'columns'),
    Output('hr-employees-table', 'data'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data') # Store component to trigger refresh
)
def update_hr_employees_table(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate

    columns = [
        {"name": "Ф.И.О.", "id": "fio"},
        {"name": "ИПН", "id": "ipn"},
        {"name": "Роль", "id": "role"},
        {"name": "Менеджер", "id": "manager_fio"},
        {"name": "С", "id": "current_vacation_start_date"},
        {"name": "До", "id": "current_vacation_end_date"},
        {"name": "Всего", "id": "current_vacation_total_days"},
        {"name": "Остаток", "id": "remaining_vacation_days"}
    ]
    # This function needs to be implemented in db_operations to fetch combined data
    employees_data = db_operations.get_employees_for_hr_table()
    return columns, employees_data

@app.callback(
    Output('hr-add-employee-manager-dropdown', 'options'),
    Input('url', 'pathname')
)
def update_manager_dropdown(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    managers = db_operations.get_managers() # [{'label': 'Manager FIO', 'value': 'Manager FIO'}]
    return managers

@app.callback(
    Output('hr-add-employee-notification', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-add-employee-submit-button', 'n_clicks'),
    State('hr-add-employee-fio-input', 'value'),
    State('hr-add-employee-ipn-input', 'value'),
    State('hr-add-employee-role-dropdown', 'value'),
    State('hr-add-employee-manager-dropdown', 'value'),
    State('hr-add-employee-vacation-days-input', 'value'),
    prevent_initial_call=True
)
def handle_add_employee(n_clicks, fio, ipn, role, manager_fio, vacation_days):
    if not n_clicks:
        raise PreventUpdate
    if not all([fio, ipn, role, vacation_days]): # Manager can be optional for top HR/Manager
        return dbc.Alert("Заполните все обязательные поля (Ф.И.О., ИПН, Роль, Отпуск в году).", color="warning"), dash.no_update
    
    try:
        vacation_days = int(vacation_days)
    except ValueError:
        return dbc.Alert("Количество дней отпуска должно быть числом.", color="danger"), dash.no_update

    employee_id = db_operations.add_employee(fio, ipn, manager_fio, role, vacation_days, vacation_days)
    if employee_id:
        return dbc.Alert(f"Сотрудник {fio} успешно добавлен.", color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert(f"Ошибка добавления сотрудника {fio}.", color="danger"), dash.no_update

@app.callback(
    Output('hr-add-vacation-employee-dropdown', 'options'),
    Input('url', 'pathname')
)
def update_vacation_employee_dropdown(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    employees = db_operations.get_all_employees() # Assumes this returns list of dicts with 'id' and 'fio'
    options = [{'label': emp['fio'], 'value': emp['id']} for emp in employees if 'id' in emp and 'fio' in emp]
    return options

@app.callback(
    Output('hr-add-vacation-total-days-output', 'children'),
    Input('hr-add-vacation-start-date', 'date'),
    Input('hr-add-vacation-end-date', 'date')
)
def calculate_vacation_total_days(start_date, end_date):
    if start_date and end_date:
        try:
            days = date_utils.calculate_days(start_date, end_date)
            return f"Всего дней: {days}" if days > 0 else "Дата окончания должна быть после даты начала."
        except ValueError:
            return "Неверный формат дат."
    return "Всего дней: -"

@app.callback(
    Output('hr-add-vacation-remaining-days-output', 'children'),
    Input('hr-add-vacation-employee-dropdown', 'value'),
    Input('hr-add-vacation-start-date', 'date'),
    Input('hr-add-vacation-end-date', 'date')
)
def calculate_vacation_remaining_days(employee_id, start_date, end_date):
    if not employee_id:
        return "Остаток дней: -"
    
    employee = db_operations.get_employee_by_id(employee_id) # Needs implementation
    if not employee or 'remaining_vacation_days' not in employee:
        return "Остаток дней: (не удалось загрузить)"

    remaining_now = employee['remaining_vacation_days']
    
    if start_date and end_date:
        try:
            days_in_this_vacation = date_utils.calculate_days(start_date, end_date)
            if days_in_this_vacation > 0:
                return f"Остаток дней (после этого отпуска): {remaining_now - days_in_this_vacation}"
        except ValueError:
            pass # Handled by total_days callback
    return f"Остаток дней (текущий): {remaining_now}"

@app.callback(
    Output('hr-add-vacation-notification', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-add-vacation-submit-button', 'n_clicks'),
    State('hr-add-vacation-employee-dropdown', 'value'),
    State('hr-add-vacation-start-date', 'date'),
    State('hr-add-vacation-end-date', 'date'),
    prevent_initial_call=True
)
def handle_add_vacation(n_clicks, employee_id, start_date, end_date):
    if not n_clicks:
        raise PreventUpdate
    if not all([employee_id, start_date, end_date]):
        return dbc.Alert("Выберите сотрудника и укажите даты отпуска.", color="warning"), dash.no_update

    try:
        total_days = date_utils.calculate_days(start_date, end_date)
        if total_days <= 0:
            return dbc.Alert("Некорректный период отпуска.", color="danger"), dash.no_update
    except ValueError:
        return dbc.Alert("Неверный формат дат.", color="danger"), dash.no_update

    success = db_operations.add_vacation(employee_id, start_date, end_date, total_days)
    if success:
        return dbc.Alert("Отпуск успешно добавлен.", color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert("Ошибка добавления отпуска. Проверьте остаток дней.", color="danger"), dash.no_update

@app.callback(
    Output('hr-vacation-history-table', 'columns'),
    Output('hr-vacation-history-table', 'data'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data')
)
def update_vacation_history_table(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate
    
    columns = [
        {"name": "Ф.И.О.", "id": "fio"},
        {"name": "Менеджер", "id": "manager_fio"},
        {"name": "Начало", "id": "start_date"},
        {"name": "Конец", "id": "end_date"},
        {"name": "Всего", "id": "total_days"}
    ]
    current_year = datetime.now().year
    history_data = db_operations.get_vacation_history(current_year)
    return columns, history_data

# --- HR Dashboard: Edit Employee Data Callbacks ---

@app.callback(
    Output('hr-edit-employee-fio-dropdown', 'options'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data')
)
def update_edit_employee_fio_dropdown(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate
    employees = db_operations.get_all_employees()
    options = [{'label': emp['fio'], 'value': emp['id']} for emp in employees if 'id' in emp and 'fio' in emp]
    return options

@app.callback(
    Output('hr-edit-employee-role-dropdown', 'options'),
    Input('url', 'pathname') # Trigger once when HR page loads
)
def update_edit_employee_role_dropdown_options(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    return [
        {'label': 'Employee', 'value': 'Employee'},
        {'label': 'Manager', 'value': 'Manager'},
        {'label': 'HR Manager', 'value': 'HR Manager'}
    ]

@app.callback(
    Output('hr-edit-employee-manager-dropdown', 'options'),
    Input('url', 'pathname') # Trigger once when HR page loads
)
def update_edit_employee_manager_dropdown_options(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    managers = db_operations.get_managers()
    return managers

@app.callback(
    Output('hr-edit-employee-ipn-input', 'value'),
    Output('hr-edit-employee-role-dropdown', 'value'),
    Output('hr-edit-employee-manager-dropdown', 'value'),
    Output('hr-edit-employee-annual-vacation-days-input', 'value'),
    Output('hr-edit-employee-remaining-vacation-days-output', 'value'),
    Output('hr-edit-employee-vacation-start-date-picker', 'date'),
    Output('hr-edit-employee-vacation-end-date-picker', 'date'),
    Output('hr-edit-employee-selected-id-store', 'data'),
    Output('hr-edit-employee-target-vacation-id-store', 'data'),
    Input('hr-edit-employee-fio-dropdown', 'value'),
    Input('hr-data-refresh-trigger', 'data') # To refresh form after save
)
def populate_edit_employee_form(selected_employee_id, refresh_trigger):
    ctx = dash.callback_context
    triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If triggered by refresh_trigger, and we have a selected employee ID from dropdown, re-fetch.
    # Otherwise, only populate if fio_dropdown is the trigger.
    if triggered_input_id == 'hr-data-refresh-trigger' and not selected_employee_id:
        raise PreventUpdate # Don't clear form on general refresh if no employee selected
        
    if not selected_employee_id:
        return [None] * 7 + [None, None] # Clear all fields and stores

    employee_details = db_operations.get_employee_details_for_edit(selected_employee_id)
    if not employee_details:
        return [dash.no_update] * 7 + [selected_employee_id, None] # Keep selected ID, clear vacation ID

    vacation_start_date = employee_details['target_vacation']['start_date'] if employee_details.get('target_vacation') else None
    vacation_end_date = employee_details['target_vacation']['end_date'] if employee_details.get('target_vacation') else None
    target_vacation_id = employee_details['target_vacation']['id'] if employee_details.get('target_vacation') else None

    return (
        employee_details.get('ipn'),
        employee_details.get('role'),
        employee_details.get('manager_fio'),
        employee_details.get('vacation_days_per_year'),
        employee_details.get('remaining_vacation_days'),
        vacation_start_date,
        vacation_end_date,
        selected_employee_id, # Store the main employee ID
        target_vacation_id    # Store the ID of the vacation being shown/edited
    )

@app.callback(
    Output('hr-edit-employee-notification-div', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-edit-employee-save-button', 'n_clicks'),
    State('hr-edit-employee-selected-id-store', 'data'),
    State('hr-edit-employee-target-vacation-id-store', 'data'),
    State('hr-edit-employee-fio-input', 'value'), # Assuming FIO is editable, though plan implies it's from dropdown
    State('hr-edit-employee-ipn-input', 'value'),
    State('hr-edit-employee-role-dropdown', 'value'),
    State('hr-edit-employee-manager-dropdown', 'value'),
    State('hr-edit-employee-annual-vacation-days-input', 'value'),
    State('hr-edit-employee-vacation-start-date-picker', 'date'),
    State('hr-edit-employee-vacation-end-date-picker', 'date'),
    prevent_initial_call=True
)
def handle_save_employee_data(n_clicks, employee_id, target_vacation_id, fio, ipn, role, manager, annual_days, vac_start, vac_end):
    if not n_clicks or not employee_id:
        raise PreventUpdate

    # Basic validation (more can be added)
    if not all([fio, ipn, role, annual_days is not None]):
        return dbc.Alert("Ф.И.О., ИПН, Роль и Отпуск в году обязательны.", color="warning"), dash.no_update
    
    try:
        annual_days_int = int(annual_days)
        if annual_days_int < 0:
            return dbc.Alert("Отпуск в году не может быть отрицательным.", color="warning"), dash.no_update
    except ValueError:
        return dbc.Alert("Отпуск в году должен быть числом.", color="danger"), dash.no_update

    if (vac_start and not vac_end) or (not vac_start and vac_end):
        return dbc.Alert("Если указана одна дата отпуска, должна быть указана и вторая.", color="warning"), dash.no_update
    
    if vac_start and vac_end and vac_end < vac_start:
        return dbc.Alert("Дата окончания отпуска не может быть раньше даты начала.", color="warning"), dash.no_update

    updates = {
        'fio': fio,
        'ipn': ipn,
        'role': role,
        'manager_fio': manager, # Can be None
        'vacation_days_per_year': annual_days_int,
        'target_vacation_id': target_vacation_id, # Might be None
        'vacation_start_date': vac_start, # Might be None
        'vacation_end_date': vac_end      # Might be None
    }

    success, message = db_operations.update_employee_data_and_vacation(employee_id, updates)

    if success:
        return dbc.Alert(message, color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert(message, color="danger"), dash.no_update

# --- Personal Vacation Details Callbacks ---

def _create_personal_vacation_details_content(employee_data, user_fio_from_session):
    """Helper function to create content for personal vacation details block."""
    if not employee_data:
        return html.P(f"Не удалось загрузить данные для пользователя {user_fio_from_session}.")

    fio = employee_data.get('fio', user_fio_from_session) # Prefer FIO from DB if available
    start_date = employee_data.get('current_vacation_start_date', 'N/A')
    end_date = employee_data.get('current_vacation_end_date', 'N/A')
    total_days = employee_data.get('current_vacation_total_days', 'N/A')
    remaining_days = employee_data.get('remaining_vacation_days', 'N/A')

    return [
        html.H5(f"Личные данные отпуска: {fio}"),
        html.P(f"Ближайший/текущий отпуск с: {start_date}"),
        html.P(f"Ближайший/текущий отпуск до: {end_date}"),
        html.P(f"Всего дней в этом отпуске: {total_days}"),
        html.P(f"Остаётся дней отпуска в году: {remaining_days}")
    ]

@app.callback(
    Output('hr-selected-employee-details-div', 'children'), # Repurposed from original
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data') # Allow refresh if underlying data changes
)
def display_hr_personal_vacation_details(pathname, refresh_trigger):
    if pathname != '/hr' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'HR Менеджер') # Fallback FIO
    
    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

@app.callback(
    Output('employee-personal-vacation-details-div', 'children'),
    Input('url', 'pathname')
)
def display_employee_personal_vacation_details(pathname):
    if pathname != '/employee' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'Співробітник') # Fallback FIO

    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

@app.callback(
    Output('manager-personal-vacation-details-div', 'children'),
    Input('url', 'pathname')
)
def display_manager_personal_vacation_details(pathname):
    if pathname != '/manager' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'Менеджер') # Fallback FIO
    
    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

# TODO: Add callbacks for employee-table and manager-table if they are meant to list
# all vacations for the current user.

if __name__ == '__main__':
    app.run(debug=True)
</file>
<file path="README.md">

</file>
<file path="requirements.txt">
dash
dash-bootstrap-components
flask
sqlite3

</file>
</file>
<file path="utils/date_utils.py">
from datetime import datetime

def calculate_days(start_date, end_date):
    d1 = datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.strptime(end_date, '%Y-%m-%d')
    return (d2 - d1).days + 1

</file>
<file path="utils/excel_handler.py">

</file>
<file path="app.py">
from dash import Dash, dcc, html, Input, Output, State
from flask import Flask, session, redirect, request
import dash
from dash.exceptions import PreventUpdate
from auth.auth_middleware import role_check_middleware
from components import employee_dashboard, manager_dashboard, hr_dashboard
from data import db_operations # Import db_operations
from utils import date_utils
import dash_bootstrap_components as dbc
import os # For secret key generation
from datetime import datetime

server = Flask(__name__)
# Use a secure secret key, e.g., from environment variable or generated
server.secret_key = os.urandom(24) # Generate a random secret key

app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server.wsgi_app = role_check_middleware(server.wsgi_app) # Middleware can remain, it's a pass-through

# Login page layout function
def login_page_layout():
    return dbc.Row(dbc.Col([
        html.H2("Авторизація Співробітника"),
        html.P("Будь ласка, введіть ваш ІПН для входу."),
        dcc.Input(id="login-ipn-input", type="text", placeholder="ІПН", className="mb-2", style={'width': '300px'}, n_submit=0),
        html.Br(),
        html.Button("Увійти", id="login-button", n_clicks=0, className="btn btn-primary"),
        html.Div(id="login-output-message", className="mt-2")
    ], width={'size': 6, 'offset': 3}, className="text-center mt-5"))

# Role to path/layout mapping
ROLE_DASHBOARDS = {
    'Employee': employee_dashboard.layout,
    'Manager': manager_dashboard.layout,
    'HR Manager': hr_dashboard.layout
}
ROLE_PATHS = {
    'Employee': '/employee',
    'Manager': '/manager',
    'HR Manager': '/hr'
}

# Main app layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='user-status-header'), # For user info and logout link
    html.Div(id='page-content')
], fluid=True)


# Callback to update header with user info and logout link
@app.callback(
    Output('user-status-header', 'children'),
    Input('url', 'pathname') # Trigger on URL change to update header
)
def update_user_header(pathname):
    if 'user_ipn' in session:
        user_fio = session.get('user_fio', session.get('user_ipn')) # Use FIO if available
        user_role = session.get('user_role', 'Невідома роль')
        
        header_content = [
            html.Span(f"Користувач: {user_fio} (Роль: {user_role})"),
            dcc.Link("Вийти", href="/logout", style={'marginLeft': '20px', 'color': 'red'})
        ]
        return html.Div(header_content, style={'padding': '10px', 'backgroundColor': '#f0f0f0', 'borderBottom': '1px solid #ccc', 'marginBottom': '15px'})
    return None # No header if not logged in


# Callback to handle login
@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('login-output-message', 'children')],
    [Input('login-button', 'n_clicks'),
     Input('login-ipn-input', 'n_submit')],
    [State('login-ipn-input', 'value')],
    prevent_initial_call=True
)
def process_login(n_clicks_login_btn, n_submit_ipn_field, ipn):
    if not ipn:
        return dash.no_update, dbc.Alert("Будь ласка, введіть ІПН.", color="warning")

    employee = db_operations.get_employee_by_ipn(ipn)

    if employee: # User found, IPN is effectively the password
        session['user_ipn'] = employee['ipn']
        session['user_role'] = employee['role']
        session['user_fio'] = employee.get('fio', employee['ipn']) # Store FIO if available

        redirect_path = ROLE_PATHS.get(employee['role'])
        if redirect_path:
            return redirect_path, dbc.Alert(f"Успішний вхід. Перенаправлення...", color="success", duration=2000)
        else:
            session.clear() 
            return dash.no_update, dbc.Alert("Помилка: Роль користувача не налаштована для перенаправлення.", color="danger")
    else: # User not found or IPN incorrect
        return dash.no_update, dbc.Alert("Помилка: Співробітника з таким ІПН не знайдено.", color="danger")


# Main callback to display pages and handle routing/auth
@app.callback(
    [Output('page-content', 'children'),
     Output('url', 'pathname', allow_duplicate=True)], # allow_duplicate because url.pathname is Input and Output
    [Input('url', 'pathname')],
    prevent_initial_call=True # Avoid initial call issues with redirects
)
def display_page_content(pathname):
    authenticated_ipn = session.get('user_ipn')
    authenticated_role = session.get('user_role')

    if pathname == '/logout':
        session.clear()
        return login_page_layout(), '/login'

    if authenticated_ipn: # User is logged in
        user_dashboard_path = ROLE_PATHS.get(authenticated_role)

        if pathname == '/login' or pathname == '/':
            return dash.no_update, user_dashboard_path if user_dashboard_path else '/'

        if pathname in ROLE_PATHS.values():
            if pathname == user_dashboard_path:
                return ROLE_DASHBOARDS[authenticated_role], dash.no_update
            else: # Trying to access a dashboard not matching their role
                return dash.no_update, user_dashboard_path
        
        # For any other path when logged in, redirect to their dashboard
        return dash.no_update, user_dashboard_path if user_dashboard_path else '/'

    else: # User is NOT logged in
        if pathname == '/login':
            return login_page_layout(), dash.no_update
        # For any other path (including dashboards or root), redirect to login
        return login_page_layout(), '/login'

# --- HR Dashboard Callbacks ---
@app.callback(
    Output('hr-employees-table', 'columns'),
    Output('hr-employees-table', 'data'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data') # Store component to trigger refresh
)
def update_hr_employees_table(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate

    columns = [
        {"name": "Ф.И.О.", "id": "fio"},
        {"name": "ИПН", "id": "ipn"},
        {"name": "Роль", "id": "role"},
        {"name": "Менеджер", "id": "manager_fio"},
        {"name": "С", "id": "current_vacation_start_date"},
        {"name": "До", "id": "current_vacation_end_date"},
        {"name": "Всего", "id": "current_vacation_total_days"},
        {"name": "Остаток", "id": "remaining_vacation_days"}
    ]
    # This function needs to be implemented in db_operations to fetch combined data
    employees_data = db_operations.get_employees_for_hr_table()
    return columns, employees_data

@app.callback(
    Output('hr-add-employee-manager-dropdown', 'options'),
    Input('url', 'pathname')
)
def update_manager_dropdown(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    managers = db_operations.get_managers() # [{'label': 'Manager FIO', 'value': 'Manager FIO'}]
    return managers

@app.callback(
    Output('hr-add-employee-notification', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-add-employee-submit-button', 'n_clicks'),
    State('hr-add-employee-fio-input', 'value'),
    State('hr-add-employee-ipn-input', 'value'),
    State('hr-add-employee-role-dropdown', 'value'),
    State('hr-add-employee-manager-dropdown', 'value'),
    State('hr-add-employee-vacation-days-input', 'value'),
    prevent_initial_call=True
)
def handle_add_employee(n_clicks, fio, ipn, role, manager_fio, vacation_days):
    if not n_clicks:
        raise PreventUpdate
    if not all([fio, ipn, role, vacation_days]): # Manager can be optional for top HR/Manager
        return dbc.Alert("Заполните все обязательные поля (Ф.И.О., ИПН, Роль, Отпуск в году).", color="warning"), dash.no_update
    
    try:
        vacation_days = int(vacation_days)
    except ValueError:
        return dbc.Alert("Количество дней отпуска должно быть числом.", color="danger"), dash.no_update

    employee_id = db_operations.add_employee(fio, ipn, manager_fio, role, vacation_days, vacation_days)
    if employee_id:
        return dbc.Alert(f"Сотрудник {fio} успешно добавлен.", color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert(f"Ошибка добавления сотрудника {fio}.", color="danger"), dash.no_update

@app.callback(
    Output('hr-add-vacation-employee-dropdown', 'options'),
    Input('url', 'pathname')
)
def update_vacation_employee_dropdown(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    employees = db_operations.get_all_employees() # Assumes this returns list of dicts with 'id' and 'fio'
    options = [{'label': emp['fio'], 'value': emp['id']} for emp in employees if 'id' in emp and 'fio' in emp]
    return options

@app.callback(
    Output('hr-add-vacation-total-days-output', 'children'),
    Input('hr-add-vacation-start-date', 'date'),
    Input('hr-add-vacation-end-date', 'date')
)
def calculate_vacation_total_days(start_date, end_date):
    if start_date and end_date:
        try:
            days = date_utils.calculate_days(start_date, end_date)
            return f"Всего дней: {days}" if days > 0 else "Дата окончания должна быть после даты начала."
        except ValueError:
            return "Неверный формат дат."
    return "Всего дней: -"

@app.callback(
    Output('hr-add-vacation-remaining-days-output', 'children'),
    Input('hr-add-vacation-employee-dropdown', 'value'),
    Input('hr-add-vacation-start-date', 'date'),
    Input('hr-add-vacation-end-date', 'date')
)
def calculate_vacation_remaining_days(employee_id, start_date, end_date):
    if not employee_id:
        return "Остаток дней: -"
    
    employee = db_operations.get_employee_by_id(employee_id) # Needs implementation
    if not employee or 'remaining_vacation_days' not in employee:
        return "Остаток дней: (не удалось загрузить)"

    remaining_now = employee['remaining_vacation_days']
    
    if start_date and end_date:
        try:
            days_in_this_vacation = date_utils.calculate_days(start_date, end_date)
            if days_in_this_vacation > 0:
                return f"Остаток дней (после этого отпуска): {remaining_now - days_in_this_vacation}"
        except ValueError:
            pass # Handled by total_days callback
    return f"Остаток дней (текущий): {remaining_now}"

@app.callback(
    Output('hr-add-vacation-notification', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-add-vacation-submit-button', 'n_clicks'),
    State('hr-add-vacation-employee-dropdown', 'value'),
    State('hr-add-vacation-start-date', 'date'),
    State('hr-add-vacation-end-date', 'date'),
    prevent_initial_call=True
)
def handle_add_vacation(n_clicks, employee_id, start_date, end_date):
    if not n_clicks:
        raise PreventUpdate
    if not all([employee_id, start_date, end_date]):
        return dbc.Alert("Выберите сотрудника и укажите даты отпуска.", color="warning"), dash.no_update

    try:
        total_days = date_utils.calculate_days(start_date, end_date)
        if total_days <= 0:
            return dbc.Alert("Некорректный период отпуска.", color="danger"), dash.no_update
    except ValueError:
        return dbc.Alert("Неверный формат дат.", color="danger"), dash.no_update

    success = db_operations.add_vacation(employee_id, start_date, end_date, total_days)
    if success:
        return dbc.Alert("Отпуск успешно добавлен.", color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert("Ошибка добавления отпуска. Проверьте остаток дней.", color="danger"), dash.no_update

@app.callback(
    Output('hr-vacation-history-table', 'columns'),
    Output('hr-vacation-history-table', 'data'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data')
)
def update_vacation_history_table(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate
    
    columns = [
        {"name": "Ф.И.О.", "id": "fio"},
        {"name": "Менеджер", "id": "manager_fio"},
        {"name": "Начало", "id": "start_date"},
        {"name": "Конец", "id": "end_date"},
        {"name": "Всего", "id": "total_days"}
    ]
    current_year = datetime.now().year
    history_data = db_operations.get_vacation_history(current_year)
    return columns, history_data

# --- HR Dashboard: Delete Employee Callback ---
@app.callback(
    [Output('hr-delete-employee-notification', 'children'),
     Output('hr-data-refresh-trigger', 'data', allow_duplicate=True)],
    [Input('hr-delete-employee-button', 'n_clicks')],
    [State('hr-employees-table', 'selected_row_ids')],
    prevent_initial_call=True
)
def handle_delete_employee(n_clicks, selected_row_ids):
    if not n_clicks or not selected_row_ids:
        raise PreventUpdate

    if len(selected_row_ids) != 1:
        return dbc.Alert("Пожалуйста, выберите одного сотрудника для удаления.", color="warning"), dash.no_update

    employee_id_to_delete_str = selected_row_ids[0]
    
    try:
        employee_id_to_delete = int(employee_id_to_delete_str)
    except ValueError:
        return dbc.Alert(f"Некорректный ID сотрудника: {employee_id_to_delete_str}.", color="danger"), dash.no_update

    success, message = db_operations.delete_employee(employee_id_to_delete)

    if success:
        alert_message = dbc.Alert(message, color="success", duration=4000)
        # Trigger data refresh for tables
        return alert_message, {'timestamp': datetime.now().timestamp()} 
    else:
        alert_message = dbc.Alert(message, color="danger")
        return alert_message, dash.no_update


# --- HR Dashboard: Edit Employee Data Callbacks ---

@app.callback(
    Output('hr-edit-employee-fio-dropdown', 'options'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data')
)
def update_edit_employee_fio_dropdown(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate
    employees = db_operations.get_all_employees()
    options = [{'label': emp['fio'], 'value': emp['id']} for emp in employees if 'id' in emp and 'fio' in emp]
    return options

@app.callback(
    Output('hr-edit-employee-role-dropdown', 'options'),
    Input('url', 'pathname') # Trigger once when HR page loads
)
def update_edit_employee_role_dropdown_options(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    return [
        {'label': 'Employee', 'value': 'Employee'},
        {'label': 'Manager', 'value': 'Manager'},
        {'label': 'HR Manager', 'value': 'HR Manager'}
    ]

@app.callback(
    Output('hr-edit-employee-manager-dropdown', 'options'),
    Input('url', 'pathname') # Trigger once when HR page loads
)
def update_edit_employee_manager_dropdown_options(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    managers = db_operations.get_managers()
    return managers

@app.callback(
    Output('hr-edit-employee-ipn-input', 'value'),
    Output('hr-edit-employee-role-dropdown', 'value'),
    Output('hr-edit-employee-manager-dropdown', 'value'),
    Output('hr-edit-employee-annual-vacation-days-input', 'value'),
    Output('hr-edit-employee-remaining-vacation-days-output', 'value'),
    Output('hr-edit-employee-vacation-start-date-picker', 'date'),
    Output('hr-edit-employee-vacation-end-date-picker', 'date'),
    Output('hr-edit-employee-selected-id-store', 'data'),
    Output('hr-edit-employee-target-vacation-id-store', 'data'),
    Input('hr-edit-employee-fio-dropdown', 'value'),
    Input('hr-data-refresh-trigger', 'data') # To refresh form after save
)
def populate_edit_employee_form(selected_employee_id, refresh_trigger):
    ctx = dash.callback_context
    triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If triggered by refresh_trigger, and we have a selected employee ID from dropdown, re-fetch.
    # Otherwise, only populate if fio_dropdown is the trigger.
    if triggered_input_id == 'hr-data-refresh-trigger' and not selected_employee_id:
        raise PreventUpdate # Don't clear form on general refresh if no employee selected
        
    if not selected_employee_id:
        return [None] * 7 + [None, None] # Clear all fields and stores

    employee_details = db_operations.get_employee_details_for_edit(selected_employee_id)
    if not employee_details:
        return [dash.no_update] * 7 + [selected_employee_id, None] # Keep selected ID, clear vacation ID

    vacation_start_date = employee_details['target_vacation']['start_date'] if employee_details.get('target_vacation') else None
    vacation_end_date = employee_details['target_vacation']['end_date'] if employee_details.get('target_vacation') else None
    target_vacation_id = employee_details['target_vacation']['id'] if employee_details.get('target_vacation') else None

    return (
        employee_details.get('ipn'),
        employee_details.get('role'),
        employee_details.get('manager_fio'),
        employee_details.get('vacation_days_per_year'),
        employee_details.get('remaining_vacation_days'),
        vacation_start_date,
        vacation_end_date,
        selected_employee_id, # Store the main employee ID
        target_vacation_id    # Store the ID of the vacation being shown/edited
    )

@app.callback(
    Output('hr-edit-employee-notification-div', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-edit-employee-save-button', 'n_clicks'),
    State('hr-edit-employee-selected-id-store', 'data'),
    State('hr-edit-employee-target-vacation-id-store', 'data'),
    State('hr-edit-employee-ipn-input', 'value'),
    State('hr-edit-employee-role-dropdown', 'value'),
    State('hr-edit-employee-manager-dropdown', 'value'),
    State('hr-edit-employee-annual-vacation-days-input', 'value'),
    State('hr-edit-employee-vacation-start-date-picker', 'date'),
    State('hr-edit-employee-vacation-end-date-picker', 'date'),
    prevent_initial_call=True
)
def handle_save_employee_data(n_clicks, employee_id, target_vacation_id, ipn, role, manager, annual_days, vac_start, vac_end):
    if not n_clicks or not employee_id:
        raise PreventUpdate

    # Fetch original FIO as it's not editable in this form anymore
    current_employee_data = db_operations.get_employee_by_id(employee_id)
    if not current_employee_data:
        return dbc.Alert("Ошибка: Сотрудник для редактирования не найден.", color="danger"), dash.no_update
    original_fio = current_employee_data['fio']

    # Basic validation (more can be added)
    if not all([ipn, role, annual_days is not None]):
        return dbc.Alert("ИПН, Роль и Отпуск в году обязательны.", color="warning"), dash.no_update

    try:
        annual_days_int = int(annual_days)
        if annual_days_int < 0:
            raise ValueError("Vacation days cannot be negative")
    except ValueError:
        return dbc.Alert("Количество дней отпуска должно быть положительным числом.", color="warning"), dash.no_update

    # Validate vacation dates if provided (both or none)
    if (vac_start or vac_end) and not (vac_start and vac_end):
        return dbc.Alert("Пожалуйста, укажите обе даты начала и окончания отпуска.", color="warning"), dash.no_update
    
    if vac_start and vac_end and vac_end < vac_start:
        return dbc.Alert("Дата окончания отпуска не может быть раньше даты начала.", color="warning"), dash.no_update

    updates = {
        'fio': original_fio, # Use fetched original FIO
        'ipn': ipn,
        'role': role,
        'manager_fio': manager, # Can be None
        'vacation_days_per_year': annual_days_int,
        'vacation_start_date': vac_start if vac_start else None,
        'vacation_end_date': vac_end if vac_end else None,
        'target_vacation_id': int(target_vacation_id) if target_vacation_id else None
    }

    success, message = db_operations.update_employee_data_and_vacation(employee_id, updates)

    if success:
        return dbc.Alert(message, color="success", duration=4000), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert(message, color="danger"), dash.no_update

# --- Personal Vacation Details Callbacks ---

def _create_personal_vacation_details_content(employee_data, user_fio_from_session):
    """Helper function to create content for personal vacation details block."""
    if not employee_data:
        return html.P(f"Не удалось загрузить данные для пользователя {user_fio_from_session}.")

    fio = employee_data.get('fio', user_fio_from_session) # Prefer FIO from DB if available
    start_date = employee_data.get('current_vacation_start_date', 'N/A')
    end_date = employee_data.get('current_vacation_end_date', 'N/A')
    total_days = employee_data.get('current_vacation_total_days', 'N/A')
    remaining_days = employee_data.get('remaining_vacation_days', 'N/A')

    return [
        html.H5(f"Личные данные отпуска: {fio}"),
        html.P(f"Ближайший/текущий отпуск с: {start_date}"),
        html.P(f"Ближайший/текущий отпуск до: {end_date}"),
        html.P(f"Всего дней в этом отпуске: {total_days}"),
        html.P(f"Остаётся дней отпуска в году: {remaining_days}")
    ]

@app.callback(
    Output('hr-selected-employee-details-div', 'children'), # Repurposed from original
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data') # Allow refresh if underlying data changes
)
def display_hr_personal_vacation_details(pathname, refresh_trigger):
    if pathname != '/hr' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'HR Менеджер') # Fallback FIO
    
    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

@app.callback(
    Output('employee-personal-vacation-details-div', 'children'),
    Input('url', 'pathname')
)
def display_employee_personal_vacation_details(pathname):
    if pathname != '/employee' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'Співробітник') # Fallback FIO

    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

@app.callback(
    Output('manager-personal-vacation-details-div', 'children'),
    Input('url', 'pathname')
)
def display_manager_personal_vacation_details(pathname):
    if pathname != '/manager' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'Менеджер') # Fallback FIO
    
    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

# --- Manager Dashboard: Subordinates Vacations Table Callback ---
@app.callback(
    [Output('subordinates-table', 'columns'),
     Output('subordinates-table', 'data')],
    [Input('url', 'pathname')]
)
def update_manager_subordinates_vacations_table(pathname):
    """
    Populates the subordinates' vacations table on the Manager dashboard.
    """
    # Define columns structure first, as per the plan
    columns = [
        {"name": "Ф.И.О.", "id": "sub_fio"},
        {"name": "ИПН", "id": "sub_ipn"},
        {"name": "Роль", "id": "sub_role"},
        {"name": "Начало", "id": "vac_start_date"},
        {"name": "Окончание", "id": "vac_end_date"},
        {"name": "Всего", "id": "vac_total_days"},
        {"name": "Осталось", "id": "sub_remaining_days"}
    ]

    if pathname != ROLE_PATHS.get('Manager') or session.get('user_role') != 'Manager':
        # Not on manager page or not a manager, prevent update or return empty table with headers
        # raise PreventUpdate # Option 1: Prevent update entirely
        return columns, []   # Option 2: Show empty table with headers, as per plan's implication

    manager_fio = session.get('user_fio')
    if not manager_fio:
        # Manager FIO not in session, return empty table with headers
        return columns, []

    subordinates_vacation_data = db_operations.get_subordinates_vacation_details(manager_fio)
    return columns, subordinates_vacation_data

# TODO: Add callbacks for employee-table and manager-table if they are meant to list
# all vacations for the current user.

if __name__ == '__main__':
    app.run(debug=True)
</file>
<file path="README.md">

</file>
<file path="requirements.txt">
dash
dash-bootstrap-components
flask
sqlite3

</file>
</file>
<file path="utils/date_utils.py">
from datetime import datetime

def calculate_days(start_date, end_date):
    d1 = datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.strptime(end_date, '%Y-%m-%d')
    return (d2 - d1).days + 1

</file>
<file path="utils/excel_handler.py">

</file>
<file path="app.py">
from dash import Dash, dcc, html, Input, Output, State
from flask import Flask, session, redirect, request
import dash
from dash.exceptions import PreventUpdate
from auth.auth_middleware import role_check_middleware
from components import employee_dashboard, manager_dashboard, hr_dashboard
from data import db_operations # Import db_operations
from utils import date_utils
import dash_bootstrap_components as dbc
import os # For secret key generation
from datetime import datetime

server = Flask(__name__)
# Use a secure secret key, e.g., from environment variable or generated
server.secret_key = os.urandom(24) # Generate a random secret key

app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server.wsgi_app = role_check_middleware(server.wsgi_app) # Middleware can remain, it's a pass-through

# Login page layout function
def login_page_layout():
    return dbc.Row(dbc.Col([
        html.H2("Авторизація Співробітника"),
        html.P("Будь ласка, введіть ваш ІПН для входу."),
        dcc.Input(id="login-ipn-input", type="text", placeholder="ІПН", className="mb-2", style={'width': '300px'}, n_submit=0),
        html.Br(),
        html.Button("Увійти", id="login-button", n_clicks=0, className="btn btn-primary"),
        html.Div(id="login-output-message", className="mt-2")
    ], width={'size': 6, 'offset': 3}, className="text-center mt-5"))

# Role to path/layout mapping
ROLE_DASHBOARDS = {
    'Employee': employee_dashboard.layout,
    'Manager': manager_dashboard.layout,
    'HR Manager': hr_dashboard.layout
}
ROLE_PATHS = {
    'Employee': '/employee',
    'Manager': '/manager',
    'HR Manager': '/hr'
}

# Main app layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='user-status-header'), # For user info and logout link
    html.Div(id='page-content')
], fluid=True)


# Callback to update header with user info and logout link
@app.callback(
    Output('user-status-header', 'children'),
    Input('url', 'pathname') # Trigger on URL change to update header
)
def update_user_header(pathname):
    if 'user_ipn' in session:
        user_fio = session.get('user_fio', session.get('user_ipn')) # Use FIO if available
        user_role = session.get('user_role', 'Невідома роль')
        
        header_content = [
            html.Span(f"Користувач: {user_fio} (Роль: {user_role})"),
            dcc.Link("Вийти", href="/logout", style={'marginLeft': '20px', 'color': 'red'})
        ]
        return html.Div(header_content, style={'padding': '10px', 'backgroundColor': '#f0f0f0', 'borderBottom': '1px solid #ccc', 'marginBottom': '15px'})
    return None # No header if not logged in


# Callback to handle login
@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('login-output-message', 'children')],
    [Input('login-button', 'n_clicks'),
     Input('login-ipn-input', 'n_submit')],
    [State('login-ipn-input', 'value')],
    prevent_initial_call=True
)
def process_login(n_clicks_login_btn, n_submit_ipn_field, ipn):
    if not ipn:
        return dash.no_update, dbc.Alert("Будь ласка, введіть ІПН.", color="warning")

    employee = db_operations.get_employee_by_ipn(ipn)

    if employee: # User found, IPN is effectively the password
        session['user_ipn'] = employee['ipn']
        session['user_role'] = employee['role']
        session['user_fio'] = employee.get('fio', employee['ipn']) # Store FIO if available

        redirect_path = ROLE_PATHS.get(employee['role'])
        if redirect_path:
            return redirect_path, dbc.Alert(f"Успішний вхід. Перенаправлення...", color="success", duration=2000)
        else:
            session.clear() 
            return dash.no_update, dbc.Alert("Помилка: Роль користувача не налаштована для перенаправлення.", color="danger")
    else: # User not found or IPN incorrect
        return dash.no_update, dbc.Alert("Помилка: Співробітника з таким ІПН не знайдено.", color="danger")


# Main callback to display pages and handle routing/auth
@app.callback(
    [Output('page-content', 'children'),
     Output('url', 'pathname', allow_duplicate=True)], # allow_duplicate because url.pathname is Input and Output
    [Input('url', 'pathname')],
    prevent_initial_call=True # Avoid initial call issues with redirects
)
def display_page_content(pathname):
    authenticated_ipn = session.get('user_ipn')
    authenticated_role = session.get('user_role')

    if pathname == '/logout':
        session.clear()
        return login_page_layout(), '/login'

    if authenticated_ipn: # User is logged in
        user_dashboard_path = ROLE_PATHS.get(authenticated_role)

        if pathname == '/login' or pathname == '/':
            return dash.no_update, user_dashboard_path if user_dashboard_path else '/'

        if pathname in ROLE_PATHS.values():
            if pathname == user_dashboard_path:
                return ROLE_DASHBOARDS[authenticated_role], dash.no_update
            else: # Trying to access a dashboard not matching their role
                return dash.no_update, user_dashboard_path
        
        # For any other path when logged in, redirect to their dashboard
        return dash.no_update, user_dashboard_path if user_dashboard_path else '/'

    else: # User is NOT logged in
        if pathname == '/login':
            return login_page_layout(), dash.no_update
        # For any other path (including dashboards or root), redirect to login
        return login_page_layout(), '/login'

# --- HR Dashboard Callbacks ---
@app.callback(
    Output('hr-employees-table', 'columns'),
    Output('hr-employees-table', 'data'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data') # Store component to trigger refresh
)
def update_hr_employees_table(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate

    columns = [
        {"name": "Ф.И.О.", "id": "fio"},
        {"name": "ИПН", "id": "ipn"},
        {"name": "Роль", "id": "role"},
        {"name": "Менеджер", "id": "manager_fio"},
        {"name": "С", "id": "current_vacation_start_date"},
        {"name": "До", "id": "current_vacation_end_date"},
        {"name": "Всего", "id": "current_vacation_total_days"},
        {"name": "Остаток", "id": "remaining_vacation_days"}
    ]
    # This function needs to be implemented in db_operations to fetch combined data
    employees_data = db_operations.get_employees_for_hr_table()
    return columns, employees_data

@app.callback(
    Output('hr-add-employee-manager-dropdown', 'options'),
    Input('url', 'pathname')
)
def update_manager_dropdown(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    managers = db_operations.get_managers() # [{'label': 'Manager FIO', 'value': 'Manager FIO'}]
    return managers

@app.callback(
    Output('hr-add-employee-notification', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-add-employee-submit-button', 'n_clicks'),
    State('hr-add-employee-fio-input', 'value'),
    State('hr-add-employee-ipn-input', 'value'),
    State('hr-add-employee-role-dropdown', 'value'),
    State('hr-add-employee-manager-dropdown', 'value'),
    State('hr-add-employee-vacation-days-input', 'value'),
    prevent_initial_call=True
)
def handle_add_employee(n_clicks, fio, ipn, role, manager_fio, vacation_days):
    if not n_clicks:
        raise PreventUpdate
    if not all([fio, ipn, role, vacation_days]): # Manager can be optional for top HR/Manager
        return dbc.Alert("Заполните все обязательные поля (Ф.И.О., ИПН, Роль, Отпуск в году).", color="warning"), dash.no_update
    
    try:
        vacation_days = int(vacation_days)
    except ValueError:
        return dbc.Alert("Количество дней отпуска должно быть числом.", color="danger"), dash.no_update

    employee_id = db_operations.add_employee(fio, ipn, manager_fio, role, vacation_days, vacation_days)
    if employee_id:
        return dbc.Alert(f"Сотрудник {fio} успешно добавлен.", color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert(f"Ошибка добавления сотрудника {fio}.", color="danger"), dash.no_update

@app.callback(
    Output('hr-add-vacation-employee-dropdown', 'options'),
    Input('url', 'pathname')
)
def update_vacation_employee_dropdown(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    employees = db_operations.get_all_employees() # Assumes this returns list of dicts with 'id' and 'fio'
    options = [{'label': emp['fio'], 'value': emp['id']} for emp in employees if 'id' in emp and 'fio' in emp]
    return options

@app.callback(
    Output('hr-add-vacation-total-days-output', 'children'),
    Input('hr-add-vacation-start-date', 'date'),
    Input('hr-add-vacation-end-date', 'date')
)
def calculate_vacation_total_days(start_date, end_date):
    if start_date and end_date:
        try:
            days = date_utils.calculate_days(start_date, end_date)
            return f"Всего дней: {days}" if days > 0 else "Дата окончания должна быть после даты начала."
        except ValueError:
            return "Неверный формат дат."
    return "Всего дней: -"

@app.callback(
    Output('hr-add-vacation-remaining-days-output', 'children'),
    Input('hr-add-vacation-employee-dropdown', 'value'),
    Input('hr-add-vacation-start-date', 'date'),
    Input('hr-add-vacation-end-date', 'date')
)
def calculate_vacation_remaining_days(employee_id, start_date, end_date):
    if not employee_id:
        return "Остаток дней: -"
    
    employee = db_operations.get_employee_by_id(employee_id) # Needs implementation
    if not employee or 'remaining_vacation_days' not in employee:
        return "Остаток дней: (не удалось загрузить)"

    remaining_now = employee['remaining_vacation_days']
    
    if start_date and end_date:
        try:
            days_in_this_vacation = date_utils.calculate_days(start_date, end_date)
            if days_in_this_vacation > 0:
                return f"Остаток дней (после этого отпуска): {remaining_now - days_in_this_vacation}"
        except ValueError:
            pass # Handled by total_days callback
    return f"Остаток дней (текущий): {remaining_now}"

@app.callback(
    Output('hr-add-vacation-notification', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-add-vacation-submit-button', 'n_clicks'),
    State('hr-add-vacation-employee-dropdown', 'value'),
    State('hr-add-vacation-start-date', 'date'),
    State('hr-add-vacation-end-date', 'date'),
    prevent_initial_call=True
)
def handle_add_vacation(n_clicks, employee_id, start_date, end_date):
    if not n_clicks:
        raise PreventUpdate
    if not all([employee_id, start_date, end_date]):
        return dbc.Alert("Выберите сотрудника и укажите даты отпуска.", color="warning"), dash.no_update

    try:
        total_days = date_utils.calculate_days(start_date, end_date)
        if total_days <= 0:
            return dbc.Alert("Некорректный период отпуска.", color="danger"), dash.no_update
    except ValueError:
        return dbc.Alert("Неверный формат дат.", color="danger"), dash.no_update

    success = db_operations.add_vacation(employee_id, start_date, end_date, total_days)
    if success:
        return dbc.Alert("Отпуск успешно добавлен.", color="success"), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert("Ошибка добавления отпуска. Проверьте остаток дней.", color="danger"), dash.no_update

@app.callback(
    Output('hr-vacation-history-table', 'columns'),
    Output('hr-vacation-history-table', 'data'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data')
)
def update_vacation_history_table(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate
    
    columns = [
        {"name": "Ф.И.О.", "id": "fio"},
        {"name": "Менеджер", "id": "manager_fio"},
        {"name": "Начало", "id": "start_date"},
        {"name": "Конец", "id": "end_date"},
        {"name": "Всего", "id": "total_days"}
    ]
    current_year = datetime.now().year
    history_data = db_operations.get_vacation_history(current_year)
    return columns, history_data

# --- HR Dashboard: Delete Employee Callback ---
@app.callback(
    [Output('hr-delete-employee-notification', 'children'),
     Output('hr-data-refresh-trigger', 'data', allow_duplicate=True)],
    [Input('hr-delete-employee-button', 'n_clicks')],
    [State('hr-employees-table', 'selected_row_ids')],
    prevent_initial_call=True
)
def handle_delete_employee(n_clicks, selected_row_ids):
    if not n_clicks or not selected_row_ids:
        raise PreventUpdate

    if len(selected_row_ids) != 1:
        return dbc.Alert("Пожалуйста, выберите одного сотрудника для удаления.", color="warning"), dash.no_update

    employee_id_to_delete_str = selected_row_ids[0]
    
    try:
        employee_id_to_delete = int(employee_id_to_delete_str)
    except ValueError:
        return dbc.Alert(f"Некорректный ID сотрудника: {employee_id_to_delete_str}.", color="danger"), dash.no_update

    success, message = db_operations.delete_employee(employee_id_to_delete)

    if success:
        alert_message = dbc.Alert(message, color="success", duration=4000)
        # Trigger data refresh for tables
        return alert_message, {'timestamp': datetime.now().timestamp()} 
    else:
        alert_message = dbc.Alert(message, color="danger")
        return alert_message, dash.no_update


# --- HR Dashboard: Edit Employee Data Callbacks ---

@app.callback(
    Output('hr-edit-employee-fio-dropdown', 'options'),
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data')
)
def update_edit_employee_fio_dropdown(pathname, refresh_trigger):
    if pathname != '/hr':
        raise PreventUpdate
    employees = db_operations.get_all_employees()
    options = [{'label': emp['fio'], 'value': emp['id']} for emp in employees if 'id' in emp and 'fio' in emp]
    return options

@app.callback(
    Output('hr-edit-employee-role-dropdown', 'options'),
    Input('url', 'pathname') # Trigger once when HR page loads
)
def update_edit_employee_role_dropdown_options(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    return [
        {'label': 'Employee', 'value': 'Employee'},
        {'label': 'Manager', 'value': 'Manager'},
        {'label': 'HR Manager', 'value': 'HR Manager'}
    ]

@app.callback(
    Output('hr-edit-employee-manager-dropdown', 'options'),
    Input('url', 'pathname') # Trigger once when HR page loads
)
def update_edit_employee_manager_dropdown_options(pathname):
    if pathname != '/hr':
        raise PreventUpdate
    managers = db_operations.get_managers()
    return managers

@app.callback(
    Output('hr-edit-employee-ipn-input', 'value'),
    Output('hr-edit-employee-role-dropdown', 'value'),
    Output('hr-edit-employee-manager-dropdown', 'value'),
    Output('hr-edit-employee-annual-vacation-days-input', 'value'),
    Output('hr-edit-employee-remaining-vacation-days-output', 'value'),
    Output('hr-edit-employee-vacation-start-date-picker', 'date'),
    Output('hr-edit-employee-vacation-end-date-picker', 'date'),
    Output('hr-edit-employee-selected-id-store', 'data'),
    Output('hr-edit-employee-target-vacation-id-store', 'data'),
    Input('hr-edit-employee-fio-dropdown', 'value'),
    Input('hr-data-refresh-trigger', 'data') # To refresh form after save
)
def populate_edit_employee_form(selected_employee_id, refresh_trigger):
    ctx = dash.callback_context
    triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If triggered by refresh_trigger, and we have a selected employee ID from dropdown, re-fetch.
    # Otherwise, only populate if fio_dropdown is the trigger.
    if triggered_input_id == 'hr-data-refresh-trigger' and not selected_employee_id:
        raise PreventUpdate # Don't clear form on general refresh if no employee selected
        
    if not selected_employee_id:
        return [None] * 7 + [None, None] # Clear all fields and stores

    employee_details = db_operations.get_employee_details_for_edit(selected_employee_id)
    if not employee_details:
        return [dash.no_update] * 7 + [selected_employee_id, None] # Keep selected ID, clear vacation ID

    vacation_start_date = employee_details['target_vacation']['start_date'] if employee_details.get('target_vacation') else None
    vacation_end_date = employee_details['target_vacation']['end_date'] if employee_details.get('target_vacation') else None
    target_vacation_id = employee_details['target_vacation']['id'] if employee_details.get('target_vacation') else None

    return (
        employee_details.get('ipn'),
        employee_details.get('role'),
        employee_details.get('manager_fio'),
        employee_details.get('vacation_days_per_year'),
        employee_details.get('remaining_vacation_days'),
        vacation_start_date,
        vacation_end_date,
        selected_employee_id, # Store the main employee ID
        target_vacation_id    # Store the ID of the vacation being shown/edited
    )

@app.callback(
    Output('hr-edit-employee-notification-div', 'children'),
    Output('hr-data-refresh-trigger', 'data', allow_duplicate=True),
    Input('hr-edit-employee-save-button', 'n_clicks'),
    State('hr-edit-employee-selected-id-store', 'data'),
    State('hr-edit-employee-target-vacation-id-store', 'data'),
    State('hr-edit-employee-ipn-input', 'value'),
    State('hr-edit-employee-role-dropdown', 'value'),
    State('hr-edit-employee-manager-dropdown', 'value'),
    State('hr-edit-employee-annual-vacation-days-input', 'value'),
    State('hr-edit-employee-vacation-start-date-picker', 'date'),
    State('hr-edit-employee-vacation-end-date-picker', 'date'),
    prevent_initial_call=True
)
def handle_save_employee_data(n_clicks, employee_id, target_vacation_id, ipn, role, manager, annual_days, vac_start, vac_end):
    if not n_clicks or not employee_id:
        raise PreventUpdate

    # Fetch original FIO as it's not editable in this form anymore
    current_employee_data = db_operations.get_employee_by_id(employee_id)
    if not current_employee_data:
        return dbc.Alert("Ошибка: Сотрудник для редактирования не найден.", color="danger"), dash.no_update
    original_fio = current_employee_data['fio']

    # Basic validation (more can be added)
    if not all([ipn, role, annual_days is not None]):
        return dbc.Alert("ИПН, Роль и Отпуск в году обязательны.", color="warning"), dash.no_update

    try:
        annual_days_int = int(annual_days)
        if annual_days_int < 0:
            raise ValueError("Vacation days cannot be negative")
    except ValueError:
        return dbc.Alert("Количество дней отпуска должно быть положительным числом.", color="warning"), dash.no_update

    # Validate vacation dates if provided (both or none)
    if (vac_start or vac_end) and not (vac_start and vac_end):
        return dbc.Alert("Пожалуйста, укажите обе даты начала и окончания отпуска.", color="warning"), dash.no_update
    
    if vac_start and vac_end and vac_end < vac_start:
        return dbc.Alert("Дата окончания отпуска не может быть раньше даты начала.", color="warning"), dash.no_update

    updates = {
        'fio': original_fio, # Use fetched original FIO
        'ipn': ipn,
        'role': role,
        'manager_fio': manager, # Can be None
        'vacation_days_per_year': annual_days_int,
        'vacation_start_date': vac_start if vac_start else None,
        'vacation_end_date': vac_end if vac_end else None,
        'target_vacation_id': int(target_vacation_id) if target_vacation_id else None
    }

    success, message = db_operations.update_employee_data_and_vacation(employee_id, updates)

    if success:
        return dbc.Alert(message, color="success", duration=4000), {'timestamp': datetime.now().timestamp()}
    else:
        return dbc.Alert(message, color="danger"), dash.no_update

# --- Personal Vacation Details Callbacks ---

def _create_personal_vacation_details_content(employee_data, user_fio_from_session):
    """Helper function to create content for personal vacation details block."""
    if not employee_data:
        return html.P(f"Не удалось загрузить данные для пользователя {user_fio_from_session}.")

    fio = employee_data.get('fio', user_fio_from_session) # Prefer FIO from DB if available
    start_date = employee_data.get('current_vacation_start_date', 'N/A')
    end_date = employee_data.get('current_vacation_end_date', 'N/A')
    total_days = employee_data.get('current_vacation_total_days', 'N/A')
    remaining_days = employee_data.get('remaining_vacation_days', 'N/A')

    return [
        html.H5(f"Личные данные отпуска: {fio}"),
        html.P(f"Ближайший/текущий отпуск с: {start_date}"),
        html.P(f"Ближайший/текущий отпуск до: {end_date}"),
        html.P(f"Всего дней в этом отпуске: {total_days}"),
        html.P(f"Остаётся дней отпуска в году: {remaining_days}")
    ]

@app.callback(
    Output('hr-selected-employee-details-div', 'children'), # Repurposed from original
    Input('url', 'pathname'),
    Input('hr-data-refresh-trigger', 'data') # Allow refresh if underlying data changes
)
def display_hr_personal_vacation_details(pathname, refresh_trigger):
    if pathname != '/hr' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'HR Менеджер') # Fallback FIO
    
    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

@app.callback(
    Output('employee-personal-vacation-details-div', 'children'),
    Input('url', 'pathname')
)
def display_employee_personal_vacation_details(pathname):
    if pathname != '/employee' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'Співробітник') # Fallback FIO

    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

@app.callback(
    Output('manager-personal-vacation-details-div', 'children'),
    Input('url', 'pathname')
)
def display_manager_personal_vacation_details(pathname):
    if pathname != '/manager' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    user_fio = session.get('user_fio', 'Менеджер') # Fallback FIO
    
    employee_data = db_operations.get_employee_vacation_summary_by_ipn(user_ipn)
    return _create_personal_vacation_details_content(employee_data, user_fio)

# --- Manager Dashboard: Subordinates Vacations Table Callback ---
@app.callback(
    [Output('subordinates-table', 'columns'),
     Output('subordinates-table', 'data')],
    [Input('url', 'pathname')]
)
def update_manager_subordinates_vacations_table(pathname):
    """
    Populates the subordinates' vacations table on the Manager dashboard.
    """
    # Define columns structure first, as per the plan
    columns = [
        {"name": "Ф.И.О.", "id": "sub_fio"},
        {"name": "ИПН", "id": "sub_ipn"},
        {"name": "Роль", "id": "sub_role"},
        {"name": "Начало", "id": "vac_start_date"},
        {"name": "Окончание", "id": "vac_end_date"},
        {"name": "Всего", "id": "vac_total_days"},
        {"name": "Осталось", "id": "sub_remaining_days"}
    ]

    if pathname != ROLE_PATHS.get('Manager') or session.get('user_role') != 'Manager':
        # Not on manager page or not a manager, prevent update or return empty table with headers
        # raise PreventUpdate # Option 1: Prevent update entirely
        return columns, []   # Option 2: Show empty table with headers, as per plan's implication

    manager_fio = session.get('user_fio')
    if not manager_fio:
        # Manager FIO not in session, return empty table with headers
        return columns, []

    subordinates_vacation_data = db_operations.get_subordinates_vacation_details(manager_fio)
    return columns, subordinates_vacation_data

# TODO: Add callbacks for employee-table and manager-table if they are meant to list
# all vacations for the current user.

if __name__ == '__main__':
    app.run(debug=True)
</file>
<file path="README.md">

</file>
<file path="requirements.txt">
dash
dash-bootstrap-components
flask
sqlite3

</file>
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
server.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24)) # Використовуйте змінну середовища або згенерований ключ як запасний варіант

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
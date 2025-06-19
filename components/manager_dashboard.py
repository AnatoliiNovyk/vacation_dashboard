from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Manager Dashboard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
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
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6),
    ]),
    dash_table.DataTable(id='manager-table', columns=[], data=[], page_size=10) # For manager's own vacation list
])

# --- Manager Dashboard: Own Vacation History Callback ---
@app.callback(
    Output('manager-table', 'columns'),
    Output('manager-table', 'data'),
    Input('url', 'pathname')
)
def update_manager_own_vacation_history(pathname):
    if pathname != '/manager' or 'user_ipn' not in session:
        raise PreventUpdate

    user_ipn = session.get('user_ipn')
    manager = db_operations.get_employee_by_ipn(user_ipn)
    if not manager:
        return [], []
    
    manager_id = manager['id']
    history_data = db_operations.get_vacation_history_for_employee(manager_id)

    columns = [
        {"name": "Мои отпуска: Начало", "id": "start_date"},
        {"name": "Конец", "id": "end_date"},
        {"name": "Всего дней", "id": "total_days"},
    ]
    return columns, history_data

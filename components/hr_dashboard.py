from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    # --- Скрытые компоненты для хранения данных ---
    dcc.Store(id='hr-data-refresh-trigger'), 
    dcc.Store(id='hr-edit-employee-selected-id-store'),
    dcc.Store(id='hr-edit-employee-target-vacation-id-store'),

    html.H2('HR Manager Dashboard'),
    html.Br(),

    # --- Основная таблица сотрудников ---
    dbc.Card([
        dbc.CardHeader(html.H4("СОТРУДНИКИ")),
        dbc.CardBody([
            dash_table.DataTable(
                id='all-employees-table',
                columns=[],
                data=[],
                row_selectable='single',
                page_size=10,
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            dbc.Button("УДАЛИТЬ", id='hr-delete-employee-button', color="danger", className="mt-2 me-2"),
            html.Div(id='hr-delete-employee-notification', className="mt-2")
        ])
    ], className="mb-3"),

    # --- Блоки управления (Добавить, Изменить, Добавить отпуск) ---
    dbc.Row([
        dbc.Col(md=4, children=[
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
                    dcc.Dropdown(id='hr-add-employee-manager-dropdown', options=[], placeholder='Менеджер', className="mb-2"),
                    dbc.Input(id='hr-add-employee-vacation-days-input', type='number', placeholder='Отпуск в текущем году (дней)', className="mb-2"),
                    dbc.Button("ДОБАВИТЬ", id='hr-add-employee-submit-button', color="primary", className="me-2"),
                    html.Div(id='hr-add-employee-notification', className="mt-2")
                ])
            ], className="mb-3"),
        ]),
        dbc.Col(md=4, children=[
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
            dbc.Card([
                dbc.CardHeader(html.H4("ДОБАВИТЬ ОТПУСК")),
                dbc.CardBody([
                    dcc.Dropdown(id='hr-add-vacation-employee-dropdown', options=[], placeholder='Ф.И.О. сотрудника', className="mb-2"),
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

    # --- Нижний ряд с историей, личными данными и импортом ---
    dbc.Row([
        # --- Левая колонка: История отпусков ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("ИСТОРИЯ ОТПУСКОВ (текущий год)")),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='hr-vacation-history-table',
                        columns=[],
                        data=[],
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ])
            ], className="mb-3"),
        ], md=6),
        # --- Правая колонка: Личные данные и Импорт ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
                dbc.CardBody(id='hr-selected-employee-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),

            # --- ПЕРЕМЕЩЕННЫЙ БЛОК ИМПОРТА ---
            dbc.Card([
                dbc.CardHeader(html.H4("Импорт сотрудников из BAS/BAF")),
                dbc.CardBody([
                    dcc.Upload(
                        id='upload-employee-data',
                        children=html.Div(['Перетащите или ', html.A('Выберите файл (CSV или Excel)')]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                            'textAlign': 'center', 'margin': '10px'
                        },
                        multiple=False
                    ),
                    html.Div(id='output-data-upload-status'),
                ])
            ], className="mb-3"),
        ], md=6)
    ]),
])

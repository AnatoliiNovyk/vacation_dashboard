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
])

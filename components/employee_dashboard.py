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
        ], md=6),
        dbc.Col(md=6) 
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("Моя история отпусков")),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='employee-vacation-history-table',
                        columns=[],
                        data=[],
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    )
                ])
            ])
        ], width=12)
    ])
])

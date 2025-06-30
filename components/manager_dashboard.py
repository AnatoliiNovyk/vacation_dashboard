from dash import html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('Manager Dashboard'),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("ВІДПУСТКИ ПІДЛЕГЛИХ  СПІВРОБІТНИКІВ")),
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
                dbc.CardHeader(html.H4("Мої особисті дані  про відпустку")),
                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
                    html.P("Загрузка данных...")
                ])
            ], className="mb-3"),
        ], md=6),
    ]),
    dash_table.DataTable(id='manager-table', columns=[], data=[], page_size=10) # For manager's own vacation list
])

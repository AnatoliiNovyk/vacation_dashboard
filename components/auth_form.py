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
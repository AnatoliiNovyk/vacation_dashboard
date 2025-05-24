diff --git a/components/manager_dashboard.py b/components/manager_dashboard.py
index f9b8e2a..a8c3d7e 100644
--- a/components/manager_dashboard.py
+++ b/components/manager_dashboard.py
@@ -4,32 +4,35 @@
 layout = html.Div([
     html.H2('Manager Dashboard'),
     html.Br(),
-    dbc.Card([
-        dbc.CardHeader(html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")),
-        dbc.CardBody([
-            dash_table.DataTable(
-                id='subordinates-table',
-                columns=[], # Populated by callback
-                data=[],    # Populated by callback
-                page_size=10,
-                style_cell={'textAlign': 'left'},
-                style_header={
-                    'backgroundColor': 'rgb(230, 230, 230)',
-                    'fontWeight': 'bold'
-                }
-            )
-        ])
-    ], className="mb-3"),
     dbc.Row([
         dbc.Col([
             dbc.Card([
-                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
-                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
-                    html.P("Загрузка данных...")
+                dbc.CardHeader(html.H4("ОТПУСКА ПОДЧИНЕННЫХ СОТРУДНИКОВ")),
+                dbc.CardBody([
+                    dash_table.DataTable(
+                        id='subordinates-table',
+                        columns=[], # Populated by callback
+                        data=[],    # Populated by callback
+                        page_size=10,
+                        style_cell={'textAlign': 'left'},
+                        style_header={
+                            'backgroundColor': 'rgb(230, 230, 230)',
+                            'fontWeight': 'bold'
+                        }
+                    )
                 ])
             ], className="mb-3"),
-        ], md=6), # Adjust width as needed
-        dbc.Col(md=6) # Placeholder for other content or to balance layout
+        ], md=6),
+        dbc.Col([
+            dbc.Card([
+                dbc.CardHeader(html.H4("Мои личные данные отпуска")),
+                dbc.CardBody(id='manager-personal-vacation-details-div', children=[
+                    html.P("Загрузка данных...")
+                ])
+            ], className="mb-3"),
+        ], md=6),
     ]),
-    html.H3('История моих отпусков'),
     dash_table.DataTable(id='manager-table', columns=[], data=[], page_size=10) # For manager's own vacation list
 ])
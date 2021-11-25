import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import dcc
from dash import html


app = dash.Dash(
    external_stylesheets=[dbc.themes.SLATE],
    suppress_callback_exceptions=True
)
server = app.server

TEMPLATE_PATH = "templates/historical_gen_data.xlsx"
TEMPLATE_HIDDEN_PASS = "DuPa"
COLORS = {
    'background': '#e6ffe6',
    'text': '#ffffff'
}

"""Homepage"""
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

index_page = html.Div(
    [
        html.H1(children="Predictor of renewable energy sources", style={'textAlign': 'center'}),
        dbc.Tabs(
            [
                dbc.Tab(label="General info", tab_id="tab-1"),
                dbc.Tab(label="Historical data", tab_id="tab-2"),
                dbc.Tab(label="Location", tab_id="tab-3"),

                dbc.Button("Submit", color="success", disabled=True, className="d-grid gap-2 col-6 mx-auto",
                           style={'margin': '10px'}),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ],
)

# General info form
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                html.H5(
                    children="Fill the form",
                    style={'textAlign': 'center'},
                ),
            ]),
            html.Hr(),

            dbc.Form([
                dbc.Row(
                    [
                        dbc.Label("Email", html_for="example-email-row", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="email", id="example-email-row", placeholder="Enter email"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Row(
                    [
                        dbc.Label("Password", html_for="example-password-row", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="example-password-row",
                                placeholder="Enter password",
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Row(
                    [
                        dbc.Label("Radios", html_for="example-radios-row", width=2),
                        dbc.Col(
                            dbc.RadioItems(
                                id="example-radios-row",
                                options=[
                                    {"label": "First radio", "value": 1},
                                    {"label": "Second radio", "value": 2},
                                    {
                                        "label": "Third disabled radio",
                                        "value": 3,
                                        "disabled": True,
                                    }]), width=10,
                                ),
                            ], className="mb-3",
                        ),
                    ],
                ),
            ],
        ),
)



# Download template and upload historical generated data
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                html.H5(
                    children="Download the excel template and fill it with historical power gen data",
                    style={'textAlign': 'center'},
                ),
            ]),
            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dbc.Button(
                            children="Download", id='download_button',
                            style={
                                'width': '60%',
                                'height': '60px',
                                'borderWidth': '1px',
                                'margin': '5px',
                                'margin-left': '15%',
                                'lineHeight': '30px',
                                'textAlign': 'center',
                                'fontWeight': 'bold'
                            },),
                        dcc.Download(id="Download-template-xlsx"),
                    ]),
                ),
                dbc.Col(
                    html.Div([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '60%',
                                'height': '60px',
                                'lineHeight': '55px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'margin-right': '15%',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '5px',
                                'fontWeight': 'bold'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),
                    ]),
                ),
            ]),
        ],
    ),
    className="mt-3",
)


tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                html.H5(
                    children="Set Marker pointing on localization of your installation",
                    style={'textAlign': 'center'},
                ),
            ]),

            html.Hr(),
            dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")],
                   id="map",
                   style={'width': '1200px', 'height': '800px', 'margin': "auto", "display": "block"}),

        ]
    ),
    className="mt-3",
)


# --- Callbacks ---"

@app.callback(dash.dependencies.Output("content", "children"), [dash.dependencies.Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    elif at == "tab-3":
        return tab3_content
    return html.P("This shouldn't ever be displayed...")


# Callbacks for tab 2
@app.callback(dash.dependencies.Output('Download-template-xlsx', 'data'),
              dash.dependencies.Input('download_button', 'n_clicks'),
              prevent_initial_call=True,
              )
def template_downloader(n_clicks):
    return dash.dcc.express.send_file(TEMPLATE_PATH)


# Callbacks for tab 3
@app.callback(dash.dependencies.Output("layer", "children"), [dash.dependencies.Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
    return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]


# Move between layouts
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_page


if __name__ == "__main__":
    app.run_server(debug=True)

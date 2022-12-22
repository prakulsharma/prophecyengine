import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.Div('Dash To-Do list'),
    dcc.Input(id="new-item"),
    html.Button("Add", id="add"),
    html.Button("Clear Done", id="clear-done"),
    html.Div(id='msgs')
    #     dbc.FormGroup(
    #         dbc.Card([
    #                 # 5.1 Message board text
    #                 dbc.Label(
    #                     'Message Board',
    #                     style={
    #                         'text-align': 'center',
    #                         'font-weight': 'Bold'
    #                     }
    #                 ),
    #
    #                 # 5.2 Output messages
    #                 dbc.CardBody([
    #                         dbc.Label(id='msg1', style={"font-family": "Consolas"}), html.Br(),
    #                     ], style={"height": "130px", "overflow": "scroll"})
    #             ])
    #     ), dbc.Label(id='totals')
    #
])


@app.callback(
    [
        Output('msgs', 'children')
    ],
    [
        Input('add', 'n_clicks')
    ]
)
def throw_msg(n):
    if n is not None:
        children = ["Throwing this message"]
        return children
    raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, port=1118, threaded=True)

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Importing User defined apps
from apps import viz_app, data_cleaning_app, score_app, train_app, whatif_app
from app_def import app


# location where the file will be saved
data_folder = "../data/raw-data"

'''


Contains
1. Headline
    i) Symphony Logo
    ii)Name of Web-app i.e. Digital Twin Studio
2. Tabs Group
    i) Data Pre-processing
    ii) Data Visualization
    iii) Model Build 
    iv) Model Scoring
    v) What-if Analysis
3. Bottom
    i) Copyright
    

'''

# 1. Headline Group
Headline = dbc.Container(
    dbc.Row(
        [
            # 1. i) Symphony AzimaAi Logo
            dbc.Col(
                html.Img(
                    src="https://www.ritec-eg.com/Products/img/Azima.png",
                    className="col",
                    style={
                        "display": "block",
                        "width": "4%", "padding-left": "0px"
                    }), md=4
            ),
            # 1. ii) Name of Web-app (alias Digital Twin Studio)
            dbc.Col(
                html.H4(
                    "Digital Twin Studio",
                    className="text-center",
                    style={"text-align": 'center',
                           "font-family": 'Open Sans',
                           "font-weight": "bold",
                           "font-size": "35px",
                           "vertical-align": "middle",
                           "padding-top": "25px"}
                ), md=4
            ),
        ]
    ), fluid=True,
)

# 2. Tabs Group
card = dbc.Card(
    [
        dbc.CardHeader(

            # Creating tabs for various functionalities
            dbc.Tabs(
                [
                    # 2. i) Data Pre-processing
                    dbc.Tab(label="Data Pre-Processing", tab_id="tab-2"),

                    # 2 ii) Data Visualization
                    dbc.Tab(label="Data Visualization", tab_id="tab-3"),

                    # 2. iii) Model Build
                    dbc.Tab(label=" Model Build ", tab_id="tab-4"),

                    # 2. iv) Model Scoring
                    dbc.Tab(label="Model Scoring", tab_id="tab-5"),

                    # 2. v) What-if Analysis
                    dbc.Tab(label="What-if Analysis", tab_id="tab-6"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-2",
                persistence=True,
                persistence_type='session'
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

# 3. Bottom Group
bottom = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                # 3.i) Copyright text
                html.Div(
                    children="Powered by Symphony AzimaAI © 2020",
                    className="col",
                    style={"width": "50%"}
                ),
            ),
            dbc.Col(" ")
        ]
    ), fluid=True
)

app.layout = dbc.Container(
    [
        Headline,
        card,
        bottom
    ], fluid=True
)


# 2. Callback for tabs
@app.callback(
    Output("card-content", "children"),
    [Input("card-tabs", "active_tab")]
)
def tab_content(tab):
    if tab == "tab-2":
        return data_cleaning_app.layout
    if tab == "tab-3":
        return viz_app.layout
    if tab == "tab-4":
        return train_app.layout
    if tab == "tab-5":
        return score_app.layout
    if tab == "tab-6":
        return whatif_app.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=1119, threaded=True)

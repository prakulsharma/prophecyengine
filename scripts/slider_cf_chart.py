import os
import pandas as pd
from analysis import read_time_series_csv

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_html_components as html
from model_widgets import score_workbench, cf_barchart, train_workbench
from dash.exceptions import PreventUpdate
import time



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

button_train = html.Div(
    [
        dbc.Button("runTrain", color="primary", className="mr-1", id='train-button')
    ]
)

button_score = html.Div(
    [
        dbc.Button("runScore", color="primary", className="mr-2", id='score-button')
    ]
)
app.layout = dbc.Container(
   [
    button_train,
    html.Div(id="train-result"),
    button_score,
    dcc.Graph(id='anomaly-chart'),
    dcc.Slider(id='date-slider'),
    dcc.Graph(id='bar-chart')
   ], fluid=True,
)


@app.callback(
              [Output("train-result", "children")],
              [Input("train-button", "n_clicks")]
)
def run_training(clicks):
    if clicks is not None:
        df_train = read_time_series_csv("../data/raw-data/ogc_train_file2.csv", date_format='%Y-%m-%dT%H:%M:%S')
        trained_model_name = "ogc_trained_artifact"
        trained_filename = trained_model_name + str(".pickled")
        trained_model_path = os.path.join("../models", trained_filename)
        out = train_workbench(df_train, config_yml_path="../config/ogc_config.yaml", trained_model_path=trained_model_path)
        if out:
            return ["training successful"]
        else:
            return ["training failed"]
    else:
        raise PreventUpdate


@app.callback(
    [Output('date-slider', 'max'),Output('date-slider', 'min'),Output('date-slider', 'value'),
     Output('date-slider', 'marks'), Output('anomaly-chart',"figure") ],
    [Input("score-button", "n_clicks")]
)
def run_scoring_update_slider(clicks):
    global df_cf
    if clicks is not None:
#        print ("clicks,valueinuhuhu", clicks)
        df_score = read_time_series_csv("../data/raw-data/ogc_test.csv", date_format='%Y-%m-%dT%H:%M:%S')
        trained_filename = "ogc_trained_artifact.pickled"
        models_folder_path = "../models"
        trained_model_path = os.path.join(models_folder_path, trained_filename)
        trained_model_path = os.path.abspath(trained_model_path)
        print (trained_model_path)
        df_cf, max_len, fig = score_workbench(df_score, config_yml_path="../config/ogc_config.yaml",
                                              trained_model_fpath=trained_model_path,outpath="../output/score.json")
        # marks = getMarks(df_cf.index, Nth=200)
        # min_val = unixTimeMillis(df_cf.index.min())
        # max_val = unixTimeMillis(df_cf.index.max())
        # actual_value = min
        marks_dict = {}
        for i in range(max_len):
            if i%200 == 0:
                marks_dict[i] = str(df_cf.index[i].strftime("%Y-%m-%d"))
        max_val = max_len
        min_val = 0
        actual_value = 0

        return max_val, min_val, actual_value, marks_dict, fig
    else:
        raise PreventUpdate


@app.callback(
    [Output("bar-chart", "figure")],
    [Input("date-slider", "value")]
)
def render_cf_chart(val):
    if val is not None:
        print (val)
        fig = cf_barchart(df_cf,int(val))
        return [fig]
    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
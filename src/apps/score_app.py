from dash.dependencies import Input, Output, State
import time
import pandas as pd
import io
import base64
import os
from dash.exceptions import PreventUpdate

# importing user defined functions
from model_widgets import score_workbench, cf_barchart
from analysis import timeindex_data
from layout.score_layout import score_layout
from app_def import app

# Global variables
# global dataframe for scoring
df = pd.DataFrame()

# global filename for scoring
fname = ""

# location where the file will be saved
data_folder = "../data/raw-data"

layout = score_layout()


# Functions
def update_global_dataframe_score(contents, filename):
    content_type, content_string = contents.split(',')
    global df
    global fname
    fname = filename
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in fname:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), index_col=0)
        elif 'xls' in fname:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        df = timeindex_data(df)
    except Exception as e:
        return [{'label': "There was an error processing this file",
                 'value': 1}]
    return " "


# callbacks
# update the "select model for scoring dropdown
@app.callback(
    [
        Output("model-select-dropdown", "options")
    ],
    [
        Input("model-select-dropdown", "placeholder")
    ]
)
def update_score_dropdown(pholder):
    model_list = [x for x in os.listdir("../models") if x.endswith(".pickled")]
    option_list = []
    for i in model_list:
        option_list.append({'label': i, 'value': i})

    return [option_list]


# Callbacks
# Upload button callback
@app.callback(
    [
        Output("table-msg", "children")
    ],
    [
        Input('upload-scoring-data', 'contents')
    ],
    [
        State('upload-scoring-data', 'filename')
    ]
)
def update_glob_df(list_of_contents, list_of_names):
    if list_of_contents is not None:
        [update_global_dataframe_score(c, n) for c, n in
         zip(list_of_contents, list_of_names)]
        children = ["File uploaded.."]
        return children
    else:
        raise PreventUpdate


# Score button callback
@app.callback(
    [
        Output("msg1", "children")
    ],
    [
        Input("score-button", "n_clicks"),
    ]
)
def scoring_button(n):
    global df
    if n is not None and not df.empty:
        children = ["Starting"]
        return children
    else:
        raise PreventUpdate


# # Progress bar callback for clean data
@app.callback(
    [Output("progress-score", "value"),
     Output("progress-score", "children"),
     Output("progress-score", "style"),
     Output("progress-interval-score", "disabled")],
    [Input("score-button", "n_clicks"),
     Input("progress-interval-score", 'n_intervals')]
)
def update_progress(clicks, n):
    global df
    if not df.empty:
        if clicks is not None:
            # check progress of some background process, in this example we'll just
            # use n_intervals constrained to be in 0-100
            progress = min(n % 110, 100)
            # only add text after 5% progress to ensure text isn't squashed too much
            return progress, f"{progress} %" if progress >= 5 else "", {"height": "30px"}, False
        else:
            return "", [""], {"height": "0px"}, True
    else:
        return "", [""], {"height": "0px"}, True


# Plot figure callback
@app.callback(
    [
        Output('date-slider', 'max'),
        Output('date-slider', 'min'),
        Output('date-slider', 'value'),
        Output('date-slider', 'marks'),
        Output('anomaly-chart', "figure")
    ],
    [
        Input("msg1", "children")
    ],
    [
        State("model-select-dropdown", "value"),
        State("ocsvm", "value"),
        State("pca", "value"),
        State("knn", "value"),
        State("auto_encoder", "value"),
        State("thresh", "value"),
        State("alerts", "value"),

    ]
)
def run_scoring_update_slider(msg, model_name, ocsvm, pca, knn, auto, threshold, n_alerts):
    global df
    if msg is not None and not df.empty:
        trained_filename = model_name
        models_folder_path = "../models"
        trained_model_path = os.path.join(models_folder_path, trained_filename)
        trained_model_path = os.path.abspath(trained_model_path)
        ade_score_param = {}

        # Updating dictionary to read true or false whenever a method is toggled
        if ocsvm is None:
            pass
        elif 1 in ocsvm:
            ade_score_param['method-OCSVM'] = 'True'
        else:
            ade_score_param['method-OCSVM'] = 'False'

        if pca is None:
            pass
        elif 2 in pca:
            ade_score_param['method-PCA'] = 'True'
        else:
            ade_score_param['method-PCA'] = 'False'

        if knn is None:
            pass
        elif 3 in knn:
            ade_score_param['method-KNN'] = 'True'
        else:
            ade_score_param['method-KNN'] = 'False'

        if auto is None:
            pass
        elif 4 in auto:
            ade_score_param['method-AUTOENCODER'] = 'True'
        else:
            ade_score_param['method-AUTOENCODER'] = 'False'

        if threshold is None:
            pass
        else:
            ade_score_param['threshold'] = str(threshold)
        if n_alerts is None:
            pass
        else:
            ade_score_param["raise_alert_count"] = int(n_alerts)

        print("Running from score_app.py")
        print(ade_score_param)
        df, max_len, fig = score_workbench(df, ade_score_param,
                                           config_yml_path="./config/default_config.yaml",
                                           outpath="../output/score.json",
                                           trained_model_fpath=trained_model_path,
                                           )
        marks_dict = {}
        for i in range(max_len):
            if i % 200 == 0:
                marks_dict[i] = str(df.index[i].strftime("%Y-%m-%d"))
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
        global df
        fig = cf_barchart(df, int(val))
        return [fig]
    raise PreventUpdate


# --------------------
# ADE - settings callbacks

# -----
# Messages callback
@app.callback(
    Output("msg8", "children"),
    [
        Input("ocsvm", "value")
    ]
)
def print_msg(n):
    if n is None:
        raise PreventUpdate
    if 1 in n:
        return ["Choosing OCSVM"]
    elif 1 not in n:
        return [""]
    else:
        raise PreventUpdate


@app.callback(
    Output("msg9", "children"),
    [
        Input("pca", "value"),
    ],
)
def print_msg(n):
    if n is None:
        raise PreventUpdate
    if 2 in n:
        return ["Choosing PCA"]
    elif 2 not in n:
        return [""]
    else:
        raise PreventUpdate


@app.callback(
    [Output("msg10", "children")],
    [
        Input("knn", "value")
    ]
)
def print_msg(n):
    if n is None:
        raise PreventUpdate
    if 3 in n:
        return ["Choosing KNN"]
    elif 3 not in n:
        return [""]
    else:
        raise PreventUpdate


@app.callback(
    [Output("msg11", "children")],
    [
        Input("auto_encoder", "value")
    ]
)
def print_msg(n):
    if n is None:
        raise PreventUpdate
    if 4 in n:
        return ["Choosing Auto Encoder"]
    elif 4 not in n:
        return [""]
    else:
        raise PreventUpdate


# Callback to print % column drops
@app.callback(
    [
        Output('msg12', "children")
    ],
    [
        Input("thresh", "value"),
    ]
)
def print_msg(num):
    if num is not None:
        return ["Selecting {} as threshold above which anomaly will be considered".format(num)]
    else:
        raise PreventUpdate


# Callback to print % column drops
@app.callback(
    [
        Output('msg13', "children")
    ],
    [
        Input("alerts", "value"),
    ]
)
def print_msg(num):
    if num is not None:
        return ["Choosing {} of anomalies above threshold values".format(num)]
    else:
        raise PreventUpdate


# Date time printing
@app.callback(
    Output("msg14", "children"),
    [
        Input("date-picker-db", "start_date"),
        Input("date-picker-db", "end_date"),
        Input("date-picker-db", "min_date_allowed"),
        Input("date-picker-db", "max_date_allowed"),

    ]
)
def display_date(start, end, min_start, min_end):
    if start is None and end is None:
        raise PreventUpdate
    elif start is None:
        min_start = min_start.split('T')[0]
        return ["Selecting data between {} | {}".format(min_start, end)]
    elif end is None and start is not None:
        min_end = min_end.split('T')[0]

        return ["Selecting data between {} | {}".format(start, min_end)]
    else:
        return ["Selecting data between {} | {}".format(start, end)]


# Messages callback
@app.callback(
    [
        Output("msg2", "children")
    ],
    [
        Input("msg1", "children")
    ]
)
def chain_2(n):
    if n is not None:
        children = ["Extracting selected model for scoring"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg3", "children")
    ],
    [
        Input("msg2", "children")
    ]
)
def chain_3(n):
    if n is not None:
        children = ["Preparing data for scoring"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg4", "children")
    ],
    [
        Input("msg3", "children")
    ]
)
def chain_4(n):
    if n is not None:
        children = ["Calculating anomaly scores and contributing factors"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg5", "children")
    ],
    [
        Input("msg4", "children")
    ]
)
def chain_5(n):
    if n is not None:
        children = ["Saving the output data"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg6", "children")
    ],
    [
        Input("msg5", "children")
    ]
)
def chain_6(n):
    if n is not None:
        children = ["Rendering the anomaly score and contributing factor chart"]
        time.sleep(6)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg7", "children")
    ],
    [
        Input("msg6", "children")
    ]
)
def chain_7(n):
    if n is not None:
        children = ["Scoring complete"]
        time.sleep(0.5)
        return children
    raise PreventUpdate


# Run ace msgs prompt
# This button is also dummy
@app.callback(
    [
        Output("adv1", "children"),
        Output("adv2", "children"),

    ],
    [
        Input("ace-button", "n_clicks")
    ]
)
def advisory_button(n):
    if n is not None:
        out1 = ["Cause: Intercooler or Cooling System Malfuction"]
        out2 = ["Advisory: Inspection and maintainance - intercooler and cooling system"]

        time.sleep(1)
        return out1, out2
    raise PreventUpdate

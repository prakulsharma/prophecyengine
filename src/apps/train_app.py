from dash.dependencies import Input, Output, State
import time
import pandas as pd
import dash_table
import io
import base64
import os
from dash.exceptions import PreventUpdate

# importing user defined functions
from model_widgets import train_workbench
from dataframe_wrangling import df_between_dates
from analysis import read_time_series_csv, timeindex_data
from layout.train_layout import layout_model_train
from app_def import app

# Global variables


flag = 0
# global dataframe for train data
df = pd.DataFrame()

# global filename for train
fname = ""

# importing layout
layout = layout_model_train()


# Functions

def table_template(dataframe):
    dataframe = dataframe.round(2)
    dff = dataframe.dropna().copy()
    if 'Template Tags' in dataframe.columns:
        selected_rows = list(dff.index)
    else:
        selected_rows = []
    dt = dash_table.DataTable(
        data=dataframe.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in dataframe.columns],

        # we have 24 hour data so setting it to 24
        page_size=140,
        style_table={'height': '730px', 'overflowY': 'auto'},
        # Change cell_style here
        style_cell={
            # Edit bg color here
            'backgroundColor': 'rgb(245, 242, 243)',
            # Edit font color here
            'color': 'black'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {'if': {'column_id': 'timestamp'},
             'width': '180px'}
        ],
        style_cell_conditional=[
            {
                "if": {'column_id': [i for i in dataframe.columns[1:]]},
                'textAlign': 'left'
            },
        ],
        style_header={
            # Bold
            'fontWeight': 'bold',
            # Color
            "color": "black",
            # Border color
            'border': '1px solid grey',
            # Bg color
            'backgroundColor': 'rgb(219, 217, 217)',
        },
        style_data={
            # Border
            'border': '1px solid grey',
        },
        row_selectable="multi",
        row_deletable=True,
        filter_action="native",
        selected_rows=selected_rows,
    )
    return dt


def update_global_dataframe_train(contents, filename):
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


# Callbacks
# Progress bar callback for train data
# Progress bar callback for train data
@app.callback(
    [Output("progress-train", "value"),
     Output("progress-train", "children"),
     Output("progress-train", "style"),
     Output("progress-interval-train", "disabled")],
    [Input("train-button", "n_clicks"),
     Input("progress-interval-train", 'n_intervals')]
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


# Upload button callback
@app.callback(
    [
        Output("table-msg-b", "children"),
        Output("pca-components", "value"),
        Output('date-picker-db-train', 'min_date_allowed'),
        Output('date-picker-db-train', 'max_date_allowed')
    ],
    [
        Input('upload-data-train', 'contents'),
    ],
    [
        State('upload-data-train', 'filename')
    ]
)
def update_columns(list_of_contents, list_of_names):
    if list_of_contents is not None:
        global df
        [update_global_dataframe_train(c, n) for c, n in
         zip(list_of_contents, list_of_names)]
        children = ["File uploaded.."]
        default_pca_comp = str(int((len(df.columns)) * 0.75))
        sd = df.index[0].to_pydatetime()
        ed = df.index[-1].to_pydatetime()
        return children, default_pca_comp, sd, ed
    # elif data_option == "pp_data_train":
    #     df = read_time_series_csv("../data/raw-data/air_comp_training_data_clean.csv")
    #     children = ["Pre-Processed Data Read Successful"]
    #     return children
    else:
        raise PreventUpdate


# # Select Existing Template button callback
# @app.callback(
#     [
#         Output("tag-map-table-html", "children"),
#         #       Output("tag-map-table", "columns"),
#     ],
#     [
#         Input("template-select", "value")
#     ]
# )
# def display_mapping_table(n):
#     if n is not None:
#         if n == "compressor":
#             path_compressor = "../data/template/Reciprocating-Compressor.csv"
#             df_tag = pd.read_csv(path_compressor)
#             children = [table_template(df_tag)]
#
#             return children
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate

#
# # PCA Default
# @app.callback(
#     Output("pca-components", "value"),
#     [Input("pca", "value")]
# )



# Train button backend
@app.callback(
    [
        Output("msg8-b", "children")
    ],
    [
        Input('msg1-b', 'children'),
        Input("input-model-name", "value")
    ],
    [
        State("model-type-select-train", "value"),
        State("custom-options-ade", "value"),
        State("ocsvm", "value"),
        State("pca", "value"),
        State("pca-components", "value"),
        State("knn", "value"),
        State("k-n", "value"),
        State("knn-method", "value"),
        State("auto_encoder", "value"),
        State("auto-epoch", "value"),
        State("auto-batch-size", "value"),
        State("hidden-neurons", "value"),
        State("date-picker-db-train", "start_date"),
        State("date-picker-db-train", "end_date")
    ]
)
def train_button(n, save_fname, model_type,
                 default,
                 ocsvm,
                 pca, pca_comp,
                 knn, knn_n, knn_method,
                 auto, auto_epoch, auto_batch, auto_hidden,
                 sd, ed):
    if n is not None and not df.empty:
        if sd is not None and ed is not None:
            sd = pd.to_datetime(sd).to_pydatetime()
            ed = pd.to_datetime(ed).to_pydatetime()
            # df2 = df.set_index(df.columns[0]).copy()
            # df2.index = pd.to_datetime(df2.index).copy()
            df2 = df_between_dates(df, sd=sd, ed=ed).copy()
        else:
            df2 = df.copy()

        trained_filename = save_fname + str(".pickled")
        save_model_path = "../models"
        trained_model_path = os.path.join(save_model_path, trained_filename)
        yml_path = "../config/default_config.yaml"  # Default
        ade_config_param = {}
        if default is None:
            out = train_workbench(df2, ade_config_param,
                                  config_yml_path=yml_path,
                                  trained_model_path=trained_model_path)
        else:
            # Updating dictionary to read true or false whenever a method is toggled
            if ocsvm is None:
                pass
            elif 1 in ocsvm:
                ade_config_param['method-OCSVM'] = 'True'
            else:
                ade_config_param['method-OCSVM'] = 'False'

            if pca is None:
                pass
            elif 2 in pca:
                ade_config_param['method-PCA'] = 'True'
                # Updating the dictionary for pca_comp parameters
                ade_config_param['PCA-n_components'] = str(pca_comp)
            else:
                ade_config_param['method-PCA'] = 'False'

            if knn is None:
                pass
            elif 3 in knn:
                ade_config_param['method-KNN'] = 'True'
                # Updating the dictionary for knn parameters
                if knn_n is None:
                    pass
                else:
                    ade_config_param['KNN-n_neighbors'] = str(knn_n)

                if knn_method is None:
                    pass
                else:
                    ade_config_param['KNN-method'] = str(knn_method)
            else:
                ade_config_param['method-KNN'] = 'False'

            if auto is None:
                pass
            elif 4 in auto:
                ade_config_param['method-AUTOENCODER'] = 'True'
                # Updating the dictionary for autoencoder parameters
                if auto_epoch is None:
                    pass
                else:
                    ade_config_param['AUTOENCODER-epochs'] = str(auto_epoch)

                if auto_batch is None:
                    pass
                else:
                    ade_config_param['AUTOENCODER-batch_size'] = str(auto_batch)

                if auto_hidden is None:
                    pass
                else:
                    ade_config_param['AUTOENCODER-hidden_neurons'] = [i for i in auto_hidden.split(',')]
            else:
                ade_config_param['method-AUTOENCODER'] = 'False'

            out = train_workbench(df2, ade_config_param,
                                  config_yml_path=yml_path,
                                  trained_model_path=trained_model_path)

        if out:
            return [""]
        else:
            return ["Training failed, could not save model"]

    else:
        raise PreventUpdate


@app.callback(
    Output("ADE", "is_open"),
    [Input("model-type-select-train", "value")],
    [State("ADE", "is_open")],
)
def toggle_collapse(n, is_open):
   # global flag
    if n == 'ADE':
       # flag += 1
        return not is_open
    elif n is not 'ADE' and flag is not 0:
        return not is_open
    return is_open


# --------------------
# ADE - settings callbacks
@app.callback(
    Output("collapse-settings", "is_open"),
    [
        Input("custom-options-ade", "value")
    ],
    [
        State("collapse-settings", "is_open")
    ],
)
def toggle_collapse(n, is_open):
    if '1' in n or len(n) == 0:
        return not is_open
    return is_open


# -----
# Messages callback

@app.callback(
    Output("config-type-text", "children"),
    [
        Input("model-type-select-train", "value")
    ]
)
def select_algorithm(algorithm):
    if algorithm == 'ADE':
        return ["Choosing Anomaly detection engine"]
    else:
        # later to be modified when more models will be added
        return [""]


@app.callback(
    Output("msg9-b", "children"),
    [
        Input("custom-options-ade", "value")
    ]
)
def default_or_not(n):
    if n is None:
        return ["Choosing default configuration"]
    elif '1' in n:
        return ["Choosing custom configuration"]
    else:
        return ["Choosing default configuration"]


@app.callback(
    Output("msg10-b", "children"),
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
    Output("msg11-b", "children"),
    [
        Input("pca", "value"),
        Input("pca-components", "value")
    ],
)
def print_msg(n, comp):
    if n is None:
        raise PreventUpdate
    if 2 in n:
        return ["Choosing PCA with {} components".format(comp)]
    elif 2 not in n:
        return [""]
    else:
        raise PreventUpdate


@app.callback(
    [Output("msg12-b", "children")],
    [
        Input("knn", "value"),
        Input("k-n", "value"),
        Input("knn-method", "value")
    ]
)
def print_msg(n, knn, method):
    if n is None:
        raise PreventUpdate
    if 3 in n:
        return ["Choosing KNN with {} nearest neighbours and method: {}".format(knn, method)]
    elif 3 not in n:
        return [""]
    else:
        raise PreventUpdate


@app.callback(
    [Output("msg13-b", "children")],
    [
        Input("auto_encoder", "value"),
        Input("auto-epoch", "value"),
        Input("auto-batch-size", "value"),
        Input("hidden-neurons", "value")
    ]
)
def print_msg(n, epoch, batch, str_neurons):
    if n is None:
        raise PreventUpdate
    if 4 in n:
        return ["Choosing Auto Encoder with {} epochs, batch size: {} and hidden neurons {}".format(epoch, batch,
                                                                                                    str_neurons)]
    elif 4 not in n:
        return [""]
    else:
        raise PreventUpdate


# Date time printing
@app.callback(
    Output("msg14-b", "children"),
    [
        Input("date-picker-db-train", "start_date"),
        Input("date-picker-db-train", "end_date"),
        Input("date-picker-db-train", "min_date_allowed"),
        Input("date-picker-db-train", "max_date_allowed"),

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


# Toggle switches
@app.callback(
    Output("ocsvm_contents", "is_open"),
    [Input("ocsvm", "value")],
    [State("ocsvm_contents", "is_open")],
)
def toggle_collapse(n, is_open):
    if 1 in n or len(n) == 0:
        return not is_open
    return is_open


@app.callback(
    Output("pca_contents", "is_open"),
    [Input("pca", "value")],
    [State("pca_contents", "is_open")]
)
def toggle_collapse(toggle, is_open):
    if 2 in toggle or len(toggle) == 0:
        return not is_open
    return is_open


@app.callback(
    Output("knn_contents", "is_open"),
    [Input("knn", "value")],
    [State("knn_contents", "is_open")],
)
def toggle_collapse(n, is_open):
    if 3 in n or len(n) == 0:
        return not is_open
    return is_open


@app.callback(
    Output("auto_encoder_contents", "is_open"),
    [Input("auto_encoder", "value")],
    [State("auto_encoder_contents", "is_open")],
)
def toggle_collapse(n, is_open):
    if 4 in n or len(n) == 0:
        return not is_open
    return is_open


# ------------------------
# Train data button message initiator
@app.callback(
    [
        Output("msg1-b", "children")
    ],
    [
        Input("train-button", "n_clicks"),
    ]
)
def train_msgs_start(n):
    global df
    if n is not None and not df.empty:
        children = ["Starting Model Training"]
        return children
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("msg2-b", "children")
    ],
    [
        Input("msg1-b", "children")
    ]
)
def chain_2(n):
    if n is not None:
        children = ["Feature extraction completed"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg3-b", "children")
    ],
    [
        Input("msg2-b", "children")
    ]
)
def chain_3(n):
    if n is not None:
        children = ["Best model ensemble selected out of KNN, PCA and Autoencoder"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg4-b", "children")
    ],
    [
        Input("msg3-b", "children")
    ]
)
def chain_4(n):
    if n is not None:
        children = ["Running training epochs"]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg5-b", "children")
    ],
    [
        Input("msg4-b", "children")
    ]
)
def chain_5(n):
    if n is not None:
        children = ["Please wait..."]
        time.sleep(2)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg6-b", "children")
    ],
    [
        Input("msg5-b", "children")
    ]
)
def chain_6(n):
    if n is not None:
        children = ["Training Complete"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg7-b", "children")
    ],
    [
        Input("msg6-b", "children")
    ]
)
def chain_7(n):
    if n is not None:
        children = ["Saving model"]
        time.sleep(0.5)
        return children
    raise PreventUpdate


# Change the visibility of upload button on training page
@app.callback(
    [
        Output("train-file-upload-html", "hidden"),
    ],
    [
        Input("data-source-option-train", "value"),
    ]
)
def upload_component_visibility(val):
    if val is not None:
        if val == "pp_data_train":
            return [True]
        else:
            return [False]
    else:
        raise PreventUpdate


# hide pre-built model selection option

@app.callback(
    [
        Output("pre-built-model-html", "hidden"),
    ],
    [
        Input("training-type", "value"),
    ]
)
def upload_component_visibility(val):
    if val is not None:
        if val == "pre_built":
            return [False]
        else:
            return [True]
    else:
        raise PreventUpdate

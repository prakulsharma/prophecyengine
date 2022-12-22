from dash.dependencies import Input, Output, State
import pandas as pd
import io
import base64
from dash.exceptions import PreventUpdate

# importing user defined functions
from widgets import visualize_df, feature_importance, imp_bar_chart
from analysis import read_time_series_csv, timeindex_data
from layout.visualization_layout import layout_viz
from app_def import app

# Global variables
# global df for visualization
df = pd.DataFrame()

# global filename for visualization
fname = ""

layout = layout_viz()


def update_global_dataframe_viz(contents, filename):
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
        #        print(e)
        return [{'label': "There was an error processing this file",
                 'value': 1}]
    return " "


# Callbacks
# Plot graph callback
@app.callback(
    [
        Output("plot-area", "figure")
    ],
    [
        Input("plot-button", "n_clicks"),
        Input("column-select-viz", "value"),
        Input("chart-type", "value"),
        Input("data-transformation", "value"),
        Input("create-subplots", "value"),
        Input("feature-select", "value")

    ],
    [State("switch-feature-sel", "on")]
)
def plot_chart(n, columns, chart_type, dt_trans, subplot, feature_val, switch):
    global df
    if n is not None and not df.empty and not switch:
        stand, norm = False, False
        if dt_trans == 2:
            stand = True
        if dt_trans == 3:
            norm = True
        figure = visualize_df(df, chart_type, columns, False, subplot, norm, stand)
        return [figure]
    elif n is not None and switch and not df.empty and feature_val is not None:
        fimp_series = feature_importance(df, feature_val)
        figure = imp_bar_chart(fimp_series, 20)
        return [figure]
    else:
        raise PreventUpdate


# Upload button callback
@app.callback(
    [
        Output("column-select-viz", "options"),
    ],
    [
        Input('upload-data-viz', 'contents'),
        Input('viz-data-option', 'value'),
    ],
    [
        State('upload-data-viz', 'filename')
    ]
)
def update_columns(list_of_contents, data_option, list_of_names):
    global df
    if list_of_contents is not None and data_option == "csv_data":
        [update_global_dataframe_viz(c, n) for c, n in
         zip(list_of_contents, list_of_names)]
        cols = [{'label': i, 'value': i} for i in df.columns]
        return [cols]
    elif data_option == "pp_data":

        df = read_time_series_csv("../data/raw-data/air_comp_training_data_clean.csv")

        cols = [{'label': i, 'value': i} for i in df.columns]
        return [cols]
    else:

        raise PreventUpdate


# Update the feature select dropdown
@app.callback(
    [
        Output("feature-select", "options"),
    ],
    [
        Input("switch-feature-sel", "on"),
    ]
)
def update_feature_selection_dropdown(n):
    if n is not None:
        cols = [{'label': i, 'value': i} for i in df.columns]
        # print (cols)
        return [cols]
    else:
        raise PreventUpdate


# Change the visibility of upload button
@app.callback(
    [
        Output("viz-upload-html", "hidden"),
    ],
    [
        Input("viz-data-option", "value"),
    ]
)
def upload_component_visibility(val):
    if val is not None:
        if val == "pp_data":
            return [True]
        else:
            return [False]
    else:
        raise PreventUpdate

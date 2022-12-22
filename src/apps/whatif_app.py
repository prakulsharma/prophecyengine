from dash.dependencies import Input, Output
import pandas as pd
import os
from dash.exceptions import PreventUpdate

# importing user defined functions
from model_widgets import plot_anomaly_score_chart
from layout.whatif_layout import layout_whatif
from app_def import app

# location where the file will be saved
data_folder = "../data/raw-data"

layout = layout_whatif()


@app.callback(
    [
        Output("whatif1-param", "options"),
        # Output("whatif2-param", "options"),
        # Output("whatif3-param", "options"),
        # Output("whatif4-param", "options"),
    ],
    [
        Input("whatif1-param", "placeholder")
    ]
)
def populate1_whatif_dropdown(p):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    column_list = list(df_whatif.columns)
    option_list = []
    for i in column_list:
        option_list.append({'label': i, 'value': i})
    return [option_list]


@app.callback(
    [
        # Output("whatif1-param", "options"),
        Output("whatif2-param", "options"),
        # Output("whatif3-param", "options"),
        # Output("whatif4-param", "options"),
    ],
    [
        Input("whatif1-param", "placeholder")
    ]
)
def populate2_whatif_dropdown(p):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    column_list = list(df_whatif.columns)
    option_list = []
    for i in column_list:
        option_list.append({'label': i, 'value': i})
    return [option_list]


@app.callback(
    [
        # Output("whatif1-param", "options"),
        # Output("whatif2-param", "options"),
        Output("whatif3-param", "options"),
        # Output("whatif4-param", "options"),
    ],
    [
        Input("whatif1-param", "placeholder")
    ]
)
def populate3_whatif_dropdown(p):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    column_list = list(df_whatif.columns)
    option_list = []
    for i in column_list:
        option_list.append({'label': i, 'value': i})
    return [option_list]


@app.callback(
    [
        # Output("whatif1-param", "options"),
        # Output("whatif2-param", "options"),
        # Output("whatif3-param", "options"),
        Output("whatif4-param", "options"),
    ],
    [
        Input("whatif1-param", "placeholder")
    ]
)
def populate4_whatif_dropdown(p):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    column_list = list(df_whatif.columns)
    option_list = []
    for i in column_list:
        option_list.append({'label': i, 'value': i})
    return [option_list]


@app.callback(
    [
        Output("whatif1-slider", "min"),
        Output("whatif1-slider", "max"),
        Output("whatif1-slider", "value"),
        Output("slider1-selected-range", "children"),
    ],
    [
        Input("whatif1-param", "value")
    ]
)
def dropdown1_val_change(val):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    df_val = df_whatif[val]
    min_val = 0
    max_val = int(df_val.max())
    slider_val = [min_val, max_val]
    stp = int((max_val - min_val) / 5)

    children = 'Range {}'.format(slider_val)
    #    print ("this is called")
    return min_val, max_val, slider_val, children


@app.callback(
    [
        Output("whatif2-slider", "min"),
        Output("whatif2-slider", "max"),
        Output("whatif2-slider", "value"),
        Output("slider2-selected-range", "children"),
    ],
    [
        Input("whatif2-param", "value")
    ]
)
def dropdown2_val_change(val):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    df_val = df_whatif[val]
    min_val = 0
    max_val = int(df_val.max())
    slider_val = [min_val, max_val]
    stp = int((max_val - min_val) / 5)

    children = 'Range {}'.format(slider_val)
    #    print ("this is called")
    return min_val, max_val, slider_val, children


@app.callback(
    [
        Output("whatif3-slider", "min"),
        Output("whatif3-slider", "max"),
        Output("whatif3-slider", "value"),
        Output("slider3-selected-range", "children"),
    ],
    [
        Input("whatif3-param", "value")
    ]
)
def dropdown3_val_change(val):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    df_val = df_whatif[val]
    min_val = 0
    max_val = int(df_val.max())
    slider_val = [min_val, max_val]
    stp = int((max_val - min_val) / 5)

    children = 'Range {}'.format(slider_val)
    #    print ("this is called")
    return min_val, max_val, slider_val, children


@app.callback(
    [
        Output("whatif4-slider", "min"),
        Output("whatif4-slider", "max"),
        Output("whatif4-slider", "value"),
        Output("slider4-selected-range", "children"),
    ],
    [
        Input("whatif4-param", "value")
    ]
)
def dropdown4_val_change(val):
    df_whatif = pd.read_csv("../output/score.csv", index_col=0)
    df_val = df_whatif[val]
    min_val = 0
    max_val = int(df_val.max())
    slider_val = [min_val, max_val]
    stp = int((max_val - min_val) / 5)

    children = 'Range {}'.format(slider_val)
    #    print ("this is called")
    return min_val, max_val, slider_val, children


@app.callback(
    [

        Output("whatif-plot", "figure"),
        Output("slider1-selected-range", "children"),
        Output("slider2-selected-range", "children"),
        Output("slider3-selected-range", "children"),
        Output("slider4-selected-range", "children"),
    ],
    [
        Input("whatif1-param", "value"),
        Input("whatif2-param", "value"),
        Input("whatif3-param", "value"),
        Input("whatif4-param", "value"),
        Input("whatif1-slider", "value"),
        Input("whatif2-slider", "value"),
        Input("whatif3-slider", "value"),
        Input("whatif4-slider", "value"),

    ]
)
def slider1_val_change(dropdown_val1, dropdown_val2, dropdown_val3, dropdown_val4,
                       slider1_val, slider2_val, slider3_val, slider4_val):
    if dropdown_val1 is not None:
        #       print ("i am in charting")
        #       print (slider1_val)
        #       print (dropdown_val)
        df_whatif = pd.read_csv("../output/score.csv", index_col=0)

        df_val = df_whatif[df_whatif[dropdown_val1].between(slider1_val[0], slider1_val[1])]
        if dropdown_val2 is not None:
            df_val = df_val[df_whatif[dropdown_val2].between(slider2_val[0], slider2_val[1])]
        if dropdown_val3 is not None:
            df_val = df_val[df_whatif[dropdown_val3].between(slider3_val[0], slider3_val[1])]
        if dropdown_val4 is not None:
            df_val = df_val[df_whatif[dropdown_val4].between(slider3_val[0], slider3_val[1])]

        figure = plot_anomaly_score_chart(df_val)
        children1 = 'Range {}'.format(slider1_val)
        children2 = 'Range {}'.format(slider2_val)
        children3 = 'Range {}'.format(slider3_val)
        children4 = 'Range {}'.format(slider4_val)
        return figure, children1, children2, children3, children4,
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("model-select-score-deploy", "options")
    ],
    [
        Input("model-select-score-deploy", "placeholder")
    ]
)
def update_deploy_dropdown(pholder):
    model_list = [x for x in os.listdir("../models") if x.endswith(".pickled")]
    option_list = []
    for i in model_list:
        option_list.append({'label': i, 'value': i})

    return [option_list]

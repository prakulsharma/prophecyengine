import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import time
import pandas as pd
import dash_table
import io
import base64
from dash.exceptions import PreventUpdate
from dash_extensions.snippets import send_data_frame
import datetime

# importing user defined functions
from widgets import data_hygiene_table, clean_data
from analysis import read_time_series_csv
from dataframe_wrangling import df_between_dates
from layout.data_clean_layout import layout_cleaning
from train_app import table_template
from app_def import app

# Global variables
# global dataframe for data cleaning page
df = pd.DataFrame()

# global filename for clean
fname = ""

# location where the file will be saved
decoded = ""
# data_folder = "../data/clean-data"
layout = layout_cleaning()


# User defined function for output table
def table(dataframe):
    """
     Parameters
    ----------
    dataframe: inputs a pandas dataframe

    Returns
    -------
    a dash data table
    """

    dataframe = dataframe.round(2)
    dt = dash_table.DataTable(
        data=dataframe.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in dataframe.columns],
        # we have 24 hour data so setting it to 24
        page_size=24,
        style_table={'height': '690px', 'overflowY': 'auto'},
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

    )
    return dt


# User defined function to parse content into readable format from upload button
def parse_contents(contents, filename):
    """
     Parameters
    ----------
    contents: takes the contents of the uploaded file in raw format
    filename: takes a file name

    Returns
    -------
    Outputs an html object ( a dash table inside the object)


    """
    content_type, content_string = contents.split(',')
    global df
    global fname
    global decoded
    fname = filename
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in fname:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in fname:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div(
        [
            html.Div(table(df)),
        ], style={'text-align': 'center'}
    )


# Callbacks
# Progress bar callback for data cleaning report
@app.callback(
    [Output("progress-cleaning", "value"),
     Output("progress-cleaning", "children"),
     Output("progress-cleaning", "style"),
     Output("progress-interval-cleaning", "disabled")],
    [Input("clean-report", "n_clicks"),
     Input("progress-interval-cleaning", 'n_intervals')]
)
def update_progress_cleaning(clicks, n):
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


# Callback for upload button and display tag detail button(combined)
@app.callback(
    [
        Output('table-display-area-c', 'children'),
        Output('card-header', 'children'),
        Output('date-picker-db', 'min_date_allowed'),
        Output('date-picker-db', 'max_date_allowed')

    ],
    [
        Input('upload-data-cleaning', 'contents'),
    ],
    [
        State('upload-data-cleaning', 'filename')
    ]
)
def update_output(list_of_contents, list_of_names):
    global df
    if list_of_contents is not None:
        children = [parse_contents(c, n) for c, n in
                    zip(list_of_contents, list_of_names)]
        df2 = df.set_index(df.columns[0]).copy()
        df2.index = pd.to_datetime(df2.index)
        sd = df2.index[0].to_pydatetime()
        ed = df2.index[-1].to_pydatetime()
        return children, "Viewing file: {}".format(list_of_names[0]), sd, ed
    # elif n is not None:
    #     path_compressor = "../data/template/Reciprocating-Compressor.csv"
    #     df_tag = pd.read_csv(path_compressor)
    #     children = [table_template(df_tag)]
    #     return children, ""
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('table-display-area-c', 'children')
    ],
    [
        Input("date-picker-db", "start_date"),
        Input("date-picker-db", "end_date")
    ]
)
def slice_based_on_dates(sd, ed):
    global df
    if sd is not None and ed is not None:
        sd = pd.to_datetime(sd).to_pydatetime()
        ed = pd.to_datetime(ed).to_pydatetime()
        df2 = df.set_index(df.columns[0]).copy()
        df2.index = pd.to_datetime(df2.index).copy()
        df2 = df_between_dates(df2, sd=sd, ed=ed).copy()
        children = html.Div(
            [
                html.Div(table(df2.tz_localize(None).reset_index())),
            ], style={'text-align': 'center'}
        )
        sliced_df = df2.reset_index().copy()
        return [children]
    elif sd is None and ed is None:
        children = html.Div(
            [
                html.Div(table(df)),
            ], style={'text-align': 'center'}
        )
        sliced_df = df.copy()
        return [children]
    else:
        raise PreventUpdate


# Callback for data generating data Hygiene report
@app.callback(
    [
        Output('table-display-area-c', 'children'),
        Output('card-header', 'children'),
        Output('download', 'data')
    ],
    [
        Input('hygiene-report-button', 'n_clicks')
    ],
    [
        State("date-picker-db", "start_date"),
        State("date-picker-db", "end_date")
    ]
)
def create_table(n, sd, ed):
    global df
    if n is not None and not df.empty:
        global fname
        filename = fname.split('.')[0]
        if sd is not None and ed is not None:
            sd = pd.to_datetime(sd).to_pydatetime()
            ed = pd.to_datetime(ed).to_pydatetime()
            df2 = df.set_index(df.columns[0]).copy()
            df2.index = pd.to_datetime(df2.index).copy()
            df2 = df_between_dates(df2, sd=sd, ed=ed).copy()
            dff = data_hygiene_table(df2)
        else:
            dff = data_hygiene_table(df)
        dff = dff.reset_index()
        table_name = [dbc.Label(" Data Hygiene Report : {}".format(filename))]
        filename = fname.split('.')[0] + '_hygiene_report.csv'
        download_prompt = send_data_frame(dff.to_csv, filename)
        children = [table(dff)]
        return children, table_name, download_prompt
    else:
        raise PreventUpdate


# Callback for clicking the generate hygiene report button with uploading the file
@app.callback(
    Output("card-header", "children"),
    [
        Input("hygiene-report-button", "n_clicks")
    ]
)
def empty_table(n):
    global df
    if n is not None and df.empty:
        return ["To see the data hygiene report, please upload a file in csv format"]


# Callback for running the program without uploading file
@app.callback(
    [
        Output("card-header", "children"),
    ],
    [
        Input("clean-report", "n_clicks"),
    ]
)
def table_empty(n):
    global df
    if n is not None and df.empty:
        table_name = [
            dbc.Label("To see the clean datafile, please upload a file in csv format first")
        ]
        return table_name
    else:
        raise PreventUpdate


# Callback to table for displaying data
@app.callback(
    [
        Output("card-header", "children"),
        Output("table-display-area-c", "children"),
        Output('download', 'data')
    ],
    [
        Input('msg1-c', 'children'),
    ],
    [
        State("drop-column", "value"),
        State("drop-row", "value"),
        State("data-imputation", "value"),
        State("outlier-algo", "value"),
        State("date-picker-db", "start_date"),
        State("date-picker-db", "end_date")]

)
def write_table(msg, col, row, missing, outlier_method, sd, ed):
    if msg is not None:
        global fname, decoded
        # f_path = os.path.join(data_folder, fname)
        # df = read_time_series_csv(f_path)
        clean_df = read_time_series_csv(io.StringIO(decoded.decode('utf-8')))
        if col is None:
            col = 25
            row = 25
            missing = 'interpolation'
            outlier_method = ['isolation_forest']
        if sd is not None and ed is not None:
            sd = pd.to_datetime(sd).to_pydatetime()
            ed = pd.to_datetime(ed).to_pydatetime()
            df2 = df_between_dates(clean_df, sd=sd, ed=ed).copy()
            df_report = clean_data(df2, fname, col, row, missing, outlier_method)
        else:
            df_report = clean_data(clean_df, fname, col, row, missing, outlier_method)
        filename = fname.split(".")[0]
        table_name = [dbc.Label("Data report of {}".format(filename))]
        df_report = df_report.reset_index()
        children = [table(df_report)]
        time.sleep(4)
        filename = fname.split('.')[0] + "_clean.csv"
        download_prompt = send_data_frame(df.to_csv, filename)
        return table_name, children, download_prompt
    raise PreventUpdate


# Callback to print label on dropping cols
@app.callback(
    Output("remove-col-text", "children"),
    [
        Input("drop-column", "value")
    ]
)
def create_label(value):
    return [dbc.Label("Drop columns when more than {}% missing values".format(value))]


# Callback to print label on dropping cols
@app.callback(
    Output("remove-row-text", "children"),
    [
        Input("drop-row", "value")
    ]
)
def create_label(value):
    return [dbc.Label("Remove rows when more than {}% missing values".format(value))]


@app.callback(
    Output("collapse-settings-pre", "is_open"),
    [
        Input("custom-options-pre", "value")
    ],
    [
        State("collapse-settings-pre", "is_open")
    ],
)
def toggle_collapse_pre(n, is_open):
    if '0' in n or len(n) == 0:
        return not is_open
    return is_open


# Callback to message board
# Callback to print % column drops
@app.callback(
    [
        Output('msg9-c', "children")
    ],
    [
        Input("drop-column", "value"),
    ]
)
def print_msg(num):
    if num is not None:
        return ["Dropping columns when greater than {}% missing values".format(num)]
    else:
        raise PreventUpdate


# Callback to print % row drops
@app.callback(
    [
        Output('msg10-c', "children")
    ],
    [
        Input("drop-row", "value"),
    ]
)
def print_msg(num):
    if num is not None:
        return ["Removing rows when greater than {}% missing values".format(num)]
    else:
        raise PreventUpdate


# Callback to print method to fill missing data
@app.callback(
    [
        Output('msg11-c', "children")
    ],
    [
        Input("data-imputation", "value")
    ]
)
def print_msg(method):
    if method == 'fill_forward':
        return ["Estimating missing values using fill forward method"]
    if method == 'fill_backward':
        return ["Estimating missing values using fill backward method"]
    if method == 'interpolation':
        return ["Estimating missing values using interpolation method"]
    if method == 'drop_na':
        return ["Dropping all missing values detected"]
    else:
        raise PreventUpdate


# Callback to print selected name of outlier printed on msg board
@app.callback(
    [
        Output('msg12-c', "children")
    ],
    [
        Input("outlier-algo", "value")
    ]
)
def print_msg(button_id):
    if button_id == 'isolation_forest':
        return ["Choosing Isolation forest for removing outliers"]
    if button_id == 'elliptic_envelope':
        return ["Choosing Elliptic Envelope for removing outliers"]
    if button_id == 'local_outlier_factor':
        return ["Choosing Local outlier factor for removing outliers"]
    if button_id == 'no_outlier_removal':
        return ["Not removing outliers"]
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('msg13-c', 'children')
    ],
    [
        Input("date-picker-db", "start_date"),
        Input("date-picker-db", "end_date")
    ]
)
def print_msg(sd, ed):
    if sd is not None and ed is not None:
        return ["Selecting data b/w {} and {}".format(sd, ed)]
    else:
        return ["Selecting all data"]

# Callback to message board from Cleaning data and remove outliers button
@app.callback(
    [
        Output("msg1-c", "children")
    ],
    [
        Input("clean-report", "n_clicks"),
    ]
)
def clean_button(n):
    global df
    if n is not None and not df.empty:
        children = ["Gathering Settings and initiating run"]
        return children
    else:
        raise PreventUpdate


# Chain of callbacks
@app.callback(
    [
        Output("msg2-c", "children")
    ],
    [
        Input("msg1-c", "children")
    ]
)
def chain_2(n):
    if n is not None:
        children = ["Reading and estimating raw data statistics"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg3-c", "children")
    ],
    [
        Input("msg2-c", "children")
    ]
)
def chain_3(n):
    if n is not None:
        children = ["Removing columns and rows with bad data"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg4-c", "children")
    ],
    [
        Input("msg3-c", "children")
    ]
)
def chain_4(n):
    if n is not None:
        children = ["Estimating the missing values"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg5-c", "children")
    ],
    [
        Input("msg4-c", "children")
    ]
)
def chain_5(n):
    if n is not None:
        children = ["Removing outliers"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg6-c", "children")
    ],
    [
        Input("msg5-c", "children")
    ]
)
def chain_6(n):
    if n is not None:
        children = ["Creating data cleaning report"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg7-c", "children")
    ],
    [
        Input("msg6-c", "children")
    ]
)
def chain_7(n):
    if n is not None:
        children = ["Saving the data clean file"]
        time.sleep(1)
        return children
    raise PreventUpdate


@app.callback(
    [
        Output("msg8-c", "children")
    ],
    [
        Input("msg7-c", "children")
    ]
)
def chain_8(n):
    if n is not None:
        children = ["Data cleaning complete"]
        time.sleep(1)
        return children
    raise PreventUpdate

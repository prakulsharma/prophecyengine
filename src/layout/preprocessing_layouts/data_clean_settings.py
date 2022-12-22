import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import datetime as dt
from preprocessing_layouts.data_clean_custom_settings import custom_settings

'''

Contains 
1. Select Data Source (dummy radio button) 
    i) Local csv 
    ii) Historian radio button 
2. Select Data source (dummy)
    -Options for selecting data sources from cloud
3. Select Date Range for DB Query (dummy)
4. Drop columns above % missing data                            "drop-column"
5. Drop rows above % missing data                               "drop-row"
6. Select methods for missing data interpolation                "data-imputation"
    i) Fill forward
    ii) Fill backward
    iii) Interpolation
    iv) Drop row
7. Select outlier removal algorithm                             "outlier-algo"
    -Options among various unsupervised learning algorithms
    Isolation forest                                            "isolation_forest"
    Elliptical Envelope                                         "elliptical_envelope"           
    Local outlier factor                                        "local_outlier_factor"
    "Not removing outliers"                                     "no_outlier_removal"                                                
                                                                    


'''

# Control menu for data cleaning
data_clean_settings_content = dbc.Card([
    # 1. Select Data Source Group
    dbc.FormGroup([

        # 1.1 Select Data Source text
        dbc.Label(
            "Select Data Source",
            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 1.i) & 1.ii) Select Data Source Radio buttons
        dbc.FormGroup([
            dbc.RadioItems(
                options=[
                    {"label": "Local CSV File", "value": True},  # Default
                    {"label": "Historian or DB", "value": False, "disabled": False},
                ],
                value=True,
                id="data-source-option",
                inline=True,
            )
        ])
    ]),

    dbc.Row([

        # 2. Select data source Group
        dbc.Col(dbc.FormGroup([

            # 2.1 Select data source text
            dbc.Label(
                "Select Data Source",
                style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

            # 2.2 Select data source options
            dcc.Dropdown(
                id='data-source-select',
                options=[
                    {'label': 'SAAI-DB', 'value': 'SAAI-DB'},
                    {'label': 'IP-21', 'value': 'IP-21'},
                    {'label': 'OPC-UA', 'value': 'OPC-UA'},
                    {'label': 'OSI-PI', 'value': 'OSI-PI'},
                ],
                placeholder='Choose a Data Source',
                disabled=False
            )
        ]),
        ),
    ]),

    dbc.Row([

        # 3. Select Date Range for DB Query Group
        dbc.Col(dbc.FormGroup([

            # 3.1 Select Date Range for DB Query text
            dbc.Label(
                "Select Date Range for DB Query",
                style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

            # 3.2 Select Date Range for DB Query dcc widget
            dcc.DatePickerRange(
                id='date-picker-db',
                min_date_allowed=dt(2010, 8, 5),
                max_date_allowed=dt(2020, 9, 19),
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                calendar_orientation='horizontal',
                disabled=False,
                with_portal=True,
                clearable=True
            ),
        ]),
        ),
    ]),

    # 4.
    dbc.FormGroup(
        dbc.Row([
            dbc.Col(
                dbc.Label(
                    "Enable custom options",
                    style={'font-weight': 'Bold'}
                )),
            dbc.Col(
                dbc.Checklist(
                    options=[{'value': '0'}],
                    switch=True,
                    id='custom-options-pre'
                )
            )
        ])
    ),

    dbc.Collapse(
        [custom_settings],
        id='collapse-settings-pre')
],
    body=True)

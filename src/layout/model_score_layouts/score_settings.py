import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import datetime as dt
from model_score_layouts.score_ade_settings import score_ade_config_content
import dash_html_components as html

'''


Contains
1. Select data source for scoring radio button (dummy)
    i) Local CSV file
    ii) Historian or DB
2. Select data source for scoring drop-down (dummy)
3. Select Date Range for DB Query widget (dummy)
4. Drop Rows above % Missing Data textbox (dummy)
5. Select Method for Missing Data Estimation radio button (dummy)
    i) Fill forward
    ii) Fill backward
    iii) Interpolation
    iv) Drop row

'''

score_settings_content = dbc.Card([
    # 1. Select data source for scoring Group
    dbc.FormGroup([

        # 1.1 Select data source for scoring text
        dbc.Label("Select Data Source for Scoring",
                  style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 1.2 i) and ii) Select data source for scoring radio button
        dbc.FormGroup(
            dbc.RadioItems(
                options=[
                    {"label": "Local CSV File", "value": True},
                    {"label": "Historian or DB", "value": False},
                ],
                value=True,
                id="data-source-option-score",
                inline=True,
            )
        )
    ]
    ),

    html.Div(
        dbc.Row(
            # 2. Select data source for scoring Group
            dbc.Col(dbc.FormGroup(
                [
                    # 2.1 Select data source for scoring text
                    dbc.Label("Select Data Source for scoring",
                              style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

                    # 2.2 Select data source for scoring drop-down
                    dcc.Dropdown(
                        id='data-source-select-score',
                        options=[
                            {'label': 'SAAI-DB', 'value': 'SAAI-DB'},
                            {'label': 'IP-21', 'value': 'IP-21'},
                            {'label': 'OPC-UA', 'value': 'OPC-UA'},
                            {'label': 'OSI-PI', 'value': 'OSI-PI'},
                        ],
                        placeholder='Choose a Data Source'
                    )
                ]
            ),
            ),
        ), hidden=True),

    dbc.Row([
        # 2. Select model type Group
        dbc.Col(dbc.FormGroup([
            # 2.1 Select model type text
            dbc.Label("Select Model Type",
                      style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),
            # 2.2 Select model type drop-down
            dbc.Select(
                id='model-type-select-train',
                options=[
                    {'label': 'Anomaly Detection', 'value': 'ADE'},
                    {'label': 'Forecast', 'value': 'forecast', "disabled": True},
                    {'label': 'Soft Sensing', 'value': 'prediction', "disabled": True},
                    {'label': 'Classification', 'value': 'classification', "disabled": True},
                ], value='ADE'
            )
        ]),
        ),
    ]),

    dbc.Collapse([
        score_ade_config_content],
        id='ADE'
    ),
    html.Div([
        dbc.Row(
            # 3. Select Date Range for DB Query widget
            dbc.Col(dbc.FormGroup([
                # 3.1 Select Date Range for DB Query text
                dbc.Label("Select Date Range for DB Query",
                          style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

                # 3.2 Select Date Range for DB Query widget
                dcc.DatePickerRange(
                    id='date-picker-db-score',
                    min_date_allowed=dt(2019, 8, 5),
                    max_date_allowed=dt(2020, 9, 19),
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    calendar_orientation='horizontal',
                ),
            ]),
            ),
        ),

        # 4. Drop Rows above % Missing Data Group
        dbc.FormGroup(
            dbc.Row([
                # 4.1 Drop Rows above % Missing Data text
                dbc.Col(
                    dbc.Label(
                        "Drop Rows above % Missing Data ",
                        style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                    width=8
                ),

                # 4.2 Drop Rows above % Missing Data textbox
                dbc.Col(
                    dbc.Input(id="drop-row-score",
                              placeholder=" 0-100 ",
                              type="text"),
                    width=4
                )
            ]),
        ),

        # 5. Select Method for Missing Data Estimation Group
        dbc.FormGroup([
            # 5.1 Select Method for Missing Data Estimation text
            dbc.Label(
                "Select Method for Missing Data Estimation",
                style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

            # 5.2 i), ii), iii) & iv) Select Method for Missing Data Estimation radio button
            dbc.RadioItems(
                options=[
                    {"label": "Fill Forward", "value": 'fill_forward'},
                    {"label": "Fill Backward", "value": 'fill_backward'},
                    {"label": "Interpolation", "value": 'interpolation'},
                    {"label": "Drop Row", "value": 'dropna'}
                ],
                value="interpolation",
                id="data-imputation-score",
            )]
        ),
    ], hidden=True)
], body=True
)

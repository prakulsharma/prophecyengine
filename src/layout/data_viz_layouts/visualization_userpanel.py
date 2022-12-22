import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

''''


Contains
1. Data option (Interactive Radio button)           "viz-data-option"
    i) Pre-processed Data                           "pp_data"
    ii) New CSV Upload                              "csv_data"
2. Drag and drop or select browse ( hidden, comes out when clicked on 1. ii) )              "upload-data-viz"    
3. Select Columns for charting (Interactive Drop-down)              "column-select-viz"
4. Select type of chart (Interactive Radio button)                  "chart-type"
    i) Time-series Line                     "time_series"
    ii) Time-series-scatter                 "scatter"
    iii) Histogram                          "distributions"
    iv) Correlation Heatmap                 "correlation_matrix"
5. Data transformation (Interactive Radio button)           "data-transformation"
    i) Raw                  1
    ii) Standardize         2
    iii) Normalize          3
6. Subplots (Interactive radio button)              "create-subplots"
    i) Enable               True
    ii) Disable             False
7. Chart button                 "plot-button"
8. Feature selection Boolean switch                "switch-feature-sel" 
9. Select parameter for feature importance drop-down                "feature-select"


'''

viz_controls_content = dbc.Card([
    html.Div(
        # 1. Data option Group
        dbc.FormGroup([
            # 1.1 Data option text
            dbc.Label(
                "Upload new csv file here",
                style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),
            # 1.2 Data option i) & ii) radio buttons
            dbc.FormGroup([
                dbc.RadioItems(
                    options=[
                        # {"label": "Pre-Processed Data", "value": "pp_data"},
                        {"label": "New CSV Upload", "value": "csv_data"},
                    ],
                    value="csv_data",
                    id="viz-data-option",
                    inline=True,
                )]
            )]
        ), hidden=True),

    # 2. Drag and drop or select browse Group
    html.Div(dbc.FormGroup(
        dbc.Row([
            dbc.Col(
                dcc.Upload(
                    id='upload-data-viz',
                    # 2.1 Drag and drop or select browse Group text
                    children=html.Div('Drag and Drop or Select Browse'),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '5px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
            ),
        ])
    ), hidden=False, id='viz-upload-html'),

    # 3. Select Columns for charting Group
    dbc.FormGroup([

        # 3.1 Select Columns for charting text
        dbc.Label(
            "Select Columns for Charting",
            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 3.2 Select Columns for charting drop-down
        dcc.Dropdown(
            id='column-select-viz',
            options=[{'label': 'Data Not Uploaded', 'value': 'data Not Uploaded'}],
            multi=True,
            placeholder='Choose Parameters for charting'
        )]
    ),

    # 4. Select type of chart Group
    dbc.FormGroup([
        # 4.1 Select type of chart text
        dbc.Label(
            "Select Type of Chart",
            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 4.2 Select type of chart radio button
        dbc.RadioItems(
            options=[
                {"label": "Time series-line", "value": 'time_series'},
                {"label": "Time series-scatter", "value": 'scatter'},
                {"label": "Histogram", "value": 'distributions'},
                {"label": "Correlation Heatmap", "value": 'correlation_matrix'}
            ],
            value="time_series",
            id="chart-type",
        )]
    ),

    # 5. Data transformation group
    dbc.FormGroup([
        # 5.1 Data transformation text
        dbc.Label(
            "Data Transformation",
            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 5.2 Data transformation radio button
        dbc.FormGroup([
            dbc.RadioItems(
                options=[
                    {"label": "Raw", "value": 1},
                    {"label": "Standardize", "value": 2},
                    {"label": "Normalize", "value": 3},
                ],
                value=2,
                id="data-transformation",
                inline=True
            )
        ])
    ]),

    # 6. Subplots group
    dbc.FormGroup([
        # 6.1 Subplots text
        dbc.Label(
            "Subplots",
            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 6.2 Subplots radio button
        dbc.FormGroup([
            dbc.RadioItems(
                options=[
                    {"label": "Enable", "value": True},
                    {"label": "Disable", "value": False},
                ],
                value=True,
                id="create-subplots",
                inline=True,
            )
        ])
    ]),

    # 7. Chart Button
    dbc.FormGroup(
        dbc.Row([
            dbc.Col(''),
            dbc.Col(
                dbc.Button(children="Chart",
                           color="primary",
                           block=True,
                           id='plot-button'
                           )
            ),
            dbc.Col('')
        ])
    ),

    # 8. Feature selection Boolean switch
    dbc.FormGroup(
        dbc.Row([
            dbc.Col(
                # 8.1 Feature selection Boolean switch text
                dbc.Label(
                    "Feature Selection",
                    style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "7px"}),
                width=5),
            # 8.2 Feature selection Boolean switch widget from daq
            dbc.Col(
                daq.BooleanSwitch(
                    id='switch-feature-sel',
                    on=False
                ), width=4, style={"padding-bottom": "2px", "padding-top": "7px"}

            ),
        ])
    ),

    # 9. Select parameter for feature importance Group
    dbc.FormGroup([
        # 9.1 Select parameter for feature importance text
        dbc.Label("Select Parameter for feature importance",
                  style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

        # 9.2 Select parameter for feature importance drop-down
        dbc.Select(
            id='feature-select',
            options=[{'label': 'Data Not Uploaded', 'value': 'data Not Uploaded'}],
        )
    ]),
    html.Div(
        [
            dcc.Store(id='session-store', storage_type='session')
        ], hidden=True)
], body=True
)

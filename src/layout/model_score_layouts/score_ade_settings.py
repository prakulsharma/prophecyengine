import dash_bootstrap_components as dbc
import dash_core_components as dcc
from datetime import datetime as dt
import dash_html_components as html

'''

Contains
1. Select Date Range for DB Query (dummy)
2. Choose method/s switch
    i) OCSVM
    ii) PCA
    iii) KNN
    iv) Autoencoder
3. Select Threshold
4. Raise alerts above



'''
score_ade_config_content = dbc.Card([
    dbc.Row([
        # 3. Select Date Range for DB Query Group
        dbc.Col(
            dbc.FormGroup([
                # 3.1 Select Date Range for DB Query text
                dbc.Label(
                    "Select Date Range for Model Scoring",
                    style={'font-weight': 'Bold',
                           "padding-bottom": "2px",
                           "padding-top": "5px"}),

                # 3.2 Select Date Range for DB Query dcc widget
                dcc.DatePickerRange(
                    id='date-picker-db',
                    min_date_allowed=dt(2019, 8, 5),
                    max_date_allowed=dt(2020, 9, 19),
                    start_date_placeholder_text="Start Period",
                    end_date_placeholder_text="End Period",
                    calendar_orientation='horizontal',
                    with_portal=True,
                    clearable=True),
            ]),
        ),
    ]),

    dbc.Row(
        # 2.
        dbc.Col(
            dbc.FormGroup([
                dbc.Label("Choose method/s",
                          style={'font-weight': 'Bold',
                                 "padding-bottom": "2px",
                                 "padding-top": "5px"}),

                # One Class SVM
                html.Div([
                    # One Class SVM
                    dbc.Checklist(
                        options=[{"label": "OCSVM", "value": 1}],
                        id="ocsvm",
                        switch=True)
                ]),

                # Principal Component Analysis
                html.Div([
                    dbc.Checklist(
                        options=[{"label": "PCA", "value": 2}],
                        id="pca",
                        switch=True
                    ),
                ]),

                # K- nearest neighbours
                html.Div([
                    dbc.Checklist(
                        options=[
                            {"label": "KNN", "value": 3}],
                        id="knn",
                        switch=True),
                ]
                ),

                # Auto-encoder
                html.Div(
                    [
                        dbc.Checklist(
                            options=[
                                {"label": "Autoencoder", "value": 4}],
                            id="auto_encoder",
                            switch=True),
                    ]
                )
            ]
            )
        )
    ),

    # Select threshold  Group
    dbc.FormGroup(

        dbc.Row([

            #  Select threshold Data text
            dbc.Col(
                dbc.Label(
                    "Select threshold ",
                    style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                width=8
            ),
            # Select threshold textbox
            dbc.Col(
                dbc.Input(id="thresh",
                          placeholder=" 1-10 ",
                          type="number",
                          min=1,
                          max=10,
                          step=0.1,
                          value=2.1),
                width=4
            )
        ]
        ),
    ),

    # Raise alert count Group
    dbc.FormGroup(

        dbc.Row([

            #  Raise alert count text
            dbc.Col(
                dbc.Label(
                    "Raise alerts above ",
                    style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                width=8
            ),
            # Raise alert textbox
            dbc.Col(
                dbc.Input(id="alerts",
                          placeholder=" 1-10 ",
                          type="number",
                          min=1,
                          max=10,
                          value=3),
                width=4
            )
        ]
        ),
    ),
], body=True)

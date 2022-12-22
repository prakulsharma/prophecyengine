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
        -Choose PCA Components
    iii) KNN
        -Choose K nearest neighbours
        -Choose method
    iv) Autoencoder
        -Choose Batch size
        -d
        -


'''
train_ade_config_content = dbc.Card([
    dbc.Row([
        # 3. Select Date Range for DB Query Group
        dbc.Col(
            dbc.FormGroup([
                # 3.1 Select Date Range for DB Query text
                dbc.Label(
                    "Select Date Range for Model Training",
                    style={'font-weight': 'Bold',
                           "padding-bottom": "2px",
                           "padding-top": "5px"}),

                # 3.2 Select Date Range for DB Query dcc widget
                dcc.DatePickerRange(
                    id='date-picker-db-train',
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
                    dbc.Collapse(
                        dbc.FormGroup(
                            dbc.Row([

                                # 5.1 Choosing PCA Components text
                                dbc.Col(
                                    dbc.Label(
                                        "Choose PCA components ",
                                        style={"font-weight": 'Bold',
                                               "padding-bottom": "20px",
                                               "padding-top": "7px"}),
                                    width=8),

                                # 5.2 Choosing PCA Components textbox
                                dbc.Col(
                                    dbc.Input(id="pca-components",
                                              placeholder=" 1-1000 ",
                                              type="number",
                                              min=1,
                                              max=1000
                                              ),
                                    width=4)
                            ]),
                        ), id="pca_contents"

                    )
                ]),
                html.Div([
                    dbc.Checklist(
                        options=[
                            {"label": "KNN", "value": 3}],
                        id="knn",
                        switch=True),

                    dbc.Collapse(
                        dbc.FormGroup(
                            [
                                dbc.Row(
                                    [
                                        # Choosing KNN nearest neighbours Components text
                                        dbc.Col(
                                            dbc.Label(
                                                "Choose K-nearest neighbours ",
                                                style={'font-weight': 'Bold', "padding-bottom": "20px",
                                                       "padding-top": "7px"}),
                                            width=8
                                        ),
                                        # Choosing KNN nearest neighbours Components textbox
                                        dbc.Col(
                                            dbc.Input(id="k-n",
                                                      placeholder=" 1-10 ",
                                                      type="number",
                                                      min=1,
                                                      max=10,
                                                      value=5),
                                            width=4
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        # Choosing KNN nearest neighbours method text
                                        dbc.Col(
                                            dbc.Label(
                                                "Choose method ",
                                                style={'font-weight': 'Bold', "padding-bottom": "20px",
                                                       "padding-top": "7px"}),
                                            width=8
                                        ),
                                        # Choosing KNN nearest neighbours method dropdown
                                        dbc.Col(
                                            dcc.Dropdown(
                                                options=[
                                                    {'label': 'largest', 'value': 'largest'},
                                                    {'label': 'mean', 'value': 'mean'},
                                                    {'label': 'median', 'value': 'median'},
                                                ],
                                                value='largest',
                                                id='knn-method'
                                            )
                                        )
                                    ]
                                )
                            ]
                        ),
                        id="knn_contents",
                    ),
                ]
                ),
                html.Div(
                    [
                        dbc.Checklist(
                            options=[
                                {"label": "Autoencoder", "value": 4}],
                            id="auto_encoder",
                            switch=True),
                        dbc.Collapse(
                            dbc.FormGroup([
                                dbc.Row([
                                    # Choosing Auto-encoder epochs text
                                    dbc.Col(
                                        dbc.Label("Choose epochs ",
                                                  style={'font-weight': 'Bold',
                                                         "padding-bottom": "20px",
                                                         "padding-top": "7px"}),
                                        width=8),
                                    # Choosing Auto-encoder epochs textbox
                                    dbc.Col(
                                        dbc.Input(id="auto-epoch",
                                                  placeholder=" 1-200 ",
                                                  type="number",
                                                  min=1,
                                                  max=200,
                                                  value=50),
                                        width=4)
                                ]),
                                dbc.Row([
                                    # Choosing Auto-encoder batch size text
                                    dbc.Col(
                                        dbc.Label("Choose batch-size ",
                                                  style={'font-weight': 'Bold',
                                                         "padding-bottom": "20px",
                                                         "padding-top": "7px"}),
                                        width=8),
                                    # Choosing Auto-encoder batch size textbox
                                    dbc.Col(
                                        dbc.Input(id="auto-batch-size",
                                                  placeholder=" 1-1000 ",
                                                  type="number",
                                                  min=1,
                                                  max=1000,
                                                  value=32),
                                        width=4)
                                ]),
                                dbc.Row([
                                    # Choosing Auto-encoder batch size text
                                    dbc.Col(
                                        dbc.Label("Enter hidden neurons ",
                                                  style={'font-weight': 'Bold',
                                                         "padding-bottom": "20px",
                                                         "padding-top": "7px"}),
                                        width=8),
                                    # Choosing Auto-encoder batch size textbox
                                    dbc.Col(
                                        dbc.Input(id="hidden-neurons",
                                                  placeholder="Enter no. of neurons separated by a comma",
                                                  type="text",
                                                  value='64, 32, 32, 64'),
                                        width=4)
                                ])
                            ]), id='auto_encoder_contents')
                    ]
                )
            ]
            )
        )
    ),
], body=True)

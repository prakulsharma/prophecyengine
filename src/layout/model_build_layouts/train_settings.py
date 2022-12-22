import dash_bootstrap_components as dbc
import dash_core_components as dcc
from model_build_layouts.train_ade_settings import train_ade_config_content
import dash_html_components as html

'''


Contains
1. Select data to be used for training radio button (dummy)
    i) Pre-processed data
    ii) New local csv file
2. Select model type drop-down (dummy)
3. Select algorithm drop-down (dummy)


'''
train_settings_content = dbc.Card(
    [

        html.Div(
            # 1. Select data to be used for training Group
            dbc.FormGroup(
                [
                    # 1.1 Select data to be used for training text
                    dbc.Label("Select Data to be used for Training",
                              style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                    # 1.2 i) & ii) Select data to be used for training radio button
                    dbc.FormGroup(
                        [
                            dbc.RadioItems(
                                options=[
                                    {"label": "Pre-Processed Data", "value": "pp_data_train"},
                                    {"label": "New Local CSV File", "value": "csv_data_train"},
                                ],
                                value="pp_data_train",
                                id="data-source-option-train",
                                inline=True,
                            )
                        ]
                    )
                ]
            ), hidden=True
        ),

        dbc.Row(
            [
                # 2. Select model type Group
                dbc.Col(dbc.FormGroup(
                    [
                        # 2.1 Select model type text
                        dbc.Label("Select Model Type",
                                  style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

                        # 2.2 Select model type drop-down
                        dbc.Select(
                            id='model-type-select-train',
                            options=[
                                {'label': 'Anomaly Detection', 'value': 'ADE'},
                                {'label': 'Forecast', 'value': 'forecast', 'disabled': True},
                                {'label': 'Soft Sensing', 'value': 'prediction', 'disabled': True},
                                {'label': 'Classification', 'value': 'classification', 'disabled': True},
                            ],
                            value='ADE')
                    ]
                ),
                ),
            ]
        ),

        dbc.Collapse(
            [
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
                                options=[{'value': '1'}],
                                switch=True,
                                id='custom-options-ade'
                            )
                        )
                    ])
                ),

                dbc.Collapse(
                    [
                        train_ade_config_content
                    ], id='collapse-settings')

            ], id='ADE'
        ),

        dbc.Row([
            # 3. Select algorithm Group
            dbc.Col(dbc.FormGroup(
                [
                    # 3.1 Select algorithm text
                    dbc.Label(
                        "Select Algorithm",
                        style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

                    # 3.2 Select algorithm drop-down
                    dcc.Dropdown(
                        id='algo-type-select-train',
                        options=[
                            {'label': 'Default', 'value': 'Default'},
                            {'label': 'LSTM', 'value': 'LSTM'},
                            {'label': 'ARIMA', 'value': 'ARIMA'},
                            {'label': 'ARMA', 'value': 'ARMA'},
                            {'label': 'Isolation Forest', 'value': 'isolation_forest'},
                            {'label': 'Elliptical Envelop', 'value': 'elliptical_envelop'},
                            {'label': 'Local Outlier Factor', 'value': 'local_outlier_factor'},
                            {'label': 'Random Forest', 'value': 'random_forest'},
                            {'label': 'Logistic Regression', 'value': 'logistic_regression'},
                            {'label': 'LDA', 'value': 'LDA'},
                        ],
                        placeholder='Choose an algorithm',
                        multi=True,
                        disabled=True
                    )
                ]
            ),
            ),
        ]
        ),
    ], body=True)

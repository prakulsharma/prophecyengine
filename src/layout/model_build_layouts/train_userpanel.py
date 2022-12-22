import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

'''


Contains
1. Model Training type (Interactive radio button)               "training-type"
    i) Pre-built                "pre_built"
    ii) New Model               "new_model"
2. Select Existing Template (Interactive Drop-down)              "template-select"
3. Select Pre-Built model (Interactive Drop-down)                "pre-built-model-dropdown"
4. Save Model as (Interactive Textbox)                      "input-model-name
5. Train Model button                   "train-button"
6. Progress Bar (Hidden, activates when clicked on 5)                   "progress-train",  "progress-interval-train" 
7. Config Board (Displays text, when clicked on 5)             "table-msg-b", "msg8-b", "msg9-b" and so on
8. Message Board (Displays text, when clicked on 5)             "table-msg-b", "msg1-b", "msg2-b" and so on


'''
train_controls_content = dbc.Card(
    [

        # Uploading file group
        dbc.FormGroup([
            # Uploading file prompt
            dbc.Label(
                "Upload Training Data File",
                style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

            # Upload file button
            dbc.FormGroup(
                dbc.Row(
                    dbc.Col(
                        dcc.Upload(
                            id='upload-data-train',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select file')
                            ]),
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
                )
            ),

        ]
        ),

        html.Div(
            # 1. Model Training type Group
            dbc.FormGroup([
                # 1.1 Model Training type text
                dbc.Label("Model Training Type",
                          style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                # 1.2 i) & ii) Model Training type radio button
                dbc.FormGroup(
                    [
                        dbc.RadioItems(
                            options=[
                                {"label": "Pre-Built", "value": "pre_built", "disabled": True},
                                {"label": "New Model", "value": "new_model"},
                            ],
                            value="new_model",
                            id="training-type",
                            inline=True,
                        )
                    ]
                )
            ]
            ), hidden=True),

        html.Div(
            # 2. Select Existing Template Group
            dbc.Row(
                dbc.Col(dbc.FormGroup(
                    [
                        # 2.1 Select Existing Template Text
                        dbc.Label("Select Existing Template",
                                  style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "5px"}),

                        # # 2.2 Select Existing Template Drop-down
                        dcc.Dropdown(
                            id='template-select',
                            options=[
                                {'label': 'Centrifugal Compressor', 'value': 'compressor'},
                                {'label': 'Reciprocating Compressor', 'value': 'compressor'},
                                {'label': 'Reciprocating Pump', 'value': 'pump'},
                                {'label': 'Centrifugal Pump', 'value': 'pump'},
                                {'label': 'Fan', 'value': 'fan'},
                                {'label': 'Gearbox', 'value': 'gearbox'},
                                {'label': 'Induction Motor', 'value': 'induction_motor'},
                                {'label': 'Heat Exchanger', 'value': 'heat_exchanger'},
                                {'label': 'Separator', 'value': 'separator'},
                                {'label': 'Flash', 'value': 'flash'},
                                {'label': 'Mill', 'value': 'mill'},
                                {'label': 'Kiln', 'value': 'kiln'},
                            ],
                            placeholder='Choose a template',
                            disabled=True
                        )
                    ]
                ),
                )
            ), hidden=True)
        ,

        html.Div(dbc.Row(
            # 3. Select Pre-Built model Group
            dbc.Col(dbc.FormGroup(
                [
                    # 3.1 Select pre-built model text
                    dbc.Label("Select Pre-Built Model",
                              style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "2px"}),

                    # 3.2 Select Pre-Built model drop-down
                    dcc.Dropdown(
                        id='pre-built-model-dropdown',
                        options=[
                            {'label': "Centrifugal Compressor ADE", 'value': "comp_trained_artifact"},
                            {'label': "Centrifugal Compressor Forecast", 'value': "comp_trained_artifact"},
                            {'label': "Reciprocating Compressor ADE", 'value': "ogc_trained_artifact"},
                            {'label': "Reciprocating Compressor Forecast", 'value': "ogc_trained_artifact"}
                        ],
                        placeholder='Choose a model'
                    )
                ]
            ),
            )

        ), hidden=False, id="pre-built-model-html"),

        # 4. Save Model as group
        dbc.FormGroup(
            [
                # 4.1 Save Model as text
                dbc.Label(
                    "Save Model as",
                    style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                # 4.2 Save Model as textbox
                dbc.Input(id="input-model-name",
                          placeholder="Type model name",
                          type="text")
            ]
        ),

        # 5. Train Model Group
        dbc.FormGroup(
            dbc.Row(
                [
                    # 5.1 Train Model text
                    dbc.Col(dbc.Label(
                        "Train model",
                        style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"})),
                    dbc.Col(""),
                    # Train Model button (alias "Train")
                    dbc.Col(dbc.Button(
                        "Train",
                        id="train-button",
                        color="primary",
                        className="mr-1",
                        block=True)),

                ]
            ),
        ),

        # 6. Progress bar
        dbc.FormGroup(
            [
                dbc.Progress(id="progress-train"),
                dcc.Interval(id="progress-interval-train", n_intervals=0, interval=100, max_intervals=100)
            ]
        ),

        # 7. Config board group
        dbc.FormGroup([
            dbc.Card([
                # 7.1 Config board text
                dbc.Label('Model Configuration Board',
                          style={
                              'text-align': 'center',
                              'font-weight': 'Bold'
                          }
                          ),

                # 7.2 Output messages
                dbc.CardBody([
                    dbc.Label(id="config-type-text", style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg9-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg10-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg11-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg12-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg13-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg14-b', style={"font-family": "Consolas"})
                ], style={"height": "230px", "overflow": "scroll"}
                )
            ])
        ]),

        # 8. Message board group
        dbc.FormGroup([
            dbc.Card([
                # 8.1 Message board text
                dbc.Label('Message Board',
                          style={
                              'text-align': 'center',
                              'font-weight': 'Bold'
                          }),

                # 8.2 Output messages
                dbc.CardBody([
                    dbc.Label(id="table-msg-b", style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg1-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg2-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg3-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg4-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg5-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg6-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg7-b', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg8-b', style={"font-family": "Consolas"})
                ], style={"height": "230px", "overflow": "scroll"}
                )
            ])
        ]),
    ], body=True
)

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

'''


Contains
1. Select Model for scoring (interactive drop-down)             "model-select-dropdown"
2. Upload scoring data file widget                      "upload-scoring-data"
3. Execute scoring button                       "score-button"
4. Progress bar (Hidden, activates when clicked on 3)               "progress-score", "progress-interval-score"
5. Message Board                "table-msg", "msg1", "msg2" and so on
6. Execute FMEA & ACE button                "ace-button"
7. Advisory Board                   "adv1", "adv2"


'''

score_controls_content = dbc.Card(
    [
        dbc.Row(
            [
                # 1. Select Model for scoring Group
                dbc.Col(dbc.FormGroup(
                    [
                        # 1.1 Select Model for scoring text
                        dbc.Label(
                            "Select Model for Scoring",
                            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "2px"}),

                        # 1.2 Select Model for scoring drop-down
                        dcc.Dropdown(
                            id='model-select-dropdown',
                            options=[{'label': "ogc_trained_artifact", 'value': "ogc_trained_artifact"}],
                            placeholder='Choose a model'
                        )
                    ]
                ),
                ),
            ]
        ),

        # 2. Upload scoring data file Group
        dbc.FormGroup(
            [
                # 2.1 Upload scoring data file text
                dbc.Label("Upload Scoring Data File",
                          style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                # 2.2 Upload scoring data file widget
                dbc.FormGroup(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Upload(
                                    id='upload-scoring-data',
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
                        ]
                    )
                ),

            ]
        ),

        # 3. Execute scoring Group
        dbc.FormGroup(
            dbc.Row(
                [
                    # 3.1 Execute scoring  text
                    dbc.Col(dbc.Label(
                        "Execute Scoring",
                        style={'font-weight': 'Bold', "padding-bottom": "2px",
                               "padding-top": "7px"})),

                    dbc.Col(""),
                    # 3.2 Execute scoring button (alias "Score")
                    dbc.Col(dbc.Button("Score",
                                       id="score-button",
                                       color="primary",
                                       className="mr-1",
                                       block=True)),

                ]
            ),
        ),

        # 4. Progress bar
        dbc.FormGroup(
            [
                dbc.Progress(id="progress-score"),
                dcc.Interval(id="progress-interval-score", n_intervals=0, interval=150, max_intervals=100)
            ]
        ),

        # 5. Message board group
        dbc.FormGroup(
            dbc.Card(
                [

                    # 5.1 Message board text
                    dbc.Label(
                        'Message Board',
                        style={
                            'text-align': 'center',
                            'font-weight': 'Bold'
                        }
                    ),

                    # 5.2 Output messages
                    dbc.CardBody(
                        [
                            dbc.Label(id="table-msg", style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg1', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg2', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg3', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg4', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg5', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg6', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg7', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg8', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg9', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg10', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg11', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg12', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id='msg13', style={"font-family": "Consolas"}), html.Br(),
                            dbc.Label(id="msg14", style={"font-family": "Consolas"})
                        ], style={"height": "130px", "overflow": "scroll"}
                    )
                ]
            )
        ),

        # 6. Execute FMEA & ACE Group
        dbc.FormGroup(
            dbc.Row(
                [
                    # 6.1 Execute FMEA & ACE text
                    dbc.Col(dbc.Label("Execute FMEA & ACE "),
                            style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "7px"}, width=8),

                    # 6.2 Execute FMEA & ACE button (alias "Run ACE")
                    dbc.Col(dbc.Button("Run ACE",
                                       id="ace-button",
                                       color="primary",
                                       className="mr-1",
                                       block=True), width=4),
                ]
            ),
        ),

        # 7. Advisory Group
        dbc.FormGroup(
            dbc.Card(
                [
                    # 7.1 Advisory Board
                    dbc.Label(
                        'Apparent Cause Engine(ACE) results and advisory',
                        style={
                            'text-align': 'center',
                            'font-weight': 'Bold',
                        }
                    ),
                    # 7.2 Advisory Board Output messages
                    dbc.CardBody(
                        [
                            dbc.Label(id="adv1",
                                      style={
                                          'text-align': 'left',
                                          'font-weight': 'Bold',
                                          "color": "#D2691E"
                                      }
                                      ),
                            html.Br(),
                            dbc.Label(id="adv2",
                                      style={
                                          'text-align': 'left',
                                          'font-weight': 'Bold',
                                          "color": "#D2691E"
                                      }
                                      )
                        ]
                    )
                ],
            )
        ),

    ], body=True
)

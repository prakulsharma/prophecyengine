import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash_extensions import Download

'''

Contains
1. Browse file/drag n drop upload button (interactive)              upload-data-cleaning
2. Display tag details and assets button (interactive)              display-tag-button
3. Generate data hygiene report button (interactive)                hygiene-report-button
4. Clean data and remove outliers button (interactive)              clean-report
5. Progress bar for generating data hygiene report                  progress-cleaning, progress-interval-cleaning
(Note: Progress bar is hidden, activates when clicked on 4. and data file is read)
6. Status message                                                   msg1-c, msg2-c and so on
(Displays messages when clicked on 4 
***issue*** # should output file not inserted when no file is read into 1 )


'''

data_clean_controls_content = dbc.Card(
    [
        # 1.Drop and drop or select files Group
        dbc.FormGroup(
            dcc.Upload(
                id='upload-data-cleaning',
                children=html.Div([
                    # 1.1 Drag and drop or select files text
                    'Drag and Drop or Select Files',
                ]),
                style={
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'textAlign': 'center',
                    'borderRadius': '5px',
                    "padding-bottom": "15px"
                },
                # Allowing multiple files to be uploaded
                multiple=True
            ),
        ),

        html.Div(
            # 2.Display Tags and asset names Group
            dbc.FormGroup(
                dbc.Row([
                    # 2.1 Display Tags and asset names text
                    dbc.Col(
                        dbc.Label(
                            "Display Tag Details and Assets",
                            style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                        width=8
                    ),

                    # 2.2 alias " Display " (Display Tags and asset names button)
                    dbc.Col(
                        dbc.Button(
                            "  Display  ",
                            outline=True,
                            color="primary",
                            block=True,
                            className="mr-1",
                            id="display-tag-button",
                            disabled=True,
                            style={"padding-bottom": "5px", "padding-top": "5px"}),
                        width=4
                    )
                ]
                ),
            ),
            hidden=True),

        # 3. Generate Data hygiene Report Group
        dbc.FormGroup(

            dbc.Row([
                # 3.1 Generate Data hygiene report text
                dbc.Col(
                    dbc.Label(
                        "Generate Data Hygiene Report",
                        style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                    width=8
                ),

                # 3.2 alias " Run " (Generate Data hygiene report button)
                dbc.Col(
                    dbc.Button(
                        "  Run  ",
                        # outline=True,
                        color="primary",
                        block=True,
                        # className="mr-1",
                        id="hygiene-report-button",
                        style={"padding-bottom": "5px",
                               "padding-top": "5px",
                               "backgroundColor": "#3B7DEB",
                               # "color": "#3B7DEB"
                               }),
                    width=4
                ),
                # 3.3 Download prompt
                Download(id="download")

            ]
            ),
        ),

        # 4. Clean data and Remove outliers group
        dbc.FormGroup([
            dbc.Row([

                # 4.1 Clean data and remove outliers text
                dbc.Col(
                    dbc.Label(
                        "Clean Data and Remove Outliers",
                        style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                    width=8
                ),

                # 4.2 alias " Run " (Clean data and remove outliers button)
                dbc.Col(
                    dbc.Button(
                        "  Run  ",
                        # outline=True,
                        color="primary",
                        block=True,
                        className="mr-1",
                        id='clean-report',
                        style={"padding-bottom": "5px", "padding-top": "5px"}),
                    width=4
                )
            ]
            )
        ]
        ),

        # 5. Progress bar for cleaning data
        dbc.FormGroup([
            dbc.Progress(id="progress-cleaning"),
            dcc.Interval(id="progress-interval-cleaning", n_intervals=0, interval=100, max_intervals=100)
        ]
        ),

        # 6. Config Message group
        dbc.FormGroup([
            dbc.Card([
                # 6.1 Config Message text
                dbc.Label(
                    'Configuration Board',
                    style={
                        'text-align': 'center',
                        'font-weight': 'Bold'
                    }),
                # 6.2 Output messages
                dbc.CardBody([
                    dbc.Label(id='msg9-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg10-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg11-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg12-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg13-c', style={"font-family": "Consolas"})
                ]
                )
            ]
            )
        ]
        ),

        # 6. Status Message group
        dbc.FormGroup([
            dbc.Card([
                # 6.1 Status Message text
                dbc.Label(
                    'Status Message',
                    style={
                        'text-align': 'center',
                        'font-weight': 'Bold'
                    }),
                # 6.2 Output messages
                dbc.CardBody([
                    dbc.Label(id='msg1-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg2-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg3-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg4-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg5-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg6-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg7-c', style={"font-family": "Consolas"}), html.Br(),
                    dbc.Label(id='msg8-c', style={"font-family": "Consolas"})

                ]
                )
            ]
            )
        ]
        ),
    ], body=True
)

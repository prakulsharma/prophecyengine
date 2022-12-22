import dash_bootstrap_components as dbc
import dash_core_components as dcc

'''


Contains
1. Select Model for Deployment drop-down (dummy)
2. Select Tenant drop-down (dummy)
3. Enter Analytic Name textbox(dummy)
4. Upload model to network button (dummy)


'''
whatif_deployment_content = dbc.Card(
    [
        dbc.Row(
            # 1. Select Model for Deployment group
            dbc.Col(
                dbc.FormGroup(
                    [
                        # 1.1 Select Model for Deployment text
                        dbc.Label("Select Model for Deployment",
                                  style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "2px"}),

                        # 1.2 Select Model for Deployment drop-down
                        dcc.Dropdown(
                            id='model-select-score-deploy',
                            options=[{'label': "kbr-demo-model.artifact", 'value': "kbr-demo-model.artifact"}],
                            placeholder='Choose a model',
                            value="kbr-demo.pickled"

                        )
                    ]
                ),
            ),
        ),
        # 2. Select Tenant Group
        dbc.Row(
            dbc.Col(
                dbc.FormGroup(
                    [
                        # 2.1 Select Tenant text
                        dbc.Label("Select Tenant",
                                  style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "2px"}),

                        # 2.2 Select Tenant drop-down
                        dcc.Dropdown(
                            id='tenant-select-score-deploy',
                            options=[
                                {'label': "KBR", 'value': "kbr"},
                                {'label': "KBR-Eurochem", 'value': "kbr-eurochem"}
                            ],
                            placeholder='Choose a model',
                            value="kbr"
                        )
                    ]
                ),
            ),
        ),

        # 3. Enter Analytic Name Group
        dbc.FormGroup(
            [

                # 3. Enter Analytic Name text
                dbc.Label(
                    "Enter Analytic Name",
                    style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                # 3. Enter Analytic Name textbox
                dbc.Input(id="input-analytic-name_score",
                          placeholder="Enter Analytic name",
                          type="text")
            ]
        ),

        # 4. Upload model to network Group
        dbc.FormGroup(
            dbc.Row(
                [
                    # 4.1 Upload model to network text
                    dbc.Col(dbc.Label("Upload Model to Network",
                                      style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "7px"}),
                            width=8),

                    # 4.2 Upload model to network button (alias "Publish")
                    dbc.Col(dbc.Button("Publish",
                                       id="publish-button",
                                       color="secondary",
                                       className="mr-1",
                                       block=True), width=4),

                ]
            ),
        ),
    ], body=True
)

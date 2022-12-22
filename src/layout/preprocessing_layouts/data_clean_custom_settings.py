import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


custom_settings = dbc.FormGroup([
            # 4. Drop Columns above % Missing Data Group
            dbc.FormGroup(
                dbc.Row([
                    # 4.1 Remove columns with more than % missing data text
                    dbc.Col(
                        html.Div(
                            dbc.Label(
                                "Drop columns when more than  % Missing Data ",
                                id='remove-col-text',
                                style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"})
                        ), id="styled-numeric-input",
                        width=8
                    ),

                    # 4.2 Remove columns with more than  % Missing Data textbox
                    dbc.Col(
                        html.Div(
                            dbc.Input(id="drop-column",
                                      placeholder=" 1-100 ",
                                      type="number",
                                      min=1,
                                      max=100,
                                      value=95),
                        ), id="styled-numeric-input",
                        width=4
                    )
                ]),
            ),
            # 5. Drop Rows above % Missing Data Group
            dbc.FormGroup(
                dbc.Row([

                    # 5.1 Drop Rows above % Missing Data
                    dbc.Col(
                        dbc.Label(
                            "Remove rows with more than % Missing Data ",
                            id='remove-row-text',
                            style={'font-weight': 'Bold', "padding-bottom": "20px", "padding-top": "7px"}),
                        width=8
                    ),
                    # 5.2 Drop Rows above % Missing Data textbox
                    dbc.Col(
                        dbc.Input(id="drop-row",
                                  placeholder=" 1-100 ",
                                  type="number",
                                  min=1,
                                  max=100,
                                  value=95),
                        width=4
                    )
                ]),
            ),
            # 6. Select methods for missing data interpolation
            dbc.FormGroup([
                # 6.1 Select methods for missing data interpolation text
                dbc.Label(
                    "Select Method for Missing Data Imputation",
                    style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                # 6.2 i), ii), iii) & iv) Select methods for missing data interpolation radio buttons
                dbc.RadioItems(
                    options=[
                        {"label": "Fill Forward", "value": 'fill_forward'},
                        {"label": "Fill Backward", "value": 'fill_backward'},
                        {"label": "Interpolation", "value": 'interpolation'},
                        {"label": "Drop Row", "value": 'drop_na'}
                    ],
                    value='interpolation',
                    id="data-imputation",
                )
            ]),
            # 7. Select outlier removal algorithm
            dbc.FormGroup([
                # 7.1 Select outlier removal algorithm text
                dbc.Label(
                    "Select Outlier Removal Algorithm",
                    style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "15px"}),

                # 7.2 Select outlier removal algorithm dropdown
                dbc.Select(
                    id='outlier-algo',
                    options=[
                        {'label': 'Isolation Forest', 'value': 'isolation_forest'},
                        {'label': 'Elliptic Envelope', 'value': 'elliptic_envelope'},
                        {'label': 'Local Outlier Factor', 'value': 'local_outlier_factor'},
                        {'label': 'Do not Remove Outliers', 'value': 'no_outlier_removal'},
                    ],
                    value='isolation_forest'
                )
            ]), ])

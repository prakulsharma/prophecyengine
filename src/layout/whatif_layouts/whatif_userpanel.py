import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

'''


Contains
1. Select what-if Parameter: Tag-1 drop-down
2. Slider 1
3. Slider 1 range
4. Select what-if Parameter: Tag-2 drop-down 
5. Slider 2
6. Slider 2 range
7. Select what-if Parameter: Tag-2 drop-down 
8. Slider 3
9. Slider 3 range
10. Select what-if Parameter: Tag-2 drop-down
11. Slider 4
12. Slider 4 range



'''
whatif_controls_content = dbc.Card(
    [
        # 1.Select what-if Parameter: Tag-1 Group
        dbc.FormGroup(
            [
                dbc.Row(
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                # 1.1 Select what-if Parameter: Tag-1 text
                                dbc.Label(
                                    "Select what-if Parameter: Tag-1",
                                    style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "2px"}),

                                # 1.2 Select what-if Parameter: Tag-1 drop-down
                                dcc.Dropdown(
                                    id='whatif1-param',
                                    options=[
                                        {'label': '1ST CYL. VALVE TEMP.', 'value': '1ST CYL. VALVE TEMP.'},
                                        {'label': '1ST CYL. VALVE TEMP..1', 'value': '1ST CYL. VALVE TEMP..1'}],
                                    placeholder='Choose a Parameter',
                                )
                            ]
                        ),
                    )
                ),

                dbc.Row(
                    [
                        # 2. Slider 1 widget
                        dbc.Col(
                            dcc.RangeSlider(
                                id='whatif1-slider',
                                updatemode='mouseup',
                                min=0,
                                max=40,
                                count=1,
                                step=1,
                                value=[0, 40]
                            ),
                            width=8, style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "10px"}
                        ),
                        # Slider 1 range
                        dbc.Col(html.Div(id='slider1-selected-range', children="Range"), width=4)
                    ]
                ),

            ]
        ),
        # 4. Select what-if Parameter: Tag-2 Group
        dbc.FormGroup(
            [
                dbc.Row(
                    dbc.Col(dbc.FormGroup(
                        [
                            # 4.1 Select what-if Parameter: Tag-2 text
                            dbc.Label("Select what-if Parameter: Tag-2",
                                      style={'font-weight': 'Bold', "padding-bottom": "2px",
                                             "padding-top": "20px"}),

                            # 4.1 Select what-if Parameter: Tag-2 drop-down
                            dcc.Dropdown(
                                id='whatif2-param',
                                options=[{'label': 'Choose', 'value': 'Choose'}],
                                placeholder='Choose a Parameter',
                            )
                        ]
                    ),
                    )
                ),
                dbc.Row(
                    [
                        # 5. Slider 2
                        dbc.Col(
                            dcc.RangeSlider(
                                id='whatif2-slider',
                                updatemode='mouseup',
                                min=0,
                                max=40,
                                count=1,
                                step=1,
                                value=[0, 40]

                            ),
                            width=8, style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "10px"}
                        ),
                        # 6. Slider 2 range
                        dbc.Col(html.Div(id='slider2-selected-range', children="Range"),
                                width=4)
                    ]
                ),

            ]
        ),
        # 7. Select what-if Parameter: Tag-2 Group
        dbc.FormGroup(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.FormGroup(
                            [
                                # 7.1 Select what-if Parameter: Tag-2 text
                                dbc.Label("Select what-if Parameter: Tag-3",
                                          style={'font-weight': 'Bold', "padding-bottom": "2px",
                                                 "padding-top": "20px"}),

                                # 7.2 Select what-if Parameter: Tag-2 drop-down
                                dcc.Dropdown(
                                    id='whatif3-param',
                                    options=[{'label': 'Choose', 'value': 'Choose'}],
                                    placeholder='Choose a Parameter',
                                    # value="Choose"
                                )
                            ]
                        ),
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        # 8. Slider 3
                        dbc.Col(
                            dcc.RangeSlider(
                                id='whatif3-slider',
                                updatemode='mouseup',
                                min=0,
                                max=40,
                                count=1,
                                step=1,
                                value=[0, 40]

                            ),
                            width=8, style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "10px"}
                        ),
                        # 9. Slider 3 range
                        dbc.Col(html.Div(id='slider3-selected-range', children="Range"), width=4)

                    ]
                ),

            ]
        ),
        # 10. Select what-if Parameter: Tag-2 Group
        dbc.FormGroup(
            [
                dbc.Row(
                    dbc.Col(dbc.FormGroup(
                        [
                            # 10. Select what-if Parameter: Tag-2 text
                            dbc.Label("Select what-if Parameter: Tag-4",
                                      style={'font-weight': 'Bold', "padding-bottom": "2px",
                                             "padding-top": "20px"}),

                            # 10. Select what-if Parameter: Tag-2 drop-down
                            dcc.Dropdown(
                                id='whatif4-param',
                                options=[{'label': 'Choose', 'value': 'Choose'}],
                                placeholder='Choose a Parameter',
                                # value="Choose"
                            )
                        ]
                    ),
                    ),
                ),
                dbc.Row(
                    [
                        # 11. Slider 4
                        dbc.Col(
                            dcc.RangeSlider(
                                id='whatif4-slider',
                                updatemode='mouseup',
                                min=0,
                                max=40,
                                count=1,
                                step=1,
                                value=[0, 40]

                            ),
                            width=8, style={'font-weight': 'Bold', "padding-bottom": "2px", "padding-top": "10px"}
                        ),
                        # 12. Slider 4 range
                        dbc.Col(html.Div(id='slider4-selected-range', children="Range"), width=4)
                    ]
                ),
            ]
        )
    ], body=True
)

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

# importing setting and controls layout
from preprocessing_layouts.data_clean_settings import data_clean_settings_content
from preprocessing_layouts.data_clean_userpanel import data_clean_controls_content

'''


Contains                        
1. Tabs Group                    
    i) User Panel (Tab 1)        
    ii) Settings (Tab 2)        
2. Data Display Panel               "card-header", "table-display-area-c"
                                    


'''

# 1. Tabs Group
data_clean_controls = dbc.Card(
    dbc.CardHeader(
        # 1. Creating tabs for user panel and settings
        dbc.Tabs(
            [
                # 1.i) Calling user panel(controls) in tab 1
                dbc.Tab(data_clean_controls_content, label="User Panel"),

                # 1.ii) Calling settings(advanced) in tab 2
                dbc.Tab(data_clean_settings_content, label="Settings")
            ],

        ), style={"height": "80vh", "overflow": "scroll"}),
)

# 2. Data display panel Group
display_panel = dbc.Card(
    [
        # 2.1 Data display panel text
        dbc.CardHeader(
            children="Data Display Panel",
            style={"text-align": "center"}, id="card-header"),

        # 2.2 Table display area widget
        dbc.FormGroup(
            dcc.Loading(
                html.Div(id="table-display-area-c")
            )
        )
    ], style={"height": "80vh", "overflow": "scroll"}
)


# Function returning the layout of cleaning
def layout_cleaning():
    layout = dbc.Container(
        [
            dbc.Row(
                [
                    # 1. Tabs
                    dbc.Col(data_clean_controls, md=4),
                    # 2. Data display Panel
                    dbc.Col(display_panel, md=8)
                ]
            )
        ], fluid=True
    )
    return layout

import dash_bootstrap_components as dbc
import dash_html_components as html

# importing controls for model building
from model_build_layouts.train_settings import train_settings_content
from model_build_layouts.train_userpanel import train_controls_content

'''


Contains
1. Tabs Group
    i) User Panel (Tab 1)
    ii) Settings (Tab 2)
    # iii) ADE settings (Tab 3)
2. Tag Map Display Panel 


'''

# 1. Tabs Group
train_controls = dbc.Card(
    dbc.CardHeader(
        # Creating tabs for user panel and settings
        dbc.Tabs(
            [
                # 1. i) Calling user panel controls in Tab 1
                dbc.Tab(train_controls_content, label="User Panel"),

                # 1. ii) Calling settings in Tab 2
                dbc.Tab(train_settings_content, label="Settings"),

                # # 1. iii) Calling ADE setting in Tab 3
                # dbc.Tab(train_ade_config_content, label="ADE-settings")
            ],
        ), style={"height": "80vh", "overflow": "scroll"}),
)

# 2. Tag Map Display Panel Group
mapping_table = dbc.Card(
    [
        # 2.1 Tag Map Display Panel text
        dbc.CardHeader(
            children="Tag Map Display Panel",
            style={"text-align": "center"}, id="train-card-header"),

        # 2.1 Tag Map Display Panel widget
        dbc.Container(
            # Table map display area
            html.Div(id="tag-map-table-html")
        )
    ], style={"height": "80vh", "overflow": "scroll"})


# Function returning layout of Model build
def layout_model_train():
    layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(train_controls, md=4),
                dbc.Col(mapping_table, md=8)
            ]
        ), fluid=True
    )
    return layout

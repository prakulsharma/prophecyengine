import dash_bootstrap_components as dbc
import dash_core_components as dcc

# importing controls for model scoring
from model_score_layouts.score_settings import score_settings_content
from model_score_layouts.score_userpanel import score_controls_content

'''


Contains
1. Tabs Group
    i) User Panel (Tab 1)
    ii) Settings (Tab 2)
2. Chart display Panel 
    i) Anomaly chart
    ii) Slider widget
    iii) Bar chart


'''

# 1. Tabs Group
score_controls = dbc.Card(
    dbc.CardHeader(
        # Creating tabs for user panel and settings
        dbc.Tabs(
            [
                # 1. i) Calling user panel controls in Tab 1
                dbc.Tab(score_controls_content, label="User Panel"),

                # 1. ii) Calling settings in Tab 2
                dbc.Tab(score_settings_content, label="Settings"),
            ],
        ), style={"height": "80vh", "overflow": "scroll"}),
)

# 2. Chart display Panel Group
mapping_table = dbc.Card(
    [
        # 2. Chart display Panel text
        dbc.CardHeader(children="Chart Display Panel", style={"text-align": "center"}, id="score-card-header"),
        dbc.Container(
            # Chart display Panel Charts and slider
            dbc.FormGroup(
                [
                    # 2.i) Anomaly chart
                    dbc.Row(
                        dcc.Graph(id="anomaly-chart"),
                        align="center", style={"height": "30%"}
                    ),

                    # 2.ii) Slider widget
                    dcc.Slider(id="date-slider"),

                    # 2.iii) Bar chart
                    dbc.Row(
                        dcc.Graph(id="bar-chart"),
                        align="center", style={"height": "30%"}
                    )
                ]
            )
        )
    ], style={"height": "80vh", "overflow": "scroll"},
)


# Function returning layout of Model Scoring
def score_layout():
    layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(score_controls, md=4),
                dbc.Col(mapping_table, md=8)
            ]
        ), fluid=True
    )
    return layout

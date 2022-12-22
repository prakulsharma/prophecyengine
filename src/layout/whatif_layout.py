import dash_bootstrap_components as dbc
import dash_core_components as dcc

# importing deployment and controls layout
from whatif_layouts.whatif_userpanel import whatif_controls_content
from whatif_layouts.whatif_deployment import whatif_deployment_content

'''


Contains
1. Tabs Group
    i) User Panel
    ii) Deployment
2. Chart Display Panel 


'''

# 1. Tabs Group
whatif_controls = dbc.Card(
    dbc.CardHeader(
        # 1. Creating Tab for user panel and deployment
        dbc.Tabs(
            [
                # 1. i) Creating Tab for user panel
                dbc.Tab(whatif_controls_content, label="User Panel"),

                # 1. ii) Creating Tab for Deployment
                dbc.Tab(whatif_deployment_content, label="Deployment")
            ],
        ), style={"height": "80vh", "overflow": "scroll"}),
)

# 2. Chart Display Panel Group
table_layout = dbc.Card(
    [
        # 2.1 Chart Display Panel text
        dbc.CardHeader(children="Chart Display Panel", style={"text-align": "center"}, id="whatif-card-header"),

        # 2.2 Chart Display Panel Group
        dbc.Container(
            # loading animation added using dcc.loading to make it look smooth
            dcc.Loading(
                id="graph-loading",
                children=dcc.Graph(id='whatif-plot')),
        )
    ], style={"height": "80vh", "overflow": "scroll"}
)


# layout of what if
def layout_whatif():
    layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(whatif_controls, md=4),
                dbc.Col(table_layout, md=8)
            ]
        ), fluid=True
    )
    return layout

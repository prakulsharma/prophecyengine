import dash_bootstrap_components as dbc
import dash_core_components as dcc

# importing controls for visualization
from data_viz_layouts.visualization_userpanel import viz_controls_content

'''


Contains
1. Tabs Group
    i) User Panel (Tab 1)
2. Chart Display Panel          - plot-area


'''

# 1. Tabs Group
controls = dbc.Card(
    dbc.CardHeader(
        # 1. Creating Tab for user panel
        dbc.Tabs(
            # 1. i)Calling user panel controls in Tab 1
            dbc.Tab(viz_controls_content, label="User Panel"),
        ), style={"height": "80vh", "overflow": "scroll"}),
)

# 2. Chart Display Panel group
plot_charts = dbc.Card(
    [
        # 2.1 Chart Display Panel text
        dbc.CardHeader(children="Chart Display Panel", style={"text-align": "center"}, id="viz-card-header"),

        # 2.1 Chart Display Panel widget
        dbc.Container(
            # loading animation added using dcc.loading to make it look smooth
            dcc.Loading(id="graph-loading",
                        children=(dcc.Graph(id='plot-area'))),
        ),
    ], style={"height": "80vh", "overflow": "scroll"})


# layout of visualization
def layout_viz():
    layout = dbc.Container(

        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(plot_charts, md=8)
            ]
        ),
        fluid=True
    )
    return layout

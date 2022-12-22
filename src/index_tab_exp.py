import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd


# importing layouts


from apps import viz_app , data_cleaning_app, score_app, train_app, whatif_app


# importing user defined functions

# Global variables
# global dataframe for data cleaning page
df_clean = pd.DataFrame()
# global df for visualization
df_viz = pd.DataFrame()
# global dataframe for train data
df = pd.DataFrame()
# global dataframe for scoring
df = pd.DataFrame()

# global filename for clean
fname_clean = ""
# global filename for visualization
fname_viz = ""
# global filename for train
fname_train = ""
# global filename for scoring
fname = ""

# location where the file will be saved
data_folder = "../data/raw-data"
from app_def import app


top = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Img(src="https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/102019/kbr.png?Gl1TizHsMBX59_ntwVZ3PW0x1WUCLw6x&itok=spHi0CSr",
                                 className="col",
                                 style={
                                     "width": "15%"
                                 }), md=4
                        ),
                dbc.Col(html.H4("Digital Twin Studio",
                                className="text-center",
                                style={"text-align": 'center', "font-family": 'Source Sans Pro',
                                       "vertical-align": "middle"}
                                ),md=4
                        ),
                # dbc.Col(html.Img(src="https://www.ritec-eg.com/Products/img/Azima.png",
                #                  className="col",
                #                  style={
                #                      "display":"block",
                #                      "width": "30%",
                #                      "text-align": "right",
                #                      "margin-right": "2px"
                #                  }), md=4
                #         ),

            ]
        )
    ], fluid=True,
    #style={"background-color":"#F5F5F5"}
)

bottom = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(children="Powered by Symphony AzimaAI © 2020",
                                 className="col",
                                 style={
                                     "width": "50%"
                                 }),
                        ),

                dbc.Col(" ")
            ]
        )
    ], fluid=True
)

# card = dbc.Card(
#     [
# #        dbc.CardHeader(
#
#             dbc.Tabs(
#                 [
# #                    dbc.Tab(label="Model Template", tab_id="tab-1"),
#                     dbc.Tab(data_cleaning_app.layout,label="Data Pre-Processing", tab_id="tab-2"),
#                     dbc.Tab(viz_app.layout, label="Data Visualization", tab_id="tab-3"),
#                     dbc.Tab(train_app.layout, label=" Model Build ", tab_id="tab-4"),
#                     dbc.Tab(score_app.layout, label="Model Scoring", tab_id="tab-5"),
#                     dbc.Tab(whatif_app.layout, label="What-if Analysis", tab_id="tab-6"),
#                 ],
#                 id="card-tabs",
#                 card=False,
#                 active_tab="tab-2",
#                 persistence=True,
#                 persistence_type='session'
#
#             ),
# #        ),
# #        dbc.CardBody(html.P(id="card-content", className="card-text")),
#     ]
# )


card = dbc.Tabs(
                [
#                    dbc.Tab(label="Model Template", tab_id="tab-1"),
                    dbc.Tab(data_cleaning_app.layout,label="Data Pre-Processing", tab_id="tab-2"),
                    dbc.Tab(viz_app.layout, label="Data Visualization", tab_id="tab-3"),
                    dbc.Tab(train_app.layout, label=" Model Build ", tab_id="tab-4"),
                    dbc.Tab(score_app.layout, label="Model Scoring", tab_id="tab-5"),
                    dbc.Tab(whatif_app.layout, label="What-if Analysis", tab_id="tab-6"),
                ],
                id="card-tabs",
                card=False,
                active_tab="tab-2",
                persistence=True,
                persistence_type='session'

            )




app.layout = dbc.Container([
    top,
    card,
    bottom
], fluid=True
)


# Index callbacks
# @app.callback(
#     Output("card-content", "children"), [Input("card-tabs", "active_tab")]
# )
# def tab_content(tab):
#     # if tab == "tab-1":
#     #     # Page 1
#     #     return dbc.Row([
#     #         html.Img(
#     #             src=app.get_asset_url('image.png'),
#     #             style={'width': "90%",
#     #                    "height": "80vh"
#     #                    }
#     #         )
#     #     ], justify="center",
#     #         align="center"
#     #
#     #     )
#
#     if tab == "tab-2":
#         return data_cleaning_app.layout
#     if tab == "tab-3":
#         return viz_app.layout
#     if tab == "tab-4":
#         return train_app.layout
#     if tab == "tab-5":
#         return score_app.layout
#     if tab == "tab-6":
#         return whatif_app.layout


if __name__ == '__main__':
    app.run_server(debug=True,port=1118, threaded=False)
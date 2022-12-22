import dash
import dash_bootstrap_components as dbc

# Using SPACELAB theme from dash bootstrap components
app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB],  suppress_callback_exceptions=True)
server = app.server

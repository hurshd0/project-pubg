import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Insights

            After selecting the final model to be a Random Forest, and limiting to Top 10 features, the test metrics were:

            <img src="https://i.imgur.com/fGPbjg6.png" class="img-fluid">

            

            <img src="https://i.imgur.com/wXCWFp1.png" class="img-fluid">

            <img src="https://i.imgur.com/8bB3hSj.png" class="img-fluid">

            <img src="https://i.imgur.com/5IIfD5b.png" class="img-fluid">

            <img src="https://i.imgur.com/9dpyGCo.png" class="img-fluid">



            """,
            dangerously_allow_html=True),
    ],
)

layout = dbc.Row([column1])

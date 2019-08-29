import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has 
twelve columns.

There are three main layout components in dash-bootstrap-components: Container, 
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column 
should take up a third of the width. Since we don't specify behaviour on 
smaller size screens Bootstrap will allow the rows to wrap so as not to squash 
the content.
"""

column1 = dbc.Col(
    [
        dcc.Markdown(
            """        
            ### So, Boys and Girls? 🤖💣💥🔫🤖

            Battle Royale-style video games have taken the world by storm. At the beginning of the play, nearly 100 people parachute onto an island without any equipment. In order to win the game, you need to scavenge for weapons and available equipment to eliminate the other people and survive to the end. The game also restricts player in Hunger Game style by reducing the playable are in map after a some amount of fixed time is passed.
            
            [PlayerUnknown's BattleGrounds (PUBG)](https://www.pubg.com/) has enjoyed massive popularity. With over 50 million copies sold, it's the fifth best selling game of all time, and has millions of active monthly players.

            The team at PUBG has made official game data available for the public using [REST API gateways](https://developer.pubg.com/). 

            The problem we have is, there is not set guide or strategy to improve player performance in PUBG, should your play style be stealth like a ninja and sneak upon unsuspecting players, or by camping in one spot and hide your way into victory, or snipe like assassin, or do you need to be aggressive and play like Rambo?

            *So, why not try out what it takes to win the game ?*

            """
        ),
        dcc.Link(dbc.Button('Call To Action', color='warning'),
                 href='/predictions')
    ],
    md=6
)


column2 = dbc.Col(
    [
        html.Img(src='assets/images/pubg-image.jpg',
                 className='rounded img-fluid')
    ],
    md=6
)


layout = dbc.Row([column1, column2])

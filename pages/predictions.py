# Dash imports
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

# My app imports
from app import app

# Other 3rd party library imports
from joblib import load
import pandas as pd


model_path = 'assets/model/model.joblib'
model = load(model_path)
print('[DEBUG] Model loaded successfully')

column1 = dbc.Col(
    [
        dcc.Markdown("""
        # Predict
        Get your approximate winning placement prediction in PUBG, by updating controls below.
        """, className='mb-6'),
        html.Br(),

        dcc.Markdown('#### Platform 🎮 (Pick your poison)'),
        dcc.RadioItems(
            id='platform',
            options=[
                {'label': 'Steam', 'value': 'steam'},
                {'label': 'PSN', 'value': 'psn'},
                {'label': 'XBox', 'value': 'xbox'},
                {'label': 'Kakao', 'value': 'kakao'}
            ],
            value='steam',
            labelStyle={'display': 'inline-block'},
            style={'margin-left': '1rem'},
            className='mb-6',
        ),
        html.Br(),

        dcc.Markdown('#### Game Mode 🕹️ (Pick your style)'),
        dcc.Dropdown(
            id='game_mode',
            options=[
                {'label': 'Solo', 'value': 'solo'},
                {'label': 'Solo-FPP', 'value': 'solo-fpp'},
                {'label': 'Duo', 'value': 'duo'},
                {'label': 'Duo-FPP', 'value': 'duo-fpp'},
                {'label': 'Squad', 'value': 'squad'},
                {'label': 'Squad-FPP', 'value': 'squad-fpp'}
            ],
            value='squad',
            className='mb-6',
        ),
        html.Br(),


        dcc.Markdown('#### Map 🗺️ (Pick your Terrain)'),
        dcc.Dropdown(
            id='map_name',
            options=[
                {'label': 'Baltic', 'value': 'Baltic_Main'},
                {'label': 'Desert', 'value': 'Desert_Main'},
                {'label': 'Erangel', 'value': 'Erangel_Main'},
                {'label': 'Savage', 'value': 'Savage_Main'},
                {'label': 'DihorOtok', 'value': 'DihorOtok_Main'}
            ],
            value='Erangel_Main',
            className='mb-6',
        ),
        html.Br(),


        dcc.Markdown(
            '#### Walk distance 🏃‍ (How far can you run?)(in meters)'),
        daq.Knob(
            id='walk_distance',
            min=0,
            max=15000,
            value=500,
            className='mb-6',
        ),
        html.Br(),


        dcc.Markdown(
            '#### Ride distance 🏎️ (How far can you ride?)(in meters)'),
        daq.Knob(
            id='ride_distance',
            min=0,
            max=20000,
            value=5000,
            className='mb-6',
        ),
        html.Br(),

        dcc.Markdown(
            '#### Time Survived ⌛ (How long can you survive?)(in seconds)'),
        daq.Knob(
            id='time_survived',
            min=0,
            max=2000,
            value=600,
            className='mb-6',
        ),
        html.Br(),

        dcc.Markdown(
            '#### Match Duration ⏲️ (How long match should last?)(in seconds)'),
        daq.Slider(
            id='duration',
            min=100,
            max=2500,
            value=1600,
            className='mb-6',
        ),
        html.Br(),

        dcc.Markdown(
            '#### Weapons Acquired 💣💥🔫 (How many weapons you can get?)'),
        daq.Slider(
            id='weapons_acquired',
            min=100,
            max=2500,
            value=1600,
            className='mb-6',
        ),
        html.Br(),

        dcc.Markdown(
            '#### Boosts 🥤 (Get pumped up?)'),
        daq.Slider(
            id='boosts',
            min=0,
            max=30,
            value=0,
            className='mb-6',
        ),
        html.Br()
    ],
    md=6,
)

column2 = dbc.Col(
    [
        html.H4('Winning Placement Precition', className='mb-6'),
        html.Div(id='prediction-label', className='lead',
                 style={'marginBottom': '.1em', 'fontWeight': 'bold', 'fontSize': '22px'}),
        html.Br(),
        html.Div(id='prediction-gauge')
    ],
    md=6
)

layout = dbc.Row([column1, column2])


@app.callback(
    [Output('prediction-label', 'children'),
     Output('prediction-gauge', 'children')],
    [Input('walk_distance', 'value'),
     Input('time_survived', 'value'),
     Input('duration', 'value'),
     Input('game_mode', 'value'),
     Input('platform', 'value'),
     Input('ride_distance', 'value'),
     Input('map_name', 'value'),
     Input('weapons_acquired', 'value'),
     Input('boosts', 'value')
     ]

)
def predict(walk_distance, time_survived, duration, game_mode, platform, ride_distance, map_name, weapons_acquired, boosts):

    # Create row
    row = pd.DataFrame(
        columns=['walkDistance', 'timeSurvived', 'duration', 'gameMode',
                 'platform', 'rideDistance', 'mapName', 'weaponsAcquired', 'boosts'],
        data=[[walk_distance, time_survived, duration, game_mode,
               platform, ride_distance, map_name, weapons_acquired, boosts]]
    )

    y_pred = model.predict(row)[0]

    output1 = f'Your chances of winning are {y_pred * 100:.2f}%'

    output2 = daq.Gauge(
        id='win-place-pred-gauge',
        value=y_pred,
        max=1,
        min=0,
        units='%')

    print(f'[DEBUG] {output1}')
    
    return [output1, output2]

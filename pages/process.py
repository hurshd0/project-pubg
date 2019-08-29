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
            ## Data Science Process
            ---
            """),

        html.Img(src='assets/images/data-science-process.jpg',
                 className='rounded img-fluid'),
        html.Br(),

        dcc.Markdown(
            """
            
            ### What is the Objective?
            
            **Defining the problem:** The problem we have is, there is not set guide or strategy to improve player performance in PUBG, should your play style be stealth like a ninja and sneak upon unsuspecting players, or by camping in one spot and hide your way into victory, or snipe like assassin, or do you need to be aggressive and play like Rambo? 

            **Solution:** Is to create a web application that allows players to improve their strategy by considering *What-if* scenarios as MVP.


            ### Get the data (Data Mining)
            Data was gathered using [PUBG REST API](https://documentation.pubg.com/) from different **platforms**:

            - **steam**
            - **psn**
            - **xbox**
            - **kakao**

            Gathered data was sample of matches retrieved from the API for each platform, and merged. 

            > NOTE: Care was taken to anonymize the data by removing player user names or any identifiable information.

            #### Read-in and split the data 3-Way (Train, Validate, and Test)
            After combining the data, it was split into 3-Way split, as seen below.
            
            <img src="https://i.imgur.com/EpGEEbi.png" class="img-fluid">
            
            #### Explore the data

            Let's glimpse at the data.

            ##### The Killers
            <img src="https://i.ytimg.com/vi/rnAeX795Jn0/maxresdefault.jpg" class="img-fluid">
            Average players had barely any kills, (noobs), 99% of the people had 7 kills or less, while the most kills ever recorded was 25.

            ##### The Runners
            <img src="https://steemitimages.com/DQmRmYLRxu1vUhVtnFAA6bHFbShtr7Wdv1wLrPjdxbRZsjc/maxresdefault%20(2).jpg" class="img-fluid">

            Average person walked about ~ 1 KM or less, while marathon runner walked almost 13 KM.

            ##### The Stuntmans 
            <img src="http://cdn.gamer-network.net/2018/metabomb/pubghowtodrivecarsandbikes.jpg" class="img-fluid">
 
            Average person never even rode any vehicles while 99% of people have drived 650m or less, while the formula 1 champion drived for 25104m.

            ##### The Michael Phelps
            <img src="https://i.ytimg.com/vi/tQxzsE0DijQ/maxresdefault.jpg" class="img-fluid">

            99% of people didn't even swimmed, but the olympic chamipon swimmed for ~ 3 KMs.

            ##### The Boosters and Healers
            <img src="https://i.ytimg.com/vi/xfI9XljX51k/maxresdefault.jpg" class="img-fluid">

            Average person didn't use any boosts or heals, which was strong reflective of how many newbie players game had, as 99% of them had even used not more than 2 items. 

            #### Decide what are we predicting

            When it comes to engineering the target, the goal was to predict player's chances of winning, which meant, converting one of the feature that showed player's match rankings. The feature that showed the player placement was `winPlace` which was normalized using **Min-Max Scaler** to indicate player's chances of winning.  

            #### Get the baseline mean
            As you might expect, everyone had equal probability of winning, so the baseline reflected it. 

            #### Perform Data Wrangling
            
            There were lot of anomalies, issues with players getting disconnected or logging out of without finishing the game, some cheaters using hacks or other exploits, trolls, and peace lovers which were removed from the dataset.

            ##### The Cheaters

            <img src="https://cdn.mos.cms.futurecdn.net/DUfdH6DxUojNR9Sf4aJHUG-650-80.jpg" class="img-fluid">

            Being the most popular game yet, it's been plagued with lot of hacks and cheats ever since it was launched on PC, from aimbots, to Wall hacks, location radars, and increasing complex hacks of source code of the game, as this allows dishonest player to get leg up on the leaderboard which affects the trust players have. 

            Developers of PUBG have used proactive measures, like using software that detects any tempering, player reported cheats, but not yet any passive measures, which allows for undetectable hacks to pass through this filter. 
            
            It was crucial to identify this types of players, and evident on them being outliers going against average players. 

            Source: [PUBG Cheats Explained](https://www.gamesradar.com/pubg-cheats-explained/)

            
            #### Addressing Leakage
            
            Target leakage was addressed by removing two leakage feature:
            
            - `killPlace` :  Ranking in match of number of enemy players killed
            - `deathType` : If player killed another player or by their teammates or self-inflicted death (i.e. suicide) or alive
            
            #### Choose a model and decide on hyper-parameters
            
            Modeling process was something like below, for each:
            
            - *Linear Regression Model*
            - *Random Forest*
            - *XGBoost*
            - *Light GBM*

            <img src="https://i.imgur.com/kNTb7H6.png" class="img-fluid">
            
            Out of all four models, Linear Regression performed the worse, which was to be expected as most features were multi-colinear, followed by Random Forest, than a tie between XGBoost and LightGBM.

            To tune hyperparameters for RandomForest, XGBoost and LightGBM, *Randomsized Search* was used to get ball park estimates due to time constraints and computing limitations.

            In the end, Random Forest was chosen to deploy due to it's time complexity, and size constraints when pickling.

            ##### Top 10 Features
            In order to make the app interactive, only the Top 10 features were selected through *Permutation Importances**.

            <img src="https://i.imgur.com/IJXy5wo.png" class="img-fluid">

            **Permutation Importances**: The basic idea is that observing how much the score decreases when a feature is not available. Above figure shows the importance of each feature. 

            ##### Understanding the Black Box

            After selecting the final model, next step was to understand actual impact of top 10 features one the model. It was crucial to understand why the model makes a certain predictions, what drives it and how it can be used to explain the user.

            """,
            dangerously_allow_html=True),

    ],
)

layout = dbc.Row([column1])

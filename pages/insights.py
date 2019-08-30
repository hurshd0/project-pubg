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
            ---

            After selecting the final model to be a Random Forest, and limiting the features, the test metrics were:
            
            <img src="https://i.imgur.com/fGPbjg6.png" class="img-fluid">
 
            ---

            ### SHAP Summary plot 
            To help interpret and determine the significane of features included in the mode, Shapley values help better way to measure the contribution of individual features. 
           
            NOTE: Since computing shapley values is computationaly expensive, only **N = 1000** observeations were sampled at random.  

            <img src="assets/images/shap_feature_importance.png" class="img-fluid">
            <br>

            Evidently the most important feature is the `walkDistance` and `timeSurvived`, followed by `duration` of the match and `gameMode`.

            Since, the game is BattleRoyale-style, it would make sense as the zone gets narrower players needs to be on constant move, thereby increasing their `walkDistance`, while the duration and time survived affects your chances of winning also.
            
            ---

            ### Understand a single player's chances of winning a particular match

            SHAP values sum to the difference between the expected output of the model and the current output for the current player. *Note that for the Tree SHAP implmementation the margin output of the model is explained, not the trasformed output (such as a probability for logistic regression).* This means that the units of the SHAP values for this model are log odds ratios. Large positive values mean a player is likely to win, while large negative values mean they are likely to lose.

            Let's take a random player from the test set, and see it's feature values and model predictions:
            <img src="https://i.imgur.com/wXCWFp1.png" class="img-fluid">

            So, model is little optimistic 😂, intuitively we would think since the player is in squad (i.e. group of 2, 3, or 4 players), has a weapon to defend himself, survied longer, would have slightly higher chances of winning, i.e. model giving 20% chance of winning because of it ??? 

            Is this what the mode is doing ? Is the intuition correct ? With the Black box models like Random Forest that are harder to interpret computing shapley values with the tree explainer method, and passing it to `force_plot` function from the **shap** package shows below explanations of the features that decide the player's prediction from the base value.
            
            <img src="https://i.imgur.com/8bB3hSj.png" class="img-fluid">
            
            So, the model didn't do what we thought, on the contrary being in a team, playing a longer duration match does the opposite, while not obvious are - factors pushing prediction higher than *actual* like the platform `xbox`, which we completely overlooked.

            ---

            ### Summarizing the impact of all features over the entire dataset

            A SHAP value for a feature of a specific prediction represents how much the model prediction changes when we observe that feature. In the summary plot below, we see all the SHAP values for each feature on y-axis and SHAP value of each player on x-axis. Features that are driving the model's prediction a lot are sorted from top to bottom, with most like `walkDistance`, and least like `mapName`. Note that the `walkDistance` in certain ranges gives higher probability of winning while if not within those ranges reduces the chances of winning. While having smaller match duration may improve the chance of winning contrary to what we intuitively think. 
            
            > Note that when points don't fit together on the line they pile up vertically to show density (e.g. such as `rideDistance`, `platform`, `boosts`, etc...). 


            <img src="assets/images/shap_summary_all_features.png" class="img-fluid">

            ---

            ### Examine how changes in a feature changes the model predictions

            Essential it is similar to how we can tune the knobs in predictions page. Similarly by plotting, the SHAP value for selected feature against the actual value of that feature for all the players we can see how changes in the feature's value affect the model's output. The plots carry the same information as Partial Dependence Plots (PDP plots) but with added advantage of displaying how much interaction terms matter.

            For example, we can see interesting relation between walking further and survival time, so further you walk, the longer you can survive, but not vice-versa, as reflected in second plot. Also, note that there are almost two groups, those that didn't walk further weren't able to survive vs. those that did walk further were able to survive longer.

            <img src="https://i.imgur.com/OcEBIT6.png" class="img-fluid">

            ---

            ### Potential Drawbacks

            As you might have noticed, `kills`, is not the most important feature contributing towards the model predictions, and this was solely due to very low amount of kills observed in the game. 

            To understand this, let's look at joint distribution of `kills` vs. `winPlacePerc` our target,

            <img src="assets/images/joint_plot_kills_target.png" class="img-fluid">

            As you can see most players were killed or won the game without making any kills, this might be due to disconnect logouts or peace lovers (those that didn't kill and just sneaked away from other players to win), ninjas (those that only needed fewer kills to win the game), and some potential cheaters mixed with newbie players that may have caused it. Problem can be remediated by gathering more sample match statistics of players over the course of week, than analyze so noise can be eliminated from actual statistic.
            """,
            dangerously_allow_html=True),
    ],
)

layout = dbc.Row([column1])

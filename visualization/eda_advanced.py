# %%
import numpy as np
import pandas as pd
import itertools

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

# %%
# extract hours per user
df_plot2 = df_plot.drop(df_plot[df_plot.race_driven == "0000-00-00 00:00:00"].index)
df_plot2["race_driven"] = pd.to_datetime(df_plot2["race_driven"], dayfirst=True)

df_aux = pd.DataFrame(df_plot2.groupby("challenger").apply(lambda x: x.race_driven.dt.strftime("%H"))).reset_index(level=1, drop=True)
df_aux.index.names = ["player_id"]
df_aux.rename(columns={"race_driven": "hour"}, inplace=True)

df_aux2 = pd.DataFrame(df_plot2.groupby("opponent").apply(lambda x: x.race_driven.dt.strftime("%H")).reset_index(level=1, drop=True))
df_aux2.rename(columns={"race_driven": "hour"}, inplace=True)
df_aux2.index.names = ["player_id"]

df_grp_player2 = df_aux.append(df_aux2)

# %%
# Count hours per user
df_play_hours = pd.DataFrame(df_grp_player2.reset_index().groupby("player_id")["hour"].value_counts())
df_play_hours.rename(columns={"hour": "total_games"}, inplace=True)
df_play_hours.reset_index(level=1, inplace=True)
df_play_hours["hour"] = df_play_hours["hour"].astype("int")


# %%
def categorize_online_time(hour):

    online_times = {"morning": list(range(6, 13)),
                    "afternoon": list(range(12, 18)),
                    "evening": list(range(17, 22)),
                    "early_night": list(range(21, 24)) + [0, 1],
                    "night": list(range(1, 7))}

    if hour in online_times["morning"]:
        return "morning"
    elif hour in online_times["afternoon"]:
        return "afternoon"
    elif hour in online_times["evening"]:
        return "evening"
    elif hour in online_times["early_night"]:
        return "early_night"
    elif hour in online_times["night"]:
        return "night"


df_play_hours["online_time"] = df_play_hours["hour"].apply(lambda x: categorize_online_time(x))


# %%
player_online_time = pd.DataFrame(df_play_hours.groupby(["player_id","online_time"])["total_games"].sum()).reset_index(level=1)
index_max_games = player_online_time.groupby("player_id")["total_games"].transform(max) == player_online_time["total_games"]
player_max_online = player_online_time[index_max_games]
player_max_online.loc[player_max_online.total_games>3]
# plot daily cycle of those with many nights and mornings
# plot total time of day play stuff
# conclude might be different time zone


# %%
# ELO-ZAHL
def compute_elo(elo_a, elo_b, winner):
    elo_diff = elo_b-elo_a
    elo_change_a = 1/(1 + 10^(elo_diff/400))
    elo_change_b = 1 - elo_change_a
    k = 10 # hier anpassen
    
    if winner=="a":
        new_elo_a = elo_a + k * (1 - elo_change_a)
        new_elo_b = elo_b + k * (0 - elo_change_b)
    elif winner=="b":
        new_elo_a = elo_a + k * (0 - elo_change_a)
        new_elo_b = elo_b + k * (1 - elo_change_b)
    elif winner="both":
        new_elo_a = elo_a + k * (0.5 - elo_change_a)
        new_elo_b = elo_b + k * (0.5 - elo_change_b)
        
    return new_elo_a, new_elo_b
    new_elo_a = 1/(1 + 10^(elo_diff/400))
    new_elo_b = 1-elo_a
    return 1/(1 + 10^(elo_diff/400))

# %%

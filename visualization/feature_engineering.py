# %%
import numpy as np
import pandas as pd
import itertools

from data.transformation import compute_elo, extract_player_info

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


# %%
data = pd.read_csv("data/cleaned_data/races_cleaned.csv")
data[["race_created", "race_driven"]] = data[["race_created", "race_driven"]].astype("datetime64")

# %%
# Extract player id
opponents = data.opponent.unique()
opponents.sort()
challengers = data.challenger.unique()
challengers.sort()

player_ids = list(set(list(opponents) + list(challengers)))


# %%
# Create Elo time series
elo_start = 1500  # which value??????????
elo_df = pd.DataFrame(columns=["date"]+["player_" + str(player_id) for player_id in player_ids])

# 1 day less for initialization
elo_df["date"] = pd.date_range(start=data["race_created"].min()-pd.to_timedelta("1D"), end=data["race_created"].max(), freq="D")
elo_df.loc[0,1:] = elo_start

# %%
import time
from tqdm import tqdm
start = time.time()
df_grouped = data.dropna().groupby("race_created")
current_index = 1 # adjust for "ghost row"!
for name, group in tqdm(df_grouped):
    elo_df.iloc[current_index] = elo_df.iloc[current_index-1:current_index+1].fillna(method="ffill").iloc[1]
    for _, row in group.iterrows():
        challenger_id, opponent_id, winner = extract_player_info(row)
        challenger_elo = elo_df.iloc[current_index, player_ids.index(challenger_id)]
        opponent_elo = elo_df.iloc[current_index, player_ids.index(opponent_id)]
        challenger_elo_new, opponent_elo_new = compute_elo(elo_challenger=challenger_elo,
                                                           elo_opponent=opponent_elo,
                                                           winner=winner)
        elo_df.iloc[current_index, player_ids.index(challenger_id)] = challenger_elo_new
        elo_df.iloc[current_index, player_ids.index(opponent_id)] = opponent_elo_new
    current_index += 1
    # ???
end= time.time()
print(end-start)

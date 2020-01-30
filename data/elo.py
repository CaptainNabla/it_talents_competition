# %%
import pandas as pd
import time
from tqdm import tqdm

from data.transformation import compute_elo, extract_player_info


# %%
data = pd.read_csv("data/cleaned_data/races_cleaned.csv")
data[["race_created", "race_driven"]] = \
    data[["race_created", "race_driven"]].astype("datetime64")


# %%
# Extract player id
player_ids = list(pd.unique(data[["challenger", "opponent"]].values.ravel("K")))
player_ids.sort()


# %%
# Create Elo time series
elo_start = 1500  # TODO: which value??????????
elo_df = pd.DataFrame(columns=["date"]+["player_" + str(player_id) for player_id in player_ids])

# 1 additional day for initialization
elo_df["date"] = pd.date_range(start=data["race_created"].min()-pd.to_timedelta("1D"),
                               end=data["race_created"].max(), freq="D")
elo_df.loc[0, 1:] = elo_start

data.dropna(inplace=True)
dates_without_games = [pd.to_datetime(date)
                       for date in elo_df["date"].values
                       if date not in data["race_created"].values]


# %%
start = time.time()
# TODO: as method
df_grouped = data.dropna().groupby("race_created")
for current_index, _ in tqdm(elo_df.loc[1:].iterrows()):
    date = elo_df.loc[current_index, "date"]
    elo_df.loc[current_index] = \
        elo_df.iloc[current_index - 1:current_index+1].fillna(method="ffill").iloc[1]
    if date not in dates_without_games:
        group = df_grouped.get_group(date)
        for _, row in group.iterrows():
            challenger_id, opponent_id, winner = extract_player_info(row)
            challenger_elo = elo_df.iloc[current_index, player_ids.index(challenger_id)]
            opponent_elo = elo_df.iloc[current_index, player_ids.index(opponent_id)]
            challenger_elo_new, opponent_elo_new = compute_elo(elo_challenger=challenger_elo,
                                                               elo_opponent=opponent_elo,
                                                               winner=winner)
            elo_df.iloc[current_index, player_ids.index(challenger_id)] = challenger_elo_new
            elo_df.iloc[current_index, player_ids.index(opponent_id)] = opponent_elo_new

end = time.time()
print(f"Total time was {end-start} seconds.")


# %%
elo_df.to_csv("data/processed_data/elo.csv", header=True, index=False)


# %%

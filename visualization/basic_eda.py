# %%
import numpy as np
import pandas as pd
import itertools

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


# %%
data = pd.read_csv("bin/data/races.csv", sep=";")
data["race_created"] = pd.to_datetime(data["race_created"], dayfirst=True)


# %%
# TODO: IN CODE VON ARBEIT REIN SCHAUEN!!!
# TODO: WIEDERHOLEN FÜR: #SPIELE, #SPIELER, #SPIELE VS SPIELER_ID
df_plot = data.copy()
df_plot["amount"] = 1
df_grouped = pd.DataFrame(df_plot.groupby("race_created")["amount"].sum())
df_grouped.reset_index(inplace=True)
df_grouped["month"] = df_grouped["race_created"].dt.strftime("%b")
df_grouped["year"] = df_grouped["race_created"].dt.strftime("%y")
df_grouped["race_date"] = df_grouped["month"] + \
    " " + df_grouped["year"].astype("str")


# %%
# Number of games vs time per year
subplot_positions = list(itertools.product(range(3), range(2)))
played_years = df_grouped.year.unique()

fig, axes = plt.subplots(3, 2, figsize=(10, 10), sharey=True)

for played_year, pos in zip(played_years, subplot_positions):

    sns.boxplot(x="month", y="amount", data=df_grouped.loc[df_grouped.year==played_year], ax=axes[pos[0], pos[1]])
    axes[pos[0], pos[1]].set_title("Year 20" + str(played_year), fontsize=15)
    axes[pos[0], pos[1]].set_xlabel("")
    if pos[1] > 0:
        axes[pos[0], pos[1]].set_ylabel("")
    else:
        axes[pos[0], pos[1]].set_ylabel("Number of races", fontsize=13)
    plt.setp(axes[pos[0], pos[1]].get_xticklabels(), rotation=45)

plt.tight_layout()
plt.show()


# %%
# Investigate Ids of opponents and challengers
data.loc[data.opponent==data.challenger]
# apparently challenger and opponents are disjunct sets (cant play against yourself)


# %%
# We would expect continous numbers, but obviously some duds in there
# TODO: MAKE PLOT NICE
opponents = data.opponent.unique()
opponents.sort()
challengers = data.challenger.unique()
challengers.sort()

fig, axes = plt.subplots(1,2, figsize=(10, 10))

axes[0].plot(range(len(opponents)), opponents)
axes[1].plot(range(len(challengers)), challengers)

plt.show()


# %%
# investigate strange large opponents ids
print(data.loc[data.opponent.isin(opponents[-3:])].status.unique())
# apperently all not played anyway so we go ahead and drop the respective columns


# %%
# remove duds
data_cleaned = data.drop(data[data.opponent.isin(opponents[-3:])].index) 


# %%
# Plot cleaned data
opponents_cleaned = data_cleaned.opponent.unique()
opponents_cleaned.sort()
challengers_cleaned = data_cleaned.challenger.unique()
challengers_cleaned.sort()

fig, axes = plt.subplots(1,2, figsize=(10, 10))

axes[0].plot(range(len(opponents_cleaned)), opponents_cleaned)
axes[1].plot(range(len(challengers_cleaned)), challengers_cleaned)

plt.show()


# %%
# get all unique ids
unique_players = list(set(list(opponents_cleaned) + list(challengers_cleaned)))
# TODO: MAKE PLOT OUT OF THIS
print(f"Number of total online players: {len(unique_players)}.\n Number of total players: {unique_players[-1]}.")


# %%
df_plot = data.copy()
df_plot["amount"] = 1
df_grp_player = pd.DataFrame(data={"challenger": df_plot.groupby("challenger")["amount"].sum()})
df_grp_player["opponent"] = df_plot.groupby("opponent")["amount"].sum()
df_grp_player.index.names = ["player_id"]
df_grp_player.fillna(0, inplace=True)
df_grp_player["games_per_player"] = df_grp_player.sum(axis=1)
df_grp_player.reset_index(inplace=True)


# %%
# plots total games per id, games opponent, games challenger
# TODO: PLOT SCHÖN MACHEN!
plt.figure(figsize=(10, 10))

sns.lineplot(x="player_id", y="games_per_player", data=df_grp_player)
sns.lineplot(x="player_id", y="challenger", data=df_grp_player)
sns.lineplot(x="player_id", y="opponent", data=df_grp_player)
# plt.yscale("log")

plt.show()


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
# tack distribution
# TODO: PLOT SCHÖN MACHEN
plt.figure(figsize=(20, 10))

sns.barplot(x=df_plot["track_id"].unique(), y=df_plot["track_id"].value_counts())
plt.yscale("log")

plt.show()


# %%
# money distribution
# TODO: PLOT SCHÖN MACHEN
# TODO: CATEGORIES (die mit 5%)
plt.figure(figsize=(20, 10))

# sns.barplot(x=df_plot["money"].unique(), y=df_plot["money"].value_counts())
sns.distplot(df_plot["money"], kde=False)
plt.yscale("log")

plt.show()

# %%
# fuel consumption distribution
# TODO: PLOT SCHÖN MACHEN
# TODO: CATEGORIES (die mit 5%)
# TODO: CLEAN DATA!
plt.figure(figsize=(20, 10))

# sns.barplot(x=df_plot["fuel_consumption"].unique(), y=df_plot["fuel_consumption"].value_counts())
sns.boxplot(df_plot["fuel_consumption"], showfliers=False)
plt.yscale("log")

plt.show()


# %%
# 2D distplots ??
# TODO: do we want that in there?
sns.jointplot("track_id", "money", data=df_plot,
                  kind="kde", space=0, color="g")

# %%
# win/loose ratio
# count number of wins divide by number of games


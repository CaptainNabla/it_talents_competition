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

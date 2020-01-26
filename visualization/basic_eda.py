# %%
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


# %%
data = pd.read_csv("bin/data/races.csv", sep=";")
# data[["race_created", "race_driven"]] = data[["race_created", "race_driven"]].astype("datetime64")
data[["race_created"]] = data[["race_created"]].astype("datetime64")


# %%
df_plot = data.copy()
df_plot["amount"] = 1
df_plot["race_created_month"] = df_plot["race_created"].dt.strftime("%m")
df_plot["race_created_year"] = df_plot["race_created"].dt.strftime("%y")
# data_grouped = df_plot.groupby("race_created")
df_plot["race_created_minus_one"] = pd.to_datetime(df_plot["race_created"]) \
    - pd.to_timedelta(7, unit="d")
df_plot = df_plot.groupby(pd.Grouper(key="race_created_minus_one", freq="M"))["amount"] \
    .sum().reset_index().sort_values("race_created_minus_one")


# %%
plt.figure(figsize=(9, 7))
sns.boxplot(x="race_created_minus_one", y="amount", data=df_plot)
plt.yscale("log")
plt.show()

# %%

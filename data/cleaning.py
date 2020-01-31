# %%
import numpy as np
import pandas as pd
import datetime

from data.transformation import date_to_numeric

# %%
data = pd.read_csv("data/races.csv", sep=";")


# %%
# Replace str in fuel_consumption by correct floats
data["fuel_consumption"] = data["fuel_consumption"].apply(lambda x: date_to_numeric(x))

# %%
# Remove fake player_id
opponents = data.opponent.unique()
opponents.sort()
data = data.drop(data[data.opponent.isin(opponents[-3:])].index)


# %%
# Cast columns in correct format

# Date columns to international standard
data["race_created"] = pd.to_datetime(data["race_created"], dayfirst=True)

data.replace(to_replace="0000-00-00 00:00:00", value=np.nan, inplace=True)  # nonexisting = nans
data["race_driven"] = data["race_driven"].apply(
    lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M") if isinstance(x, str) else x)

# fuel_consumption
data["fuel_consumption"] = data["fuel_consumption"].astype("float")


# %%
# Save cleaned data
data.to_csv("data/cleaned_data/races_cleaned.csv", header=True, index=False)

# Save sample of cleaned data (first 100 rows)
data.loc[:100].to_csv("data/cleaned_data/sample_races_cleaned.csv", header=True, index=False)

# %%

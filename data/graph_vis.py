# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import networkx as nx

G = nx.Graph()

data = pd.read_csv("cleaned_data/races_cleaned.csv")
data.dropna(inplace=True)

#data['win_weight'] = [-1 for c, w in zip(data['challenger'], data['winner'])

data = data.head(500)

# %%

G = nx.DiGraph()
G.add_edges_from([(c, o) for c,o in zip(data.challenger, data.opponent)])

# val_map = {'A': 1.0,
#            'D': 0.5714285714285714,
#            'H': 0.0}

# values = [val_map.get(node, 0.25) for node in G.nodes()]

nx.draw(G, cmap = plt.get_cmap('jet'), node_color = "grey", with_labels=True)
plt.show()

# %%
data

# %%

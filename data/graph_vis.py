# %%
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import itertools
import networkx as nx
from networkx.algorithms import clique
from random import randint


def draw_graph(node_list, title):

    G = nx.DiGraph()
    G.add_edges_from(node_list)

    nx.draw(G,
            cmap=plt.get_cmap('jet'),
            node_color="lightgrey",
            with_labels=True)
    
    plt.title(title)
    plt.show()


data = pd.read_csv("data/cleaned_data/races_cleaned.csv")
data.dropna(inplace=True)
# %%

for _ in range(10):
    random_racer = data.challenger.values[randint(0, len(data)-1)]

    random_racer_df = data[(data['challenger'] == random_racer)
                        | (data['opponent'] == random_racer)]

    draw_graph([(a, b) for a, b in zip(random_racer_df.challenger,
                                       random_racer_df.opponent)], "")
# %%


# %%

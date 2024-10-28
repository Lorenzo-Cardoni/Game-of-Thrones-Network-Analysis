import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community as community_louvain
from netgraph import Graph

# Lista dei file CSV dei libri
file_list = ["dataset//book1.csv", "dataset//book2.csv", "dataset//book3.csv", "dataset//book4.csv", "dataset//book5.csv"]

# Leggiamo e uniamo i file CSV
df_list = [pd.read_csv(file) for file in file_list]

# Concatenare tutti i DataFrame in uno solo
df_combined = pd.concat(df_list, ignore_index=True)

# Verifica se ci sono valori duplicati
df_combined.drop_duplicates(inplace=True)

# Creiamo il grafo non orientato
G = nx.Graph()

# Aggiungiamo gli archi (relazioni) al grafo
for index, row in df_combined.iterrows():
    source = row['Source']
    target = row['Target']
    weight = row['weight']
    book = row['book']
    
    # Aggiungi gli archi con attributi 'weight' e 'book'
    G.add_edge(source, target, weight=weight, book=book)


# # alternatively, we can infer the best partition using Louvain:
node = 0
node_to_community = community_louvain.best_partition(G)

for community_id, size in enumerate(partition_sizes):
    for _ in range(size):
        node_to_community[node] = community_id
        node += 1

community_to_color = {
    0 : 'tab:blue',
    1 : 'tab:orange',
    2 : 'tab:green',
    3 : 'tab:red',
    4 : 'tab:purple',
    6 : 'tab:yellow',
    7 : 'tab: brown',
    8 : 'tab: pink',
    9 : 'tab: gray',
    10 : 'tab:olive',
    11 : 'tab:cyan'  
}
node_color = {node: community_to_color[community_id] for node, community_id in node_to_community.items()}

Graph(G,
      node_color=node_color, node_edge_width=0, edge_alpha=0.1,
      node_layout='community', node_layout_kwargs=dict(node_to_community=node_to_community),
      edge_layout='bundled', edge_layout_kwargs=dict(k=2000),
)

plt.show()
"""
Analisi delle ego_network tra Jon Snow e Tyrion
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Lista dei file CSV dei libri
file_list = ["dataset//book1.csv", "dataset//book2.csv", "dataset//book3.csv", "dataset//book4.csv", "dataset//book5.csv"]

# Leggiamo e uniamo i file CSV
df_list = [pd.read_csv(file) for file in file_list]
df_combined = pd.concat(df_list, ignore_index=True)
df_combined.drop_duplicates(inplace=True)  # Rimuovi duplicati

# Crea il grafo
G = nx.Graph()
for index, row in df_combined.iterrows():
    source = row['Source']
    target = row['Target']
    weight = row['weight']
    G.add_edge(source, target, weight=weight)

# Funzione per visualizzare una ego network
def plot_ego_network(graph, character_name, node_color='lightblue'):
    # Crea la ego network per il personaggio
    ego_net = nx.ego_graph(graph, character_name)
    
    # Visualizza la ego network
    plt.figure(figsize=(12, 6))
    pos = nx.fruchterman_reingold_layout(ego_net)  # Layout grafico
    node_sizes = [100 + 1000 * (ego_net.degree(node) / max(dict(ego_net.degree()).values())) for node in ego_net.nodes()]
    nx.draw_networkx_nodes(ego_net, pos, node_size=node_sizes, node_color=node_color, alpha=0.8)
    nx.draw_networkx_edges(ego_net, pos, alpha=0.5)
    nx.draw_networkx_labels(ego_net, pos, font_size=5, font_weight="bold")
    plt.title(f"Ego Network di {character_name}")
    plt.show()

# Visualizza le ego network per Jon Snow e Tyrion Lannister
plot_ego_network(G, "Jon-Snow", node_color='lightcoral')
plot_ego_network(G, "Tyrion-Lannister", node_color='lightgreen')

# Centralità di Jon e Tyron
degree_jon = G.degree("Jon-Snow")
degree_tyrion = G.degree("Tyrion-Lannister")
print(f"Degree di Jon Snow: {degree_jon}")
print(f"Degree di Tyrion Lannister: {degree_tyrion}")

# Centralità ponderata in base al peso dell'interazione
weighted_degree_jon = sum(attr['weight'] for _, _, attr in G.edges("Jon-Snow", data=True))
weighted_degree_tyrion = sum(attr['weight'] for _, _, attr in G.edges("Tyrion-Lannister", data=True))
print(f"Weighted Degree di Jon Snow: {weighted_degree_jon}")
print(f"Weighted Degree di Tyrion Lannister: {weighted_degree_tyrion}")

# Misura di quanto i vicini sono collegati tra di loro e quindi andiamo ad osservare quanto è connesso il gruppo attorno a loro
density_jon = nx.density(nx.ego_graph(G, "Jon-Snow"))
density_tyrion = nx.density(nx.ego_graph(G, "Tyrion-Lannister"))
print(f"Density di Jon Snow: {density_jon}")
print(f"Density di Tyrion Lannister: {density_tyrion}")




import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community as community_louvain


# Lista dei file CSV dei libri
file_list = ["dataset//book1.csv", "dataset//book2.csv", "dataset//book3.csv", "dataset//book4.csv", "dataset//book5.csv"]

# Leggiamo e uniamo i file CSV
df_list = [pd.read_csv(file) for file in file_list]

# Concatenare tutti i DataFrame in uno solo
df_combined = pd.concat(df_list, ignore_index=True)

# Verifica: Mostra le prime righe del DataFrame combinato
# print(df_combined.head())

#Verifica se ci sono valori duplicati
df_combined.drop_duplicates(inplace=True)

#Verifica se ci sono valori nulli
# print(df_combined.isnull().sum())

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

# Rilevazione delle comunità usando Louvain
partition = community_louvain.best_partition(G)

# Ogni comunità ha un ID nel dizionario partition
# partition è una mappatura: {nodo: ID_comunità}

# Stampare le comunità identificate
# for node, community in partition.items():
#    print(f"Personaggio: {node}, Famiglia o alleanza: {community}")

# Calcola la centralità di grado per identificare i personaggi principali
degree_centrality = nx.degree_centrality(G)

# Trova i personaggi principali in ogni comunità
for community_id in set(partition.values()):
    nodes_in_community = [node for node in partition if partition[node] == community_id]
    print(f"Dimensione della comunità {community_id}: "+ str(len(nodes_in_community)))
    centrality_in_community = {node: degree_centrality[node] for node in nodes_in_community}
    top_character = max(centrality_in_community, key=centrality_in_community.get)
    print(f"Persona più popolare della comunità {community_id}: {top_character}\n")

# Trova i collegamenti tra comunità
edges_between_communities = [
    (u, v) for u, v in G.edges() if partition[u] != partition[v]
]

# Calcola la centralità di intermediazione
betweenness = nx.betweenness_centrality(G)

# Trova i nodi con alta centralità di intermediazione che collegano comunità diverse
bridges = [node for node in G.nodes() if betweenness[node] > 0.085 and any(partition[neighbor] != partition[node] for neighbor in G.neighbors(node))]

print("Personaggi che fungono da ponte tra comunità:")
for bridge in bridges:
    print(f"{bridge} - Comunità {str(partition[bridge])} - Centralità di intermediazione: {betweenness[bridge]:.2f}")

# print("Collegamenti tra comunità (alleanze o conflitti):")
# for u, v in edges_between_communities:
#     print(f"{u} (famiglia {partition[u]}) - {v} (famiglia {partition[v]})")

# Assegna un colore diverso a ciascuna comunità
colors = [partition[node] for node in G.nodes()]

plt.figure(figsize=(12, 10))
pos = nx.fruchterman_reingold_layout(G, seed=42)  # Layout grafico per posizionare i nodi
nx.draw_networkx_nodes(G, pos, node_color=colors, cmap=plt.cm.rainbow, linewidths = 0.30, node_size=50)
nx.draw_networkx_edges(G, pos, alpha=0.3)
# Creazione della leggenda
unique_communities = set(partition.values())
colors_map = plt.cm.rainbow(np.linspace(0, 1, len(unique_communities)))

# Aggiungi la leggenda
for i, community in enumerate(unique_communities):
    plt.scatter([], [], color=colors_map[i], label=f'Comunità {community}', s=50)  # s è la dimensione della marker

plt.legend(title="Comunità", loc='upper right')
plt.title("Famiglie e Alleanze in Game of Thrones")
plt.axis('off')  # Nasconde gli assi
plt.show()


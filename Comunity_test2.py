import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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

# Rilevazione delle comunità usando Louvain
communities = nx.community.louvain_communities(G, seed=123)

# Stampa le comunità identificate
for i, community in enumerate(communities):
    print(f"Comunità {i}: {community}")

# Assegna un colore diverso a ciascuna comunità
color_map = {}
for i, community in enumerate(communities):
    for node in community:
        color_map[node] = i  # Assegna il colore della comunità al nodo

# Genera una mappa di colori
colors = [color_map[node] for node in G.nodes()]

plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)  # Layout grafico per posizionare i nodi
nx.draw_networkx_nodes(G, pos, node_color=colors, cmap=plt.cm.rainbow, node_size=100)
nx.draw_networkx_edges(G, pos, alpha=0.3)

# Creazione della leggenda
unique_communities = set(color_map.values())
colors_map = plt.cm.rainbow(np.linspace(0, 1, len(unique_communities)))

# Aggiungi la leggenda
for i, community in enumerate(unique_communities):
    plt.scatter([], [], color=colors_map[i], label=f'Comunità {community}', s=100)

plt.legend(title="Comunità", loc='upper right')
plt.title("Famiglie e Alleanze in Game of Thrones")
plt.axis('off')  # Nasconde gli assi
plt.show()

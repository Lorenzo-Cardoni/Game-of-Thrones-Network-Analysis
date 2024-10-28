import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
from pyvis.network import Network

# Funzione per trovare N-clan con una clique minima di 4 nodi
def find_n_clans(G, N):
    n_clans = []
    for clique in nx.find_cliques(G):
        # Considera solo le clique di almeno 4 nodi
        if len(clique) >= 15:
            # Crea sottografo della clique
            subgraph = G.subgraph(clique)
            # Verifica se la distanza massima tra ogni coppia di nodi è <= N
            if all(
                nx.shortest_path_length(subgraph, source=node1, target=node2) <= N
                for node1, node2 in combinations(subgraph.nodes(), 2)
            ):
                n_clans.append(clique)
    return n_clans

# Lettura e unione dei dati
file_list = ["dataset//book1.csv", "dataset//book2.csv", "dataset//book3.csv", "dataset//book4.csv", "dataset//book5.csv"]
df_list = [pd.read_csv(file) for file in file_list]
df_combined = pd.concat(df_list, ignore_index=True)
df_combined.drop_duplicates(inplace=True)

# Crea il grafo
G = nx.Graph()
for index, row in df_combined.iterrows():
    source = row['Source']
    target = row['Target']
    weight = row['weight']
    G.add_edge(source, target, weight=weight)

# Trova tutte le clique nel grafo
all_cliques = list(nx.find_cliques(G))


pos = nx.kamada_kawai_layout(G) 

# Trova la clique massima
max_clique = max(all_cliques, key=len)
subgraph = G.subgraph(max_clique)
plt.figure(figsize=(8, 8))
nx.draw(subgraph, pos = pos, with_labels=True, node_color='lightblue', node_size=100, font_size=10, font_weight='bold', edge_color='gray')
plt.title("Clique Massima")
plt.savefig('images//Clique Massima.jpg', format='jpg',bbox_inches='tight')
plt.show()

net = Network(notebook = True, width='1900px', height = "900px", bgcolor = '#222222', font_color = 'white')
net.from_nx(subgraph)
net.show("GoT_clique_max.html")

print(f"Massima clique trovata ({len(max_clique)} nodi): {max_clique}")

# Trova le clique di dimensione >= 4
large_cliques = [clique for clique in all_cliques if len(clique) >= 4]
print(f"\nClique di dimensione >= 4 trovate: {len(large_cliques)}")

# Stampa le clique più grandi
# print("Le Clique con almeno 12 nodi sono: ")
# for i, clique in enumerate(large_cliques, start=1):
#    if len(clique) >= 12:
#        print(f"Clique {i} ({len(clique)} nodi): {clique}")

# Analisi del numero di clique per dimensione
clique_sizes = [len(clique) for clique in all_cliques]
size_distribution = {size: clique_sizes.count(size) for size in set(clique_sizes)}

print("\nDistribuzione delle clique per dimensione:")
for size, count in sorted(size_distribution.items()):
    if size > 3:
        print(f"Clique di dimensione {size}: {count}")
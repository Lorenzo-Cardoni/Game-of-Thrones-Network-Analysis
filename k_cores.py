"""
k_cores.py fornisce una analisi del grafo tramite k_Core
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

# Creazione del grafo
G = nx.Graph()
for index, row in df_combined.iterrows():
    source = row['Source']
    target = row['Target']
    weight = row['weight']
    G.add_edge(source, target, weight=weight)

# Calcolo del core_number per ciascun nodo
core_numbers = nx.core_number(G)

# Identificazione del core massimo
max_k = max(core_numbers.values())
print(f"K-core massimo nel grafo: {max_k}")

k_core = nx.k_core(G, k=13)

pos = nx.kamada_kawai_layout(G) 

plt.figure(figsize=(15, 7))
nx.draw_networkx_nodes(k_core, pos, node_size=100, node_color='lightblue')
nx.draw_networkx_edges(k_core, pos, alpha=0.3)
nx.draw_networkx_labels(k_core, pos, font_size=8, font_weight="bold")
plt.title("k-core del Grafo (Personaggi con almeno grado 13)")
plt.savefig('images//kcore_Massimo.jpg', format='jpg',bbox_inches='tight')
plt.show()
"""
# Visualizzazione dei core per valori di k
for k in range(1, max_k + 1):
    k_core = nx.k_core(G, k=k)
    print(f"\nNumero di nodi nel {k}-core: {len(k_core)}")

    # Visualizzazione grafica del k-core
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(k_core, seed=42)
    node_sizes = [300 + 100 * core_numbers[node] for node in k_core.nodes()]  # Scala le dimensioni in base al core_number
    nx.draw_networkx_nodes(k_core, pos, node_size=node_sizes, node_color=[core_numbers[node] for node in k_core.nodes()], cmap=plt.cm.viridis)
    nx.draw_networkx_edges(k_core, pos, alpha=0.3)
    nx.draw_networkx_labels(k_core, pos, font_size=8, font_weight="bold")
    plt.title(f"{k}-core del Grafo (Personaggi con almeno grado {k})")
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), label="Core Number")
    plt.show()
"""

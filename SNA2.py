import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network
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



# Verifica: Mostra alcune informazioni del grafo
# print(G.edges(data=True))
    
# Disegna il grafo con i nomi dei nodi
plt.figure(figsize=(8,6))

"""
Layout del grafo
altri layout:
- circular_layout
- spectral_layout
- shell_layout
- fruchterman_reingold_layout
- kamada_kawai_layout
"""
pos = nx.kamada_kawai_layout(G)  
# Disegnare nodi e archi
nx.draw(G, pos, with_labels=True, node_color="blue", edge_color="black", node_size=50, font_size=4, font_weight="bold")
# Mostra il grafo
plt.show()

net = Network(notebook = True, width='1900px', height = "900px", bgcolor = '#222222', font_color = 'white')

node_degree = dict(G.degree)

nx.set_node_attributes(G, node_degree, 'size')

net.from_nx(G)
net.show("GoT.html")

# Rilevazione delle comunità usando Louvain
partition = community_louvain.best_partition(G)

nx.set_node_attributes(G, partition, 'group')
net = Network(notebook = True, width='1900px', height = "900px", bgcolor = '#222222', font_color = 'white')
net.from_nx(G)
net.show("GoT_community.html")
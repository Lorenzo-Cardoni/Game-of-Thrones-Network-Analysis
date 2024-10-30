"""
Top 10 triadi con più peso del grafo 
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Lista dei file CSV dei libri
file_list = ["dataset//book1.csv", "dataset//book2.csv", "dataset//book3.csv", "dataset//book4.csv", "dataset//book5.csv"]

# Leggiamo e uniamo i file CSV
df_list = [pd.read_csv(file) for file in file_list]

# Concatenare tutti i DataFrame in uno solo
df_combined = pd.concat(df_list, ignore_index=True)

# Rimuovi duplicati
df_combined.drop_duplicates(inplace=True)

# Crea il grafo
G = nx.Graph()

# Aggiungi gli archi con attributo 'weight'
for index, row in df_combined.iterrows():
    source = row['Source']
    target = row['Target']
    weight = row['weight']
    G.add_edge(source, target, weight=weight)

# Trova tutte le triadi nel grafo (triangoli)
triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]

# Calcola il peso di ciascuna triade
triad_weights = []
for triad in triangles:
    u, v, w = triad  # nodi della triade
    # Somma dei pesi degli archi della triade
    weight_sum = (
        G[u][v]['weight'] +
        G[u][w]['weight'] +
        G[v][w]['weight']
    )
    triad_weights.append((triad, weight_sum))

# Ordina le triadi per peso decrescente e seleziona le prime 10
top_10_triad_weights = sorted(triad_weights, key=lambda x: x[1], reverse=True)[:10]

# Stampa le 10 triadi con peso maggiore
print("Top 10 triadi con peso maggiore:")
with open('triadi.txt', 'w') as f:
    f.write("Le triadi piu' forti in GoT:\n\n")
    for i, (triad, weight_sum) in enumerate(top_10_triad_weights, start=1):
        f.write(f"{i}. Triade {triad} - Peso Totale: {weight_sum}\n")
        print(f"{i}. Triade {triad} - Peso Totale: {weight_sum}")

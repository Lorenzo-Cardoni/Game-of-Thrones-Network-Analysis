"""
centrality.py fornisce le misure di centralità del grafo
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Lista dei file CSV dei libri
file_list = ["..//dataset//book1.csv", "..//dataset//book2.csv", "..//dataset//book3.csv", "..//dataset//book4.csv", "..//dataset//book5.csv"]

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


"""
# Distribuzione peso delle relazioni

# Estrai i pesi degli archi
weights = [G[u][v]['weight'] for u, v in G.edges()]

# Calcola le frequenze dei pesi
weight_counts = pd.Series(weights).value_counts().sort_index()

# Crea il grafico a barre della distribuzione dei pesi

plt.figure(figsize=(10, 6))
weight_counts.plot(kind='bar', color='blue', edgecolor='black')
plt.title('Distribuzione dei Pesi degli Archi (in ordine crescente)')
plt.xlabel('Peso degli Archi')
plt.ylabel('Frequenza')
plt.xticks(rotation=0)  # Ruota le etichette dell'asse x per una migliore leggibilità
plt.grid(axis='y', alpha=0.75)
plt.savefig('images//hist_weight_edges.jpg', format='jpg',bbox_inches='tight')
plt.show()
"""
# Misure di centralità

# Funzione per salvare i migliori nodi in base alla centralità
def save_top_centrality(G, centrality_dict, title, top_n=10, cmap="viridis"):
    """
    Salva i migliori nodi per centralità su un file di testo.

    Args:
    centrality_dict (dict): Dizionario con i nodi e la loro centralità.
    filename (str): Nome del file dove salvare i risultati.
    top_n (int): Numero di nodi da salvare (default 10).
    """
    # Ordinare i nodi in base alla centralità (dal più alto al più basso)
    sorted_centrality = sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
    

    # HEAT MAP
    pos = nx.spring_layout(G) 
    # Creare un array con i valori di centralità per colorare i nodi
    centrality_values = np.array(list(centrality_dict.values()))
    
    # Normalizzare i valori di centralità per la colorazione
    norm = plt.Normalize(vmin=min(centrality_values), vmax=max(centrality_values))
    colors = plt.cm.get_cmap(cmap)(norm(centrality_values))

    # Disegnare il grafo
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=50, font_size=4, font_weight='bold', edge_color='gray', cmap=cmap)
    
    # Aggiungere una colorbar per visualizzare la scala dei valori di centralità
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, label=f"Valore di {title}")
    
    plt.title(f"Heatmap dei Nodi per {title}")
    plt.savefig(f'..//images//{title}_heatmap.jpg', format='jpg',bbox_inches='tight')
    plt.show()


    # TOP 10 NODI
    centrality_dict = pd.DataFrame.from_dict(centrality_dict, orient = 'index', columns=['centrality'])
    # Plot top 10 nodes
    centrality_dict.sort_values('centrality', ascending = False)[0:9].plot(kind="bar",figsize=(15, 7), title=f"Top 10 Nodi per {title}")
    plt.xticks(rotation=0)  # Ruota le etichette dell'asse x per una migliore leggibilità
    plt.savefig(f'..//images//{title}_hist.jpg', format='jpg',bbox_inches='tight')

    """
    # Prendere i migliori top_n nodi
    top_nodes = [node for node, _ in sorted_centrality]

    # Estrarre il sotto-grafo contenente solo i migliori nodi
    subgraph = G.subgraph(top_nodes)
    # Creare un array con i valori di centralità per colorare i nodi
    centrality_values = [centrality_dict[node] for node in top_nodes]
    
    # Normalizzare i valori di centralità per la colorazione
    norm = plt.Normalize(vmin=min(centrality_values), vmax=max(centrality_values))
    colors = plt.cm.rainbow(norm(centrality_values))  # Usare la mappa rainbow per i colori

    # Disegnare il grafo
    plt.figure(figsize=(8, 8))
    nx.draw(subgraph, pos, with_labels=True, node_color=colors, node_size=50, font_size=10, font_weight='bold', edge_color='gray')
    plt.title(title)
    plt.savefig('images//'+ title + '.jpg', format='jpg',bbox_inches='tight')
    plt.show()
    """

# degree centrality
degree_centrality = nx.degree_centrality(G)
save_top_centrality(G, degree_centrality, "degree_centrality")

# betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)
save_top_centrality(G, betweenness_centrality, "betweenness_centrality")

# closeness centrality
closeness_centrality = nx.closeness_centrality(G)
save_top_centrality(G, closeness_centrality, "closeness_centrality")

# eigenvector centrality
eigenvector_centrality = nx.eigenvector_centrality(G)
save_top_centrality(G, eigenvector_centrality, "eigenvector_centrality")

# Calcolare il PageRank
pagerank = nx.pagerank(G)
# Visualizzare il grafo con colori in base ai valori di PageRank
save_top_centrality(G, pagerank, "PageRank", cmap="plasma")
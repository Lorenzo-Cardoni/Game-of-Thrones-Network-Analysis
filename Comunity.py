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

def plot_community_graph(G):
    # Step 1: Detect communities
    partition = community_louvain.best_partition(G)
    
    # Step 2: Create a color map for the communities
    communities = set(partition.values())
    print(communities)
    color_map = {community: plt.cm.rainbow(i / len(communities)) for i, community in enumerate(communities)}

    # Step 3: Create a layout that clusters nodes by community
    pos = nx.spring_layout(G, seed=42)  # spring layout with fixed seed for reproducibility

    # Step 4: Draw nodes and edges, coloring by community
    plt.figure(figsize=(10, 8))
    for community in communities:
        # Select nodes belonging to this community
        nodes_in_community = [node for node in partition if partition[node] == community]
        
        # Draw nodes and edges within this community
        nx.draw_networkx_nodes(G, pos, nodelist=nodes_in_community, node_color=[color_map[community]], node_size=50)
    
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=0)

    plt.title("Community Detection Visualization")
    plt.show()


plot_community_graph(G)
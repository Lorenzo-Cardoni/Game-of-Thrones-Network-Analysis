"""
Analisi descrittiva generale del grafo

"""
import pandas as pd
import networkx as nx

# Lista dei file CSV dei libri
file_list = ["..//dataset//book1.csv", "..//dataset//book2.csv", "..//dataset//book3.csv", "..//dataset//book4.csv", "..//dataset//book5.csv"]

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

# Numero totale di personaggi (nodi) e connessioni (archi)
total_nodes = G.number_of_nodes()
total_edges = G.number_of_edges()

# Calcolo del weighted degree per ogni nodo
weighted_degree = {node: sum(attr['weight'] for _, _, attr in G.edges(node, data=True)) for node in G.nodes()}
# Ordina i personaggi per weighted degree e seleziona i primi 10
top_10_characters = sorted(weighted_degree.items(), key=lambda x: x[1], reverse=True)[:10]

# Stampa i risultati
print(f"Numero totale di personaggi: {total_nodes}")
print(f"Numero totale di connessioni: {total_edges}")
print("\nI 10 personaggi con maggior peso delle connessioni:")
for character, weight in top_10_characters:
    print(f"{character}: {weight}")

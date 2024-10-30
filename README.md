# Game of Thrones Network Analysis

Questo progetto applica metodi di analisi delle reti sociali a un dataset di interazioni tra i personaggi di *Game of Thrones*, utilizzando metriche di centralità e algoritmi di rilevamento delle comunità per estrarre informazioni chiave sui personaggi principali e le dinamiche sociali della serie.

## Descrizione

L'obiettivo del progetto è analizzare la struttura della rete dei personaggi di *Game of Thrones* e identificare nodi influenti, gruppi sociali e comunità principali. Utilizziamo diverse misure di centralità e visualizziamo i risultati tramite grafici interattivi, con un'attenzione particolare ai seguenti elementi:

- **Degree Centrality**: misura la popolarità di ogni personaggio.
- **Betweenness Centrality**: identifica i nodi che fungono da "ponti" nella rete.
- **Closeness Centrality**: valuta la vicinanza di un personaggio agli altri.
- **Eigenvector Centrality**: misura l'influenza di un personaggio in base all'importanza dei suoi vicini.
- **PageRank**: identifica i personaggi a cui si può accedere con maggiore probabilità durante la navigazione della rete.
- **Comunità (Louvain Algorithm)**: rilevamento di gruppi sociali (famiglie, fazioni) tra i personaggi.

## Requisiti

### Librerie Necessarie

Le librerie utilizzate per il progetto sono elencate nel file `requirements.txt`. Per lo studio del grafo si è utilizzato l'ambiente Anaconda. Per installarle tutte in una volta, usa il seguente comando:

```bash
conda create --name <env> --file requirements.txt
```
## Risultati
Per osservare i risultati consultare il file pdf `Progetto_Graph.pdf`

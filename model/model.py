import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n # assegna nel dizionario l'id con l'art object
        self._optPath = []
        self._optCost = 0


    def buildGraph(self):
        self._graph.add_nodes_from(self._nodes)
        self.addEdgesV2()


    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)
                    print(f"Aggiunto arco fra {u} e {v} con peso {peso}")


    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)


    def getInfoCompConnessa(self, id_ogetto):
        # cercare la componente connessa che contiene l'id oggetto
        if not self.hasNodes(id_ogetto):
            return None
        source = self._idMapAO[id_ogetto]

        # posso fare una ricerca di tipo dfs e contare i nodi dell'albero trovato
        dfsTree = nx.dfs_tree(self._graph, source) # mi dà un albero
        print("size connessa con dfs_tree", len(dfsTree.nodes()))

        # posso usare una strategia depth first dove prendo i prdecessori
        dfsPred = nx.dfs_predecessors(self._graph, source) # mi dà un dizionario
        print("size connessa con dfs_predecessors", len(dfsPred.values()))

        # (strategia migliore) posso usare i metodi appositi della libreria
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con node_connected_components", len(conn))

        # mi verrà lo stesso numero per il primo e il terzo e uno in meno per il secondo perchè i predecessori
        # non contengono l'ultimo nodo

        return len(conn)


    def getOptPath(self, source, lun):
        parziale = [source]
        for n in self._graph.neighbors(source): # ciclo sui vicini di source
            # capisco se ognuno di questi vicini posso aggiungerlo o no
            if n.classification == parziale[-1].classification: # se la classificazione del nodo che voglio a
            # ggiungere è la stessa dell'ultimo nodo che ho aggiunto
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop() # riporto lo stato del vettore parziale a com'era
        return self._optPath, self._optCost


    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # verifico che questa parziale sia meglio del mio best, in ogni caso esco
            if self._costoPath(parziale) > self._optCost:
                self._optCost = self._costoPath(parziale)
                self._optPath = copy.deepcopy(parziale)
            return

        else:
            for n in self._graph.neighbors(parziale[-1]):
                if parziale[-1].classification == n.classification:
                    parziale.append(n)
                    self._ricorsione(parziale, lun)
                    parziale.pop()


    def _costoPath(self, path):
        costo = 0
        for i in range(0, len(path) - 1): # cicla su tutti gli archi e somma i valori del peso
            costo += self._graph[path[i]][path[i + 1]]["weight"]

        return costo


    def getNodeFromId(self, id_oggetto):
        return self._idMapAO[id_oggetto]


    def hasNodes(self, id_oggetto):
        return id_oggetto in self._idMapAO # se l'id è nell'id map mi dà true, se no false


    def getNumNodes(self):
        return len(self._graph.nodes)


    def getNumEdges(self):
        return len(self._graph.edges)


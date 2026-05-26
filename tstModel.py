from model.model import Model

mod = Model()
mod.buildGraph()
print(f"Il grafo creato contiene {mod.getNumNodes()} nodi e {mod.getNumEdges()} archi")

mod.getInfoCompConnessa(1224)
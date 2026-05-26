import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e "
                                                      f"{self._model.getNumEdges()} archi"))
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()


    def handleCompConnessa(self,e):
        txtIdOggetto = self._view._txtIdOggetto.value
        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore nel campo id",
                                                          color = "red"))
            self._view.update_page()
            return

        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un valore numerico nel campo id",
                        color = "red"))
            self._view.update_page()
            return

        if not self._model.hasNodes(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, il valore inserito non è nel grafo",
                        color = "red"))
            self._view.update_page()
            return

        sizeCompConnessa = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {idOggetto} "
                    f"è composta di {sizeCompConnessa} nodi",
                    color="green"))


        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        lunValues = list(range(2, sizeCompConnessa))
        # for v in lunValues:
        #     self._view._ddLun.options.append(ft.dropdown.Option(v))

        lunValuesDD = list(map(lambda x: ft.dropdown.Option(x), lunValues)) # passando una lista e una funzione mi dà una nuova
        # lista in cui c'è un elemento della lista vecchia con una funzione applicata
        self._view._ddLun.options = lunValuesDD

        self._view.update_page()


    def handleCerca(self, e):
        source = self._model.getNodeFromId(int(self._view._txtIdOggetto.value))
        lun = self._view._ddLun.value

        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un valore di lunghezza tra le scelte proposte"),
                color="red")
            self._view.update_page()
            return

        lunInt = int(lun)
        path, cost = self._model.getOptPath(source, lunInt)
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un cammino che parte da {source} e ha un peso totale pari a {cost}",
            color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i nodi che compongono questo cammino: "))

        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()

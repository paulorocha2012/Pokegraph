from collections import deque


# BFS para o menor caminho

def BFS(grafo, inicio, fim):
    fila = deque([[inicio]])
    visitado = set()

    while fila:
        caminho = fila.popleft()
        nodo = caminho[-1]

        if nodo == fim:
            return caminho  # achou o caminho mais curto

        if nodo not in visitado:
            visitado.add(nodo)
            for viz in grafo[nodo]:
                novo_caminho = list(caminho)
                novo_caminho.append(viz)
                fila.append(novo_caminho)

    return None  # nenhum caminho

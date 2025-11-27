import tkinter as tk
import tkinter.messagebox as messagebox
import math
from collections import deque
from PIL import Image, ImageTk 

# Grafo DIRECIONADO
graph = {
    "Fogo": ["Planta", "Aço"],
    "Planta": ["Água", "Elétrico"],
    "Água": ["Fogo"],
    "Elétrico": ["Voador", "Água"],
    "Voador": ["Planta"],
    "Fantasma": [],
    "Aço": []
}


# Posições dos nós
positions = {
    "Fogo": (300, 100),
    "Planta": (300, 250),
    "Água": (150, 400),
    "Elétrico": (450, 400),
    "Voador": (450, 200),
    "Fantasma":(550, 300),
    "Aço": (150, 200)
}

player_node = "Fogo"  # nó inicial do jogador
NODE_RADIUS = 45   # Raio do círculo
IMG_SIZE = 60      # Tamanho do PNG final (em pixels)
player_node = "Fogo"     # onde o jogador está AGORA
start_node  = "Fogo"     # início do jogo
end_node    = "Água"     # objetivo final
player_path = [player_node] # caminho percorrido pelo jogador

# Verifica o estado do jogo após cada movimento
def check_game_state():
    if player_node == end_node:
        menor = BFS(graph, start_node, end_node)

        if player_path == menor:
            messagebox.showinfo("Vitória", 
                f"Você chegou ao destino!\nCaminho perfeito: {player_path}")
        else:
            messagebox.showinfo("Vitória",
                f"Você chegou ao destino!\n"
                f"Seu caminho: {player_path}\n"
                f"Melhor caminho: {menor}")

        root.destroy()
        return

    if len(graph[player_node]) == 0:
        messagebox.showerror("Game Over", "Você ficou preso!")
        root.destroy()
        return
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



# carrega imagens PNG e redimensiona
def load_images():
    images = {}
    for node in graph.keys():
        try:
            img = Image.open(f"{node}.png")   # abre qualquer PNG
            img = img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
            images[node] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"ERRO ao carregar {node}.png → {e}")
    return images


# Desenhar grafo
def draw_graph(canvas, images):
    canvas.delete("all")

    # Arestas direcionadas 
    for node, neighbours in graph.items():
        x1, y1 = positions[node]

        for nb in neighbours:
            x2, y2 = positions[nb]

            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)

            if dist == 0:
                continue  

            ux = dx / dist
            uy = dy / dist

            start_x = x1 + ux * NODE_RADIUS
            start_y = y1 + uy * NODE_RADIUS
            end_x   = x2 - ux * NODE_RADIUS
            end_y   = y2 - uy * NODE_RADIUS

            canvas.create_line(
                start_x, start_y, end_x, end_y,
                width=3,
                fill="#555",
                arrow=tk.LAST,
                arrowshape=(20, 25, 10)
            )

    # --- Nós circulares com PNG dentro ---
    for node, (x, y) in positions.items():

        if node == player_node:
            fill = "#ffdb4d"  
        else:
            fill = "#88ccff"  

        canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS,
            x + NODE_RADIUS, y + NODE_RADIUS,
            fill=fill, outline="black", width=3
        )

        canvas.create_image(x, y, image=images[node])


# Clique para mover
def on_click(event, images):
    global player_node
    x, y = event.x, event.y

    for node, (nx, ny) in positions.items():
        if math.dist((x, y), (nx, ny)) <= NODE_RADIUS:
            if node in graph[player_node]:
                player_node = node
                player_path.append(player_node)
                draw_graph(canvas, images)
                check_game_state()   
            return


# Janela principal
root = tk.Tk()
root.title("Pokegraph")

canvas = tk.Canvas(root, width=650, height=550, bg="white")
canvas.pack()

images = load_images()  # carrega e redimensiona PNGs com PIL

canvas.bind("<Button-1>", lambda e: on_click(e, images))

draw_graph(canvas, images)

root.mainloop()

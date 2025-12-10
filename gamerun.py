import os
import tkinter as tk
import tkinter.messagebox as messagebox
import math
from collections import deque
from images.loadimage import load_images
from algorithm import BFS



# Grafo DIRECIONADO
graph = {
    "Fogo": ["Planta", "Aço", "Gelo", "Inseto"],
    "Planta": ["Água", "Pedra", "Terrestre"],
    "Água": ["Fogo", "Pedra", "Terrestre"],
    "Elétrico": ["Voador", "Água"],
    "Aço": ["Fada", "Gelo", "Pedra"],
    "Dragão": ["Dragão"],
    "Fada": ["Dragão", "Lutador", "Sombrio"],
    "Fantasma": ["Fantasma", "Psíquico"],
    "Gelo": ["Dragão","Planta", "Terrestre", "Voador"],
    "Inseto": ["Planta", "Psíquico", "Sombrio"],
    "Lutador": ["Aço", "Gelo", "Normal", "Pedra", "Sombrio"],
    "Normal": [],
    "Pedra": ["Fogo", "Gelo", "Inseto", "Voador"],
    "Psíquico": ["Lutador", "Venenoso"],
    "Sombrio": ["Fantasma", "Psíquico"],
    "Terrestre": ["Aço", "Elétrico", "Fogo", "Pedra", "Venenoso"],
    "Venenoso": ["Fada", "Planta"],
    "Voador": ["Planta", "Lutador", "Inseto"]
}


# Posições dos nós
positions = {
    # --- Seus nós originais (Mantidos ou levemente ajustados) ---
    "Fogo": (300, 100),      # Topo Centro
    "Planta": (300, 250),    # Centro (O coração do grafo)
    "Água": (150, 400),      # Inferior Esquerdo
    "Elétrico": (450, 400),  # Inferior Direito
    "Voador": (450, 200),    # Superior Direito
    "Aço": (150, 200),       # Superior Esquerdo
    "Fantasma": (550, 300),  # Extremo Direito

    # --- Novos nós (Preenchendo as lacunas) ---
    
    # Camada Superior (Acima/Ao lado de Fogo)
    "Gelo": (225, 80),       # Entre Aço e Fogo, mais acima
    "Dragão": (375, 80),     # Entre Voador e Fogo, mais acima
    
    # Camada Inferior (Abaixo de Água/Elétrico)
    "Terrestre": (300, 500), # Base central
    "Pedra": (200, 480),     # Base esquerda
    "Lutador": (400, 480),   # Base direita
    
    # Laterais (Expandindo a largura)
    "Sombrio": (50, 300),    # Extremo Esquerdo (Oposto ao Fantasma)
    "Fada": (520, 130),      # Canto Superior Direito (Perto de Dragão/Voador)
    "Venenoso": (80, 130),   # Canto Superior Esquerdo (Perto de Aço)
    "Psíquico": (520, 450),  # Canto Inferior Direito
    
    # Camada Interna (Ao redor de Planta)
    "Inseto": (200, 320),    # Esquerda de Planta
    "Normal": (400, 320),    # Direita de Planta
}

player_node = "Fogo"  # nó inicial do jogador
NODE_RADIUS = 45   # Raio do círculo
      # Tamanho do PNG final (em pixels)
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
    
    if len(graph[player_node]) == 0 or (player_node == graph[player_node] and len(graph[player_node] == 1)):
        messagebox.showerror("Game Over", "Você ficou preso!")
        root.destroy()
        return
    



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


def start_pan(event):
    canvas.scan_mark(event.x, event.y)

def move_pan(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

altura_base = 600
largura_base = 600

nova_altura = 1200 
nova_largura = 800

f_x = nova_largura / largura_base
f_y = nova_altura / altura_base

#redimensiona para as arestas não ficarem coladas umas nas outras

for node, (x, y) in positions.items():
    positions[node] = (int(x * f_x), int(y * f_y))

# Janela principal
root = tk.Tk()
root.title("Pokegraph")
root.geometry(f"{nova_largura}x{nova_altura}")
load_images(graph)

canvas = tk.Canvas(root, width=nova_largura, height=nova_altura, bg="white")
canvas.pack(fill="both", expand=True)

canvas.config(scrollregion =(0, 0, nova_largura, nova_altura))

images = load_images(graph)  # carrega e redimensiona PNGs com PIL

canvas.bind("<Button-1>", lambda e: on_click(e, images))

canvas.bind("<ButtonPress-3>", start_pan)
canvas.bind("<B3-Motion>", move_pan)

draw_graph(canvas, images)

root.mainloop()

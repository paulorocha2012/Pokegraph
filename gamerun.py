import os
import tkinter as tk
from tkinter import ttk
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

# para ajudar a diferenciar
TYPE_COLORS = {
    "Fogo": "#F08030",      "Água": "#6890F0",    "Planta": "#78C850",
    "Elétrico": "#F8D030",  "Gelo": "#98D8D8",    "Lutador": "#C22E28",
    "Venenoso": "#A040A0",  "Terrestre": "#E0C068","Voador": "#A890F0",
    "Psíquico": "#F85888",  "Inseto": "#A8B820",  "Pedra": "#B8A038",
    "Fantasma": "#705898",  "Dragão": "#7038F8",  "Aço": "#B8B8D0",
    "Fada": "#EE99AC",      "Normal": "#A8A878",  "Sombrio": "#705848"
}

# posições dos nós
positions = {
    "Fogo": (300, 100),      # topo Centro
    "Planta": (300, 250),    # centro (O coração do grafo)
    "Água": (150, 400),      # inferior Esquerdo
    "Elétrico": (450, 400),  # inferior Direito
    "Voador": (450, 200),    # superior Direito
    "Aço": (150, 200),       # superior Esquerdo
    "Fantasma": (550, 300),  # extremo Direito
    
    # camada Superior (Acima/Ao lado de Fogo)
    "Gelo": (225, 80),       # entre Aço e Fogo, mais acima
    "Dragão": (375, 80),     # entre Voador e Fogo, mais acima
    
    # camada Inferior (Abaixo de Água/Elétrico)
    "Terrestre": (300, 500), # base central
    "Pedra": (200, 480),     # base esquerda
    "Lutador": (400, 480),   # base direita
    
    # laterais (Expandindo a largura)
    "Sombrio": (50, 300),    # extremo Esquerdo (Oposto ao Fantasma)
    "Fada": (520, 130),      # canto Superior Direito (Perto de Dragão/Voador)
    "Venenoso": (80, 130),   # canto Superior Esquerdo (Perto de Aço)
    "Psíquico": (520, 450),  # canto Inferior Direito
    
    # camada Interna (Ao redor de Planta)
    "Inseto": (200, 320),    # esquerda de Planta
    "Normal": (400, 320),    # direita de Planta
}
#tamanho da janela
LARGURA_VIRTUAL = 1800
ALTURA_VIRTUAL = 1200
#redimensionamento da janela
fator_x = LARGURA_VIRTUAL / 650
fator_y = ALTURA_VIRTUAL / 550

for node, (x, y) in positions.items():
    # Centraliza um pouco mais somando margens
    positions[node] = (int(x * fator_x) + 50, int(y * fator_y) + 50)


player_node = ""     # onde o jogador está AGORA
start_node  = ""     # início do jogo
end_node    = ""     # fim do jogo
player_path = []     # caminho percorrido pelo jogador


def configurar_jogo():
    global start_node, end_node, player_node, player_path
    
    # janela temporária
    launcher = tk.Tk()
    launcher.title("Configuração da Partida")
    launcher.geometry("300x250")
    launcher.eval('tk::PlaceWindow . center')
    tk.Label(launcher, text="POKEGRAPH", font=("Arial", 16, "bold")).pack(pady=10)

    opcoes = sorted(list(graph.keys()))
    tk.Label(launcher, text="Onde você começa?").pack()
    combo_start = ttk.Combobox(launcher, values=opcoes, state="readonly")
    combo_start.pack(pady=5)
    tk.Label(launcher, text="Para onde você vai?").pack()
    combo_end = ttk.Combobox(launcher, values=opcoes, state="readonly")
    combo_end.pack(pady=5)

    def confirmar():
        global start_node, end_node, player_node, player_path
        start = combo_start.get()
        end = combo_end.get()
        
        if start == end:
            messagebox.showwarning("Ops", "O início e o fim não podem ser iguais!")
            return

        start_node = start
        player_node = start
        end_node = end
        player_path = [start_node]
        
        launcher.destroy() # fecha o launcher e deixa o código seguir

    tk.Button(launcher, text="INICIAR JOGO", bg="#4CAF50", fg="white", 
              font=("Arial", 10, "bold"), command=confirmar).pack(pady=20)

    launcher.mainloop()


NODE_RADIUS = 45   # Raio do círculo
      # Tamanho do PNG final (em pixels)

# verifica o estado do jogo após cada movimento
def check_game_state():
    if player_node == end_node:
        menor = BFS(graph, start_node, end_node)

        if player_path == menor or len(player_path) == len(menor):
            messagebox.showinfo("Vitória", 
                f"Você chegou ao destino!\nCaminho perfeito: {player_path}")
        else:
            messagebox.showinfo("Vitória",
                f"Você chegou ao destino!\n"
                f"Seu caminho: {player_path}\n"
                f"Melhor caminho: {menor}")

        root.destroy()
        return
    
    vizinhos = graph[player_node]
    sem_saida = (len(vizinhos) == 0)
    so_tem_ele_mesmo = (len(vizinhos) == 1 and vizinhos[0] == player_node)

    if sem_saida or so_tem_ele_mesmo:       
        messagebox.showerror("Game Over", "Você ficou preso!")
        root.destroy()
        return
    


def atualizar_sidebar():
    listbox_path.delete(0, tk.END)
    
    for i, passo in enumerate(player_path):
        texto = f"{i}. {passo}"
        listbox_path.insert(tk.END, texto)
        
        if i == len(player_path) - 1:
            listbox_path.itemconfig(tk.END, {'bg':'#ffdb4d'})
    listbox_path.see(tk.END)


# Desenhar grafo
def draw_graph(canvas, images):
    canvas.delete("all")
    
    # --- 1. FUNDO SUAVE ---
    canvas.create_rectangle(0, 0, LARGURA_VIRTUAL, ALTURA_VIRTUAL, fill="#f4f4f9", outline="")
    
    for i in range(0, LARGURA_VIRTUAL, 200):
        canvas.create_line(i, 0, i, ALTURA_VIRTUAL, fill="#e0e0eb", width=1)
    for i in range(0, ALTURA_VIRTUAL, 200):
        canvas.create_line(0, i, LARGURA_VIRTUAL, i, fill="#e0e0eb", width=1)

    # --- 2. ARESTAS (LINHAS) ---
    for node, neighbours in graph.items():
        if node not in positions: continue
        x1, y1 = positions[node]
        
        cor_origem = TYPE_COLORS.get(node, "#888888")

        for nb in neighbours:
            if nb not in positions: continue
            x2, y2 = positions[nb]
            
            dx, dy = x2 - x1, y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)
            if dist == 0: continue
            
            ux, uy = dx/dist, dy/dist
            
            offset_radius = NODE_RADIUS + 5
            
            canvas.create_line(
                x1 + ux*offset_radius, y1 + uy*offset_radius,
                x2 - ux*offset_radius, y2 - uy*offset_radius,
                width=3, 
                fill=cor_origem, 
                arrow=tk.LAST, 
                arrowshape=(18, 20, 6)
            )

    # --- 3. NÓS (SOMBRA + COR + DESTAQUE) ---
    for node, (x, y) in positions.items():
        
        cor_base = TYPE_COLORS.get(node, "#cccccc")
        
        if node == player_node:
            cor_borda = "#FF0000" # Vermelho
            width_borda = 5
            raio_extra = 5 
        elif node == end_node:
            cor_borda = "#00AA00" # Verde
            width_borda = 4
            raio_extra = 0
        else:
            cor_borda = "#FFFFFF" # Branco
            width_borda = 2
            raio_extra = 0
        
        raio_final = NODE_RADIUS + raio_extra

        canvas.create_oval(
            x - raio_final + 6, y - raio_final + 6,
            x + raio_final + 6, y + raio_final + 6,
            fill="#cccccc", 
            outline=""
        )

        # Círculo Principal
        canvas.create_oval(
            x - raio_final, y - raio_final,
            x + raio_final, y + raio_final,
            fill=cor_base, 
            outline=cor_borda, 
            width=width_borda
        )
        
        # Imagem ou Texto
        if node in images:
            canvas.create_image(x, y, image=images[node])

# clique para mover
def on_click(event, images):
    global player_node
    canvas_x = canvas.canvasx(event.x)
    canvas_y = canvas.canvasy(event.y)

    for node, (nx, ny) in positions.items():
        if math.dist((canvas_x, canvas_y), (nx, ny)) <= NODE_RADIUS:
            if node in graph[player_node]:
                player_node = node
                player_path.append(player_node)
                atualizar_sidebar() 
                draw_graph(canvas, images)
                check_game_state()

            return
        
    

def start_pan(event):
    canvas.scan_mark(event.x, event.y)

def move_pan(event):
    canvas.scan_dragto(event.x, event.y, gain=1)


configurar_jogo()
if not start_node or not end_node:
    print("Jogo cancelado pelo usuário.")
    exit()

# Janela principal
root = tk.Tk()
root.title("Pokegraph")
root.geometry("1000x700")
load_images(graph)

root.grid_columnconfigure(0, weight=1) # esticar "mapa"
root.grid_columnconfigure(1, weight=0) # barra fixa
root.grid_columnconfigure(2, weight=0) # lista
root.grid_rowconfigure(0, weight=0) # outra barra
root.grid_rowconfigure(1, weight=1)

canvas = tk.Canvas(root, bg="white", scrollregion=(0, 0, LARGURA_VIRTUAL, ALTURA_VIRTUAL))
h_scroll = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
v_scroll = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)


#painel lateral
sidebar = tk.Frame(root, width=220, bg="#e1e1e1", relief="sunken", borderwidth=1)
sidebar.grid_propagate(False) #para impedir que o painel encolha 

tk.Label(sidebar, text="CAMINHO", bg="#e1e1e1", font=("Arial", 12, "bold")).pack(pady=10)
listbox_path = tk.Listbox(sidebar, width=28, height=25, font=("Consolas", 10))
listbox_path.pack(padx=10)

tk.Label(sidebar, text=f"Destino Final:\n{end_node}", bg="#e1e1e1", fg="green", font=("Arial", 11, "bold")).pack(side="bottom", pady=20) #vértice final <--------

atualizar_sidebar() #chama lista
h_scroll.grid(row=2, column=0, sticky="ew") 

canvas.grid(row=1, column=0, sticky="nsew") 

v_scroll.grid(row=1, column=1, sticky="ns")

sidebar.grid(row=1, column=2, sticky="ns")

images = load_images(graph)  # carrega e redimensiona PNGs com PIL

canvas.bind("<Button-1>", lambda e: on_click(e, images))

canvas.bind("<ButtonPress-3>", start_pan)
canvas.bind("<B3-Motion>", move_pan)

draw_graph(canvas, images)

root.mainloop()

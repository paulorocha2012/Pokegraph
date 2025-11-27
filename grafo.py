import networkx as nx
import matplotlib.pyplot as plt

# --- LISTA OFICIAL DE TIPOS ---
tipos = [
    "Normal", "Fogo", "Água", "Elétrico", "Grama", "Gelo", "Lutador", "Veneno",
    "Terra", "Voador", "Psíquico", "Inseto", "Pedra", "Fantasma", "Dragão",
    "Sombrio", "Aço", "Fada"
]

# --- VANTAGENS OFICIAIS ---
vantagens = [
    ("Fogo", "Grama"), ("Fogo", "Gelo"), ("Fogo", "Inseto"), ("Fogo", "Aço"),
    ("Água", "Fogo"), ("Água", "Terra"), ("Água", "Pedra"),
    ("Elétrico", "Água"), ("Elétrico", "Voador"),
    ("Grama", "Água"), ("Grama", "Terra"), ("Grama", "Pedra"),
    ("Gelo", "Grama"), ("Gelo", "Terra"), ("Gelo", "Voador"), ("Gelo", "Dragão"),
    ("Lutador", "Normal"), ("Lutador", "Gelo"), ("Lutador", "Pedra"), ("Lutador", "Sombrio"), ("Lutador", "Aço"),
    ("Veneno", "Grama"), ("Veneno", "Fada"),
    ("Terra", "Fogo"), ("Terra", "Elétrico"), ("Terra", "Veneno"), ("Terra", "Pedra"), ("Terra", "Aço"),
    ("Voador", "Grama"), ("Voador", "Lutador"), ("Voador", "Inseto"),
    ("Psíquico", "Lutador"), ("Psíquico", "Veneno"),
    ("Inseto", "Grama"), ("Inseto", "Psíquico"), ("Inseto", "Sombrio"),
    ("Pedra", "Fogo"), ("Pedra", "Gelo"), ("Pedra", "Voador"), ("Pedra", "Inseto"),
    ("Fantasma", "Psíquico"), ("Fantasma", "Fantasma"),
    ("Dragão", "Dragão"),
    ("Sombrio", "Psíquico"), ("Sombrio", "Fantasma"),
    ("Aço", "Gelo"), ("Aço", "Fada"), ("Aço", "Pedra"),
    ("Fada", "Lutador"), ("Fada", "Dragão"), ("Fada", "Sombrio")
]

# --- GRAFO ---
G = nx.DiGraph()
G.add_nodes_from(tipos)
G.add_edges_from(vantagens)

# --- LAYOUT: MUITO MAIS ESPAÇADO ---
pos = nx.spring_layout(
    G,
    seed=40,
    k=3.0,       # quanto maior, mais espaçado fica
    iterations=200
)

# --- VISUALIZAÇÃO ---
plt.figure(figsize=(35, 20))

nx.draw(
    G, pos,
    with_labels=True,
    node_color="red",
    node_size=2500,
    font_size=12,
    font_weight="bold",
    arrowsize=22,
    arrowstyle="-|>"
)

# nx.draw_networkx_edge_labels(
#     G, pos,
#     edge_labels={edge: "SE" for edge in G.edges()},
#     font_color="red",
#     font_size=8
# )

plt.title("Grafo de Tipos Pokémon — Versão Mais Espaçada e Legível", fontsize=18)
plt.show()
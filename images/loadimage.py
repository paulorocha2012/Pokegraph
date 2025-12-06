import os
from PIL import Image, ImageTk

IMG_SIZE = 50

def load_images(graph):
    images = {}
    
    diretorio_script = os.path.dirname(__file__)
    
    subpasta = "" 

    for node in graph.keys():
        try:
            # Monta o caminho completo: C:/Users/voce/projeto/assets/Fogo.png
            caminho_completo = os.path.join(diretorio_script, subpasta, f"{node}.png")
            
            img = Image.open(caminho_completo)
            img = img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
            images[node] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"ERRO ao carregar {caminho_completo} → {e}")
            
    return images
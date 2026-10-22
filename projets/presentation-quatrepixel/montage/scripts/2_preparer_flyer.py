"""Prépare les images du flyer de fin (v2, image TMAX) pour HyperFrames, en pleine définition 4K :
- flyer_base.png : flyer_tmax.jpg mis en 2160x3840 (lanczos, sans déformation, léger recadrage vertical) ;
- snapcode_carte.png : le carré jaune du Snapcode (sans le texte du dessous), coins arrondis transparents."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ICI = Path(__file__).resolve().parent
REF = ICI.parents[1] / "references/flyer"
OUT = ICI.parent / "hyperframes/assets/flyer"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 2160, 3840

src = Image.open(REF / "flyer_tmax.jpg").convert("RGB")
hs = round(src.height * W / src.width)
big = src.resize((W, hs), Image.LANCZOS)
dy = hs - H  # on retire le surplus en haut (ciel) pour garder un peu plus de sol libre en bas
big.crop((0, dy, W, dy + H)).save(OUT / "flyer_base.png")

# Carré du Snapcode : bord noir arrondi de (154, 281) à (729, 856) sur l'image 884x1323.
code = Image.open(REF / "snapcode_quatrepixel.jpg").convert("RGB").crop((150, 277, 734, 861))
S = 4  # masque suréchantillonné pour des coins lisses
m = Image.new("L", (code.width * S, code.height * S), 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, code.width * S - 1, code.height * S - 1), radius=100 * S, fill=255)
carte = code.convert("RGBA")
carte.putalpha(m.resize(code.size, Image.LANCZOS))
carte.save(OUT / "snapcode_carte.png")
print("ok", big.size, dy, carte.size)

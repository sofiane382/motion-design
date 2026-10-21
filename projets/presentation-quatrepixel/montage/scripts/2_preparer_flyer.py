"""Prépare les calques du flyer de fin (1080x1920) pour HyperFrames :
- flyer_base.png  : l'image, logo « Ai » retiré, écran du téléphone éteint (noir), sans liseré vert ;
- flyer_ecran.png : le Snapcode en perspective dans l'écran (RGBA, coins arrondis gardés par le masque vert) ;
- flyer_halo.png  : halo jaune doux autour de l'écran (RGBA), pour l'allumage."""
import subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ICI = Path(__file__).resolve().parent
REF = ICI.parents[1] / "references/flyer"
OUT = ICI.parent / "hyperframes/assets/flyer"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1920

# 1. Logo « Ai » (x 25-75, y 25-70 sur 1116x2000) retiré au delogo, sur le ciel.
with tempfile.TemporaryDirectory() as t:
    p = Path(t) / "f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(REF / "flyer_ecran_vert.webp"),
                    "-vf", "delogo=x=18:y=18:w=72:h=62", str(p)], check=True)
    src = Image.open(p).convert("RGB")

# 2. Mise à l'échelle sans déformer : largeur 1080, recadrage vertical centré.
k = W / src.width
hs = round(src.height * k)
dy = (hs - H) // 2
img = src.resize((W, hs), Image.LANCZOS).crop((0, dy, W, dy + H))
a = np.asarray(img).astype(np.float32)


def pt(x, y):
    return (x * k, y * k - dy)


# 3. Masque de l'écran vert (doux), un peu élargi pour avaler le liseré.
r, g, b = a[..., 0], a[..., 1], a[..., 2]
vert = g - np.maximum(r, b)
masque = np.clip((vert - 25) / 70, 0, 1)
# Uniquement autour du téléphone (les billets aussi sont verts).
zone_tel = np.zeros_like(masque); zone_tel[int(400 * k - dy):int(770 * k - dy), int(170 * k):int(370 * k)] = 1
masque *= zone_tel
m_img = Image.fromarray((masque * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
masque = np.asarray(m_img).astype(np.float32) / 255

# Despill : partout où le vert domine encore autour du téléphone, on le ramène au niveau des autres.
ys, xs = np.nonzero(masque > 0.01)
x0, x1, y0, y1 = xs.min() - 20, xs.max() + 20, ys.min() - 20, ys.max() + 20
zone = a[y0:y1, x0:x1]
gmax = np.maximum(zone[..., 0], zone[..., 2])
zone[..., 1] = np.minimum(zone[..., 1], gmax + 4)
a[y0:y1, x0:x1] = zone

# Écran éteint : noir légèrement bleuté sous le masque.
eteint = np.array([10, 11, 14], np.float32)
base = a * (1 - masque[..., None]) + eteint * masque[..., None]
Image.fromarray(base.clip(0, 255).astype(np.uint8)).save(OUT / "flyer_base.png")

# 4. Contenu de l'écran : fond jaune Snap + Snapcode, rendu en grand puis mis en perspective.
quad = [pt(188, 440), pt(332, 436), pt(356, 744), pt(210, 754)]  # hg, hd, bd, bg (un peu élargi)
cw = 900
ch = int(cw * (np.hypot(*np.subtract(quad[3], quad[0])) / np.hypot(*np.subtract(quad[1], quad[0]))))
contenu = Image.new("RGB", (cw, ch), (255, 247, 0))
grad = np.linspace(252, 236, ch)[:, None]  # léger dégradé comme la carte
c = np.asarray(contenu).astype(np.float32); c[..., 1] = grad; contenu = Image.fromarray(c.astype(np.uint8))
code = Image.open(REF / "snapcode_quatrepixel.jpg").convert("RGB")
code = code.crop((0, 80, code.width, code.height - 80))  # sans les coins blancs arrondis de la carte
code = code.resize((cw, round(code.height * cw / code.width)), Image.LANCZOS)
contenu.paste(code, (0, (ch - code.height) // 2 + int(ch * 0.03)))

SS = 4  # suréchantillonnage pour une perspective nette


def coeffs(dst, srcpts):
    m = []
    for (x, y), (u, v) in zip(dst, srcpts):
        m += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
    return np.linalg.solve(np.array(m, float), np.array([c for p in srcpts for c in p], float))


bx0, by0 = int(min(p[0] for p in quad)) - 10, int(min(p[1] for p in quad)) - 10
bx1, by1 = int(max(p[0] for p in quad)) + 10, int(max(p[1] for p in quad)) + 10
dst = [((x - bx0) * SS, (y - by0) * SS) for x, y in quad]
cf = coeffs(dst, [(0, 0), (cw, 0), (cw, ch), (0, ch)])
big = contenu.convert("RGBA").transform(((bx1 - bx0) * SS, (by1 - by0) * SS), Image.PERSPECTIVE, cf, Image.BICUBIC)
petit = big.resize((bx1 - bx0, by1 - by0), Image.LANCZOS)
ecran = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ecran.paste(petit, (bx0, by0))
e = np.asarray(ecran).astype(np.float32)
e[..., 3] = masque * 255
Image.fromarray(e.astype(np.uint8)).save(OUT / "flyer_ecran.png")

# 5. Halo : la forme de l'écran en jaune, très floutée.
halo = np.zeros((H, W, 4), np.uint8)
halo[..., 0], halo[..., 1], halo[..., 2] = 255, 248, 120
halo[..., 3] = (masque * 255).astype(np.uint8)
Image.fromarray(halo).filter(ImageFilter.GaussianBlur(28)).save(OUT / "flyer_halo.png")

# Contrôle : composition complète.
ctrl = Image.open(OUT / "flyer_base.png").convert("RGBA")
ctrl.alpha_composite(Image.open(OUT / "flyer_ecran.png"))
ctrl.convert("RGB").save(Path(tempfile.gettempdir()) / "controle_flyer.png")
print("ok", quad)

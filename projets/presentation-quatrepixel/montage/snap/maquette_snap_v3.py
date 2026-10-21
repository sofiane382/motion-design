"""Maquette v3 de la séquence Snap, en 720x1280 à 30 i/s.
Partie 1 : Quatrepixel écrit… « Ton flyer est prêt 🔥 », écrit… « Mets-le en story ».
Partie 2 : il répond « C'est posté 🔥 », Quatrepixel écrit… « Regarde dehors 👀 »,
et en haut une notification « Ta story a été vue par … » dont le compteur s'emballe."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
REF = Path(__file__).resolve().parents[2] / "references"
W, H, FPS = 720, 1280, 30
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
BLUE, RED = (14, 173, 255), (242, 60, 87)
font = lambda w, s: ImageFont.truetype(F.format(w), s)
FMSG = font("Medium", 38)


def emoji(ch, size):
    im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)


def rond(img, size):
    img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    base = Image.new("RGBA", (size, size), (255, 252, 0, 255)); base.alpha_composite(img)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(base, (0, 0), mask)
    return out


AV = rond(Image.open(REF / "flyer/snapcode_quatrepixel.jpg").crop((372, 462, 512, 602)), 76)
AV_S = rond(Image.open(REF / "flyer/snapcode_quatrepixel.jpg").crop((372, 462, 512, 602)), 64)
EMO = {"🔥": emoji("🔥", 40), "👀": emoji("👀", 40)}

# Chaque message : (expéditeur, texte, emoji de fin ou None)
MSGS = [("QP", "Ton flyer est prêt", "🔥"), ("QP", "Mets-le en story", None),
        ("MOI", "C'est posté", "🔥"), ("QP", "Regarde dehors", "👀")]


def chat(n, typing=False, dot=0, saisie="", vues=None):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    d.line((0, 170, W, 170), fill=(230, 230, 230), width=2)
    d.text((34, 100), "‹", font=font("Bold", 64), fill=(40, 40, 40), anchor="lm")
    im.alpha_composite(AV, (90, 62))
    d.text((184, 84), "Quatrepixel", font=font("Bold", 34), fill=(20, 20, 20))
    d.text((184, 126), "en train d'écrire…" if typing else "à l'instant", font=font("Medium", 22), fill=(140, 140, 140))
    # Les blocs de messages sont empilés en partant du bas, comme dans Snap.
    blocs = []
    for who, txt, emo in MSGS[:n]:
        if blocs and blocs[-1][0] == who:
            blocs[-1][1].append((txt, emo))
        else:
            blocs.append((who, [(txt, emo)]))
    hauteur = sum(50 + 58 * len(lignes) + 20 for _, lignes in blocs) + (110 if typing else 0)
    y = H - 170 - hauteur
    for who, lignes in blocs:
        coul = RED if who == "QP" else BLUE
        d.text((40, y), "QUATREPIXEL" if who == "QP" else "MOI", font=font("Bold", 24), fill=coul)
        d.rectangle((40, y + 40, 45, y + 40 + 58 * len(lignes)), fill=coul)
        for i, (txt, emo) in enumerate(lignes):
            d.text((66, y + 44 + 58 * i), txt, font=FMSG, fill=(20, 20, 20))
            if emo:
                im.alpha_composite(EMO[emo], (66 + int(d.textlength(txt + " ", font=FMSG)), y + 46 + 58 * i))
        y += 50 + 58 * len(lignes) + 20
    if typing:
        im.alpha_composite(AV_S, (40, y + 10))
        d.rounded_rectangle((116, y + 20, 236, y + 70), radius=25, fill=(238, 238, 242))
        for i in range(3):
            c = 90 if i == dot else 170
            d.ellipse((140 + 30 * i, y + 37, 156 + 30 * i, y + 53), fill=(c, c, c))
    d.rounded_rectangle((30, H - 130, W - 30, H - 60), radius=35, fill=(242, 242, 245))
    if saisie:
        d.text((70, H - 95), saisie, font=font("Medium", 30), fill=(20, 20, 20), anchor="lm")
    else:
        d.text((70, H - 95), "Envoyer un chat", font=font("Medium", 28), fill=(150, 150, 155), anchor="lm")
    if vues is not None:
        notif(im, vues)
    return im


def notif(im, vues):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 24, 24, W - 24, 150
    d.rounded_rectangle((x0 + 3, y0 + 6, x1 + 3, y1 + 6), radius=30, fill=(0, 0, 0, 40))
    d.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(250, 250, 250, 250))
    d.rounded_rectangle((x0 + 22, y0 + 24, x0 + 100, y0 + 102), radius=20, fill=(255, 252, 0))
    im.alpha_composite(emoji("👀", 46), (x0 + 38, y0 + 40))
    d.text((x0 + 124, y0 + 30), "Ma story", font=font("Bold", 30), fill=(20, 20, 20))
    d.text((x0 + 124, y0 + 72), f"Vue par {vues:,} personnes".replace(",", " "), font=font("Medium", 30), fill=(40, 40, 40))


def ecrire(prefix, n, sec, typing):
    k0 = len(list(OUT.glob(f"{prefix}_*.png")))
    for k in range(int(round(sec * FPS))):
        chat(n, typing, (k // 6) % 3).convert("RGB").save(OUT / f"{prefix}_{k0 + k:04d}.png")


def tenir(prefix, img, sec):
    k0 = len(list(OUT.glob(f"{prefix}_*.png")))
    rgb = img.convert("RGB")
    for k in range(int(round(sec * FPS))):
        rgb.save(OUT / f"{prefix}_{k0 + k:04d}.png")


# Partie 1 (validée)
ecrire("p1", 0, 0.9, True)
tenir("p1", chat(1), 1.0)
ecrire("p1", 1, 0.7, True)
tenir("p1", chat(2), 1.2)

# Partie 2 : il tape sa réponse, l'envoie, Quatrepixel répond, le compteur s'emballe.
rep = "C'est posté"
for k in range(len(rep) + 1):
    tenir("p2", chat(2, saisie=rep[:k]), 0.05)
tenir("p2", chat(3), 0.5)
ecrire("p2", 3, 0.6, True)
paliers = [12, 85, 340, 1200, 2800, 6400, 9700, 15400, 23800]
for i, v in enumerate(paliers):
    tenir("p2", chat(4, vues=v), 0.14)
tenir("p2", chat(4, vues=paliers[-1]), 0.5)

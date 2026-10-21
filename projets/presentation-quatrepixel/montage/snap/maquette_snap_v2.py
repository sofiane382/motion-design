"""Maquette v2 de la séquence Snap : conversation (écrit… message 1, écrit… message 2)
puis écran « Envoyer à » où il coche « Ma story » et envoie. Sort des PNG 30 i/s en 720x1280."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]); PREVIEW = Path(sys.argv[2])
REF = Path(__file__).resolve().parents[2] / "references"
W, H, FPS = 720, 1280, 30
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
BLUE, RED = (14, 173, 255), (242, 60, 87)
font = lambda w, s: ImageFont.truetype(F.format(w), s)


def emoji(ch, size):
    im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)


def rond(img, size, bg=(255, 252, 0)):
    img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    base = Image.new("RGBA", (size, size), bg + (255,)); base.alpha_composite(img)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(base, (0, 0), mask)
    return out


AV_QP = Image.open(REF / "flyer/snapcode_quatrepixel.jpg").crop((372, 462, 512, 602))
AV_VENDEUR = Image.open(REF / "1_visage_vendeur.jpg").crop((200, 60, 840, 700))
APERCU = Image.open(PREVIEW).convert("RGB")


def chat(n_msgs, typing, dot=0):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    d.line((0, 170, W, 170), fill=(230, 230, 230), width=2)
    d.text((34, 100), "‹", font=font("Bold", 64), fill=(40, 40, 40), anchor="lm")
    im.alpha_composite(rond(AV_QP, 76), (90, 62))
    d.text((184, 84), "Quatrepixel", font=font("Bold", 34), fill=(20, 20, 20))
    d.text((184, 126), "en train d'écrire…" if typing else "à l'instant", font=font("Medium", 22), fill=(140, 140, 140))
    f = font("Medium", 38)
    y = 700
    if n_msgs:
        d.text((40, y), "QUATREPIXEL", font=font("Bold", 24), fill=RED)
        lines = ["Ton flyer est prêt", "Mets-le en story"][:n_msgs]
        d.rectangle((40, y + 40, 45, y + 40 + 58 * len(lines)), fill=RED)
        for i, t in enumerate(lines):
            d.text((66, y + 44 + 58 * i), t, font=f, fill=(20, 20, 20))
        im.alpha_composite(emoji("🔥", 40), (66 + int(d.textlength("Ton flyer est prêt ", font=f)), y + 46))
        y += 50 + 58 * len(lines)
    if typing:
        # Bitmoji + bulle à trois points qui pulsent
        im.alpha_composite(rond(AV_QP, 64), (40, y + 30))
        d.rounded_rectangle((116, y + 40, 236, y + 90), radius=25, fill=(238, 238, 242))
        for i in range(3):
            c = 90 if i == dot else 170
            d.ellipse((140 + 30 * i, y + 57, 156 + 30 * i, y + 73), fill=(c, c, c))
    d.rounded_rectangle((30, H - 130, W - 30, H - 60), radius=35, fill=(242, 242, 245))
    d.text((70, H - 95), "Envoyer un chat", font=font("Medium", 28), fill=(150, 150, 155), anchor="lm")
    return im


def envoyer(coche, tap=None):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    d.text((34, 100), "‹", font=font("Bold", 64), fill=(40, 40, 40), anchor="lm")
    d.text((W / 2, 100), "Envoyer à…", font=font("Bold", 34), fill=(20, 20, 20), anchor="mm")
    th = APERCU.resize((150, 266)); im.paste(th, ((W - 150) // 2, 160))
    d.rounded_rectangle(((W - 150) // 2, 160, (W + 150) // 2, 426), radius=14, outline=(220, 220, 220), width=3)
    d.text((40, 470), "Stories", font=font("Bold", 28), fill=(20, 20, 20))
    for i, (nom, av) in enumerate([("Ma story", AV_VENDEUR), ("Story privée", None)]):
        y = 520 + i * 110
        if av is not None:
            im.alpha_composite(rond(av, 76, (200, 200, 200)), (40, y))
        else:
            d.ellipse((40, y, 116, y + 76), fill=(230, 230, 235))
        d.text((136, y + 38), nom, font=font("Bold" if i == 0 else "Medium", 32), fill=(20, 20, 20), anchor="lm")
        cx, cy = W - 70, y + 38
        if i == 0 and coche:
            d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=BLUE)
            d.line((cx - 10, cy, cx - 2, cy + 9, cx + 12, cy - 9), fill="white", width=5)
        else:
            d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=(190, 190, 195), width=4)
    if coche:
        d.rectangle((0, H - 150, W, H), fill=BLUE)
        d.text((40, H - 75), "Ma story", font=font("Bold", 32), fill="white", anchor="lm")
        d.ellipse((W - 130, H - 120, W - 40, H - 30), fill="white")
        d.polygon([(W - 100, H - 98), (W - 62, H - 75), (W - 100, H - 52)], fill=BLUE)
    if tap:
        x, y, r = tap
        d.ellipse((x - r, y - r, x + r, y + r), fill=(120, 120, 120, 90))
    return im


frames = []
def hold(img, sec):
    frames.extend([img.convert("RGB")] * int(round(sec * FPS)))
def typing(n, sec):
    for k in range(int(round(sec * FPS))):
        frames.append(chat(n, True, (k // 6) % 3).convert("RGB"))

typing(0, 0.9)
hold(chat(1, False), 1.0)
typing(1, 0.7)
hold(chat(2, False), 1.2)
OUT.mkdir(parents=True, exist_ok=True)
for i, fr in enumerate(frames):
    fr.save(OUT / f"chat_{i:04d}.png")

frames = []
hold(envoyer(False), 0.4)
hold(envoyer(False, (W - 70, 558, 34)), 0.15)
hold(envoyer(True), 0.6)
hold(envoyer(True, (W - 85, H - 75, 50)), 0.2)
hold(envoyer(True), 0.25)
for i, fr in enumerate(frames):
    fr.save(OUT / f"envoi_{i:04d}.png")

"""Maquette de la séquence Snap (écran de conversation + bulle « Ajouté à ta story »), en 720x1280."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SNAPCODE = Path(__file__).resolve().parents[2] / "references/flyer/snapcode_quatrepixel.jpg"
W, H = 720, 1280
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
font = lambda w, s: ImageFont.truetype(F.format(w), s)


def emoji(ch, size):
    im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True)
    return im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)


def avatar(size):
    # Le Bitmoji au centre du Snapcode de Quatrepixel, dans un rond.
    sc = Image.open(SNAPCODE).convert("RGBA").crop((372, 462, 512, 602)).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    bg = Image.new("RGBA", (size, size), (255, 252, 0, 255)); bg.alpha_composite(sc)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(bg, (0, 0), mask)
    return out


def chat(with_message):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 170), fill=(255, 255, 255))
    d.line((0, 170, W, 170), fill=(230, 230, 230), width=2)
    d.text((34, 100), "‹", font=font("Bold", 64), fill=(40, 40, 40), anchor="lm")
    im.alpha_composite(avatar(76), (90, 62))
    d.text((184, 84), "Quatrepixel", font=font("Bold", 34), fill=(20, 20, 20))
    d.text((184, 126), "en train d'écrire…" if not with_message else "à l'instant", font=font("Medium", 22), fill=(140, 140, 140))
    if with_message:
        y = 820
        d.text((40, y), "QUATREPIXEL", font=font("Bold", 24), fill=(242, 60, 87))
        d.rectangle((40, y + 40, 45, y + 150), fill=(242, 60, 87))
        f = font("Medium", 38)
        d.text((66, y + 44), "Ton flyer est prêt", font=f, fill=(20, 20, 20))
        im.alpha_composite(emoji("🔥", 40), (66 + int(d.textlength("Ton flyer est prêt ", font=f)), y + 46))
        d.text((66, y + 100), "Mets-le en story", font=f, fill=(20, 20, 20))
    # Barre d'écriture en bas
    d.rounded_rectangle((30, H - 130, W - 30, H - 60), radius=35, fill=(242, 242, 245))
    d.text((70, H - 95), "Envoyer un chat", font=font("Medium", 28), fill=(150, 150, 155), anchor="lm")
    return im


chat(False).convert("RGB").save(OUT / "snap_vide.png")
chat(True).convert("RGB").save(OUT / "snap_message.png")

story = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(story)
label, f = "Ajouté à ta story", font("Bold", 32)
pw = int(d.textlength(label, font=f)) + 110
px, py = (W - pw) // 2, 1060
d.rounded_rectangle((px, py, px + pw, py + 72), radius=36, fill=(255, 255, 255, 240))
d.ellipse((px + 20, py + 16, px + 60, py + 56), fill=(255, 252, 0))
d.line((px + 30, py + 37, px + 38, py + 45, px + 51, py + 28), fill=(20, 20, 20), width=5)
d.text((px + 76, py + 36), label, font=f, fill=(15, 15, 15), anchor="lm")
story.save(OUT / "bulle_story.png")

"""Images et sons des écrans Snap : emojis couleur, avatar rond (Bitmoji du Snapcode),
ding (message reçu), swoosh (envoi), clic (frappe), tick (compteur). Sortie : ../hyperframes/assets/snap/"""
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent
REF = ICI.parents[1] / "references/flyer"
OUT = ICI.parent / "hyperframes/assets/snap"
OUT.mkdir(parents=True, exist_ok=True)
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

for nom, ch in [("feu", "🔥"), ("yeux", "👀"), ("fantome", "👻")]:
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True)
    im.crop(im.getbbox()).save(OUT / f"{nom}.png")

# Avatar : le Bitmoji au centre du Snapcode, dans un rond sur fond jaune Snap.
code = Image.open(REF / "snapcode_quatrepixel.jpg").convert("RGBA")
bit = code.crop((366, 466, 518, 618)).resize((256, 256), Image.LANCZOS)
fond = Image.new("RGBA", (256, 256), (255, 252, 0, 255)); fond.alpha_composite(bit)
masque = Image.new("L", (1024, 1024), 0); ImageDraw.Draw(masque).ellipse((0, 0, 1023, 1023), fill=255)
av = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); av.paste(fond, (0, 0), masque.resize((256, 256), Image.LANCZOS))
av.save(OUT / "avatar.png")

# Sons, 48 kHz stéréo, volume modéré.
SR = 48000


def ecrire(nom, x, gain_db):
    x = x / max(1e-9, np.abs(x).max()) * 10 ** (gain_db / 20)
    s = (np.stack([x, x], 1) * 32767).astype(np.int16)
    with wave.open(str(OUT / f"{nom}.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())


t = lambda d: np.arange(int(d * SR)) / SR
# Ding : deux notes douces (cloche), attaque rapide, longue décroissance.
d = t(0.7)
ding = sum(a * np.sin(2 * np.pi * f * d) * np.exp(-d * k) for f, a, k in [(1318.5, 1, 7), (2637, .35, 11), (3951, .12, 16)])
d2 = t(0.6); ding2 = sum(a * np.sin(2 * np.pi * f * d2) * np.exp(-d2 * k) for f, a, k in [(1760, 1, 7), (3520, .3, 12)])
x = np.zeros(int(0.8 * SR)); x[:len(ding)] += ding; o = int(0.075 * SR); x[o:o + len(ding2)] += 0.8 * ding2[:len(x) - o]
x *= np.minimum(1, t(0.8) / 0.004)
ecrire("ding", x, -12)
# Swoosh : bruit filtré qui monte puis descend.
rng = np.random.default_rng(4)
d = t(0.32); n = rng.standard_normal(len(d))
env = np.sin(np.pi * np.clip(d / 0.32, 0, 1)) ** 2
# filtre passe-bande glissant simple (résonateur à 2 pôles)
y = np.zeros_like(n); y1 = y2 = 0.0
for i in range(len(n)):
    f = 900 + 3200 * (d[i] / 0.32); r = 0.97; th = 2 * np.pi * f / SR
    v = n[i] + 2 * r * np.cos(th) * y1 - r * r * y2; y2, y1 = y1, v; y[i] = v
ecrire("swoosh", y * env, -15)
# Clic de frappe : petit transitoire court.
d = t(0.03); clic = rng.standard_normal(len(d)) * np.exp(-d * 260) + 0.6 * np.sin(2 * np.pi * 2400 * d) * np.exp(-d * 300)
ecrire("clic", clic, -24)
# Tick du compteur : très court et aigu.
d = t(0.04); tick = np.sin(2 * np.pi * 3200 * d) * np.exp(-d * 170)
ecrire("tick", tick, -26)
print(sorted(p.name for p in OUT.iterdir()))


# Pistes son des deux écrans Snap, calées sur les temps des compositions snap1.html et snap2.html.
def lire(nom):
    with wave.open(str(OUT / f"{nom}.wav")) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2)[:, 0] / 32767


def piste(nom, duree, evts):
    x = np.zeros(int(duree * SR))
    for son, t0 in evts:
        s = lire(son); i = int(t0 * SR); n = min(len(s), len(x) - i); x[i:i + n] += s[:n]
    s = (np.stack([x, x], 1).clip(-1, 1) * 32767).astype(np.int16)
    with wave.open(str(OUT / f"{nom}.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())


piste("snap1_sons", 3.8, [("ding", 0.9), ("ding", 2.6)])
TEXTE = "C'est posté"
evts = [("clic", 0.25 + i * 0.055) for i, c in enumerate(TEXTE) if c != " "]
evts += [("swoosh", 0.95 - 0.16)]
evts += [("tick", 1.15 + i * 0.17) for i in range(9)]
evts += [("ding", 2.0)]
piste("snap2_sons", 3.6, evts)

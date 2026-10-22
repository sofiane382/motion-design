"""Génère, à partir d'UNE seule timeline (en images, 30 i/s) :
- hyperframes/index.html : le montage (coupes nettes ; fondus de 5 images pour entrer et sortir des écrans Snap ;
  fondu de 9 images du calme vers le flyer ; la transition poussière zbeul → calme est déjà dans p08/p09) ;
- hyperframes/assets/audio/mix.wav : le son complet (sons des clips + sons Snap), sans musique, sans perte.
Les vidéos sont muettes dans la composition : tout le son vient de mix.wav, qui sert aussi à l'export final."""
import wave
from pathlib import Path

import numpy as np

HF = Path(__file__).resolve().parents[1] / "hyperframes"
FPS, SR = 30, 48000
FONDU_SNAP, FONDU_FLYER = 5, 9  # en images

# (id, type, source, durée en images, fondu d'entrée en images)
PLANS = [
    ("p01", "video", "p01_calme", 127, 0),
    ("p02", "video", "p02_ennui", 70, 0),
    ("snap1", "snap", "snap1", 99, FONDU_SNAP),
    ("p04", "video", "p04_lecture", 86, FONDU_SNAP),
    ("snap2", "snap", "snap2", 99, FONDU_SNAP),
    ("p06", "video", "p06_tete", 37, FONDU_SNAP),
    ("p07", "video", "p07_zbeul", 211, 0),
    ("p08", "video", "p08_airpods", 96, 0),
    ("p09", "video", "p09_calme", 114, 0),
    ("flyer", "flyer", "flyer", 75, FONDU_FLYER),
]

t = 0
TL = []
for pid, kind, src, dur, fondu in PLANS:
    t -= fondu
    TL.append(dict(id=pid, kind=kind, src=src, start=t, dur=dur, fondu=fondu))
    t += dur
TOTAL = t
s = lambda f: f"{f / FPS:.4f}".rstrip("0").rstrip(".")

# ---------------- index.html ----------------
lignes = []
for z, p in enumerate(TL, start=1):
    if p["kind"] == "video":
        lignes.append(f'      <video id="{p["id"]}" class="clip" src="assets/plans/{p["src"]}.mp4" data-start="{s(p["start"])}" '
                      f'data-duration="{s(p["dur"])}" data-track-index="{1 + z % 2}" muted playsinline style="z-index: {z}"></video>')
    else:
        lignes.append(f'      <div id="{p["id"]}" data-composition-id="{p["id"]}" data-composition-src="compositions/{p["src"]}.html" '
                      f'data-start="{s(p["start"])}" data-duration="{s(p["dur"])}" data-track-index="3" data-track-kind="graphics" '
                      f'data-width="1080" data-height="1920" style="z-index: {z}"></div>')
fondus = [f'      tl.fromTo("#{p["id"]}", {{ opacity: 0 }}, {{ opacity: 1, duration: {s(p["fondu"])}, ease: "none" }}, {s(p["start"])});'
          for p in TL if p["fondu"]]

html = f'''<!doctype html>
<!-- Montage final « Présentation Quatrepixel » — GÉNÉRÉ par ../scripts/5_generer_montage.py (modifier le script, pas ce fichier).
     1080x1920 en CSS, rendu en 2160x3840 (--resolution portrait-4k) : les plans sont en 4K sans perte.
     Coupes nettes ; fondus courts pour entrer/sortir des écrans Snap et vers le flyer. Son : assets/audio/mix.wav. -->
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      .fond {{ position: absolute; inset: 0; background: #000; }}
      video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{s(TOTAL)}" data-width="1080" data-height="1920">
      <div class="fond"></div>
{chr(10).join(lignes)}
      <audio id="mix" class="clip" src="assets/audio/mix.wav" data-start="0" data-duration="{s(TOTAL)}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(fondus)}
      tl.to({{}}, {{ duration: 0.01 }}, {s(TOTAL - 1)});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
(HF / "index.html").write_text(html)


# ---------------- mix.wav ----------------
def lire(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 2
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32767


mix = np.zeros((round(TOTAL / FPS * SR), 2), np.float32)
DECLIC = int(0.004 * SR)  # 4 ms aux coupes pour éviter un clic, sans adoucir la coupe
for i, p in enumerate(TL):
    if p["kind"] == "flyer":
        continue
    x = lire(HF / ("assets/plans" if p["kind"] == "video" else "assets/snap") / (p["src"] + (".wav" if p["kind"] == "video" else "_sons.wav")))
    n = round(p["dur"] / FPS * SR)
    x = np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n].copy()
    fin = TL[i + 1]["fondu"] if i + 1 < len(TL) else 0
    a_in = max(round(p["fondu"] / FPS * SR), DECLIC)
    a_out = max(round(fin / FPS * SR), DECLIC)
    x[:a_in] *= np.linspace(0, 1, a_in)[:, None]
    x[-a_out:] *= np.linspace(1, 0, a_out)[:, None]
    d = round(p["start"] / FPS * SR)
    mix[d:d + n] += x[: len(mix) - d]

pic = np.abs(mix).max()
if pic > 10 ** (-2 / 20):  # garde une marge : pic final ≤ -2 dBFS
    mix *= 10 ** (-2 / 20) / pic
(HF / "assets/audio").mkdir(exist_ok=True)
with wave.open(str(HF / "assets/audio/mix.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.clip(-1, 1) * 32767).astype(np.int16).tobytes())

for p in TL:
    print(f'{p["id"]:6s} {p["start"] / FPS:7.3f} → {(p["start"] + p["dur"]) / FPS:7.3f}  ({p["dur"] / FPS:.3f} s)')
print(f"total {TOTAL / FPS:.3f} s, pic {20 * np.log10(np.abs(mix).max()):.1f} dBFS")

"""Transition zbeul → calme (« changement de monde »), calculée directement sur les images en 2160x3840 :

  plan AirPods (p08) : 2,4 → 2,9 s  la poussière dorée monte du bas et des côtés et envahit l'écran,
                       2,9 → 3,2 s  elle s'assombrit jusqu'au noir complet ;
                       son : passe-bas qui descend (tête sous l'eau) puis s'éteint.
  plan calme (p09)   : 0 → 0,3 s    noir et silence,
                       0,3 → 0,7 s  le calme apparaît depuis le noir, avec le vent,
                       0,3 → 1,3 s  quelques grains de poussière flottent dans les rayons du soleil puis disparaissent.

Entrées : assets/plans/p08_airpods_src.*, p09_calme_src.* (scripts/1_preparer_clips.sh).
Sorties : assets/plans/p08_airpods.mp4/.wav, p09_calme.mp4/.wav (vidéo sans perte, -crf 0)."""
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

PLANS = Path(__file__).resolve().parents[1] / "hyperframes/assets/plans"
W, H, FPS, SR = 2160, 3840, 30, 48000
rng = np.random.default_rng(7)


def lire_video(p):
    cmd = ["ffmpeg", "-v", "error", "-i", str(p), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while True:
        b = pr.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    pr.wait()


def ecrivain(p):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "0", "-pix_fmt", "yuv420p", "-g", "30", str(p)]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def lire_wav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32767


def ecrire_wav(p, x):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x.clip(-1, 1) * 32767).astype(np.int16).tobytes())


# ---------- Bruit de fumée (fBm) : grandes textures qu'on fait défiler vers le haut ----------
LW, LH = 540, 960  # la fumée est calculée en quart de définition puis agrandie (elle est douce)


def texture(rayon, hauteur):
    """Champ aléatoire flouté (gaussien) : des nuées organiques, sans grille visible. Normalisé autour de 0,5."""
    g = rng.standard_normal((hauteur, LW)).astype(np.float32)
    # Flou gaussien en flottant par FFT (périodique : les textures bouclent sans couture).
    fy = np.fft.fftfreq(hauteur)[:, None]; fx = np.fft.fftfreq(LW)[None, :]
    f = np.real(np.fft.ifft2(np.fft.fft2(g) * np.exp(-2 * (np.pi * rayon) ** 2 * (fx ** 2 + fy ** 2)))).astype(np.float32)
    f = (f - f.mean()) / (f.std() + 1e-6)
    return 0.5 + 0.18 * f


OCT = [(70, 0.45, 260), (34, 0.30, 420), (15, 0.17, 640), (6, 0.05, 900)]  # rayon de flou, poids, vitesse px/s
TEX = [(texture(r, LH * 4), poids, vit) for r, poids, vit in OCT]
TEX_W = [(texture(r, LH * 4), poids, vit * 0.6) for r, poids, vit in OCT[:2]]


def fbm(t, tex, decal=0, dy=0):
    out = np.zeros((LH, LW), np.float32)
    for k, (tx, poids, vit) in enumerate(tex):
        y0 = int(LH * 2 - t * vit - decal * 97 * k) % (LH * 3) + dy
        out += poids * tx[y0:y0 + LH]
    return out / sum(p for _, p, _ in tex)


yy, xx = np.mgrid[0:LH, 0:LW].astype(np.float32)
d_bas = (LH - yy) / LH                       # 0 en bas
d_cote = np.minimum(xx, LW - xx) / (LW / 2)   # 0 sur les bords
dist = np.minimum(d_bas * 1.0, d_cote * 0.85 + 0.12)
lumiere = np.clip(1.15 - np.hypot((xx - LW * 0.55) / LW, (yy - LH * 0.15) / LH) * 1.1, 0.35, 1.0)  # soleil en haut
DORE = np.array([255, 200, 122], np.float32)
OMBRE = np.array([112, 66, 34], np.float32)


def lisse(e0, e1, x):
    x = np.clip((x - e0) / (e1 - e0), 0, 1)
    return x * x * (3 - 2 * x)


def poussiere(t, avance):
    """t : temps depuis le début de la poussière ; avance : 0 → 1 (invasion). Renvoie couleur et alpha en 2160x3840."""
    # Nuées qui montent, contraste doux ; relief éclairé par le haut (dessus des volutes plus clair).
    warp = fbm(t, TEX_W, 3) - 0.5
    n = np.clip(fbm(t, TEX) + 0.35 * warp, 0, 1)
    n_haut = np.clip(fbm(t, TEX, dy=14) + 0.35 * warp, 0, 1)
    relief = np.clip((n - n_haut) * 9, -1, 1)
    c = lisse(0.28, 0.78, n)  # densité locale de la poussière
    front = avance * 1.35
    m = lisse(0, 0.35, front - dist + 0.45 * (n - 0.5))
    a = np.clip(m * (0.35 + 0.65 * c) + lisse(0.7, 1.0, avance) * 0.6, 0, 0.98)
    eclair = np.clip(0.15 + 0.95 * lumiere * (0.35 + 0.75 * c) + 0.3 * relief, 0, 1.25)[..., None]
    coul = OMBRE * (1 - np.clip(eclair, 0, 1)) + DORE * eclair
    A = np.asarray(Image.fromarray(a).resize((W, H), Image.BICUBIC), np.float32)[..., None]
    C = np.stack([np.asarray(Image.fromarray(coul[..., c]).resize((W, H), Image.BICUBIC), np.float32) for c in range(3)], -1)
    return C, np.clip(A, 0, 1)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ---------- p08 : AirPods → poussière → noir ----------
T0, T1, T2 = 2.4, 2.9, 3.2
w = ecrivain(PLANS / "p08_airpods.mp4")
for i, fr in enumerate(lire_video(PLANS / "p08_airpods_src.mp4")):
    t = i / FPS
    if t < T0:
        w.stdin.write(fr.tobytes()); continue
    C, A = poussiere(t - T0, ease((t - T0) / (T1 - T0)))
    img = fr.astype(np.float32)
    img = img * (1 + 0.25 * A)  # la lumière diffuse dans la poussière
    out = img * (1 - A) + C * A
    sombre = ease((t - T1) / (T2 - T1 - 1 / FPS))  # noir complet sur la dernière image
    out *= 1 - sombre
    w.stdin.write(out.clip(0, 255).astype(np.uint8).tobytes())
w.stdin.close(); w.wait()

# Son : passe-bas qui descend de 16 kHz à 220 Hz, puis extinction.
x = lire_wav(PLANS / "p08_airpods_src.wav")
n0, n1, n2 = int(T0 * SR), int(T1 * SR), int(T2 * SR)
y = x.copy()
z1 = np.zeros(2); z2 = np.zeros(2)
for i in range(n0, len(x)):
    u = min((i - n0) / (n1 + int(0.15 * SR) - n0), 1.0)
    fc = 16000 * (220 / 16000) ** u
    w0 = 2 * np.pi * fc / SR; al = np.sin(w0) / (2 * 0.707); cw = np.cos(w0)
    b0 = (1 - cw) / 2 / (1 + al); b1 = (1 - cw) / (1 + al); a1 = -2 * cw / (1 + al); a2 = (1 - al) / (1 + al)
    # forme transposée directe II, coefficients recalculés à chaque échantillon
    v = x[i]
    o = b0 * v + z1
    z1 = b1 * v - a1 * o + z2
    z2 = b0 * v - a2 * o
    y[i] = o
gain = np.ones(len(x), np.float32)
g = np.clip((np.arange(len(x)) - (n1 - int(0.2 * SR))) / (n2 - n1 + int(0.2 * SR)), 0, 1)
gain = (1 - g) ** 2
gain[n0:] *= 1.15  # compense un peu la perte des aigus au début de l'étouffement
ecrire_wav(PLANS / "p08_airpods.wav", y * gain[:, None])

# ---------- p09 : noir 0,3 s → le calme apparaît, grains de poussière dans les rayons ----------
NOIR, FONDU, GRAINS = 0.3, 0.4, 1.0
N = 140
px = rng.uniform(0, W, N); py = rng.uniform(250, H * 0.72, N)
vx = rng.uniform(15, 70, N); vy = rng.uniform(-90, -25, N)
taille = rng.uniform(2.0, 6.5, N); phase = rng.uniform(0, 6.28, N); freq = rng.uniform(4, 11, N)
soleil = np.array([W * 0.18, H * 0.2])
eclat = np.clip(1.25 - np.hypot(px - soleil[0], py - soleil[1]) / (W * 1.1), 0.15, 1.0)
noir = np.zeros((H, W, 3), np.uint8).tobytes()
w = ecrivain(PLANS / "p09_calme.mp4")
for _ in range(int(round(NOIR * FPS))):
    w.stdin.write(noir)
for i, fr in enumerate(lire_video(PLANS / "p09_calme_src.mp4")):
    t = i / FPS
    img = fr.astype(np.float32) * ease(t / FONDU)
    if t < GRAINS:
        env = 1 - ease((t - 0.35) / (GRAINS - 0.35))
        for k in range(N):
            cx = px[k] + vx[k] * t; cy = py[k] + vy[k] * t
            s = taille[k]; r = int(s * 3) + 1
            x0, x1 = int(cx) - r, int(cx) + r + 1; y0, y1 = int(cy) - r, int(cy) + r + 1
            if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
                continue
            gy, gx = np.mgrid[y0:y1, x0:x1]
            spr = np.exp(-((gx - cx) ** 2 + (gy - cy) ** 2) / (2 * s * s))
            fl = 0.6 + 0.4 * np.sin(phase[k] + freq[k] * t)
            img[y0:y1, x0:x1] += spr[..., None] * np.array([255, 214, 150]) * (0.85 * eclat[k] * fl * env * ease(t / FONDU))
    w.stdin.write(img.clip(0, 255).astype(np.uint8).tobytes())
w.stdin.close(); w.wait()

x = lire_wav(PLANS / "p09_calme_src.wav")
fade = np.clip(np.arange(len(x)) / (FONDU * SR), 0, 1) ** 1.5
ecrire_wav(PLANS / "p09_calme.wav", np.concatenate([np.zeros((int(NOIR * SR), 2), np.float32), x * fade[:, None]]))
print("ok")

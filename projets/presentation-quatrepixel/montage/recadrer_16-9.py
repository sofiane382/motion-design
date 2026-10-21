"""Recadre le plan large de 16.9_clip_2 en 9:16 et passe les parachutes en noir.

Usage : python3 recadrer_16-9.py <video_16-9.mp4> <sortie.mp4>
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
START, DUR = 3.625, 4.70          # plan large, avant la ruée sur les cartons
CROP_X = 590                      # fenêtre 405 px centrée sur LE VENDEUR
W, H = 720, 1280
SKY = int(H * 0.55)               # les parachutes ne sont que dans le ciel

dec = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-ss", str(START), "-t", str(DUR), "-i", SRC,
     "-vf", f"crop=405:720:{CROP_X}:0,scale={W}:{H}:flags=lanczos,unsharp=5:5:0.6",
     "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
     "-r", "24", "-i", "-", "-ss", str(START), "-t", str(DUR), "-i", SRC,
     "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", OUT], stdin=subprocess.PIPE)

size = W * H * 3
while True:
    buf = dec.stdout.read(size)
    if len(buf) < size:
        break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    sky = f[:SKY]
    r, g, b = sky[..., 0], sky[..., 1], sky[..., 2]
    mx, mn = sky.max(2), sky.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    hue = (np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) + 360) % 360
    # Le ciel et les tours sont orange/rose : seules les toiles arc-en-ciel ont du vert,
    # du bleu ou du violet. On part de ces zones et on les étend à toute la toile.
    seed = (sat > 0.35) & (hue > 70) & (hue < 300) & (mx > 0.2)
    # Bandes rouges/jaunes d'une toile coupée par le bord gauche (la tour commence vers x=230).
    seed[:, :220] |= (sat[:, :220] > 0.6) & (mx[:, :220] > 0.35)
    grown = np.asarray(Image.fromarray((seed * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)), np.float32) / 255
    m = grown * (sat > 0.22)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    luma = sky @ np.array([0.299, 0.587, 0.114], np.float32)
    black = np.repeat((0.06 + 0.12 * luma)[..., None], 3, 2)
    f[:SKY] = sky * (1 - m[..., None]) + black * m[..., None]
    enc.stdin.write((f * 255).clip(0, 255).astype(np.uint8).tobytes())

enc.stdin.close()
enc.wait()
dec.wait()

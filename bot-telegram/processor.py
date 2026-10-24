"""Traitement d'image : rend une photo de produit plus propre pour la vente.

- vérifie que le fichier est une vraie image (JPEG, PNG, WEBP, HEIC)
- redresse la photo selon l'orientation de l'appareil
- réduit les images trop larges (> 4000 px) pour économiser la mémoire
- corrige légèrement luminosité, contraste et netteté
- place la photo sur un fond blanc carré (format idéal pour les annonces)
- enregistre en JPEG sans métadonnées (ni GPS, ni modèle de téléphone)
"""

import gc
import io

from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:  # pragma: no cover - dépend de l'installation
    HEIC_SUPPORTED = False

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP", "HEIF", "HEIC"}
MAX_INPUT_WIDTH = 4000
OUTPUT_SIZE = 2048
# Refuse les "bombes" d'image (fichier minuscule qui se décompresse en image géante)
Image.MAX_IMAGE_PIXELS = 60_000_000


class NotAnImageError(ValueError):
    """Le fichier n'est pas une image acceptée."""


def detect_format(data: bytes) -> str:
    """Renvoie le format réel de l'image, ou lève NotAnImageError."""
    try:
        with Image.open(io.BytesIO(data)) as img:
            fmt = (img.format or "").upper()
            img.verify()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, Image.DecompressionBombError) as exc:
        raise NotAnImageError("format non reconnu") from exc
    if fmt not in ALLOWED_FORMATS:
        raise NotAnImageError(f"format {fmt} non accepté")
    return fmt


def process_image(data: bytes) -> bytes:
    """Traite une photo et renvoie le résultat en JPEG."""
    detect_format(data)
    img = Image.open(io.BytesIO(data))
    try:
        # Pour les JPEG, décode directement en taille réduite : moins de mémoire
        img.draft("RGB", (MAX_INPUT_WIDTH, MAX_INPUT_WIDTH))
        img = ImageOps.exif_transpose(img)

        if img.width > MAX_INPUT_WIDTH:
            height = round(img.height * MAX_INPUT_WIDTH / img.width)
            img = img.resize((MAX_INPUT_WIDTH, height), Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            background = Image.new("RGB", img.size, "white")
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")

        img = ImageOps.autocontrast(img, cutoff=1)
        img = ImageEnhance.Brightness(img).enhance(1.05)
        img = ImageEnhance.Color(img).enhance(1.08)
        img = ImageEnhance.Sharpness(img).enhance(1.3)

        img.thumbnail((OUTPUT_SIZE, OUTPUT_SIZE), Image.Resampling.LANCZOS)
        side = max(img.size)
        square = Image.new("RGB", (side, side), "white")
        square.paste(img, ((side - img.width) // 2, (side - img.height) // 2))

        out = io.BytesIO()
        # Pas de paramètre exif= : aucune métadonnée n'est recopiée
        square.save(out, "JPEG", quality=90, optimize=True)
        square.close()
        return out.getvalue()
    finally:
        img.close()
        gc.collect()

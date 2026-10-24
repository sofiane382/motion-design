import io

import pytest
from PIL import Image

from processor import MAX_INPUT_WIDTH, NotAnImageError, detect_format, process_image


def make_image(fmt="JPEG", size=(800, 600), mode="RGB", exif=None):
    img = Image.new(mode, size, (200, 120, 60) if mode == "RGB" else (200, 120, 60, 128))
    out = io.BytesIO()
    kwargs = {"exif": exif} if exif is not None else {}
    img.save(out, fmt, **kwargs)
    return out.getvalue()


@pytest.mark.parametrize("fmt", ["JPEG", "PNG", "WEBP"])
def test_accepts_real_images(fmt):
    result = process_image(make_image(fmt))
    with Image.open(io.BytesIO(result)) as out:
        assert out.format == "JPEG"
        assert out.width == out.height  # format carré


def test_png_with_transparency_gets_white_background():
    result = process_image(make_image("PNG", mode="RGBA"))
    with Image.open(io.BytesIO(result)) as out:
        assert out.mode == "RGB"


def test_heic_is_accepted():
    pytest.importorskip("pillow_heif")
    img = Image.new("RGB", (300, 200), "red")
    out = io.BytesIO()
    try:
        img.save(out, "HEIF")
    except Exception:
        pytest.skip("encodeur HEIC indisponible")
    assert detect_format(out.getvalue()) in ("HEIF", "HEIC")
    process_image(out.getvalue())


@pytest.mark.parametrize("data", [b"", b"bonjour je ne suis pas une image", b"%PDF-1.4 faux pdf"])
def test_rejects_non_images(data):
    with pytest.raises(NotAnImageError):
        process_image(data)


def test_rejects_other_image_formats():
    with pytest.raises(NotAnImageError):
        process_image(make_image("GIF"))


def test_large_images_are_reduced():
    result = process_image(make_image("PNG", size=(MAX_INPUT_WIDTH + 1000, 500)))
    with Image.open(io.BytesIO(result)) as out:
        assert max(out.size) <= 2048


def test_metadata_is_removed():
    exif = Image.Exif()
    exif[0x0110] = "Telephone secret"  # modèle de l'appareil
    result = process_image(make_image("JPEG", exif=exif.tobytes()))
    with Image.open(io.BytesIO(result)) as out:
        assert len(out.getexif()) == 0

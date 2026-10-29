#!/usr/bin/env python3
"""Make web-sized copies of the illustrations.

Quarto runs this before every render (see `pre-render` in _quarto.yml), so you
can drop full-resolution drawings into images/illustrations/ and forget about
file sizes. The originals are never changed; resized copies go to
images/illustrations/web/, which is not committed to git.

Resizing uses Pillow if it is installed, otherwise the `sips` tool that ships
with macOS, otherwise ImageMagick. If none is available the originals are
copied as they are, so the preview still works.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "illustrations"
OUT = SRC / "web"
# name -> (max width, max height)
SIZES = {"thumb": (720, 1400), "large": (2000, 2000)}
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def resize_pillow(src, dst, box):
    from PIL import Image, ImageOps

    Image.MAX_IMAGE_PIXELS = None  # these are your own (large) scans, not untrusted uploads
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            flat = Image.new("RGB", im.size, "white")
            flat.paste(im, mask=im.getchannel("A"))
            im = flat
        else:
            im = im.convert("RGB")
        im.thumbnail(box, Image.LANCZOS)
        im.save(dst, "JPEG", quality=85, optimize=True, progressive=True)


def resize_sips(src, dst, box):
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
         "-Z", str(max(box)), str(src), "--out", str(dst)],
        check=True, capture_output=True,
    )


def resize_magick(src, dst, box):
    tool = shutil.which("magick") or shutil.which("convert")
    subprocess.run(
        [tool, f"{src}[0]", "-auto-orient", "-background", "white", "-flatten",
         "-resize", f"{box[0]}x{box[1]}>", "-quality", "85", str(dst)],
        check=True, capture_output=True,
    )


def pick_resizer():
    try:
        import PIL  # noqa: F401
        return "Pillow", resize_pillow
    except ImportError:
        pass
    if shutil.which("sips"):
        return "sips", resize_sips
    if shutil.which("magick") or shutil.which("convert"):
        return "ImageMagick", resize_magick
    return None, None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    name, resize = pick_resizer()
    if not resize:
        print("prepare_images: no resizer found (pip install pillow); using originals as they are")

    sources = [p for p in sorted(SRC.iterdir()) if p.is_file() and p.suffix.lower() in EXTENSIONS]
    wanted = set()
    made = 0
    for src in sources:
        for size, box in SIZES.items():
            dst = OUT / f"{src.stem}-{size}.jpg"
            wanted.add(dst.name)
            if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                continue
            try:
                if resize:
                    resize(src, dst, box)
                else:
                    shutil.copyfile(src, dst)
            except Exception as err:  # keep the build going; show the problem
                print(f"prepare_images: could not convert {src.name} ({err}); copying original")
                shutil.copyfile(src, dst)
            made += 1

    for old in OUT.glob("*.jpg"):
        if old.name not in wanted:
            old.unlink()

    if made:
        print(f"prepare_images: made {made} web image(s) with {name or 'plain copy'}")


if __name__ == "__main__":
    sys.exit(main())

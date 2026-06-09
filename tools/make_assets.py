#!/usr/bin/env python3
"""Garden Festival asset processor.
Removes the white background (corner flood-fill so interior whites survive),
auto-crops, squares up, and writes transparent PNGs with the game's filenames.
Originals are moved to assets/source/.
"""
import os, shutil
import numpy as np
from scipy import ndimage
from PIL import Image

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS = os.path.abspath(ASSETS)
SOURCE = os.path.join(ASSETS, "source")
os.makedirs(SOURCE, exist_ok=True)

# source jpg  ->  (game png name, kind)   kind: char | item | logo
MAP = {
    "PoPo_00.jpg":      ("popo_1.png",      "char"),
    "PoPo_01.jpg":      ("popo_2.png",      "char"),
    "GongGong_00.jpg":  ("gonggong_1.png",  "char"),
    "GongGong_01.jpg":  ("gonggong_2.png",  "char"),
    "apple.jpg":        ("apple.png",       "item"),
    "banana.jpg":       ("banana.png",      "item"),
    "Orange.jpg":       ("orange.png",      "item"),
    "Grape.jpg":        ("grapes.png",      "item"),
    "Pear.jpg":         ("pear.png",        "item"),
    "mango.jpg":        ("mango.png",       "item"),
    "brocoli.jpg":      ("broccoli.png",    "item"),
    "strawberry.jpg":   ("strawberry.png",  "item"),
    "Lychee.jpg":       ("lychee.png",      "item"),
    "Longan.jpg":       ("longan.png",      "item"),
    "Dragonfruit.jpg":  ("dragonfruit.png", "item"),
    "Durian.jpg":       ("durian.png",      "item"),
    "Hamburger.jpg":    ("burger.png",      "item"),
    "Fries.jpg":        ("fries.png",       "item"),
    "Ice-cream.jpg":    ("icecream.png",    "item"),
    "Donut.jpg":        ("donut.png",       "item"),
    "Pizza.jpg":        ("pizza.png",       "item"),
    "Soda.jpg":         ("soda.png",        "item"),
    # --- second batch ---
    "Chocolate.jpg":    ("chocolate.png",   "item"),
    "Gai Lan.jpg":      ("gailan.png",      "item"),
    "bok choy.jpg":     ("bokchoy.png",     "item"),
    "corn.jpg":         ("corn.png",        "item"),
    "pineapple.jpg":    ("pineapple.png",   "item"),
    "watermelon.jpg":   ("watermelon.png",  "item"),
    "pear.jpg":         ("pear.png",        "item"),
    "Tomato.jpg":       ("tomato.png",      "item"),
    "carrot.jpg":       ("carrot.png",      "item"),
    "peach.jpg":        ("peach.png",       "item"),
    # open-mouth "eating" frames (played when catching fruit/veg)
    "popo_3.jpg":       ("popo_3.png",      "char"),
    "popo_4.jpg":       ("popo_4.png",      "char"),
    "gonggong3.jpg":    ("gonggong_3.png",  "char"),
    "gonggong4.jpg":    ("gonggong_4.png",  "char"),
    # frames 5 & 6 = "yuck" reaction cycle (played when catching junk food)
    "popo5.jpg":        ("popo_5.png",      "char"),
    "gonggong_5.jpg":   ("gonggong_5.png",  "char"),
    "popo_6.jpg":       ("popo_6.png",      "char"),
    "gonggong6.jpg":    ("gonggong_6.png",  "char"),
    "Garden Festival Logo.jpg": ("logo.png", "logo"),
}

FUZZ = 30          # how close to white counts as background (0-255 per channel)
TARGET = 256       # output square size for chars/items

def remove_white_bg(img):
    """Return RGBA with the border-connected near-white region made transparent."""
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    # near-white = every channel within FUZZ of 255
    near_white = (rgb.min(axis=2) >= 255 - FUZZ)
    # connected components of near-white; keep only those touching the border
    labeled, n = ndimage.label(near_white)
    border = set(labeled[0, :]) | set(labeled[-1, :]) | set(labeled[:, 0]) | set(labeled[:, -1])
    border.discard(0)
    bg = np.isin(labeled, list(border))
    # grow the background by 1px to eat the light anti-aliased fringe
    bg = ndimage.binary_dilation(bg, iterations=1)
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    out = np.dstack([np.asarray(img.convert("RGB")), alpha])
    return Image.fromarray(out, "RGBA")

def square(img, align):
    """Crop to content, paste onto a padded square. align: 'center' or 'bottom'."""
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    w, h = img.size
    s = max(w, h)
    pad = int(s * 0.05)
    size = s + 2 * pad
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - w) // 2
    y = (size - h - pad) if align == "bottom" else (size - h) // 2
    canvas.paste(img, (x, y), img)
    return canvas

def pct_transparent(img):
    a = np.asarray(img)[..., 3]
    return 100.0 * (a == 0).sum() / a.size

print(f"Processing into {ASSETS}\n")
for src, (dst, kind) in MAP.items():
    sp = os.path.join(ASSETS, src)
    if not os.path.exists(sp):
        print(f"  SKIP  {src} (not found)")
        continue
    img = Image.open(sp)
    rgba = remove_white_bg(img)
    if kind == "logo":
        bbox = rgba.getbbox()
        if bbox: rgba = rgba.crop(bbox)
        w, h = rgba.size
        scale = 600 / w
        rgba = rgba.resize((600, int(h * scale)), Image.LANCZOS)
    else:
        rgba = square(rgba, align="bottom" if kind == "char" else "center")
        rgba = rgba.resize((TARGET, TARGET), Image.LANCZOS)
    rgba.save(os.path.join(ASSETS, dst))
    shutil.move(sp, os.path.join(SOURCE, src))
    print(f"  OK    {src:28s} -> {dst:16s}  ({pct_transparent(rgba):.0f}% transparent)")

print("\nDone.")

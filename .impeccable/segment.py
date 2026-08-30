#!/usr/bin/env python3
"""Split tall GTM screenshots into review segments and trim trailing blank."""
from PIL import Image
import os, sys

REV = "/Users/allengaller/Documents/GitHub/allengaller/allengaller.github.io/.impeccable/review"

def bg_color(img):
    # sample a pixel far down the left edge inside padding (bg)
    return img.convert("RGB").getpixel((10, img.height - 3))

def content_bottom(img, bg, tol=6):
    px = img.convert("RGB")
    w, h = px.size
    for y in range(h - 1, -1, -1):
        row_has_content = False
        for x in range(0, w, 7):
            r, g, b = px.getpixel((x, y))
            if abs(r-bg[0]) > tol or abs(g-bg[1]) > tol or abs(b-bg[2]) > tol:
                row_has_content = True
                break
        if row_has_content:
            return y
    return h

def process(name, seg_h=1000):
    p = os.path.join(REV, name + ".png")
    img = Image.open(p)
    bg = bg_color(img)
    bottom = content_bottom(img, bg)
    pad = 40
    bottom = min(img.height, bottom + pad)
    if bottom < img.height - 5:
        img = img.crop((0, 0, img.width, bottom))
        img.save(p)
        print(f"{name}: trimmed to {img.height}px")
    # split into segments
    n = 0
    for y in range(0, img.height, seg_h):
        seg = img.crop((0, y, img.width, min(img.height, y + seg_h)))
        out = os.path.join(REV, f"_seg_{name}_{n:02d}.png")
        seg.save(out)
        n += 1
    print(f"{name}: {n} segments, content {img.width}x{img.height}")

for name in ["desktop-light", "desktop-dark", "mobile-light", "mobile-dark"]:
    process(name)

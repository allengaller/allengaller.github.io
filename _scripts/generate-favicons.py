#!/usr/bin/env python3
"""
Generate favicon variants and OG default image from the master favicon.svg.
Output:
  - favicon-32.png        (32x32)   browsers tab
  - favicon-180.png       (180x180) iOS Apple touch icon
  - og-default.png        (1200x630) Open Graph / Twitter Card default
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_cjk_font(size, weight="regular"):
    """Best-effort CJK font loading for '法' character."""
    candidates = []
    if weight == "bold":
        candidates += [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
        ]
    candidates += [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_square_icon(size, font_weight="regular"):
    """Render a solid dark rounded square with the '法' character centered."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Solid rounded square (#111111)
    radius = max(2, size // 6)
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=(17, 17, 17, 255))

    # '法' character, centered
    font_size = int(size * 0.7)
    font = load_cjk_font(font_size, font_weight)
    text = "法"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - max(1, size // 32)  # slight optical lift
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

    return img


def make_og_image():
    """1200x630 branded card: dark background, large name + tagline, no separate mark."""
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), (17, 17, 17, 255))  # #111 background
    draw = ImageDraw.Draw(img)

    # Name "法喜" — centered, white
    name_font = load_cjk_font(200, "bold")
    name = "法喜"
    bbox = draw.textbbox((0, 0), name, font=name_font)
    name_w = bbox[2] - bbox[0]
    name_h = bbox[3] - bbox[1]
    name_x = (W - name_w) // 2 - bbox[0]
    name_y = (H - name_h) // 2 - bbox[1] - 80
    draw.text((name_x, name_y), name, fill=(255, 255, 255, 255), font=name_font)

    # Underline accent (subtle)
    accent_w = 60
    accent_x = (W - accent_w) // 2
    accent_y = name_y + name_h + 36
    draw.rectangle([(accent_x, accent_y), (accent_x + accent_w, accent_y + 2)], fill=(255, 255, 255, 255))

    # Tagline — uppercase, light gray, below the name
    tag_font = ImageFont.truetype(
        "/System/Library/Fonts/Helvetica.ttc", 30
    ) if os.path.exists("/System/Library/Fonts/Helvetica.ttc") else ImageFont.load_default()
    tag_text = "CLOUD NATIVE SRE  ·  AI TOOLSMITH  ·  KNOWLEDGE ARCHITECT"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = (W - tag_w) // 2 - tag_bbox[0]
    draw.text((tag_x, accent_y + 28), tag_text, fill=(170, 170, 170, 255), font=tag_font)

    # Bottom URL — bottom-left, monospace-ish
    url_font = ImageFont.truetype(
        "/System/Library/Fonts/Helvetica.ttc", 32
    ) if os.path.exists("/System/Library/Fonts/Helvetica.ttc") else ImageFont.load_default()
    draw.text((120, H - 110), "allengaller.github.io", fill=(140, 140, 140, 255), font=url_font)

    # Subtle 1px border
    draw.rectangle([(0, 0), (W - 1, H - 1)], outline=(40, 40, 40, 255), width=2)

    return img


def main():
    out_32 = os.path.join(BASE, "favicon-32.png")
    out_180 = os.path.join(BASE, "favicon-180.png")
    out_og = os.path.join(BASE, "og-default.png")

    make_square_icon(32, "regular").save(out_32, "PNG")
    print(f"  Wrote: {out_32}")

    make_square_icon(180, "bold").save(out_180, "PNG")
    print(f"  Wrote: {out_180}")

    make_og_image().convert("RGB").save(out_og, "PNG", optimize=True)
    print(f"  Wrote: {out_og}")


if __name__ == "__main__":
    main()

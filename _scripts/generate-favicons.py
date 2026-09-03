#!/usr/bin/env python3
"""
Generate favicon variants and OG default image.

Output:
  - favicon-32.png        (32x32)    browser tab
  - favicon-180.png       (180x180)  iOS Apple touch icon
  - og-default.png        (1200x630) Open Graph / Twitter Card
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_font(size, weight="regular"):
    """Best-effort font loading. Returns ImageFont."""
    candidates = []
    # Try variable CJK fonts first (work for Chinese characters)
    if weight == "display":
        # Display — use a variable font for Fraunces-like feel (system serif)
        candidates += [
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
        ]
    else:
        candidates += [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
        ]
    # Latin fonts
    candidates += [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_square_icon(size, weight="regular"):
    """Render a solid dark rounded square with the '法' character centered."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = max(2, size // 6)
    draw.rounded_rectangle(
        [(0, 0), (size - 1, size - 1)],
        radius=radius,
        fill=(14, 14, 14, 255)  # --text: #0e0e0e
    )

    font_size = int(size * 0.7)
    font = load_font(font_size, weight)
    text = "法"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - max(1, size // 32)
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

    return img


def make_og_image():
    """1200x630 branded card: editorial composition with name + tagline + accent."""
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), (10, 10, 10, 255))  # #0a0a0a
    draw = ImageDraw.Draw(img)

    # Hairline frame (very subtle)
    draw.rectangle([(0, 0), (W - 1, H - 1)], outline=(40, 40, 40, 255), width=1)

    # Small accent eyebrow top-left
    accent_font = load_font(22, "display")
    accent_text = "✦  ALLEGALLER.GITHUB.IO"
    bbox = draw.textbbox((0, 0), accent_text, font=accent_font)
    draw.text((96, 80), accent_text, fill=(224, 120, 88, 255), font=accent_font)  # accent

    # Monogram "AG" — large, characterful serif feel
    name_font = load_font(220, "display")
    name = "AG"
    bbox = draw.textbbox((0, 0), name, font=name_font)
    name_w = bbox[2] - bbox[0]
    name_h = bbox[3] - bbox[1]
    name_x = (W - name_w) // 2 - bbox[0]
    name_y = (H - name_h) // 2 - bbox[1] - 90
    draw.text((name_x, name_y), name, fill=(245, 243, 238, 255), font=name_font)  # off-white

    # Underline accent
    accent_w = 64
    accent_x = (W - accent_w) // 2
    accent_y = name_y + name_h + 36
    draw.rectangle(
        [(accent_x, accent_y), (accent_x + accent_w, accent_y + 3)],
        fill=(224, 120, 88, 255)  # accent
    )

    # Tagline — uppercase, light gray
    tag_font = load_font(30, "display")
    tag_text = "CLOUD NATIVE SRE  ·  AI TOOLSMITH  ·  KNOWLEDGE ARCHITECT"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = (W - tag_w) // 2 - tag_bbox[0]
    draw.text((tag_x, accent_y + 32), tag_text, fill=(180, 178, 170, 255), font=tag_font)

    # Bottom-left meta
    meta_font = load_font(26, "display")
    meta_text = "Build in public  ·  Learn in public"
    draw.text((96, H - 90), meta_text, fill=(140, 140, 140, 255), font=meta_font)

    # Bottom-right year
    year_font = load_font(26, "display")
    year_text = "— 2026"
    yb = draw.textbbox((0, 0), year_text, font=year_font)
    yw = yb[2] - yb[0]
    draw.text((W - 96 - yw, H - 90), year_text, fill=(140, 140, 140, 255), font=year_font)

    return img


def main():
    out_32 = os.path.join(BASE, "favicon-32.png")
    out_180 = os.path.join(BASE, "favicon-180.png")
    out_og = os.path.join(BASE, "og-default.png")

    make_square_icon(32).save(out_32, "PNG")
    print(f"  Wrote: {out_32}")

    make_square_icon(180, "display").save(out_180, "PNG")
    print(f"  Wrote: {out_180}")

    make_og_image().convert("RGB").save(out_og, "PNG", optimize=True)
    print(f"  Wrote: {out_og}")


if __name__ == "__main__":
    main()

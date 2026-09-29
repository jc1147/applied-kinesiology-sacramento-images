"""Review sheet: python sheet.py <out.jpg> <name> [<name> ...]  (renders/<name>.png or bakeoff/, 3 per row, labelled)"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
out, names = sys.argv[1], sys.argv[2:]
W, H = 640, 440
cols = 3
rows = (len(names) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * (H + 26)), (24, 24, 24))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(names):
    p = next((os.path.join(HERE, d_, n + ".png") for d_ in ("renders", "bakeoff") if os.path.exists(os.path.join(HERE, d_, n + ".png"))), None)
    x, y = (i % cols) * W, (i // cols) * (H + 26)
    if p is None:
        d.text((x + 8, y + 8), f"{n}: missing", fill=(255, 120, 120))
        continue
    im = Image.open(p).convert("RGB")
    im.thumbnail((W - 8, H))
    sheet.paste(im, (x + (W - im.width) // 2, y))
    d.text((x + 8, y + H + 6), n, fill=(240, 240, 240))
sheet.save(os.path.join(HERE, out), quality=90)
print("sheet", out, len(names))

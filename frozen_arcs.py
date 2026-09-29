"""Frozen-shoulder plate with geometrically correct range-of-motion arcs (image models drew them wrong twice).
Base: v2/plates/cond-frozen-hero-b.png (bones reviewed fine; its arcs were wrong).
1. Remove the model's arcs: ink that is not part of a bone (thin lines and dots removed by a morphological opening)
   is inpainted back to paper.
2. Draw both arcs on ONE circle centred on the humeral head: a dotted arc for the full path of the arm raised out to
   the side (from hanging down to overhead, 180 degrees) and a solid arc with an arrowhead for the first 70 degrees
   (the restricted range). Supersampled 4x for clean edges.
Writes v2/plates/cond-frozen-hero-fixed.png and v2/frozen-arcs-mask.png (what was removed, for review)."""
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

SRC = "v2/plates/cond-frozen-hero-b.png"
CX, CY = 905, 465          # centre of the humeral head (measured on a grid)
R = 420                    # radius: a point ~60% down the humerus (the elbow's arc would leave the frame)
DARK = (22, 62, 72)        # house outline teal
MID = (62, 140, 142)       # solid arc teal
SOLID_DEG = 70             # restricted range shown

img = cv2.imread(SRC)
h, w = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
paper = cv2.GaussianBlur(cv2.morphologyEx(img, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))), (0, 0), 25)
diff = np.abs(img.astype(np.int16) - paper.astype(np.int16)).max(axis=2)
ink = ((diff > 28) | (gray < 170)).astype(np.uint8)
# Bones = regions enclosed by the dark outlines (the pale fill is close to paper, so fill the closed shapes)
dark = cv2.morphologyEx((gray < 170).astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
flood = (1 - dark).copy()
ff = np.zeros((h + 2, w + 2), np.uint8)
cv2.floodFill(flood, ff, (0, 0), 2)           # outside paper -> 2
filled = ((flood != 2) | (dark == 1)).astype(np.uint8)
# thin things attached to a bone (the old solid arc touches the humerus) are cut off by an opening before the bone
# shapes are taken; the bones themselves are wide filled shapes and survive it
filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27)))
n, lab, stats, _ = cv2.connectedComponentsWithStats(filled)
keep = np.zeros_like(filled)
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] > 20000:   # the bones; the old arcs' dots and thin arc are far smaller
        keep[lab == i] = 1
bone_region = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
arcs = ink & (1 - bone_region)
n2, lab2, stats2, _ = cv2.connectedComponentsWithStats(arcs)
clean = np.zeros_like(arcs)
for i in range(1, n2):
    if stats2[i, cv2.CC_STAT_AREA] >= 25:
        clean[lab2 == i] = 1
print("bone components kept:", int(sum(1 for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 20000)), "bone px:", int(keep.sum()))
mask = cv2.dilate(clean, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))) * 255
cv2.imwrite("v2/frozen-arcs-mask.png", mask)
out = cv2.inpaint(img, mask, 9, cv2.INPAINT_TELEA)
# leftovers touching the bone, measured on 4x crops: the old dotted arc's end dot on the humerus edge is covered by the
# straight bone edge copied from 45 px below; a faint smudge beside the head and faint specks are inpainted
out[940:981, 852:893] = out[985:1026, 852:893]
spot = np.zeros((h, w), np.uint8)
cv2.circle(spot, (813, 507), 11, 255, -1)
reg = out[905:962, 790:858].astype(np.int16)
pap = cv2.GaussianBlur(out, (0, 0), 20)[905:962, 790:858].astype(np.int16)
spot[905:962, 790:858] |= ((np.abs(reg - pap).max(axis=2) > 10).astype(np.uint8) * 255)
out = cv2.inpaint(out, cv2.dilate(spot, np.ones((5, 5), np.uint8)), 7, cv2.INPAINT_TELEA)
out[492:522, 798:818] = out[492:522, 766:786]   # the smudge by the head: plain paper from just to its left

# --- draw the arcs (angles in the math convention: 270 = straight down, 180 = out to the side, 90 = overhead)
S = 4
layer = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)


def pt(deg, r=R):
    a = math.radians(deg)
    return (CX + r * math.cos(a)) * S, (CY - r * math.sin(a)) * S


# dotted full path: 270 -> 90 through 180
step = 26 / R  # radians between dots (~26 px apart)
a = math.radians(270)
while a >= math.radians(90) - 1e-6:
    x, y = CX + R * math.cos(a), CY - R * math.sin(a)
    d.ellipse(((x - 6.5) * S, (y - 6.5) * S, (x + 6.5) * S, (y + 6.5) * S), fill=DARK + (255,))
    a -= step
# solid restricted arc: 270 -> 270 - SOLID_DEG, drawn just inside the dotted path
rs = R - 34
pts = [pt(270 - t * SOLID_DEG / 60, rs) for t in range(61)]
d.line(pts, fill=MID + (255,), width=12 * S, joint="curve")
x0, y0 = pts[0]
d.ellipse((x0 - 9 * S, y0 - 9 * S, x0 + 9 * S, y0 + 9 * S), fill=DARK + (255,))
# arrowhead at the end, pointing along the direction of travel (decreasing angle)
end = math.radians(270 - SOLID_DEG)
ex, ey = CX + rs * math.cos(end), CY - rs * math.sin(end)
tx, ty = math.sin(end), math.cos(end)          # tangent for decreasing angle (image coords, y down)
nx, ny = -ty, tx
L, W2 = 34, 18
tip = ((ex + tx * L * 0.6) * S, (ey + ty * L * 0.6) * S)
base1 = ((ex - tx * L * 0.4 + nx * W2) * S, (ey - ty * L * 0.4 + ny * W2) * S)
base2 = ((ex - tx * L * 0.4 - nx * W2) * S, (ey - ty * L * 0.4 - ny * W2) * S)
d.polygon([tip, base1, base2], fill=MID + (255,))
layer = layer.resize((w, h), Image.LANCZOS)
base = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).convert("RGBA")
Image.alpha_composite(base, layer).convert("RGB").save("v2/plates/cond-frozen-hero-fixed.png")
print("removed px:", int(clean.sum()), "| arc centre", (CX, CY), "radius", R)

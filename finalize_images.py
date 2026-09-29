"""Crop every render (and the three reused bake-off images) to its slot's aspect ratio and export:
  final/full/<name>.jpg   full resolution, quality 92
  final/web/<name>.jpg    long side 1600 px, quality 86 (what a page would load)
Prints a manifest (final/manifest.json) of page, section, slot, style and file for each image."""
import glob
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SL = json.load(open(os.path.join(HERE, "shotlist.json")))
os.makedirs(os.path.join(HERE, "final", "full"), exist_ok=True)
os.makedirs(os.path.join(HERE, "final", "web"), exist_ok=True)


def ratio(a):
    w, h = map(float, a.split(":"))
    return w / h


def center_crop(im, r):
    w, h = im.size
    if w / h > r:  # too wide
        nw = int(round(h * r))
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h))
    nh = int(round(w / r))
    y0 = (h - nh) // 2
    return im.crop((0, y0, w, y0 + nh))


DROP = {"cond-stress-assess", "cond-whiplash-assess"}  # rejected on review (a face in frame; hands over the face)
EXTRA = {"cond-scoliosis-assess", "cond-shoulder-assess", "cond-work-assess"}  # good, but the page's slot went to a treatment scene
CROP_OVERRIDE = {"cond-sciatica-treat": "3:2"}  # its slot on the page is a wide 200x130 card
# The model kept letting the practitioner's chin/beard into the top edge (and one patient's head at the far end), against
# the no-faces rule. Each box (fractions of the render: x0, y0, x1, y1) was set by eye on a guide grid to cut below or
# beside the face while keeping the hands and the treatment; the result is then centre-cropped to the slot's aspect.
FACE_CROPS = {
    "cond-headache-assess": (0, 0, 0.82, 0.873), "cond-lbp-assess": (0, 0.10, 0.78, 0.93),
    "cond-lbp-treat": (0.136, 0.12, 0.963, 1.0), "cond-frozen-assess": (0, 0, 0.84, 0.894),
    "cond-oa-assess": (0.063, 0.07, 0.937, 1.0), "cond-pregnancy-treat": (0.035, 0.07, 0.965, 1.0),
    "cond-tennis-treat": (0.085, 0.17, 0.915, 1.0), "cond-plantar-treat": (0.09, 0.09, 1.0, 1.0),
    "cond-disc-treat": (0.12, 0.06, 1.0, 0.94), "svc-fx635-device": (0.10, 0.10, 1.0, 1.0),
    "svc-pemf-hero": (0.075, 0.15, 0.925, 1.0), "ak-roof": (0.07, 0.07, 1.0, 1.0),
    "pi-faq-hero": (0.037, 0.07, 0.963, 1.0), "cond-scoliosis-treat": (0.04, 0.08, 0.96, 1.0),
    "cond-shoulder-treat": (0.045, 0.09, 0.955, 1.0), "cond-whiplash-treat": (0, 0.08, 1.0, 1.0),
    "svc-nutrition-consult": (0, 0, 0.89, 0.89), "cond-shoulder-assess": (0.025, 0.05, 0.975, 1.0),
    "ak-mtest": (0, 0.06, 1.0, 1.0),
}
items = [(s["name"], os.path.join(HERE, "renders", s["name"] + ".png"), s["page"], s["section"], s["slot"], s["style"],
          CROP_OVERRIDE.get(s["name"], s["crop"])) for s in SL["shots"] if s["name"] not in DROP]
items += [(n, os.path.join(HERE, src), page, sec, slot, "plate" if "osteo" in n else "photo", crop)
          for n, (src, page, sec, slot, crop) in SL["reuse"].items()]
manifest, missing = [], []
for name, src, page, sec, slot, style, crop in items:
    if not os.path.exists(src):
        missing.append(name)
        continue
    im = Image.open(src).convert("RGB")
    if name in FACE_CROPS:
        x0, y0, x1, y1 = FACE_CROPS[name]
        w, h = im.size
        im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    im = center_crop(im, ratio(crop))
    im.save(os.path.join(HERE, "final", "full", name + ".jpg"), quality=92)
    web = im.copy()
    web.thumbnail((1600, 1600), Image.LANCZOS)
    web.save(os.path.join(HERE, "final", "web", name + ".jpg"), quality=86)
    manifest.append({"name": name, "page": page, "section": sec, "slot": slot, "style": style, "aspect": crop,
                     "full": f"final/full/{name}.jpg", "web": f"final/web/{name}.jpg", "size": list(im.size),
                     "web_size": list(web.size), "extra": name in EXTRA})
json.dump(manifest, open(os.path.join(HERE, "final", "manifest.json"), "w"), indent=1)
print(f"exported {len(manifest)}; missing {len(missing)}: {missing}")

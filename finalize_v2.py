"""Assemble the v2 set: new overlay/editorial photos (Higgsfield Flare, v2/renders) + the illustration plates (reviewed
redraws from v2/plate_picks.json, or first-set plates the owner likes), cropped to each slot's aspect, into
final_v2/full (q92) and final_v2/web (1600 px, q86) with manifest.json and manifest.csv (page, section, slot, files,
size, alt text from v2/alt_text.json). Images the owner may prefer but that did not pass review go to
final_v2/alternatives/ with alternatives.json; they are not part of the set.

The first-set carpal-tunnel assessment plate (arm with the nerve traced to the fingertip) stays in its slot because the
owner singled it out ("I really like these"); the v2 photo for that slot failed review and is left out (SKIP)."""
import csv
import json
import os
import shutil
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "final_v2")
V2 = json.load(open(os.path.join(HERE, "shotlist_v2.json")))
V1 = {m["name"]: m for m in json.load(open(os.path.join(HERE, "final", "manifest.json")))}
KEEP_PLATES = ["cond-auto-hero", "cond-carpal-hero", "cond-carpal-assess", "cond-fibro-hero", "cond-frozen-hero",
               "cond-headache-hero", "cond-lbp-hero", "cond-oa-hero", "cond-osteo-hero", "cond-pinched-hero",
               "svc-hormone-thyroid", "ak-balance", "ak-chain"]
ALT = {"cond-carpal-assess": "cond-carpal-assess-alt"}
# photos left out of the set: the carpal-tunnel assessment photo failed round-1 review (hands and overlay) and was not
# redone, because the owner's favourite plate fills that slot
SKIP = {"cond-carpal-assess"}
CROP_BOX = json.load(open(os.path.join(HERE, "v2", "crop_boxes.json"))) if os.path.exists(os.path.join(HERE, "v2", "crop_boxes.json")) else {}
ALT_TEXT = json.load(open(os.path.join(HERE, "v2", "alt_text.json"), encoding="utf-8"))
# slot -> (source image, note): shown to the owner beside the set's pick; exported, never placed
ALTERNATES = {
    "cond-carpal-hero": ("v2/plates/cond-carpal-hero-v1edit-a.png",
                         "Edit of the owner's favourite first-set hand plate (nerve moved under the band). Failed review: "
                         "finger outlines fused with the nerve at the web spaces; the band reads as a wristband."),
}
LIVE = "https://carlcelinodspnza.github.io/applied-kinesiology-sacramento-preview/"


def ratio(a):
    w, h = map(float, a.split(":"))
    return w / h


def center_crop(im, r):
    w, h = im.size
    if w / h > r:
        nw = int(round(h * r))
        x0 = (w - nw) // 2
        return im.crop((x0, 0, x0 + nw, h))
    nh = int(round(w / r))
    y0 = (h - nh) // 2
    return im.crop((0, y0, w, y0 + nh))


def export(im, name):
    im.save(os.path.join(OUT, "full", name + ".jpg"), quality=92)
    web = im.copy()
    web.thumbnail((1600, 1600), Image.LANCZOS)
    web.save(os.path.join(OUT, "web", name + ".jpg"), quality=86)
    return list(im.size)


def main():
    for d in ("full", "web"):  # start clean so files from an earlier run (a dropped or renamed image) don't linger
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
        os.makedirs(os.path.join(OUT, d))
    manifest, missing = [], []
    for s in V2:
        if s["name"] in SKIP:
            continue
        src = os.path.join(HERE, "v2", "renders", s["name"] + ".png")
        if not os.path.exists(src):
            missing.append(s["name"])
            continue
        im = Image.open(src).convert("RGB")
        if s["name"] in CROP_BOX:
            x0, y0, x1, y1 = CROP_BOX[s["name"]]
            w, h = im.size
            im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
        im = center_crop(im, ratio(s["crop"]))
        name = ALT.get(s["name"], s["name"])
        size = export(im, name)
        manifest.append({"name": name, "page": s["page"], "section": s["section"], "slot": s["slot"],
                         "style": "overlay" if s["kind"] == "overlay" else "editorial", "aspect": s["crop"],
                         "full": f"final_v2/full/{name}.jpg", "web": f"final_v2/web/{name}.jpg", "size": size,
                         "alt": name != s["name"], "source": "Higgsfield Marketing Studio 2.5 Flare"})
    # v2/plate_picks.json: plate name -> "v2/plates/<file>.png" (a reviewed redraw) or "v1" (keep the first-set plate)
    picks_path = os.path.join(HERE, "v2", "plate_picks.json")
    picks = json.load(open(picks_path)) if os.path.exists(picks_path) else {}
    for n in KEEP_PLATES:
        m = V1[n]
        pick = picks.get(n, "v1")
        if pick == "v1":
            im = Image.open(os.path.join(HERE, m["full"])).convert("RGB")
            source = "fal Nano Banana Pro (first-set plate, kept)"
        else:
            im = center_crop(Image.open(os.path.join(HERE, pick)).convert("RGB"), ratio(m["aspect"]))
            source = "Higgsfield Marketing Studio 2.5 Flare (redrawn plate)"
        size = export(im, n)
        manifest.append({"name": n, "page": m["page"], "section": m["section"], "slot": m["slot"], "style": "plate",
                         "aspect": m["aspect"], "full": f"final_v2/full/{n}.jpg", "web": f"final_v2/web/{n}.jpg",
                         "size": size, "alt": False, "source": source, "pick": pick})
    for m in manifest:
        m["alt_text"] = ALT_TEXT[m["name"]]
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, "manifest.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["image", "page", "live_page", "section", "slot", "type", "aspect", "web_file", "full_file",
                    "full_size", "alt_text", "made_with"])
        for m in sorted(manifest, key=lambda m: (m["page"], m["name"])):
            path = m["page"].split(" ")[0]
            w.writerow([m["name"] + ".jpg", m["page"], LIVE + path + "/", m["section"], m["slot"], m["style"], m["aspect"],
                        m["web"], m["full"], "x".join(map(str, m["size"])), m["alt_text"], m["source"]])
    # alternatives: exported beside the set for the owner's decision, never placed
    alt_dir = os.path.join(OUT, "alternatives")
    shutil.rmtree(alt_dir, ignore_errors=True)
    alts = []
    for slot, (src, note) in ALTERNATES.items():
        os.makedirs(os.path.join(alt_dir, "full"), exist_ok=True)
        os.makedirs(os.path.join(alt_dir, "web"), exist_ok=True)
        aspect = next(m["aspect"] for m in manifest if m["name"] == slot)
        im = center_crop(Image.open(os.path.join(HERE, src)).convert("RGB"), ratio(aspect))
        name = slot + "-alternative"
        im.save(os.path.join(alt_dir, "full", name + ".jpg"), quality=92)
        web = im.copy()
        web.thumbnail((1600, 1600), Image.LANCZOS)
        web.save(os.path.join(alt_dir, "web", name + ".jpg"), quality=86)
        alts.append({"name": name, "for_slot": slot, "aspect": aspect, "full": f"final_v2/alternatives/full/{name}.jpg",
                     "web": f"final_v2/alternatives/web/{name}.jpg", "size": list(im.size), "source": src, "review": "FAIL",
                     "note": note, "alt_text": ALT_TEXT[name]})
    json.dump(alts, open(os.path.join(OUT, "alternatives.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"exported {len(manifest)} ({sum(m['style'] == 'plate' for m in manifest)} plates) + {len(alts)} alternative(s); missing {missing}")
    if missing and "--allow-missing" not in sys.argv:
        sys.exit(1)


if __name__ == "__main__":
    main()

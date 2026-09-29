"""Page mockups: a local mirror of the preview site with the new images placed in their slots, screenshotted with
headless Chrome next to the live page.

  mirror/            the live pages as downloaded (same paths), CSS and assets
  mirror/assets/new/ the new images (final/web)
Slots are found with the same enumeration as site/slots.py (content <img>/<svg> inside <main>, in document order).
PLACE replaces a slot; SPLITS adds a frame beside a full-width text section (turning col--full into the site's own
7/5 text + frame split), for pages that have no slot where the image belongs.

Usage: python mockups.py build | shoot [page ...]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
# SET=v2 builds from final_v2/ into mirror_v2/ and shots_v2/ (the first set stays in final/, mirror/, shots/)
SET = os.environ.get("SET", "")
FINAL = os.path.join(HERE, "final_v2" if SET == "v2" else "final")
MIRROR = os.path.join(HERE, "mirror_v2" if SET == "v2" else "mirror")
SHOTS = os.path.join(HERE, "shots_v2" if SET == "v2" else "shots")
BASE = "https://carlcelinodspnza.github.io/applied-kinesiology-sacramento-preview/"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

TRIO = lambda k: {1: f"cond-{k}-hero", 2: f"cond-{k}-assess", 3: f"cond-{k}-treat"}
PLACE = {
    "conditions/auto-accident-injury": TRIO("auto"), "conditions/carpal-tunnel": TRIO("carpal"),
    "conditions/fibromyalgia": TRIO("fibro"), "conditions/frozen-shoulder": TRIO("frozen"),
    "conditions/headache-migraine": TRIO("headache"), "conditions/low-back-pain": TRIO("lbp"),
    "conditions/osteoarthritis": TRIO("oa"), "conditions/osteoporosis": TRIO("osteo"),
    "conditions/pinched-nerve": TRIO("pinched"),
    "conditions/sciatica": {2: "cond-sciatica-treat"},
    "services": {1: "svc-hub-hero"},
    "services/cold-laser-therapy": {1: "svc-cold-hero"},
    "services/fx-635-laser-therapy": {1: "svc-fx635-device"},
    "services/hormone-therapy-management": {1: "svc-hormone-thyroid"},
    "services/pemf-therapy": {1: "svc-pemf-hero"},
    "applied-kinesiology": {1: "ak-balance", 3: "ak-mtest", 9: "ak-roof"},
    "applied-kinesiology/is-muscle-testing-legitimate": {1: "ak-legit-hero", 2: "ak-balance", 3: "ak-chain"},
    "applied-kinesiology/who-its-for": {4: "ak-who-imaging"},
    "about": {1: "about-hero"},
    "patient-info/faq": {1: "pi-faq-hero", 2: "ak-legit-hero", 3: "ak-balance"},
    "patient-info/first-visit": {1: "pi-first-hero", 2: "ak-mtest", 3: "pi-first-bring"},
    "patient-info/forms": {1: "pi-forms-hero"},
    "book": {1: "book-hero"},
}
SPLITS = {
    "conditions/plantar-fasciitis": [("What treatment involves", "cond-plantar-treat")],
    "conditions/pregnancy-pain": [("What treatment involves", "cond-pregnancy-treat")],
    "conditions/scoliosis": [("What treatment involves", "cond-scoliosis-treat")],
    "conditions/shoulder-pain": [("What treatment involves", "cond-shoulder-treat")],
    "conditions/slipped-disc": [("What treatment involves", "cond-disc-treat")],
    "conditions/stress": [("What treatment involves", "cond-stress-treat")],
    "conditions/tennis-elbow": [("What treatment involves", "cond-tennis-treat")],
    "conditions/upper-back-neck-pain": [("What treatment involves", "cond-neck-treat")],
    "conditions/whiplash": [("What treatment involves", "cond-whiplash-treat")],
    "conditions/work-injury": [("What treatment involves", "cond-work-treat")],
    "about/dr-van-wagenen": [("Still learning", "about-drvw-learning")],
    "services/nutritional-counseling": [("Who is actually giving the advice", "svc-nutrition-consult")],
}
SKIP_VB = {"0 0 24 24", "0 0 1440 78", "0 0 20 20", "0 0 16 16"}
IMG_STYLE = "display:block;width:100%;height:auto;border-radius:10px"


def slot_kind(el):
    if el.name == "img":
        return None if any(k in el.get("src", "") for k in ("texture", "logo")) else "img"
    vb = el.get("viewBox") or el.get("viewbox") or ""
    if vb in SKIP_VB or el.find_parent("svg") is not None:
        return None
    if el.find_parent(class_=re.compile(r"ck-(bar|drawer|dk|band|act)|sticky-cta|btn")):
        return None
    return "svg"


def rel(page):
    return "../" * (page.count("/") + 1) if page else ""


def figure(soup, page, name, alt):
    # height:auto: .bw-frame is height:100% (fills its column); in a tall column that stretched the frame past the section
    fig = soup.new_tag("figure", attrs={"class": "bw-frame", "data-new": name, "style": "height:auto"})
    fig.append(soup.new_tag("img", attrs={"src": f"{rel(page)}assets/new/{name}.jpg", "alt": alt, "style": IMG_STYLE}))
    return fig


def build():
    pages = [p.strip().strip("/") for p in open(os.path.join(SITE, "pages.txt")) if p.strip()]
    if os.path.exists(MIRROR):
        shutil.rmtree(MIRROR)
    os.makedirs(os.path.join(MIRROR, "assets", "new"))
    shutil.copytree(os.path.join(SITE, "assets"), os.path.join(MIRROR, "assets"), dirs_exist_ok=True)
    for f in os.listdir(os.path.join(FINAL, "web")):
        shutil.copy(os.path.join(FINAL, "web", f), os.path.join(MIRROR, "assets", "new", f))
    css = set()
    manifest = {m["name"]: m for m in json.load(open(os.path.join(FINAL, "manifest.json")))}
    report = []
    for page in pages:
        html = open(os.path.join(SITE, "pages", page.replace("/", "__") + ".html"), encoding="utf-8").read()
        css |= set(re.findall(r'href="(?:\.\./)*(design-system/[^"?]+)', html))
        soup = BeautifulSoup(html, "html.parser")
        main = soup.find("main") or soup
        slots = [el for el in main.find_all(["img", "svg"]) if slot_kind(el)]
        for n, name in PLACE.get(page, {}).items():
            el = slots[n - 1]
            if name not in manifest:
                report.append(f"{page}: {name} not rendered yet")
                continue
            alt = el.get("aria-label") or el.get("alt") or manifest[name]["section"]
            if el.name == "img" and el.find_parent(class_=re.compile(r"bw-(frame|shot)")):
                el["src"] = f"{rel(page)}assets/new/{name}.jpg"   # keep the page's own frame
                el["style"] = IMG_STYLE
                el["data-new"] = name
            else:
                el.replace_with(figure(soup, page, name, alt))
            report.append(f"{page}: slot {n} -> {name}")
        for head, name in SPLITS.get(page, []):
            h = next((x for x in main.find_all(["h2", "h3"]) if x.get_text(" ", strip=True) == head), None)
            row = h.find_parent(class_="row") if h else None
            col = row.find(class_="col--full", recursive=False) if row else None
            if name not in manifest or col is None:
                report.append(f"{page}: split '{head}' -> {name} SKIPPED ({'no render' if name not in manifest else 'no full-width column'})")
                continue
            col["class"] = [c for c in col["class"] if c != "col--full"] + ["col--span-7"]
            row["class"] = row.get("class", []) + ["row--loose", "row--center"]
            side = soup.new_tag("div", attrs={"class": "col col--span-5"})
            side.append(figure(soup, page, name, manifest[name]["section"]))
            col.insert_after(side)
            report.append(f"{page}: split beside '{head}' -> {name}")
        out = os.path.join(MIRROR, page, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(str(soup))
    shutil.copy(os.path.join(SITE, "index.html"), os.path.join(MIRROR, "index.html"))
    css |= set(re.findall(r'href="(design-system/[^"?]+)', open(os.path.join(SITE, "index.html"), encoding="utf-8").read()))
    os.makedirs(os.path.join(MIRROR, "design-system"), exist_ok=True)
    for c in sorted(css):
        urllib.request.urlretrieve(BASE + c, os.path.join(MIRROR, c))
    print("\n".join(report))
    print(f"mirror built: {len(pages)} pages, {len(css)} stylesheets")


def trim(path):
    from PIL import Image
    import numpy as np
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    dark = (a.sum(axis=2) < 200).mean(axis=1) > 0.5          # the footer is the last dark band
    rows = np.flatnonzero(dark)
    bottom = rows.max() + 2 if len(rows) else im.height
    im.crop((0, 0, im.width, min(im.height, bottom))).save(path)
    return im.width, bottom


def shoot(which):
    os.makedirs(SHOTS, exist_ok=True)
    port = 8765
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=MIRROR,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import time
    import urllib.error
    for _ in range(50):  # wait until the server answers (the first v2 run raced it and Chrome wrote nothing)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
            break
        except (urllib.error.URLError, OSError):
            time.sleep(0.2)
    try:
        for page in which:
            slug = page.replace("/", "__")
            for tag, url in (("after", f"http://127.0.0.1:{port}/{page}/"),):
                out = os.path.join(SHOTS, f"{slug}__{tag}.png")
                for attempt in range(3):
                    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=12000",
                                    "--window-size=1440,7200", f"--screenshot={out}", url], capture_output=True, timeout=120)
                    if os.path.exists(out):
                        break
                    print(f"  retry {slug} (no screenshot written)")
                w, h = trim(out)
                print(f"{slug} {tag}: {w}x{h}")
    finally:
        srv.terminate()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    else:
        shoot(sys.argv[2:] or list(PLACE) + [p for p in SPLITS if p not in PLACE])

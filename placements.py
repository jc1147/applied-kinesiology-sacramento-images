"""Where each final image goes on the site, one row per placement: final_v2/placements.csv.

Built from the same map the page mockups use (mockups.PLACE / mockups.SPLITS) against the saved copy of the preview site
(site/pages), so it matches the mockups on the review page. For a replaced slot it names the element being replaced
(its current file or aria-label) and the heading it sits under; for pages that had no slot it names the section the
new frame goes beside."""
import csv
import json
import os

from bs4 import BeautifulSoup

import mockups as MK

HERE = os.path.dirname(os.path.abspath(__file__))
M = {m["name"]: m for m in json.load(open(os.path.join(HERE, "final_v2", "manifest.json"), encoding="utf-8"))}


def heading_before(el):
    h = el.find_previous(["h1", "h2", "h3"])
    return " ".join(h.get_text(" ", strip=True).split()) if h else ""


def describe(el):
    if el.name == "img":
        return f'the image {os.path.basename(el.get("src", ""))}'
    label = el.get("aria-label") or ""
    return f'the line drawing "{label}"' if label else "the line drawing"


rows = []
for page in sorted(set(MK.PLACE) | set(MK.SPLITS)):
    soup = BeautifulSoup(open(os.path.join(MK.SITE, "pages", page.replace("/", "__") + ".html"), encoding="utf-8").read(),
                         "html.parser")
    main = soup.find("main") or soup
    slots = [el for el in main.find_all(["img", "svg"]) if MK.slot_kind(el)]
    for n, name in sorted(MK.PLACE.get(page, {}).items()):
        el = slots[n - 1]
        rows.append([page, MK.BASE + page + "/", name + ".jpg", "replace",
                     f'replaces {describe(el)} (slot {n} in <main>), under "{heading_before(el)}"',
                     M[name]["aspect"], M[name]["web"], M[name]["alt_text"]])
    for head, name in MK.SPLITS.get(page, []):
        rows.append([page, MK.BASE + page + "/", name + ".jpg", "new frame",
                     f'new frame beside the "{head}" section: turn its full-width text column into the site\'s 7/5 '
                     f'text + frame split and put the image in the 5-column frame',
                     M[name]["aspect"], M[name]["web"], M[name]["alt_text"]])
with open(os.path.join(HERE, "final_v2", "placements.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["page", "live_page", "image", "action", "where", "aspect", "web_file", "alt_text"])
    w.writerows(rows)
placed = {r[2][:-4] for r in rows}
print(len(rows), "placements on", len({r[0] for r in rows}), "pages;", len(placed), "distinct images;",
      "not placed:", sorted(set(M) - placed))

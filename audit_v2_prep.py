"""Split the v2 photo renders into review batches with the brief each image was made from."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "shotlist_v2.json")))
os.makedirs(os.path.join(HERE, "audit_v2", "crops"), exist_ok=True)
items, missing = [], []
for s in S:
    p = os.path.join(HERE, "v2", "renders", s["name"] + ".png")
    if not os.path.exists(p):
        missing.append(s["name"])
        continue
    it = {"name": s["name"], "path": p.replace("\\", "/"), "kind": s["kind"], "page_section": f'{s["page"]} :: {s["section"]}',
          "scene": s["scene"]}
    if s["kind"] == "overlay":
        it.update({"patient": s["who"], "overlay_anatomy": s["anat"], "pain_site_red_glow": s["pain"]})
    items.append(it)
n = 4
size = (len(items) + n - 1) // n
for k in range(n):
    json.dump(items[k * size:(k + 1) * size], open(os.path.join(HERE, "audit_v2", f"batch{k + 1}.json"), "w"), indent=1)
    print(k + 1, len(items[k * size:(k + 1) * size]))
print("missing:", missing)

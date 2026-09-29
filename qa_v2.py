"""Which review covers each image in the final v2 set, and what it found. Writes v2/final_qa.json, keyed by the
exported name (the gallery shows it on each card).

Photos: the round-3 pick if the shot was redone in round 3 (checked by me at zoom; empty scenes with no people),
else the round-2 review of the picked variant, else the round-1 review of the original render.
Plates: the review of the picked redraw (v2 plate reviews), the v1 audit for the v1 plates that were kept, and the
frozen-shoulder plate whose arcs were redrawn geometrically (frozen_arcs.py) on a reviewed base."""
import glob
import hashlib
import json
import os

import finalize_v2 as F

HERE = os.path.dirname(os.path.abspath(__file__))


def load(pattern):
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, pattern))):
        for e in json.load(open(p, encoding="utf-8")):
            out[e["name"]] = dict(e, _file=os.path.relpath(p, HERE).replace("\\", "/"))
    return out


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def hands_line(e):
    hs = e.get("hands") or []
    if not hs:
        return ""
    bad = [h for h in hs if not h.get("ok", True)]
    return f"{len(hs)} hand{'s' if len(hs) != 1 else ''} checked" + (f", {len(bad)} flagged" if bad else ", all correct")


def notes(e):
    return [d.get("description", "") for d in (e.get("defects") or []) if d.get("description")]


r1 = load("audit_v2/batch*-report.json")
r2 = load("audit_v2/r2_batch*-report.json")
wv_path = os.path.join(HERE, "v2", "r2_waivers.json")
for v, w in (json.load(open(wv_path)) if os.path.exists(wv_path) else {}).items():
    if v in r2:  # a review point overruled on purpose: the new verdict, with the reason shown first in the notes
        r2[v]["verdict_reviewer"] = r2[v]["verdict"]
        r2[v]["verdict"] = w["verdict"]
        r2[v]["defects"] = [{"category": "waiver", "description": f"Reviewer said {r2[v]['verdict_reviewer']}; "
                             f"{w['by']} overruled: {w['reason']}"}] + list(r2[v].get("defects") or [])
p1 = load("audit_v2/plates*-report.json")
p3 = load("audit_v2/r3_plates-report.json")
pw_path = os.path.join(HERE, "v2", "plate_waivers.json")
for v, w in (json.load(open(pw_path)) if os.path.exists(pw_path) else {}).items():
    for src in (p1, p3):
        if v in src:  # a plate review point overruled on purpose, with the reason shown first in the notes
            src[v]["verdict_reviewer"] = src[v]["verdict"]
            src[v]["verdict"] = w["verdict"]
            src[v]["defects"] = [{"category": "waiver", "description": f"Reviewer said {src[v]['verdict_reviewer']}; "
                                  f"{w['by']} overruled: {w['reason']}"}] + list(src[v].get("defects") or [])
v1 = load("audit/batch4-report.json")
r2a = json.load(open(os.path.join(HERE, "v2", "r2_applied.json"))) if os.path.exists(os.path.join(HERE, "v2", "r2_applied.json")) else {"applied": {}}
r3a = json.load(open(os.path.join(HERE, "v2", "r3_applied.json"))) if os.path.exists(os.path.join(HERE, "v2", "r3_applied.json")) else {}
r3c = load("audit_v2/r3c_batch*-report.json")
r3ca = json.load(open(os.path.join(HERE, "v2", "r3c_applied.json"))) if os.path.exists(os.path.join(HERE, "v2", "r3c_applied.json")) else {"applied": {}}
picks = json.load(open(os.path.join(HERE, "v2", "plate_picks.json")))

qa, gaps = {}, []
for s in F.V2:
    n = s["name"]
    if n in F.SKIP:
        continue
    path = os.path.join(HERE, "v2", "renders", n + ".png")
    if not os.path.exists(path):
        gaps.append(f"{n}: no render")
        continue
    name = F.ALT.get(n, n)
    if n in r3ca["applied"]:
        pick = r3ca["applied"][n]["pick"]
        e = r3c[pick]
        qa[name] = {"verdict": e["verdict"], "round": 3, "by": "independent reviewer", "hands": hands_line(e),
                    "notes": notes(e), "variant": pick, "report": e["_file"], "md5": md5(path)}
    elif n in r3a:
        qa[name] = {"verdict": "PASS", "round": 3, "by": "Claude (zoomed detail check)", "hands": "no people in frame",
                    "notes": [], "variant": r3a[n]["pick"], "md5": md5(path)}
    elif n in r2a["applied"]:
        pick = r2a["applied"][n]["pick"]
        e = r2[pick]
        qa[name] = {"verdict": e["verdict"], "round": 2, "by": "independent reviewer", "hands": hands_line(e),
                    "notes": notes(e), "variant": pick, "report": e["_file"], "md5": md5(path)}
    elif n in r1:
        e = r1[n]
        qa[name] = {"verdict": e["verdict"], "round": 1, "by": "independent reviewer", "hands": hands_line(e),
                    "notes": notes(e), "report": e["_file"], "md5": md5(path)}
        if e["verdict"] == "FAIL":
            gaps.append(f"{n}: the render in the set failed round 1 and was not replaced")
    else:
        gaps.append(f"{n}: no review found")
for n in F.KEEP_PLATES:
    pick = picks.get(n, "v1")
    if pick == "v1":
        e = v1.get(n)
        if not e:
            gaps.append(f"{n}: kept v1 plate has no audit entry")
            continue
        qa[n] = {"verdict": e["verdict"], "round": 1, "by": "independent reviewer (first-set audit)", "hands": "",
                 "notes": [d.get("description", "") for d in e.get("defects", [])], "variant": "v1", "report": e["_file"]}
    elif pick.endswith("cond-frozen-hero-fixed.png"):
        e = p1.get("cond-frozen-hero-b", {})
        qa[n] = {"verdict": "PASS", "round": 2, "by": "Claude (arcs redrawn geometrically on the reviewed base; checked at 4x)",
                 "hands": "", "notes": ["Base drawing reviewed: bones correct; the model's arcs were wrong, so they were removed and "
                                        "redrawn on one circle centred on the humeral head (frozen_arcs.py)."],
                 "variant": os.path.basename(pick), "base_review": e.get("verdict")}
    else:
        v = os.path.splitext(os.path.basename(pick))[0]
        e = p3.get(v) or r2.get(v) or p1.get(v)
        if not e:
            gaps.append(f"{n}: picked plate {v} has no review")
            continue
        qa[n] = {"verdict": e["verdict"], "round": 3 if v in p3 else (2 if v in r2 else 1), "by": "independent reviewer", "hands": "",
                 "notes": notes(e), "variant": v, "report": e["_file"]}
# shots and plates whose re-renders are still with a reviewer: shown as in review rather than with the verdict of the
# render currently in the slot (a batch input without its -report.json means its review hasn't come back yet)
pending = {}
for inp in sorted(glob.glob(os.path.join(HERE, "audit_v2", "r2_batch*.json")) + glob.glob(os.path.join(HERE, "audit_v2", "r3c_batch*.json"))
                  + glob.glob(os.path.join(HERE, "audit_v2", "r3_plates.json"))):
    if inp.endswith("-report.json") or os.path.exists(inp[:-5] + "-report.json"):
        continue
    for it in json.load(open(inp, encoding="utf-8")):
        slot = next((p for p in ("cond-auto-hero", "cond-carpal-hero") if it["name"].startswith(p + "-")), None) or it["pair"]
        pending.setdefault(F.ALT.get(slot, slot), [os.path.basename(inp), []])[1].append(it["path"])
for name, (src, cands) in pending.items():
    if name in qa or name in F.KEEP_PLATES:
        qa[name] = {"verdict": "PENDING", "round": 3 if "r3" in src else 2, "by": "independent reviewer", "hands": "",
                    "notes": ["Re-rendered after failing review; the new versions are with an independent reviewer now."],
                    "batch": src, "candidates": cands}
json.dump(qa, open(os.path.join(HERE, "v2", "final_qa.json"), "w"), indent=1)
c = {}
for q in qa.values():
    c[q["verdict"]] = c.get(q["verdict"], 0) + 1
print(len(qa), "images:", c)
print("gaps:", gaps or "none")

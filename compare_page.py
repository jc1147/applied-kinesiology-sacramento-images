"""Local review page for the FAL vs Higgsfield photo-direction test + the audit of the first image set.
Writes compare/page/Photo-Direction-Test.html (standalone: doctype, charset) with images in compare/page/img."""
import glob
import html
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "compare", "page")
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
esc = lambda s: html.escape(str(s or ""), quote=True)

MODELS = [  # key, label, platform, $/image, seconds, resolution, pose, face, anatomy, notes
    ("hf-flare", "Marketing Studio 2.5 Flare", "Higgsfield", "~$0.20–0.30 est. (token-metered; the API doesn't return the charge, your console does)", "23–27 s", "2048×1360", "6/6", "6/6", "6/6",
     "Did exactly what the brief said every time: laser on the low back, arm straight out to the side with the hand pressing above the wrist, practitioner cropped at the chest. Premium, consistent, realistic. Tends to reuse the same model woman, so each page needs its own patient described."),
    ("fal-seedream45", "Seedream 4.5", "fal", "$0.04", "14–18 s", "2400×1600", "1/6", "3/6", "6/6",
     "The most striking glow, and the overlay look is gorgeous. But it drifts off the brief: the laser lands mid or upper back, the arm goes forward instead of out to the side, and the practitioner's face creeps in. Great value; would need more redos."),
    ("fal-nbp", "Nano Banana Pro", "fal", "$0.15", "26–41 s", "2528×1696", "3/6", "4/6", "6/6",
     "Solid and sharp, but the most generic of the five. The overlay on a clothed back reads oddly. This is the model the first set used."),
    ("hf-soulv2", "Soul V2", "Higgsfield", "~$0.004", "22–167 s", "1680×1120", "2/6", "6/6", "5/6",
     "Nearly free and moody, but lower resolution. Poses are loose, and one overlay drew the skeleton upside down (pelvis at the head end)."),
    ("hf-soul", "Soul", "Higgsfield", "~$0.19 (1080p max)", "78–253 s", "2016×1344", "2/6", "0/6", "5/6",
     "Ignored the brief most: faces in every shot, arms raised overhead instead of out to the side, and a low-back patient lying on her back. Slowest by far."),
]
LOOKS = [("cinematic", "Cinematic", "Dark slate and teal, one sculpted key light, the red laser glowing."),
         ("overlay", "Anatomy overlay", "Your plate linework glowing in teal over the body, exactly where the anatomy sits."),
         ("bright", "Bright editorial", "An architect-designed clinic in crisp sunlight with clean, defined shadows.")]
SCENES = [("lowback", "Low back laser treatment", "The shot that had half a body."), ("mtest", "Arm muscle test", "The core of the method.")]


def thumb(name):
    src = [x for x in glob.glob(os.path.join(HERE, "compare", "out", name + ".*")) if not x.endswith(".json")][0]
    im = Image.open(src).convert("RGB")
    full = im.size
    im.thumbnail((1200, 1200), Image.LANCZOS)
    im.save(os.path.join(OUT, "img", name + ".jpg"), quality=84)
    rid = ""
    rj = os.path.join(HERE, "compare", "out", name + ".result.json")
    if os.path.exists(rj):
        r = json.load(open(rj))
        rid = r.get("requestId", "")
    return im.size, full, rid


def audit_html():
    reps = []
    for k in (1, 2, 3, 4):
        p = os.path.join(HERE, "audit", f"batch{k}-report.json")
        if os.path.exists(p):
            reps += json.load(open(p))
    if not reps:
        return '<p class="hint">Audit reports not in yet.</p>', {}
    counts = {}
    for r in reps:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    rows = []
    order = {"FAIL": 0, "MINOR": 1, "PASS": 2}
    for r in sorted(reps, key=lambda r: (order.get(r["verdict"], 3), r["name"])):
        if r["verdict"] == "PASS":
            continue
        defects = "; ".join(f'{d.get("category", "")}: {d.get("description", "")} ({d.get("where", "")})' for d in r.get("defects", []))
        rows.append(f'<tr><td class="v v--{r["verdict"].lower()}">{r["verdict"]}</td><td><code>{esc(r["name"])}</code></td><td>{esc(defects)}</td></tr>')
    table = ('<div class="scroll"><table class="audit"><thead><tr><th>Verdict</th><th>Image</th><th>What is wrong</th></tr></thead><tbody>'
             + "".join(rows) + "</tbody></table></div>")
    return table, counts


def build():
    grid = []
    for sk, stitle, snote in SCENES:
        grid.append(f'<section class="scene"><h2>{esc(stitle)}</h2><p class="hint">{esc(snote)} The same prompt went to every model.</p>')
        for lk, ltitle, lnote in LOOKS:
            cells = []
            for mk, mlabel, plat, *_ in MODELS:
                name = f"{sk}-{lk}-{mk}"
                (w, h), full, rid = thumb(name)
                cells.append(f'<figure class="cell"><img src="img/{name}.jpg" width="{w}" height="{h}" loading="lazy" alt="{esc(mlabel)} {esc(ltitle)}">'
                             f'<figcaption><b>{esc(plat)} · {esc(mlabel)}</b><span>{full[0]}×{full[1]}</span>'
                             + (f'<code>{esc(rid)}</code>' if rid else "") + "</figcaption></figure>")
            grid.append(f'<div class="look"><h3>{esc(ltitle)}</h3><p class="hint">{esc(lnote)}</p><div class="row5">{"".join(cells)}</div></div>')
        grid.append("</section>")
    score_rows = "".join(
        f'<tr><td><b>{esc(m[1])}</b><br><span class="plat plat--{m[2].lower()}">{esc(m[2])}</span></td><td>{esc(m[3])}</td><td>{esc(m[4])}</td>'
        f'<td>{esc(m[5])}</td><td class="n">{m[6]}</td><td class="n">{m[7]}</td><td class="n">{m[8]}</td><td>{esc(m[9])}</td></tr>' for m in MODELS)
    audit_table, counts = audit_html()
    count_line = " · ".join(f"<b>{v}</b> {k.lower()}" for k, v in sorted(counts.items(), key=lambda kv: {"FAIL": 0, "MINOR": 1, "PASS": 2}.get(kv[0], 3)))
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Photo Direction Test</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Mulish:wght@400;600;700&display=swap">
<style>
:root{{--paper:#FFFDFA;--card:#F7F3EC;--ink:#232B31;--head:#1E2A33;--soft:#55606A;--line:#E4DCD0;--accent:#0a748a;--chip:#E4F4F7;--bad:#b3261e;--warn:#9a6a1a;--good:#1e7a4c;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--paper:#1E2A33;--card:#263440;--ink:#E8EDF0;--head:#fff;--soft:#C3CDD4;--line:#3A4A56;--accent:#4FC0D8;--chip:#26404A;--bad:#ff8a80;--warn:#f0c36a;--good:#7fd6a8;color-scheme:dark}}}}
body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 "Mulish",system-ui,sans-serif}}
.wrap{{max-width:1760px;margin:0 auto;padding:32px 24px 72px;display:grid;gap:40px}}
h1,h2,h3{{font-family:"Playfair Display",Georgia,serif;color:var(--head);margin:0;text-wrap:balance}}
h1{{font-size:clamp(32px,4vw,52px);line-height:1.05}} h2{{font-size:30px}} h3{{font-size:21px}}
p{{margin:0;max-width:80ch}} .hint{{color:var(--soft);font-size:14px}}
.eyebrow{{font:700 12px/1.3 "Mulish";letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}}
.intro{{display:grid;gap:14px}} .lede{{font-size:18px}}
.callout{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:12px;padding:16px 18px;display:grid;gap:8px}}
.scroll{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;min-width:900px;font-size:14.5px}}
th,td{{text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid var(--line)}}
th{{font:700 11px/1.2 "Mulish";letter-spacing:.08em;text-transform:uppercase;color:var(--soft)}}
td.n{{font-variant-numeric:tabular-nums;font-weight:700;white-space:nowrap}}
.plat{{font:700 11px/1 "Mulish";letter-spacing:.06em;text-transform:uppercase;padding:3px 7px;border-radius:99px;display:inline-block;margin-top:4px}}
.plat--higgsfield{{background:#e9e0ff;color:#4b2a9a}} .plat--fal{{background:var(--chip);color:var(--accent)}}
.scene{{display:grid;gap:18px;border-top:1px solid var(--line);padding-top:18px}}
.look{{display:grid;gap:10px}}
.row5{{display:grid;gap:12px;grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (max-width:1100px){{.row5{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.cell{{margin:0;display:grid;gap:6px}} .cell img{{width:100%;height:auto;border-radius:10px;display:block;background:#111}}
.cell figcaption{{display:grid;gap:2px;font-size:13px}} .cell span{{color:var(--soft)}}
code{{font:12px/1.4 ui-monospace,Consolas,monospace;color:var(--soft);word-break:break-all}}
.rec{{display:grid;gap:10px}} .rec ul{{margin:0;padding-left:20px;display:grid;gap:6px;max-width:90ch}}
.audit td.v{{font-weight:800;white-space:nowrap}} .v--fail{{color:var(--bad)}} .v--minor{{color:var(--warn)}}
</style></head><body><div class="wrap">
<header class="intro">
  <p class="eyebrow">Sacramento Applied Kinesiology · new photo direction</p>
  <h1>FAL vs Higgsfield: finding the look</h1>
  <div class="callout"><p><b>Did the first set use Higgsfield?</b> No. All 60 images ran on <b>fal.ai</b> (Nano Banana Pro); the files only sat in the higgsfield folder. This test ran on both: the 18 Higgsfield requests below show in your Higgsfield console, with request IDs under each image.</p></div>
  <p class="lede">Two scenes × three looks × five models, 30 renders, with the same prompt for every model. The plates you liked stay as they are; this test is only about the photographs.</p>
</header>
<section class="intro"><h2>Scoreboard</h2>
<p class="hint">Scored on the 6 renders per model. Pose right: the laser on the low back, and the arm straight out to the side with one hand pressing above the wrist. Face hidden: the practitioner stays cropped at the chest (he's a real person). Anatomy: every body complete and continuous.</p>
<div class="scroll"><table><thead><tr><th>Model</th><th>Cost per image</th><th>Time</th><th>Size</th><th>Pose right</th><th>Face hidden</th><th>Anatomy</th><th>What I saw</th></tr></thead><tbody>{score_rows}</tbody></table></div>
</section>
<section class="rec"><h2>My recommendation</h2><ul>
<li><b>Model: Higgsfield Marketing Studio 2.5 Flare.</b> It was the only one that followed the brief in all six. That's what stops "half a body" and random faces, and it looks premium. Seedream 4.5 on fal is the runner-up: the most striking, but it would need many more redos.</li>
<li><b>Look: give each look a job,</b> rather than one look everywhere. <b>Anatomy overlay</b> for "how we assess it" (the method made visible, tied to your plates). <b>Cinematic</b> for treatments (the laser and PEMF glow). <b>Bright editorial</b> for people pages (first visit, FAQ, forms, booking, about). Or pick one look for everything.</li>
<li><b>People:</b> a different, real-looking patient for each condition (older adults for osteoporosis and osteoarthritis, a pregnant patient, a worker in work clothes, and so on). Patients' faces can show now, relaxed or eyes closed. The practitioner stays cropped at the chest, because he's a real person.</li>
<li><b>Quality gate:</b> every image checked zoomed for whole bodies, hands and faces, then a second independent review, before you see it.</li>
</ul></section>
{''.join(grid)}
<section class="scene" id="audit"><h2>Audit of the first set (60 images)</h2>
<p class="hint">Four independent reviewers checked every image zoomed in, in this order: body integrity, faces, devices, text, match to the brief, render quality. {count_line}</p>
{audit_table}
</section>
</div></body></html>"""
    open(os.path.join(OUT, "Photo-Direction-Test.html"), "w", encoding="utf-8").write(page)
    print("page written;", "audit:", counts)


if __name__ == "__main__":
    build()

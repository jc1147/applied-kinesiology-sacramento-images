"""Local review page for image set v2 (standalone HTML, opened on the owner's machine; no artifact).
Reads final_v2/manifest.json, v2/final_qa.json (qa_v2.py), shots_v2/ mockups and the review reports (v1 + v2), and
writes page_v2/AK-Image-Set-v2.html."""
import glob
import html
import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "page_v2")
LIVE = "https://carlcelinodspnza.github.io/applied-kinesiology-sacramento-preview/"
esc = lambda s: html.escape(str(s or ""), quote=True)
M = json.load(open(os.path.join(HERE, "final_v2", "manifest.json")))
QA = json.load(open(os.path.join(HERE, "v2", "final_qa.json")))
SURVEY = json.load(open(os.path.join(HERE, "site", "survey.json")))
GROUPS = [("Conditions", "conditions/"), ("Services", "services"), ("Applied kinesiology", "applied-kinesiology"),
          ("About", "about"), ("Patient information", "patient-info"), ("Booking", "book")]
# fal spend (list price x requests, worked out when each batch ran): first set $8.10 + model test $0.69 + 19 redos
# $2.85 + 5 added scenes $0.75; the direction test's fal half: 6 x Nano Banana Pro $0.15 + 6 x Seedream 4.5 $0.04
FAL_V1, FAL_TEST = 12.39, 1.14
FLARE_EST = (0.20, 0.30)  # per image, an estimate: the API returns no charge (see compare page); exact spend is in the console
# slots where an image the owner may prefer exists but did not pass review: shown beside the set's pick, not used
ALTERNATES = {
    "cond-carpal-hero": ("v2/plates/cond-carpal-hero-v1edit-a.png",
                         "Your favourite first-set hand plate, edited so the nerve runs under the band. Review failed it: "
                         "the finger outlines fused with the nerve at the web spaces and the band reads as a wristband. "
                         "The redraw beside it passed. If you prefer this look, I'll clean those up."),
}
# the direction test (compare/page/Photo-Direction-Test.html): renders that followed the brief, out of 6 per model
TEST = [("Higgsfield · Marketing Studio 2.5 Flare", "6/6"), ("fal · Nano Banana Pro (the first set's model)", "3/6"),
        ("Higgsfield · Soul V2", "2/6"), ("Higgsfield · Soul", "2/6"), ("fal · Seedream 4.5", "1/6")]


def load_reports(pattern):
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, pattern))):
        try:
            out += json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return out


def counts(reps):
    c = {"PASS": 0, "MINOR": 0, "FAIL": 0}
    for r in reps:
        c[r.get("verdict", "?")] = c.get(r.get("verdict", "?"), 0) + 1
    return c


def title_of(page):
    d = SURVEY.get(page.split(" ")[0].replace("/", "__"))
    if not d:
        return page
    return next((x for t, x in d["h"] if t == "h1"), d["title"])


def flare_requests():
    """Unique Flare request ids across every saved result (renders, variants, rejects, plates, rounds, the test) and
    every runner log line (applying a pick overwrites the replaced render's result file, but its log line stays).
    A lower bound: a few early log files were overwritten by later runs."""
    import re
    ids = set()
    for f in glob.glob(os.path.join(HERE, "**", "*.result.json"), recursive=True):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("model") == "marketing-studio/image/flare" and d.get("requestId"):
            ids.add(d["requestId"])
    pat = re.compile(r"\] ok   \S+\s.*metered.*\(([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\)")
    for f in glob.glob(os.path.join(HERE, "v2", "*.log")) + [os.path.join(HERE, "compare", "hf.log")]:
        for line in open(f, encoding="utf-8", errors="ignore"):
            m = pat.search(line)
            if m:
                ids.add(m.group(1))
    return len(ids)


def round1_causes():
    """Round-1 photo failures: how many had an overlay error and how many a hand/body error."""
    ov = ppl = n = 0
    for e in load_reports("audit_v2/batch*-report.json"):
        if e["verdict"] != "FAIL":
            continue
        n += 1
        cats = [d.get("category", "").lower() for d in e.get("defects", [])]
        ov += any("overlay" in c or "glow" in c for c in cats)
        ppl += any(k in c for c in cats for k in ("hand", "finger", "body", "limb", "foot", "toe", "leg", "arm")) or \
            any(not h.get("ok", True) for h in e.get("hands", []))
    return n, ov, ppl


def build(extra_notes):
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for d in ("img", "mock", "ref"):
        os.makedirs(os.path.join(OUT, d))
    sizes = {}
    for m in M:
        im = Image.open(os.path.join(HERE, m["full"])).convert("RGB")
        im.thumbnail((1400, 1400), Image.LANCZOS)
        im.save(os.path.join(OUT, "img", m["name"] + ".jpg"), quality=84)
        sizes[m["name"]] = im.size
    cand_sizes = {}  # pending slots: the new versions with the reviewer, shown instead of the render they replace
    for name, q in QA.items():
        for p in q.get("candidates", []):
            im = Image.open(p).convert("RGB")
            im.thumbnail((900, 900), Image.LANCZOS)
            base = os.path.splitext(os.path.basename(p))[0]
            os.makedirs(os.path.join(OUT, "img", "new"), exist_ok=True)
            im.save(os.path.join(OUT, "img", "new", base + ".jpg"), quality=82)
            cand_sizes[base] = im.size
    mocks = {}
    for f in sorted(glob.glob(os.path.join(HERE, "shots_v2", "*__after.png"))):
        slug = os.path.basename(f)[:-len("__after.png")]
        im = Image.open(f).convert("RGB")
        im = im.resize((820, int(im.height * 820 / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT, "mock", slug + ".jpg"), quality=78)
        mocks[slug] = im.size
    for n in ("cond-auto-treat", "cond-frozen-treat", "cond-lbp-hero", "cond-carpal-hero"):  # v1 examples for the audit
        src = os.path.join(HERE, "final", "full", n + ".jpg")
        if os.path.exists(src):
            im = Image.open(src).convert("RGB")
            im.thumbnail((900, 900))
            im.save(os.path.join(OUT, "ref", "v1-" + n + ".jpg"), quality=82)
    by_page = {}
    for m in M:
        by_page.setdefault(m["page"].split(" ")[0], []).append(m)
    alt_sizes = {}
    for slot, (src, _) in ALTERNATES.items():
        im = Image.open(os.path.join(HERE, src)).convert("RGB")
        im.thumbnail((1400, 1400), Image.LANCZOS)
        im.save(os.path.join(OUT, "img", slot + "-alternative.jpg"), quality=84)
        alt_sizes[slot] = im.size

    def alt_card(m):
        if m["name"] not in ALTERNATES:
            return ""
        w, h = alt_sizes[m["name"]]
        return (f'<figure class="card"><img src="img/{m["name"]}-alternative.jpg" width="{w}" height="{h}" loading="lazy" alt="Alternative: {esc(m["section"])}">'
                f'<figcaption><span class="tags"><span class="tag tag--soft">alternative, not in the set</span></span><strong>{esc(m["section"])}</strong>'
                f'<p class="qa qa--fail"><span class="dot" aria-hidden="true"></span><b>Failed review</b></p>'
                f'<p class="soft" style="font-size:13px;margin:0">{esc(ALTERNATES[m["name"]][1])}</p></figcaption></figure>')

    def qa_line(name):
        q = QA.get(name)
        if not q:
            return '<p class="qa qa--none">Not reviewed</p>'
        v = q["verdict"]
        label = {"PASS": "Pass", "MINOR": "Minor notes", "FAIL": "Failed", "PENDING": "In final review"}[v]
        bits = [f"Round {q['round']}", "checked by me" if q["by"].startswith("Claude") else "independent review"]
        if v == "PENDING":
            bits = ["re-rendered, being checked now"]
        if q.get("hands"):
            bits.append(q["hands"])
        notes = "".join(f"<li>{esc(n)}</li>" for n in q.get("notes", []))
        det = f'<details class="qa-notes"><summary>Review notes ({len(q["notes"])})</summary><ul>{notes}</ul></details>' if notes else ""
        return f'<p class="qa qa--{v.lower()}"><span class="dot" aria-hidden="true"></span><b>{label}</b> · {esc(" · ".join(bits))}</p>{det}'

    def card(m):
        q = QA.get(m["name"], {})
        if q.get("verdict") == "PENDING" and q.get("candidates"):
            kind = {"overlay": "Anatomy overlay photo", "editorial": "Clinic photo", "plate": "Illustration plate"}[m["style"]]
            imgs = "".join(
                f'<img src="img/new/{b}.jpg" width="{cand_sizes[b][0]}" height="{cand_sizes[b][1]}" loading="lazy" alt="New version {b[-1]}">'
                for b in (os.path.splitext(os.path.basename(p))[0] for p in q["candidates"]))
            return (f'<figure class="card card--pending"><div class="pair">{imgs}</div>'
                    f'<figcaption><span class="tags"><span class="tag">{kind}</span><span class="tag tag--soft">two new versions</span></span>'
                    f'<strong>{esc(m["section"])}</strong>{qa_line(m["name"])}<code>{m["name"]}.jpg</code></figcaption></figure>')
        w, h = sizes[m["name"]]
        kind = {"overlay": "Anatomy overlay photo", "editorial": "Clinic photo", "plate": "Illustration plate"}[m["style"]]
        src = "first set, kept" if "kept" in m["source"] else ("redrawn" if m["style"] == "plate" else "")
        tag2 = f'<span class="tag tag--soft">{src}</span>' if src else ""
        return (f'<figure class="card"><img src="img/{m["name"]}.jpg" width="{w}" height="{h}" loading="lazy" alt="{esc(m["section"])}">'
                f'<figcaption><span class="tags"><span class="tag">{kind}</span>{tag2}</span><strong>{esc(m["section"])}</strong>'
                f'{qa_line(m["name"])}<code>{m["name"]}.jpg</code></figcaption></figure>')

    body = []
    for gname, prefix in GROUPS:
        keys = sorted([k for k in by_page if k.startswith(prefix)], key=lambda k: (k.count("/"), k))
        if not keys:
            continue
        body.append(f'<section class="group" id="{prefix.strip("/")}"><h2>{gname}</h2>')
        for k in keys:
            slug = k.replace("/", "__")
            items = sorted(by_page[k], key=lambda m: ({"plate": 0, "overlay": 1, "editorial": 2}[m["style"]], m["name"]))
            mock = ""
            if any(QA.get(m["name"], {}).get("verdict") == "PENDING" for m in by_page[k]):
                mock = '<p class="soft" style="font-size:14px">Page mockup comes with the final update, once the new versions above clear review.</p>'
            elif slug in mocks:
                mw, mh = mocks[slug]
                mock = (f'<details class="mock"><summary>See it on the page</summary>'
                        f'<img src="mock/{slug}.jpg" width="{mw}" height="{mh}" loading="lazy" alt="Mockup of {esc(title_of(k))}"></details>')
            body.append(f'<article class="page"><header><h3>{esc(title_of(k))}</h3><a href="{LIVE}{k}/" target="_blank" rel="noopener">/{k}/</a></header>'
                        f'<div class="grid">{"".join(card(m) + alt_card(m) for m in items)}</div>{mock}</article>')
        body.append("</section>")

    # --- numbers for the top of the page (all computed from the files on disk)
    v1 = counts(load_reports("audit/batch*-report.json"))
    v1p = counts(load_reports("audit/batch4-report.json"))
    r1 = counts(load_reports("audit_v2/batch*-report.json"))
    r1p = counts(load_reports("audit_v2/plates*-report.json"))
    r2 = counts(load_reports("audit_v2/r2_batch*-report.json"))
    r2a = json.load(open(os.path.join(HERE, "v2", "r2_applied.json")))
    r3a = json.load(open(os.path.join(HERE, "v2", "r3_applied.json"))) if os.path.exists(os.path.join(HERE, "v2", "r3_applied.json")) else {}
    r3c = counts(load_reports("audit_v2/r3c_batch*-report.json"))
    r3ca = json.load(open(os.path.join(HERE, "v2", "r3c_applied.json"))) if os.path.exists(os.path.join(HERE, "v2", "r3c_applied.json")) else {"applied": {}, "still_failing": []}
    def batch_pairs(pattern):
        """(pairs in the review inputs, number of those inputs whose report is still out)"""
        pairs, out = set(), 0
        for p in glob.glob(os.path.join(HERE, "audit_v2", pattern)):
            if p.endswith("-report.json"):
                continue
            out += not os.path.exists(p[:-5] + "-report.json")
            pairs |= {next((q for q in ("cond-auto-hero", "cond-carpal-hero") if it["name"].startswith(q + "-")), it["pair"])
                      for it in json.load(open(p, encoding="utf-8"))}
        return pairs, out
    r2_pairs, r2_out = batch_pairs("r2_batch*.json")
    # the round-2 plates were listed in r2_plates.json and reviewed inside r2_batch6-report.json
    r2_plate_pairs = {next(q for q in ("cond-auto-hero", "cond-carpal-hero") if it["name"].startswith(q + "-"))
                      for it in json.load(open(os.path.join(HERE, "audit_v2", "r2_plates.json"), encoding="utf-8"))}
    r2_pairs |= r2_plate_pairs
    r3c_pairs, r3c_out = batch_pairs("r3c_batch*.json")
    n_r3c = len(r3c_pairs)
    n_r3c_twice = len(r3c_pairs & set(r2a.get("still_failing", [])))  # no usable round-2 variant
    r2_note = f" ({r2_out} batch still being checked)" if r2_out else ""
    r3c_result = ("being checked now" if not sum(r3c.values()) else
                  f'<span class="stat good">{r3c["PASS"]} pass</span>, <span class="stat warn">{r3c["MINOR"]} minor</span>, '
                  f'<span class="stat bad">{r3c["FAIL"]} fail</span> across the {sum(r3c.values())} variants' + (" so far" if r3c_out else "; the best of each shot went in"))
    fin = counts(QA.values())
    n_r1, n_ov, n_ppl = round1_causes()
    n_photos1 = sum(r1.values())
    n_flare = flare_requests()
    n_overlay = sum(m["style"] == "overlay" for m in M)
    n_edit = sum(m["style"] == "editorial" for m in M)
    n_plate = sum(m["style"] == "plate" for m in M)
    n_plate_kept = sum(m["style"] == "plate" and "kept" in m["source"] for m in M)
    n_pages = len(by_page)
    hands = sum(len(e.get("hands", [])) for e in load_reports("audit_v2/batch*-report.json") + load_reports("audit_v2/r2_batch*-report.json"))
    lo, hi = n_flare * FLARE_EST[0], n_flare * FLARE_EST[1]
    test_rows = "".join(f"<tr><td>{esc(a)}</td><td class='num'>{b}</td></tr>" for a, b in TEST)
    notes = "".join(f"<li>{n}</li>" for n in extra_notes)

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AK Image Set v2</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Mulish:wght@400;600;700&display=swap">
<style>
:root{{--paper:#FFFDFA;--card:#F7F3EC;--ink:#232B31;--head:#1E2A33;--soft:#55606A;--line:#E4DCD0;--accent:#0a748a;--chip:#E4F4F7;--warn:#9a6a1a;--bad:#b3261e;--good:#1e7a4c;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root{{--paper:#1E2A33;--card:#263440;--ink:#E8EDF0;--head:#fff;--soft:#C3CDD4;--line:#3A4A56;--accent:#4FC0D8;--chip:#26404A;--warn:#f0c36a;--bad:#ff8a80;--good:#7fd6a8;color-scheme:dark}}}}
body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 "Mulish",system-ui,sans-serif}}
.wrap{{max-width:1500px;margin:0 auto;padding:32px 24px 72px;display:grid;gap:40px}}
h1,h2,h3{{font-family:"Playfair Display",Georgia,serif;color:var(--head);margin:0;text-wrap:balance}}
h1{{font-size:clamp(34px,4vw,56px);line-height:1.05}} h2{{font-size:32px}} h3{{font-size:22px}}
p{{margin:0;max-width:78ch}} .soft{{color:var(--soft)}}
.eyebrow{{font:700 12px/1.3 "Mulish";letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}}
.intro{{display:grid;gap:14px}} .lede{{font-size:18px}}
.cols{{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:grid;gap:8px;align-content:start}}
.box ul{{margin:0;padding-left:20px;display:grid;gap:6px}}
.stat,.num{{font-variant-numeric:tabular-nums;font-weight:700}} .bad{{color:var(--bad)}} .warn{{color:var(--warn)}} .good{{color:var(--good)}}
table{{border-collapse:collapse;width:100%;font-size:15px}} td{{padding:5px 0;border-bottom:1px solid var(--line);vertical-align:top}} td.num{{text-align:right;padding-left:12px}}
.before{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))}}
.before figure{{margin:0;display:grid;gap:4px}} .before img{{width:100%;height:auto;border-radius:10px;display:block}}
.before figcaption{{font-size:13px;color:var(--soft)}}
.group{{display:grid;gap:18px;border-top:1px solid var(--line);padding-top:16px}}
.page{{display:grid;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px}}
.page header{{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline}} .page header a{{font-size:13px;color:var(--accent);word-break:break-all}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));align-items:start}}
.card{{margin:0;display:grid;gap:8px}} .card img{{width:100%;height:auto;border-radius:12px;display:block;background:#111}}
.card figcaption{{display:grid;gap:4px;font-size:14px}} .pair{{display:grid;gap:6px;grid-template-columns:1fr 1fr}} .pair img{{width:100%;height:auto;border-radius:10px;display:block}} .card strong{{color:var(--head)}}
.tags{{display:flex;flex-wrap:wrap;gap:4px 10px}}
.tag{{font:700 11px/1.2 "Mulish";letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}} .tag--soft{{color:var(--soft)}}
.qa{{font-size:13px;color:var(--soft);display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}}
.qa .dot{{width:8px;height:8px;border-radius:50%;display:inline-block;background:var(--soft);flex:none;transform:translateY(-1px)}}
.qa--pass b,.qa--pass{{}} .qa--pass .dot{{background:var(--good)}} .qa--pass b{{color:var(--good)}}
.qa--pending .dot{{background:var(--accent)}} .qa--pending b{{color:var(--accent)}} .qa--minor .dot{{background:var(--warn)}} .qa--minor b{{color:var(--warn)}} .qa--fail .dot{{background:var(--bad)}} .qa--fail b{{color:var(--bad)}}
.qa-notes{{font-size:13px;color:var(--soft)}} .qa-notes summary{{cursor:pointer;color:var(--accent)}} .qa-notes ul{{margin:6px 0 0;padding-left:18px;display:grid;gap:4px}}
code{{font:12px/1.4 ui-monospace,Consolas,monospace;color:var(--soft);word-break:break-all}}
.mock summary{{cursor:pointer;font-weight:700;color:var(--accent);font-size:14px}} .mock{{display:grid;gap:10px}}
.mock img{{width:100%;max-width:820px;height:auto;border:1px solid var(--line);border-radius:10px;display:block}}
</style></head><body><div class="wrap">
<header class="intro">
  <p class="eyebrow">Sacramento Applied Kinesiology · inner pages · image set v2</p>
  <h1>Anatomy you can see, in a real clinic</h1>
  <p class="lede">The direction you picked: a real clinic, a glowing teal anatomy overlay of the structure each page talks about, and a soft red glow where it hurts, with the treatment aimed right at it. It's mixed with the illustration plates. <b>{n_overlay}</b> overlay photos, <b>{n_edit}</b> clinic photos and <b>{n_plate}</b> plates across <b>{n_pages}</b> pages. The photos are Higgsfield (Marketing Studio 2.5 Flare); {n_plate - n_plate_kept} plates were redrawn there, and {n_plate_kept} are kept from the first set (fal).</p>
</header>
<section class="cols" aria-label="What you asked for">
  <div class="box"><h3>A real room behind every shot</h3><p>Every photo is set in a real clinic (oak shelves, a window, equipment) with the room softly out of focus. No plain backdrops.</p></div>
  <div class="box"><h3>Red where it hurts</h3><p>Every overlay photo has a soft red-orange glow at the painful structure, and the hands, laser, PEMF coil or adjusting instrument work right on it.</p></div>
  <div class="box"><h3>Hands reviewed</h3><p>Independent reviewers zoomed in and counted every finger on every hand, and checked every body was whole and every overlay was the right way round: <b class="stat">{hands}</b> hands counted across both rounds.</p></div>
  <div class="box"><h3>Photos and plates, mixed</h3><p>The bone-only plates sit alongside the photos. The ones you liked stay; the ones with anatomy a chiropractor would catch were redrawn.</p></div>
</section>
<section class="cols" aria-label="Review and comparison">
  <div class="box"><h3>Review, round by round</h3>
    <ul><li><b>First pass:</b> <span class="stat bad">{r1["FAIL"]} of {n_photos1}</span> photos failed. {n_ov} had an overlay error (drawn upside down, shoulder blades on the lower back, extra vertebrae) and {n_ppl} a hand or body error (a third leg, a four-fingered hand, six toes). Plate redraws: <span class="stat bad">{r1p["FAIL"]}</span> of {sum(r1p.values())} failed.</li>
    <li><b>Round 2:</b> {len(r2_pairs) - len(r2_plate_pairs)} failed shots and {len(r2_plate_pairs)} plates re-rendered twice each with tighter prompts, then reviewed again: <span class="stat good">{r2["PASS"]} pass</span>, <span class="stat warn">{r2["MINOR"]} minor</span>, <span class="stat bad">{r2["FAIL"]} fail</span> across the variants{r2_note}; the better one of each pair went in.</li>
    <li><b>Round 3:</b> {len(r3a)} clinic shots redone (people had appeared in scenes meant to be empty, a three-fingered hand, a melted phone keypad), and {n_r3c} treatment shots were re-shot from a new angle: {n_r3c_twice} that had failed twice, and {n_r3c - n_r3c_twice} whose round-2 version had a flaw worth fixing (a spine off the body's axis, a foot with no heel bone, a crop that cut off the head). The fixes: face-down patients shot from the foot end, where the spine overlay lands right; one hand on the patient instead of a reach that grew a third arm; one foot seen from the side; a wider frame so the page crop keeps the head and toes. Reviewed again: {r3c_result}.</li>
    {notes}
    <li><b>In the set now:</b> <span class="stat good">{fin["PASS"]} pass</span>, <span class="stat warn">{fin["MINOR"]} with minor notes</span>, <span class="stat bad">{fin["FAIL"]} failed</span>{f', <span class="stat">{fin.get("PENDING", 0)}</span> re-rendered and in final review (this page updates when they clear)' if fin.get("PENDING") else ""}. Each image shows its result; open "Review notes" for the details.</li></ul></div>
  <div class="box"><h3>FAL vs Higgsfield</h3>
    <p>Same-prompt test, 6 renders per model, counting the ones that followed the brief:</p>
    <table>{test_rows}</table>
    <p>At full scale Flare still followed the poses, framing and devices, and that's why every photo here comes from it. The first pass failure rate ({r1["FAIL"]} of {n_photos1}) is higher than the first set's ({v1["FAIL"] - v1p["FAIL"]} of {sum(v1.values()) - sum(v1p.values())}), because every photo now has to get the anatomy overlay right as well. Hands and overlays still need a reviewer; no model gets them right every time. The full test: <a href="../compare/page/Photo-Direction-Test.html">compare/page/Photo-Direction-Test.html</a>.</p></div>
  <div class="box"><h3>Cost</h3>
    <ul><li>fal: first set <b class="stat">${FAL_V1:.2f}</b>, plus <b class="stat">${FAL_TEST:.2f}</b> for its half of the test.</li>
    <li>Higgsfield: at least <b class="stat">{n_flare}</b> Flare renders (every variant and redo, including the test), plus 12 Soul and Soul V2 test renders.</li>
    <li>Flare is billed by tokens and the API doesn't return the charge. At my estimate of ${FLARE_EST[0]:.2f}–{FLARE_EST[1]:.2f} per image that's about <b class="stat">${lo:.0f}–{hi:.0f}</b>. That figure is unverified; your Higgsfield console has the exact spend, and every render's request ID is saved next to it.</li></ul></div>
</section>
<section class="intro"><h2>What was wrong with the first set</h2>
  <div class="before">
    <figure><img src="ref/v1-cond-auto-treat.jpg" alt=""><figcaption>v1: the "back" is a pillow; no body below the shoulders.</figcaption></figure>
    <figure><img src="ref/v1-cond-frozen-treat.jpg" alt=""><figcaption>v1: the torso ends at the waist.</figcaption></figure>
    <figure><img src="ref/v1-cond-lbp-hero.jpg" alt=""><figcaption>v1: 4 lumbar vertebrae (there are 5).</figcaption></figure>
    <figure><img src="ref/v1-cond-carpal-hero.jpg" alt=""><figcaption>v1: the nerve runs over the ligament instead of under it.</figcaption></figure>
  </div>
</section>
{''.join(body)}
<section class="group"><h2>Files</h2>
  <p>In this repo: <code>final_v2/</code>. <code>full/</code> has full resolution, cropped to each slot's shape; <code>web/</code> has 1600 px versions for the pages; <code>manifest.json</code> lists which page and section each one is for.</p>
</section>
</div></body></html>"""
    open(os.path.join(OUT, "AK-Image-Set-v2.html"), "w", encoding="utf-8").write(page)
    print("page built:", len(M), "images,", len(mocks), "mockups; round1", r1, "round2", r2, "final", fin, "flare", n_flare)


if __name__ == "__main__":
    notes = json.load(open(os.path.join(HERE, "v2", "notes.json"))) if os.path.exists(os.path.join(HERE, "v2", "notes.json")) else []
    build(notes)

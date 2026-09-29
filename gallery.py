"""Build the review page (page/index.html + page/img, page/mock, page/ref) from final/manifest.json and shots/."""
import html
import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "page")
LIVE = "https://carlcelinodspnza.github.io/applied-kinesiology-sacramento-preview/"
M = json.load(open(os.path.join(HERE, "final", "manifest.json")))
SURVEY = json.load(open(os.path.join(HERE, "site", "survey.json")))
COST = os.environ.get("COST", "")

GROUPS = [
    ("Conditions", "conditions/", "Nine older condition pages had three line-drawing placeholders each: a hero, an "
     "assessment panel and a treatment panel. Each now gets a plate for its hero and photographs of the assessment and "
     "the treatment that page describes. The ten newer condition pages already had two plates each, so they get one "
     "treatment photograph for their full-width treatment section."),
    ("Services", "services", "The service pages reused plates that did not match their subject: a knee on cold laser, "
     "FX-635 and PEMF, and a spine on the hub. Each now shows its own instrument in use. The thyroid plate is redrawn "
     "because the current one does not show a thyroid."),
    ("Applied kinesiology", "applied-kinesiology", "The method pages get the muscle test itself: an arm test, a close "
     "test of the forearm, the balance the page describes, and the chain the page describes."),
    ("About", "about", "No likeness of Dr. Van Wagenen is invented. His real portrait stays; around it, only rooms, "
     "hands and objects."),
    ("Patient information", "patient-info", "First visit, FAQ and forms: the conversation, the examination, and what "
     "to bring."),
    ("Booking", "book", "The front desk, the phone and the appointment book."),
]


def title_of(page):
    slug = page.split(" ")[0].strip().replace("/", "__")
    d = SURVEY.get(slug)
    if not d:
        return page
    h1 = next((x for t, x in d["h"] if t == "h1"), None)
    return h1 or d["title"]


def esc(s):
    return html.escape(s or "", quote=True)


def resized(src, dst, long_side, q):
    im = Image.open(src).convert("RGB")
    im.thumbnail((long_side, long_side), Image.LANCZOS)
    im.save(dst, quality=q)
    return im.size


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for d in ("img", "mock", "ref"):
        os.makedirs(os.path.join(OUT, d))
    by_page = {}
    for m in M:
        key = m["page"].split(" ")[0]
        by_page.setdefault(key, []).append(m)
    # a page listed as "applied-kinesiology (+ faq, ...)" is the image's first home; mockups show every placement
    sizes = {}
    for m in M:
        sizes[m["name"]] = resized(os.path.join(HERE, m["full"]), os.path.join(OUT, "img", m["name"] + ".jpg"), 1100, 82)
    mocks = {}
    for f in sorted(os.listdir(os.path.join(HERE, "shots"))):
        if f.endswith("__after.png"):
            slug = f[:-len("__after.png")]
            im = Image.open(os.path.join(HERE, "shots", f)).convert("RGB")
            w = 760
            im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
            im.save(os.path.join(OUT, "mock", slug + ".jpg"), quality=78)
            mocks[slug] = im.size
    for src in ("img_clinic_method_muscle_test.jpg", "gen_anatomy_knee_joint.jpg"):
        resized(os.path.join(HERE, "site", "assets", src), os.path.join(OUT, "ref", src), 700, 84)
    total = len(M)
    extras = sum(1 for m in M if m.get("extra"))
    pages_with = len({p for p in by_page})

    def also(m):
        where = {"ak-balance": "also placed on Is Muscle Testing Real? and the FAQ",
                 "ak-mtest": "also placed on Your First Visit",
                 "ak-legit-hero": "also placed on the FAQ"}.get(m["name"])
        return f'<span class="slot">{esc(where)}</span>' if where else ""

    def card(m):
        w, h = sizes[m["name"]]
        extra = '<span class="tag tag--extra">extra</span>' if m.get("extra") else ""
        kind = "Plate" if m["style"] == "plate" else "Photograph"
        return (f'<figure class="card"><div class="media" style="aspect-ratio:{w}/{h}"><img src="img/{m["name"]}.jpg" '
                f'width="{w}" height="{h}" loading="lazy" alt="{esc(m["section"])}"></div>'
                f'<figcaption><span class="tag">{kind} · {m["aspect"]}</span>{extra}<strong>{esc(m["section"])}</strong>'
                f'<span class="slot">{esc(m["slot"])}</span>{also(m)}<code>{m["name"]}.jpg</code></figcaption></figure>')

    body = []
    for gname, prefix, blurb in GROUPS:
        keys = [k for k in by_page if k.startswith(prefix)]
        keys.sort(key=lambda k: (k.count("/"), k))
        if not keys:
            continue
        n_img = sum(len(by_page[k]) for k in keys)
        body.append(f'<section class="group" id="{prefix.strip("/").replace("/", "-")}"><div class="group__head"><h2>{gname}</h2>'
                    f'<p class="count">{len(keys)} pages · {n_img} images</p></div><p class="blurb">{esc(blurb)}</p>')
        for k in keys:
            slug = k.replace("/", "__")
            items = sorted(by_page[k], key=lambda m: (m.get("extra", False), m["name"]))
            mock = ""
            if slug in mocks:
                mw, mh = mocks[slug]
                mock = (f'<details class="mock"><summary>See it on the page</summary><p class="hint">A local copy of the live '
                        f'page with these images dropped in. Nothing on the live site was changed.</p>'
                        f'<img src="mock/{slug}.jpg" width="{mw}" height="{mh}" loading="lazy" alt="Mockup of {esc(title_of(k))}"></details>')
            body.append(f'<article class="page"><header class="page__head"><h3>{esc(title_of(k))}</h3>'
                        f'<a href="{LIVE}{k}/" target="_blank" rel="noopener">/{k}/</a></header>'
                        f'<div class="grid">{"".join(card(m) for m in items)}</div>{mock}</article>')
        body.append("</section>")
    return total, extras, pages_with, "\n".join(body)


CSS = """
:root{--paper:#FFFDFA;--card:#F7F3EC;--warm:#F2EADF;--ink:#232B31;--head:#1E2A33;--soft:#55606A;--line:#E4DCD0;
--accent:#0a748a;--accent-2:#0E9BB8;--chip:#E4F4F7;--shadow:0 1px 2px rgb(30 42 51/6%),0 8px 24px rgb(30 42 51/7%);color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#1E2A33;--card:#263440;--warm:#223039;--ink:#E8EDF0;
--head:#FFFFFF;--soft:#C3CDD4;--line:#3A4A56;--accent:#4FC0D8;--accent-2:#2fb3ce;--chip:#26404A;--shadow:none;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#1E2A33;--card:#263440;--warm:#223039;--ink:#E8EDF0;--head:#FFFFFF;--soft:#C3CDD4;
--line:#3A4A56;--accent:#4FC0D8;--accent-2:#2fb3ce;--chip:#26404A;--shadow:none;color-scheme:dark}
body{background:var(--paper);color:var(--ink);font:16px/1.6 "Mulish",system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding-inline:16px;padding-block:32px 72px;display:grid;gap:44px}
h1,h2,h3{font-family:"Playfair Display",Georgia,"Times New Roman",serif;color:var(--head);margin:0;text-wrap:balance}
h1{font-size:clamp(34px,6vw,56px);line-height:1.05;font-weight:600}
h2{font-size:clamp(26px,4vw,34px);font-weight:600}
h3{font-size:22px;font-weight:600}
p{margin:0;max-width:70ch}
.eyebrow{font:700 12px/1.3 "Mulish",sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.intro{display:grid;gap:16px}
.lede{font-size:18px;color:var(--ink)}
.stats{display:flex;flex-wrap:wrap;gap:8px 20px;font-size:14px;color:var(--soft)}
.stats b{color:var(--head);font-variant-numeric:tabular-nums}
.looks{display:grid;gap:20px;grid-template-columns:1fr}
@media (min-width:860px){.looks{grid-template-columns:1fr 1fr}}
.look{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;display:grid;gap:12px;box-shadow:var(--shadow)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.pair figure{margin:0;display:grid;gap:6px}
.pair img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:10px;display:block}
.pair figcaption{font-size:12.5px;color:var(--soft)}
.rules{margin:0;padding-left:20px;display:grid;gap:8px;max-width:78ch}
.toc{display:flex;flex-wrap:wrap;gap:8px}
.toc a{background:var(--chip);color:var(--accent);text-decoration:none;font-weight:700;font-size:14px;padding:7px 12px;border-radius:999px}
.group{display:grid;gap:18px;padding-top:12px;border-top:1px solid var(--line)}
.group__head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px}
.count{font-size:14px;color:var(--soft)}
.blurb{color:var(--soft)}
.page{display:grid;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:var(--shadow)}
.page__head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px}
.page__head a{font-size:13px;color:var(--accent);word-break:break-all}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));align-items:start}
.card{margin:0;display:grid;gap:10px}
.media{width:100%;max-width:100%;border-radius:12px;overflow:hidden;background:var(--warm)}
.media img{display:block;width:100%;height:100%;object-fit:cover}
.card figcaption{display:grid;gap:4px;font-size:14px}
.card strong{color:var(--head);font-size:15px;line-height:1.35}
.slot{color:var(--soft);font-size:13px}
.tag{font:700 11px/1.2 "Mulish",sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.tag--extra{color:#9a6a1a}
code{font:12px/1.4 ui-monospace,Consolas,monospace;color:var(--soft);word-break:break-all}
.mock summary{cursor:pointer;font-weight:700;color:var(--accent);font-size:14px}
.mock{display:grid;gap:10px}
.mock img{width:100%;max-width:760px;height:auto;border:1px solid var(--line);border-radius:10px;display:block}
.hint{font-size:13px;color:var(--soft)}
.left{display:grid;gap:10px}
.left ul{margin:0;padding-left:20px;display:grid;gap:6px;max-width:78ch}
.files code{font-size:13px}
"""


def page_html(total, extras, pages_with, groups_html):
    return f"""<title>Sacramento AK Image Set</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Mulish:wght@400;600;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header class="intro">
  <p class="eyebrow">Sacramento Applied Kinesiology · preview site</p>
  <h1>Images for every page after the home page</h1>
  <p class="lede">I read all 47 inner pages and wrote each image for the section it sits beside. They match the two looks the home page already uses: warm, window-lit clinic photographs in cream and sage, and deep-teal anatomy plates on cream paper.</p>
  <p class="stats"><span><b>{total}</b> images</span><span><b>{pages_with}</b> pages</span><span><b>{extras}</b> extras</span><span>Nano Banana Pro, with the home page's own images as the style reference</span>{f'<span>{COST}</span>' if COST else ''}</p>
</header>
<section class="looks" aria-label="How the new images match the home page">
  <div class="look"><h3>Clinic photographs</h3><div class="pair">
    <figure><img src="ref/img_clinic_method_muscle_test.jpg" alt="Home page photograph"><figcaption>On the home page now</figcaption></figure>
    <figure><img src="img/ak-mtest.jpg" alt="New photograph"><figcaption>New: muscle testing, in plain terms</figcaption></figure></div></div>
  <div class="look"><h3>Anatomy plates</h3><div class="pair">
    <figure><img src="ref/gen_anatomy_knee_joint.jpg" alt="Home page plate"><figcaption>On the home page now</figcaption></figure>
    <figure><img src="img/cond-oa-hero.jpg" alt="New plate"><figcaption>New: osteoarthritis, narrowed joint space</figcaption></figure></div></div>
</section>
<section class="intro" aria-label="Rules">
  <h2>Rules every image follows</h2>
  <ul class="rules">
    <li><strong>No faces.</strong> The home page never shows one, so patients face away or down into the table's face cradle, and the practitioner is cropped at the chest.</li>
    <li><strong>One practitioner.</strong> The site says one licensed practitioner does everything, so every photograph shows the same person: a man's hands in a white shirt with the sleeves rolled. No white coats and no second clinician. No likeness of Dr. Van Wagenen is invented.</li>
    <li><strong>Instruments as the site describes them.</strong> The FX-635 is fixed heads over a patient lying still. Cold laser is a small handheld probe. PEMF is a coil. The adjusting instrument is a spring tool, not anything that could read as a needle.</li>
    <li><strong>Nothing to fact-check.</strong> No text, labels, brands or readable screens, and no before-and-after or "cured" imagery, in keeping with the site's "what we will not claim" tone.</li>
  </ul>
  <nav class="toc" aria-label="Sections"><a href="#conditions">Conditions</a><a href="#services">Services</a><a href="#applied-kinesiology">Applied kinesiology</a><a href="#about">About</a><a href="#patient-info">Patient information</a><a href="#book">Booking</a><a href="#left">Left as they are</a></nav>
</section>
{groups_html}
<section class="group left" id="left">
  <h2>Left as they are</h2>
  <ul>
    <li><strong>Diagrams that carry facts</strong> stay as drawings. That covers the contact timeline (1994, 2007), the street plan of North Sunrise Avenue, the office-hours strip, the paperwork steps, the sitemap tree, and the "two lines, one conclusion" and "treated in pieces" diagrams. An AI image would blur or invent the facts they show.</li>
    <li><strong>Legal and utility pages</strong> (privacy, terms, accessibility, healthcare disclaimer, good faith estimate, sitemap, service area, contact, testimonials) have no picture slots, and imagery would add nothing. Testimonials in particular should not get photographs that imply results.</li>
    <li><strong>Plates that already fit</strong> stay: the plantar fascia, sciatic nerve, pelvis, rotator cuff, digestive and endocrine plates, and the real portrait.</li>
  </ul>
</section>
<section class="group files">
  <h2>Where the files are</h2>
  <p>On your machine in <code>ace/Code/higgsfield/outputs/ak-sacramento/final/</code>. <code>full/</code> holds each image at full resolution, cropped to its slot's shape; <code>web/</code> holds the same images at 1600 px for the pages. The file names are the ones shown on each card.</p>
</section>
</div>
"""


if __name__ == "__main__":
    total, extras, pages_with, groups_html = build()
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page_html(total, extras, pages_with, groups_html))
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
    print(f"page built: {total} images, {pages_with} pages, {n} files, {size / 2**20:.1f} MiB")

# Sacramento Applied Kinesiology: inner-page images

Images for every inner page of the preview site
(https://carlcelinodspnza.github.io/applied-kinesiology-sacramento-preview/), made 28 Sep 2026: a real clinic in every
photo, a glowing teal anatomy overlay of the structure each page talks about, a soft red glow where it hurts, and
engraving-style illustration plates alongside.

## What's here

| Path | What it is |
|---|---|
| `final_v2/web/` | The 57 images for the site: 1600 px, already cropped to each slot's shape. |
| `final_v2/full/` | The same 57 at full resolution. |
| `final_v2/placements.csv` | **Start here to place images.** One row per placement (61 on 35 pages): the page, what the image replaces or where its new frame goes, the file and its alt text. |
| `final_v2/manifest.csv` / `.json` | One row per image: page, section, slot, size, alt text, which model made it. |
| `final_v2/alternatives/` | An image the owner may prefer that did **not** pass review. Not part of the set (see open decisions). |
| `page_v2/AK-Image-Set-v2.html` | The review page: every image with its review result, and a mockup of each page with the images in place. Open it in a browser. |
| `v2/final_qa.json` | The review verdict and notes for every image. |
| `audit_v2/`, `audit/` | Review inputs and reports for every round (second set and first set). |
| `jobs*.json`, `shotlist*.json`, `plates*_jobs.json` | Every prompt that was sent. |
| `*.py`, `*.mjs`, `*.mts` | The pipeline (below). |
| `compare/page/` | The fal vs Higgsfield same-prompt test page. |

## Placing the images (for the developer)

- Use `final_v2/web/<image>.jpg` and the `alt_text` column from `placements.csv`.
- **action = replace**: swap out the placeholder named in `where` (its current file or its aria-label, and the heading
  it sits under). If it is an `<img>` inside the site's frame, change the `src` and keep the frame.
- **action = new frame** (12 pages had no image slot where the image belongs): turn the named section's full-width text
  column into the site's own 7/5 split (text in 7 columns, a frame in 5) and put the image in the frame.
- Three images are used on more than one page (`ak-balance`, `ak-mtest`, `ak-legit-hero`); `placements.csv` lists
  every placement.
- The mockups on the review page ("See it on the page") show each page with the images placed this way.

## Review status

57 images: **19 pass, 38 with minor notes, 0 failed.** Every image was checked by an independent reviewer at zoom
(every finger and toe counted, every body whole, anatomy placed and oriented correctly, no stray text). Minor notes are
listed per image in `v2/final_qa.json` and on the review page.

## Open decisions (owner)

1. **Carpal tunnel hero plate.** The set uses the redraw that passed review. The owner's favourite first-set hand plate,
   edited so the nerve runs under the ligament band, is in `final_v2/alternatives/`. It failed review: the finger
   outlines fused with the nerve at the web spaces, and the band reads as a wristband. Use it only if the owner prefers
   that look, and fix those outlines first.
2. **Pinched nerve hero plate** shows a lower-back (lumbar) segment rather than the neck. It was accepted because the
   page copy talks about nerves leaving the spine in general. The site also has a sciatica page covering the lower back.

## Not in git (about 3.8 GB, kept on the machine that made them)

The uncropped renders of every final (`v2/renders/`, `v2/plates/`), every rejected render and round variant, the review
crops, the mockup screenshots and mirrors, the saved copy of the preview site (`site/`), and the rejected first set
(`final/`, `renders/`, `page/`). Rebuilding the
finals from source needs `v2/renders/` and `v2/plates/`.

## How it was made

1. `shots_v2.py` writes the prompts (`jobs_v2.json`); `hf-batch.mts` renders them on Higgsfield Marketing Studio 2.5
   Flare. It imports the API wrapper from our Higgsfield toolkit
   ([jc1147/higgsfield-playbook](https://github.com/jc1147/higgsfield-playbook)), so run it from a checkout of that repo,
   with this repo at `outputs/ak-sacramento`.
2. `audit_v2_prep.py` makes review batches; independent reviewers write `audit_v2/*-report.json`.
3. Fix rounds: `shots_v2r2.py`, `shots_v2r3.py`, `shots_v2r3c.py` (prompts), then `apply_r2.py`, `apply_r3.py`,
   `apply_r3c.py`, `apply_r3p.py` (picks go to `v2/renders/`, replaced renders are parked in `v2/rejected/`). Reviewer
   picks and overruled points (with reasons) are in `v2/r2_reviewer_picks.json`, `v2/r2_waivers.json` and
   `v2/plate_waivers.json`.
4. `qa_v2.py` (review record per image), `finalize_v2.py` (crops, manifest, CSV, alternatives), `placements.py`.
5. `SET=v2 python mockups.py build` then `shoot` (page mockups), and `gallery_v2.py` (the review page).


## Cost

At least 157 Higgsfield Flare renders, about $31–47 at an estimated $0.20–0.30 each. That estimate is unverified: the
Higgsfield API does not return the charge, and the console has the real spend. The rejected first set cost about
$12.39 on fal (Nano Banana Pro).

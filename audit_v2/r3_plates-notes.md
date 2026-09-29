# r3_plates review notes (round-3 plate edits)

Method: full-size Read of each plate + crops in audit_v2/crops/r3p__<name>__*.png (2-4x LANCZOS, full-image
fraction ticks in the top/left margin). Numeric checks with scratchpad r3p_measure.py (paper-deviation components,
faint-smudge scan, 8x contrast-amplified crops, row/column ink scans). Boxes are full-image fractions [x0,y0,x1,y1].
Sources opened read-only; md5 recorded before review in scratchpad r3p_md5_before.txt.
Page crop: all four plates are 2048x1360 (3:2); the 7:5 page crop removes x<0.035 and x>0.965 (72 px each side).

## 1. cond-auto-hero-c-edit-a (pair cond-auto-hero) -- verdict MINOR

Crops read: column_overview, c1_c2, c3_c4, c5_c6, c7_bottom, c7_junction_4x, bottom_amp (8x contrast), plus the
pre-edit source cond-auto-hero-c full image and its orig_bottom crop for comparison.

COUNTS
- Vertebrae: 7 = C1 atlas (ring + posterior arch/tubercle at x 0.40-0.43, y 0.14-0.18, plus an anterior body-like block
  x 0.575-0.605, y 0.135-0.205) + 6 vertebral bodies C2-C7:
  C2 y 0.22-0.30, C3 0.33-0.41, C4 0.43-0.505, C5 0.525-0.605, C6 0.625-0.705, C7 0.735-0.835.
- Posterior elements: 7 (atlas tubercle + 6 spinous processes). Tips: C2 x0.39 y0.25-0.32 (largest, bifid-looking tip),
  C3 0.436/0.385, C4 0.43/0.49, C5 0.43/0.575, C6 0.43/0.67, C7 0.405/0.78 (longest of C3-C7 = vertebra prominens, correct).
- Disc bands: 6 (under the atlas block y~0.215, then 0.31, 0.41, 0.51, 0.61, 0.71). No disc below C7; the column ends
  on C7's closed lower endplate (y ~0.835), as the edit asked.
- Rings: exactly 3, concentric. Row y 0.49: left crossings x 0.377/0.396/0.414, right 0.606/0.624/0.643 -> common
  centre x 0.510, radii 272/234/197 px, centred on C4 (mid-neck). No partial 4th ring.
- Pre-edit source had 8 vertebrae (8th body y 0.84-0.93). The edit removed one: anterior-edge profile of edit-a matches
  the source to 1-2 px from y 0.13 to 0.72 (C1-C6 untouched); the new C7 sits where the source's 7th was but carries the
  source's 8th-vertebra shape (flared posterior-inferior body, long spinous process).

EDIT QUALITY (the bottom of the column)
- C7 is complete: closed outline all round, top endplate y~0.745, concave anterior wall x~0.578, sloping lower endplate
  (0.511,0.818)->(0.576,0.837) (re-measured on the 4x crop); posterior-inferior "heel" of the body reaches back to x~0.51
  (same stylisation as the source's 8th vertebra); lamina + spinous process complete and closed.
- Below C7 (x 0.36-0.68, y 0.835-0.99): blurred deviation from paper mean 1.88 / p99 4.4 vs reference paper at the top of
  the plate mean 1.77 / p99 4.9 -> identical. The only object in that box is C7's own lower outline. The 8x amplified
  crop shows only uniform paper grain: no ghost outline, patch, smudge or open line where the removed vertebra was.
- Stray-mark scan (non-paper components, thr 40): every component lies inside the column/ring area
  [0.376,0.077,0.645,0.839]; nothing elsewhere on the paper; nothing in the 7:5 crop strips.
- Negligible: a 2-3 px cream nick in the dark outline where C7's spinous-process underside meets the body
  (~0.498,0.772); reads as an engraving highlight, not an open outline; invisible at page size. (The source's 8th
  vertebra had the same kind of nick.)

ANATOMY (a chiropractor would notice; all INHERITED from the base plate, identical in edit-b's upper column)
- Atlas drawn with a body-like anterior block and a disc band under it (C1 has no body; there is no C1-C2 disc).
  The spec's own wording ("C1 the atlas at the top, then six vertebral bodies C2-C7") matches this drawing, so it is
  counted as C1, but it is anatomically loose. Box [0.555,0.09,0.61,0.225].
- Lordosis is weak: anterior body edges (mid-height x) C2 0.592, C3 0.584, C4 0.590, C5 0.585, C6 0.579, C7 0.574.
  Against the C2-C7 chord, C4-C5 sit only ~0.005 (about 10 px) forward (sagitta ~1.4% of the 708 px span, about 6-7
  degrees of arc) and C3 sits slightly behind it. The middle does bow toward the body side, so the spec is technically
  met, but the neck reads nearly straight, slightly inclined forward at the top. Box [0.52,0.20,0.61,0.84].
- C2 has the largest spinous process (correct). No skull. The bodies are waisted with flared lips, which fits the style.

OTHER
- No text, letters, numbers or labels anywhere. Style unchanged (teal engraving, pale-teal fill, cream paper, halo glow).
- Frame: column spans x 0.376-0.645, y 0.077-0.839; nothing cut off; 7:5 strips empty. After the removal the subject
  sits a little high (top margin 0.077 vs bottom 0.161); acceptable.

Verdict: MINOR. The edit itself is clean and complete (7 vertebrae, no leftovers). The only listed items are inherited
anatomy: an atlas with a body-like block and C1-C2 disc band, and a weak (near-straight) lordosis.

## 2. cond-auto-hero-c-edit-b (pair cond-auto-hero) -- verdict MINOR

Crops read: column_overview, c1_c2, c3_c4, c5_c6, c7_bottom, c7_junction_4x, bottom_amp (8x contrast), and the
three-panel lower-column comparison r3p__cond-auto-hero__lower_compare_src_a_b.png (source / edit-a / edit-b).

COUNTS
- Vertebrae: 7 = C1 atlas (same drawing as edit-a: ring, posterior tubercle, anterior body-like block) + 6 bodies:
  C2 y 0.22-0.30, C3 0.33-0.41, C4 0.43-0.505, C5 0.525-0.605, C6 0.62-0.70, C7 0.735-0.827.
- Posterior elements: 7; C2 spinous largest (x 0.39-0.52); C7 spinous longest of C3-C7 (tip x~0.405, y 0.76-0.785).
- Disc bands: 6 (under the atlas block, C2/3, C3/4, C4/5, C5/6, C6/7). Column ends on C7's closed lower endplate.
- Rings: exactly 3, concentric. Row y 0.49: left 0.377/0.396/0.414, right 0.607/0.625/0.643 -> centre x 0.510.

EDIT QUALITY
- Most faithful of the pair to "remove only the lowest vertebra": blurred luminance diff vs the source is tiny
  everywhere above y 0.70 (band means 1.8-2.8, p99 <= 14.3); all large differences sit at y 0.77-0.92 (the removed 8th
  vertebra, its disc and its long spinous process) plus the redrawn lower edge of C7. Edit-a, by contrast, also redrew
  parts of C6/C7 (diff p99 88 at y 0.6-0.7), which does not matter visually but is less faithful to the source.
- C7 is complete: closed outline, top endplate ~0.735, lower endplate (0.503,0.804)->(0.576,0.827), posterior-inferior
  "heel" reaching x~0.503 (edit-a ~0.511; same stylisation as the source's 8th vertebra). Outline at the
  spinous/body junction is continuous (no nick, unlike edit-a).
- Below C7 (x 0.36-0.68, y 0.83-0.99): mean deviation 1.34 / p99 4.4, the same as clean reference paper (1.34 / 3.5).
  The only faint object (max dev 10.6) hugs C7's lower outline = the style's normal light halo. The 8x amplified crop
  shows uniform paper grain: no ghost of the removed vertebra, patch, smudge or open outline.
- Stray-mark scan: every non-paper component lies inside [0.376,0.0765,0.645,0.828] (column + rings); nothing elsewhere,
  nothing in the 7:5 crop strips.

ANATOMY (inherited from the base plate, identical to edit-a)
- Atlas drawn with a body-like anterior block and a disc band under it (no C1 body / no C1-C2 disc in reality).
  Box [0.555,0.09,0.61,0.225].
- Weak lordosis: anterior edges C2 0.592, C3 0.584, C4 0.590, C5 0.584, C6 0.576, C7 0.5725. C4-C5 sit about 0.005-0.006
  in front of the C2-C7 chord (~10-12 px), so the neck reads nearly straight, tilted forward at the top.
  Box [0.52,0.20,0.61,0.83].

OTHER
- No text/labels. Style unchanged. Nothing cut off; subject x 0.376-0.645, y 0.0765-0.828 (sits slightly high:
  top margin 0.077, bottom 0.172). 7:5 strips empty.

Verdict: MINOR (same inherited items as edit-a; the edit itself is clean).

PAIR cond-auto-hero -> pick edit-b (marginal). Both edits reach 7 vertebrae with clean paper below. Edit-b keeps C1-C6
essentially pixel-faithful to the approved source (only the lowest vertebra and its disc were removed), and its C7
outline is continuous; edit-a has a 2-3 px outline nick and redrew more of the lower column than asked. Neither fixes
the inherited near-straight curve or the atlas "body" + C1-C2 disc band.

## 3. cond-carpal-hero-v1edit-a (pair cond-carpal-hero) -- verdict FAIL

Crops read: wrist_band, band_top_end, band_bottom_end, nerve_entry_left, nerve_exit_right, nerve_branches, thumb, index,
middle, ring, little, webs_fingers, fingers_webs, web_index_middle_4x, web_mid_ring_little_4x, web_thumb_index (in thumb),
forearm_left; comparisons r3p__cond-carpal-hero__pageview_orig_a_b, __right_edge_pagecrop, __wrist_orig_a_b and the
original's r3p__cond-carpal-hero-orig__fingers_webs. Original = final/full/cond-carpal-hero.jpg (2374x1696, 7:5).

COUNTS
- Digits 5. Thumb: metacarpal (0.40-0.52,0.23-0.40) + proximal (0.52-0.62) + distal phalanx (0.62-0.665) = 2 phalanges.
  Index MC + 3 phalanges (P1 0.64-0.77, P2 0.77-0.84, P3 0.84-0.88); middle MC + 3 (0.64-0.78, 0.78-0.87, 0.87-0.93);
  ring MC + 3 (0.62-0.765, 0.765-0.84, 0.84-0.895); little MC + 3 (0.61-0.72, 0.72-0.78, 0.78-0.82). Metacarpals 5.
- Carpals: mostly hidden by the new wide band (inherent to "band across the whole wrist"). Visible: 2 partial
  proximal-row bones left of the band, 4 distal-row bones right of it (trapezium, trapezoid, capitate, hamate).
  Radius (thumb side) and ulna correct.
- Nerve branches: 4 = thumb (up the thumb's ulnar side to P1), index (fork at 0.643,0.46 -> P1 of index),
  middle/ring (branch from 0.54,0.48 curving over the middle MC to end at 0.61,0.575 between the middle and ring MC
  heads = the thumb side of the ring finger). No branch to the little finger.

REQUESTED EDIT
- Band across the WHOLE wrist: yes. It is a wide straight fibred band x 0.316-0.39, from the top skin outline (y~0.35-0.38)
  to the bottom skin outline (y~0.68). Its ends are NOT "clean ends inside the outline": the band runs into the skin
  outline at both ends and bridges the soft tissue above the radius and below the ulna, so it reads as a wrist strap
  or bracelet rather than the transverse carpal ligament (which spans the carpal bones). Its right edge is frayed into
  hairy dark fringes at both ends: (0.375-0.395,0.33-0.38) and (0.385-0.395,0.62-0.685).
- Nerve UNDER the band: yes, correct. It meets the band's left edge at x~0.332, y 0.51-0.535; the band's edge line
  runs unbroken over it; it reappears at the right edge x~0.398, y 0.475-0.49, with the thumb branch forking right
  at that edge.
- Web spaces: NOT fixed, and worse than the original. In the original every finger has a complete skin outline with
  U-turn webs (each ending in a small open curl). In edit-a:
  * index-middle web is formed by the nerve itself: the index's lower skin outline and the middle's upper skin outline
    grow out of the nerve fork at (0.643-0.665,0.44-0.478); no U-shaped web; nerve and skin outline fused.
  * middle finger's lower outline ends by fusing into the MCP/P1 bone contour at (0.655-0.66,0.565).
  * ring finger has NO upper skin outline along P1-P2 (x 0.62-0.84); its outline starts at the DIP (0.84,0.627),
    so it is only a cap around the tip. Its lower outline ends on the little finger's P1 at (0.635,0.70).
  * little finger's upper outline only starts at P2 (0.745,0.748).
  * thumb-index web: clean U-turn at (0.535,0.30). This is the only good web.
- Old band leftover: none (the old thumb-side band is fully replaced). No patches. No text or labels.
  Stray-mark scan: 1 isolated 5 px fleck (hatching, 0.122,0.454) only. A tiny star-shaped hatch fleck under the nerve
  at (0.426,0.49) is negligible.

STYLE / COMPOSITION
- Colours kept: ink median (10,68,79) vs original (21,67,77); pale-teal fill (201,232,224) vs (200,228,219); paper
  (251,244,225) vs (252,242,225). Engraved line work and hatching match.
- Composition changed: the hand is re-framed about 7% larger (ink bbox 1874x966 px vs the original's 2180x1138 scaled
  to 1748x913) and sits lower (bottom 0.809 vs 0.770). After the page's 7:5 crop (x 72-1976) the middle fingertip
  outline (x 1966) is only about 10 px from the right edge, and the forearm lines (x 92) about 20 px from the left edge.
  The original had about 92/101 px. Nothing is actually cut, but the hand is cramped against both page edges.

Verdict: FAIL. The anatomy fix works (5 digits / 14 phalanges, band across the wrist, nerve under it, no little-finger
branch). But the explicit requirement that finger outlines join the palm cleanly at the web spaces is not met: 3 of 4
finger webs are missing and the nerve fuses into the index-middle web. The loved soft hand outline is visibly degraded
(the ring and little fingers lose their proximal outline). Also: band ends run into the skin outline (strap look) and
the page-crop margins are tight.

## 4. cond-carpal-hero-v1edit-b (pair cond-carpal-hero) -- verdict FAIL

Crops read: wrist_band, band_top_end, band_bottom_end, patch_4x, nerve_entry_left, nerve_entry_band_5x, nerve_exit_right,
nerve_branches, thumb, index, middle, ring, little, fingers_webs, web_index_middle_4x, web_mid_ring_little_4x,
specks_ring_little_4x, mark_thumb_index_4x, carpals_right, forearm_left, plus the shared side-by-side comparisons
(pageview, right_edge_pagecrop, wrist_orig_a_b) and the original's carpals / fingers_webs crops.

COUNTS
- Digits 5: thumb MC + 2 phalanges (0.52-0.62, 0.62-0.66); index, middle, ring, little each MC + 3 phalanges
  (same bone layout as edit-a). Metacarpals 5. Carpals mostly under the band: 2 partial proximal-row bones left of it,
  trapezium/trapezoid/capitate/hamate right of it (same as edit-a; plausible articulation with the MC bases).
- Nerve branches: thumb (with a small twig at the thumb MCP ~0.515,0.30), index (fork at 0.65,0.455 -> P1),
  middle (digital branch running along P1 and tapering over P2 at 0.845,0.52, as in the original), ring thumb side
  (branch from 0.54,0.475 across the middle MC then along the radial edge of ring P1). No little-finger branch.

REQUESTED EDIT
- Band across the WHOLE wrist: yes, a gently curved fibred band x ~0.325-0.395. Like edit-a it runs from the top skin
  outline to the bottom one (strap look), not "clean ends inside the outline". Top end cleaner than edit-a (crisp edge).
- Nerve UNDER the band: yes, correct. Squared nerve end at x~0.346 just short of the band's continuous left edge line
  (0.35) at y 0.505-0.525; it reappears at the right edge x~0.398 with the thumb fork there.
- LEFTOVER PATCH (new defect): a pale hatched quadrilateral at [0.378,0.641,0.405,0.702], right of the band's lower end
  over the hamate/pisiform area. Uneven horizontal hatch strokes, ragged right edge with no outline, lowest strokes
  lying on the skin outline. It reads as a stray band fragment and is visible at page size.
- Web spaces: NOT fixed (same failure as edit-a, plus one worse detail):
  * index-middle web = nerve fork at (0.64-0.665,0.44-0.478): both finger skin outlines grow out of the nerve.
  * middle's lower outline fuses into the MCP/P1 bone at (0.655,0.565).
  * the ring-side nerve branch runs along the upper contour of ring P1, merges into it at ~(0.735,0.62), and the ring's
    upper skin outline starts right there (0.745,0.62). Nerve, bone edge and skin outline read as one line.
  * ring's lower outline only begins at ~(0.745,0.683); no ring-little web.
  * little finger's upper outline is broken: a dark stub (0.705-0.727,0.725) ending in a dot, a faint grey section to
    0.765, solid only after that.
  * thumb-index web: clean U-turn at (0.535,0.31).
- Stray marks: a ~6 px diagonal dash at (0.714,0.692) and several dust dots (0.695-0.735,0.697-0.712) on the paper in
  the ring-little gap; two tiny dots near the left edge (0.043-0.046,0.59-0.60). Tiny, but real. (The scan hits at
  0.53,0.415 and 0.241,0.44 are hatch dashes inside bones, not defects.) No text or labels.

STYLE / COMPOSITION
- Colours kept (ink median (7,65,77), fill (201,233,223), paper (252,244,226)); line work matches.
- Same re-framing as edit-a: hand ~7% larger; after the 7:5 page crop the middle fingertip outline (x 1968) is only
  about 8 px from the right edge and the forearm lines (x 89) about 17 px from the left edge (original ~92/101 px).
  Nothing cut, but cramped.

Verdict: FAIL. It shares edit-a's broken web-space / soft-outline failure (and adds the nerve fused into the ring outline).
It also has a visible leftover band patch and stray specks.

PAIR cond-carpal-hero -> pick NEITHER. Both edits deliver the anatomy fix: band across the wrist, nerve correctly under
it, no little-finger branch, 5 digits with correct phalanges. Both fail the explicit web-space requirement and
visibly degrade the owner's loved soft hand outline. The ring and little fingers lose their proximal outline and the
nerve forms the index-middle web. Edit-a is the closer of the two (no patch, no specks, no nerve/outline fusion on
the ring). A re-edit from edit-a should restore complete finger outlines with U-shaped webs clear of the nerve, stop the
band ends inside the skin outline, and keep the original's framing (about 90-100 px side margins at 7:5).

# r3c_batch4 review notes (round-3c re-renders of cond-lbp-assess, straight-leg-raise)

Method: full image read, then 1-5x LANCZOS crops via audit_v2/r3c4_crop.py into
audit_v2/crops/r3c4__<name>__<what>.png (crops whose name ends in `_grid` carry a magenta ruler in ORIGINAL
pixel units, ticks every 10 px, labels every 50 px). Final margins are pixel-measured with r3c4_edges.py
(toe skin = R-G > 33, which excludes beige wood) and r3c4_margin.py (hair luminance scan), cross-checked on the rulers (+-2 px).
Page crop simulated with PIL (`__pagecrop.png`): 7:5, full width, centred vertical trim.
Boxes below are full-image fractions [x0,y0,x1,y1].
Sides: the patient lies supine, head to image-left, so his RIGHT side faces the camera. "Near/resting leg" =
his right leg; "raised leg" = the far (left) leg. margins_px.toes_left_foot = raised foot,
toes_right_foot = resting foot; each is the distance to the NEAREST frame edge in the full image.

## 1. cond-lbp-assess-c (2048x2048, page crop keeps rows 293-1755) -- verdict FAIL (previous failure NOT fixed)

Crops read: head_grid, headedge_grid, edge_left, edge_right, foot_raised_grid, toes_raised_grid,
foot_resting_grid, toes_resting_grid, pagecrop, hand_prac_thigh(_wide), hand_prac_hip(_wide),
hand_patient(_wide/_tall/_fingers), overlay, hipjoint, practitioner_top, bg_device.

FRAMING
- Head: FAIL. The back of the head/hair runs straight into the LEFT edge: hair pixels at x=0 on rows ~735-830
  (luminance scan, r3c4_margin.py; headedge_grid). Margin 0 px, back of the skull cut off. Same failure as rounds 2-3.
- Resting (right) foot toes: tips end at x=2031 (pixel-measured, R-G skin test separates toe from the beige wood
  behind), so the margin to the right edge is 16 px. Not touching, but tight.
- Raised (left) foot toes: topmost toe at y=158 (measured), rightmost toe skin at x<=1859 -> 158 px to the top edge,
  ~190 px to the right edge. Fine in the full square.
- PAGE CROP (7:5, rows 293-1755): FAIL. The raised foot's toes (y 158-300) fall ABOVE the crop line (toe top
  135 px above it), so the page image cuts the raised foot through the toes/forefoot (visible in __pagecrop.png).
  The head is still cut on the left. Resting toes keep 16 px.

HANDS
- Practitioner LEFT hand on the raised shin [0.645,0.181,0.791,0.293]: thumb + 4 fingers. The thumb curls under on
  the image-left side (correct for a left hand, palm down, fingers toward the camera). All nails present, natural
  size, attached. OK.
- Practitioner RIGHT hand on the patient's hip [0.356,0.278,0.493,0.386]: 4 fingers pointing down, thumb pointing
  image-right along the hip (correct side for a right hand). Natural. OK.
- Patient RIGHT hand flat on the table [0.410,0.430,0.566,0.503]: 3-4 fingers visible (overlapping), thumb hidden on
  the far side. Nothing fused or extra. OK.
- Patient left hand/arm: hidden behind the torso (plausible).

FEET / BODY
- Raised foot: 5 toes, natural. Resting foot: 5 toes, natural. No lobe or growth on either ankle (previous
  toe-like lobe is gone).
- 2 legs, 1 arm visible (far arm hidden). Legs (hip to ankle ~840-850 px) vs torso (shoulder to hip ~650 px): ratio
  ~1.3, clearly longer. OK.

OVERLAY
- Lumbar spine in teal along the lower back; pelvis (iliac wing and ischium) with the femoral head at its upper
  right, i.e. the hip joint; femur runs up into the RAISED leg (previous "bone in resting leg" error fixed). The
  overlay also draws the knee and shin bones. Stylised but no gross error. The overlay knee sits at ~46% of the
  hip-to-ankle line (femur a little short). This is under the trousers, so a visitor would not notice.
- Red glow: fibres from the lumbar spine to the hip (psoas / hip flexor) under the practitioner's hip hand. OK.

OTHER
- Practitioner cut at the chest by the top edge: no face, chin or beard. The device screen is blank and there is no
  readable text. OK.
- Scene note, not scored: the "ankle" hand sits on the upper shin just below the knee, not just above the ankle.

VERDICT: FAIL. The head is cut by the left frame edge (0 px) and the page crop cuts the raised toes.
previous_failure_fixed: false.

## 2. cond-lbp-assess-d (2048x2048, page crop keeps rows 293-1755) -- verdict FAIL (previous failure NOT fixed)

Crops read: head_grid, headedge_grid, edge_left, edge_right, toes_raised_grid, toes_raised_wide_grid,
foot_resting_grid, toes_resting_grid, toes_resting_zoom, pagecrop, hand_prac_hip, hand_prac_shin(_wide),
hand_patient(_tall), overlay, hipjoint, practitioner_top, prac_neck_top, bg_left_items, bg_device_right.

FRAMING
- Head: FAIL. Hair runs into the LEFT edge: hair pixels at x=0 on rows ~715-860 (luminance scan; headedge_grid). Margin 0 px,
  back of the skull cut off, as in rounds 2-3.
- Resting (right) foot toes: tips end at x=2014 (measured), so the margin to the right edge is 33 px. Clear but small.
- Raised (left) foot toes: toe top at y=250, rightmost at x=1870 (measured) -> 250 px to the top edge, 177 px to the
  right edge.
- PAGE CROP (7:5, rows 293-1755): FAIL. The raised toes (y 250-~340) cross the crop line at y=293, so the page
  image cuts the raised toes (visible in __pagecrop.png). The head is still cut on the left. Resting toes keep ~33 px.

HANDS
- Practitioner RIGHT hand on the patient's hip [0.352,0.288,0.454,0.386]: 4 fingers pointing down with nails, thumb
  pointing image-right (correct side for a right hand). Natural. OK.
- Practitioner LEFT hand flat on the raised lower leg just above the ankle [0.659,0.161,0.830,0.234]: thumb underneath
  on the camera side (correct for a left hand, palm down, fingers toward the foot) plus 3-4 fingers (the little
  finger is behind the ring finger). Natural, attached. OK. This matches the brief's "just above the ankle".
- Patient RIGHT hand flat on the table [0.410,0.454,0.562,0.522]: 3-4 fingers visible, thumb hidden on the far
  side. OK.
- Patient left arm: hidden behind the torso.

FEET / BODY
- Raised foot: 5 toes (5 nails counted), natural. Resting foot: only 4 toe tips are distinguishable in the stacked
  side view at 6x (toes_resting_zoom). The 5th is presumably hidden behind its neighbour. Nothing deformed or extra,
  and no lobe on either ankle. Logged as MINOR only.
- 2 legs, 1 arm visible. Legs (hip joint to heel sole ~990 px) vs torso (shoulder to hip joint ~745 px): ratio ~1.3,
  longer. The torso reads a little long, but OK.

OVERLAY
- Long teal spine along the back into the lower back; stylised pelvis (iliac wing plus ischium/pubis loop with the
  obturator hole); the femoral head sits in the notch at the pelvis' right side (hip socket). The femur runs into the
  RAISED leg, then knee and shin bones. No gross error.
- Red glow: from the lumbar spine to the hip (psoas / hip flexor) under the practitioner's hip hand. OK.

OTHER
- Practitioner cut at the collar: only the throat shows in the open collar, no chin, lips, nose or beard. Background
  box and device screens are blurred or blank, with no readable text. OK.

VERDICT: FAIL. The head is cut by the left frame edge (0 px) and the page crop cuts the raised toes.
previous_failure_fixed: false.

## 3. cond-lbp-assess-e (2336x1744, page crop keeps rows 38-1706) -- verdict FAIL (previous failure NOT fixed)

Crops read: head_grid, headedge_grid, edge_left, edge_right, toes_raised_grid, foot_raised_grid, toes_resting_grid,
foot_resting_grid, pagecrop, hand_prac_hip, hand_prac_leg, hand_patient, overlay, hipjoint, practitioner_top,
prac_neck_top, bg_device_right, bg_box_shelf, bg_frame.

FRAMING
- Head: FAIL. Hair runs into the LEFT edge: hair pixels at x=0 on rows ~735-875 (luminance scan; headedge_grid). Margin 0 px,
  back of the skull cut off, as in rounds 2-3.
- Resting (right) foot toes: tips end at x=2304 (measured), so the margin to the right edge is 31 px. Clear but small.
- Raised (left) foot toes: toe top at y=228, rightmost at x=2021 (measured) -> 228 px to the top edge, 314 px to the
  right edge.
- PAGE CROP (7:5, rows 38-1706): both feet stay inside (raised toes ~190 px below the crop top, resting toes ~30 px
  from the right). The head is still cut on the left, so FAIL.

HANDS
- Practitioner RIGHT hand on the patient's hip [0.377,0.344,0.462,0.459]: 4 fingers pointing down with nails, thumb
  pointing image-right (correct side). Natural. OK.
- Practitioner LEFT hand wrapped over the bare lower shin just above the ankle [0.693,0.195,0.805,0.292]: 4 fingers
  curling toward the camera side of the leg, thumb wrapping the far side (image-left/behind, correct for a left
  hand). Natural, attached. OK. This matches the brief.
- Patient RIGHT hand flat on the table [0.445,0.522,0.578,0.608]: 4 fingers visible, thumb hidden on the far side.
  Natural. OK.
- Patient left arm: hidden behind the torso.

FEET / BODY
- Raised foot: big toe foremost with 4 smaller toe tips stepping behind it = 5, natural. Resting foot: 5 toes with
  nails, natural. Both ankles clean, with no lobe or growth.
- 2 legs, 1 arm visible. Legs (hip to heel sole ~1100 px) vs torso (shoulder to hip ~745 px): ratio ~1.5, clearly
  longer. OK.

OVERLAY
- Teal lumbar/lower-thoracic spine along the back; pelvis at the hip; femur runs up inside the RAISED leg to a knee,
  then the shin bone to the ankle. Red glow at the lower back and at the hip / top of the femur. OK.
- MINOR: the pelvis is a lumpy, pretzel-like shape with three openings, and the femoral head is drawn as a separate
  ball in the middle of the pelvis. The femur shaft ends in a rounded knob against a crescent notch at the pelvis
  top, with no clear femoral neck. It reads as "pelvis + hip joint" at page size, but a chiropractor would find the
  pelvis odd. Not gross enough to fail on its own. Box ~[0.40,0.37,0.53,0.55].

OTHER
- Practitioner cut at the collar: throat only, no chin, lips, nose or beard. Device screen, shelf box and wall frame
  are blurred, with no readable text. OK.

VERDICT: FAIL. The head is cut by the left frame edge (0 px). Feet margins are OK in both the full frame and the page crop.
previous_failure_fixed: false.

## 4. cond-lbp-assess-f (2336x1744, page crop keeps rows 38-1706) -- verdict MINOR (previous failure FIXED)

Crops read: head_grid, headedge_grid, edge_left, edge_right, toes_raised_grid, foot_raised_grid, toe_mark_zoom,
toes_resting_grid, foot_resting_grid, pagecrop, hand_prac_hip, hand_prac_hip_ulnar_zoom, hand_prac_leg,
hand_patient, overlay, hipjoint, practitioner_top, prac_neck_top, bg_device, bg_frame, bg_cart.

FRAMING (pixel-measured with r3c4_edges.py / r3c4_margin.py, cross-checked on the ruler crops)
- Head: INSIDE. Columns 0-3 are wall only (luminance 183-200) on every hair row (775-860). Outermost grey hair
  wisps start at x=17 (rows 829-850) and solid dark hair at x=25. Margin 17 px (0.7% of width): small but clear.
  The pillow runs off the left edge, which is fine.
- Resting (right) foot toes: rightmost toe skin at x=2307 (4th toe, y~926), so 28 px to the right edge. Clear but
  small.
- Raised (left) foot toes: topmost toe at y=141 (big toe), rightmost at x=2084 -> 141 px to the top edge, 251 px to
  the right edge.
- PAGE CROP (7:5, rows 38-1706): the head stays at 17 px, resting toes at 28 px, and the raised toes sit 103 px below
  the crop top. Everything stays inside (__pagecrop.png checked). PASS, but the margins are tighter than the brief's
  "well inside" (only a thin strip of wall shows beyond the hair and toes).

HANDS
- Practitioner RIGHT hand on the patient's hip [0.381,0.373,0.471,0.482]: thumb on the image-right (correct for a
  right hand) plus 4 fingers pointing down. The ring finger is partly behind its neighbours; the 6x zoom shows a
  clean ulnar edge. Natural. OK.
- Practitioner LEFT hand draped over the lower shin just above the ankle [0.762,0.172,0.856,0.269]: thumb spread
  toward the knee side (image-left) plus 4 fingers curling over the camera side of the shin. Natural, attached. OK.
  Matches the brief.
- Patient RIGHT hand flat on the table [0.437,0.591,0.574,0.671]: 4 fingers visible, thumb hidden on the far side.
  Natural. OK.
- Patient left arm: hidden behind the torso.

FEET / BODY
- Raised foot: 5 toes (big toe with nail, then 4 smaller tips stepping down). A small dark lens-shaped crease/mark
  (~12x10 px) on the big toe's knuckle, box ~[0.862,0.098,0.869,0.105]: cosmetic, invisible at page size, not an
  extra digit. Resting foot: 5 toes with nails, natural. Both ankles clean, with no lobe or growth.
- 2 legs, 1 arm visible. Legs (hip to heel ~1050 px) vs torso (shoulder to hip ~630-700 px): ratio ~1.5-1.6,
  clearly longer. OK.

OVERLAY
- Teal lumbar/lower-thoracic spine along the lower back, glowing red from the lower lumbar spine with red fibres
  running up to the hip under the practitioner's hand (hip flexor/psoas). OK.
- Femur inside the RAISED thigh from the hip to the knee, then shin bones to the ankle; the femur is ~1.3x the shin
  length. OK.
- MINOR: the pelvis is a stylised rounded blob with one opening. The femur's proximal end (head + trochanter merged
  into one rounded knob) sits on the pelvis' upper (front) edge rather than centred in the socket. A short
  dog-bone-shaped stub at the pelvis' lower right [~0.48,0.53,0.53,0.58] reads as the ischium/pubis or the
  resting femur's neck. At page size it reads as "pelvis + hip joint", and a chiropractor may find it schematic, but
  there is no gross error. The previous "femur in the resting leg" failure is fixed.

OTHER
- Practitioner cut at the collar: throat only, no chin, lips, nose or beard. Device screen, wall art and cart label
  are blurred, with no readable text. OK.

VERDICT: MINOR. Head 17 px, resting toes 28 px, raised toes 141 px (103 px in the page crop): all inside the frame
and inside the page crop, but tight. The overlay pelvis is stylised and the big toe has a tiny crease mark.
previous_failure_fixed: true.

## Pick

cond-lbp-assess-f is the only image with the back of the head and all toes inside the frame, both in the full image
and in the 7:5 page crop. c, d and e all have hair running into the left frame edge (column 0), and c and d also
lose the raised toes in the page crop.

Margins summary (full frame / page crop), px:
| image | head (left) | raised toes (nearest edge) | resting toes (right) |
|---|---|---|---|
| c | 0 (cut) / 0 (cut) | 158 top / -135 (cut by crop) | 16 / 16 |
| d | 0 (cut) / 0 (cut) | 177 right (250 top) / top -43 (cut by crop) | 33 / 33 |
| e | 0 (cut) / 0 (cut) | 228 top / 190 | 31 / 31 |
| f | 17 / 17 | 141 top / 103 | 28 / 28 |

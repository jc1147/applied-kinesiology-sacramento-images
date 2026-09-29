# r3c_batch3 review notes (round-3c re-renders)

Method: full image read, then 1.5-4x LANCZOS crops via audit_v2/r3c3_crop.py into
audit_v2/crops/r3c3__<name>__<what>.png. Boxes are full-image fractions [x0,y0,x1,y1].

## 1. cond-neck-treat-a (2048x2048) -- verdict FAIL (previous failure NOT fixed)

Crops read: prac_hands, prac_hand_bottom_zoom, prac_hand_topright_zoom, prac_hands_gap_zoom, overlay,
pat_arm_imgleft, pat_arm_imgright, screen_text.

Composition: camera is still at the HEAD end. Her head/bun sits in the face cradle at the bottom of the frame
(y ~0.63-1.0) and the blanket over her hips is at the top (y ~0.29-0.55 at the sides). The practitioner stands at the
far (hip) end of the table facing the camera, not at the side. His face is out of frame (cut at the chest). OK.

HANDS
- Practitioner RIGHT hand (top of the stack; forearm from image-left) [0.40,0.23,0.60,0.37]: 4 fingers visible, all
  with nails and 3 knuckle creases, pointing down-right. The thumb is on the upper-right (radial) side, hidden under
  his left forearm/wrist. That is the correct side for a right hand palm-down with the fingers toward the camera. OK.
- Practitioner LEFT hand (underneath; forearm from image-right) [0.42,0.29,0.58,0.40]: 4 fingers visible, pointing
  down-left, all with nails. The thumb would be on the upper-left, under the top hand; a small rounded tip shows
  there. Nothing fused, no ribbon strips, no extra digit in the gap between the hands (gap zoom). OK.
- Patient hands: not in frame. Both upper arms run from the shoulders to the elbows at the bottom edge, and the
  forearms leave the frame. Arms are symmetric, natural for the close perspective. No feet (blanket).

OVERLAY [0.28,0.37,0.68,0.64]
- Spine: a single midline column from under his fingertips (y ~0.37) to the hairline (y ~0.63). OK as a column.
- Shoulder blades: UPSIDE DOWN again. Her head is at the BOTTOM of the frame and her shoulder line (where the arms
  leave the torso) is at y ~0.65-0.70. Both blades have their broad top edge / acromion hook at y ~0.41-0.45 (toward
  the blanket and hips) and their lower tips at y ~0.60-0.62, pointing DOWN the frame toward her head and neck.
  Image-left blade [0.28,0.40,0.43,0.62], image-right blade [0.53,0.40,0.68,0.62]. This is the exact round-2 failure.
- The drawn "upper back" also sits too far toward the hips (it starts at his hands at the blanket line).

RED GLOW [0.36,0.38,0.58,0.57]
- Between the drawn blade tops, on the hip-side half of the column (y ~0.39-0.57). It does not reach the base of the
  neck (column ends at the hairline, y ~0.63). Against the real body this is the mid back. Partial.

SCENE
- Brief asked for the camera at the foot end, the practitioner at the side, and his hands between the shoulder blades.
  Here his stacked hands rest at the blanket line on her lower back [0.40,0.22,0.60,0.40], far from the shoulders.

TEXT: background device screen is fully blurred (screen_text crop). No readable text.
PAGE CROP 1:1 (no crop): nothing further cut. Her head is in frame and the practitioner's face stays out. OK.
PREVIOUS FAILURE (blades upside down relative to her head): NOT FIXED. Variant -a still shows the head end, and the
blade tips point toward her head.

## 2. cond-neck-treat-b (2048x2048) -- verdict MINOR (previous failure FIXED)

Crops read: prac_hands, prac_arms, prac_wrist_junction_zoom, prac_lower_fingers_zoom, prac_hand_underside_zoom,
prac_bottomlayer_zoom, prac_arm_hand_gestalt (1x), overlay, pat_arm_imgleft, pat_arm_imgright, screen_text, shelf_bg.

Composition: camera at the FOOT end as briefed. Her head/bun is in the face cradle at the top centre (y ~0.24-0.44),
the blanket over her hips/legs fills the bottom, and her spine runs straight up the middle. The practitioner stands at
the side (image right) facing her. His face is out of frame (cut at the chest). OK.

HANDS
- Stacked pair on the base of her neck / top of the upper back. The far (right) forearm comes straight down and the
  near (left) forearm comes diagonally from image-right, crossing in front of it.
- Top hand [0.43,0.36,0.61,0.49]: 4 fingers visible pointing down-left, each with a nail and knuckle creases. Natural
  size. Thumb not visible (tucked or hidden by the hand).
- Lower hand [0.50,0.44,0.615,0.495]: 1 finger visible (nail + 2 creases) emerging from under the top hand's
  lower-right edge. The rest is covered by the top hand.
- No fused fingers, no ribbon strips, no extra digit. At page size (1x crop) it reads as a normal one-over-the-other
  stack.
- MINOR: at 3.5x the back of the top hand blends smoothly into the vertical forearm's wrist, while the diagonal forearm
  stops at a crease against its side [0.51,0.32,0.645,0.43]. Which forearm owns the top hand is ambiguous, and neither
  thumb is visible. Not a visible defect at page size.
- Patient hands: not visible. Both upper arms run from the shoulders along her sides to elbows at the blanket edge;
  the forearms are tucked under the blanket [0.115,0.815,0.17,0.915] / [0.777,0.817,0.847,0.917]. The upper arms look
  long but match the high foot-end view (the elbows drop to table level). No extra or missing limbs. No feet (blanket).

OVERLAY [0.26,0.45,0.70,0.74]
- Spine: one midline column (x ~0.48, back centre ~0.48) from the base of the neck under his fingertips down to the
  blanket. OK.
- Shoulder blades: CORRECT orientation. Head at the top. Each blade has its broad top edge / scapular spine and
  acromion at the shoulder line (y ~0.47-0.50), and its lower tip points down the back toward her feet (tips at
  y ~0.65-0.66). Image-left [0.27,0.47,0.43,0.67], image-right [0.52,0.47,0.69,0.67]. Inside the body, symmetric.
- Stylised clavicle/scapular-spine bars run from the midline out to each shoulder. Acceptable stylisation.

RED GLOW [0.41,0.45,0.55,0.57]: at the base of the neck and between the upper parts of the blades, right under his
fingertips. Matches "between the shoulder blades and the base of the neck". OK.

SCENE: his hands sit at the cervicothoracic junction (top edge of the glow), slightly above mid-blade. Acceptable.
TEXT: device screen and shelf (bottles, spine model) fully blurred. No readable text.
PAGE CROP 1:1 (no crop): her head, his hands and the treated area are all in frame. OK.
PREVIOUS FAILURE (blades upside down): FIXED. Blade tips point toward her feet, with her head at the top.
PAIR PICK cond-neck-treat: -b (-a still has upside-down blades).

## 3. cond-osteo-assess-a (2048x1360) -- verdict PASS (previous failure FIXED)

Crops read: pat_left_hand_table, pat_left_hand_digits_zoom, prac_hands, prac_lower_hand_zoom, prac_upper_hand_zoom,
foot_standing, foot_standing_toes_zoom, foot_raised, foot_raised_toes_zoom, legs (1x), knee_junction, overlay,
prac_face_topedge, pat_head_topedge, monitor_text.

Composition: silver-haired woman in a cardigan and slacks, seen from her left side (slightly from behind), facing
image-left. Her left hand is on the near edge of the table, her right arm is fully out of view, and she stands on her
right leg with her left knee bent and the shin horizontal behind her. The practitioner stands behind her; frame cut at
his collar (only a sliver of neck in the open collar, no chin/lips/nose/beard).

HANDS
- Patient LEFT hand on the table [0.194,0.465,0.279,0.532]: 3 visible (index/middle on top, ring finger with a ring,
  little finger nearest the camera). Palm down, seen from the little-finger side, so the thumb is hidden on the far
  side. Correct for a left hand viewed from her left. Veined back of hand, natural size, attached to her left
  forearm. No ribbon strips.
- Practitioner LEFT hand (near arm) on her buttock/hip [0.466,0.313,0.535,0.426]: 5 digits (thumb extended toward
  her waist + 4 fingers pointing down, 4 nails). Back of hand to camera with fingers down puts the thumb on the image
  left = correct for a left hand. OK.
- Practitioner RIGHT hand (far arm) on her lower back at the waist [0.428,0.263,0.476,0.331]: thumb + palm visible,
  4 fingers wrapped around her flank out of view. Nothing wrong.
- Her right arm/hand: not visible (on the far side, as briefed).

FEET / BODY
- Raised (near, left) foot [0.620,0.632,0.703,0.790]: 5 toes (little toe nearest the camera with its nail face-on,
  3 middle toes with nail tips, big toe on the far side). Plantar-flexed, natural size, attached at the ankle.
- Standing (far, right) foot [0.381,0.915,0.483,0.978]: side view of the inner arch. Big toe in front, small toes
  just visible behind it (5-toe foot, hidden toes behind the big toe). Flat on the floor, natural.
- Legs: at the knee the raised left leg overlaps the standing right leg (knee_junction). Thigh/shin lengths are
  consistent. No extra, missing or over-long limbs. Her left arm is natural.

OVERLAY [0.349,0.088,0.503,0.662]
- Spine: S-curved column just inside her back contour, from the base of the neck to the sacrum, following her
  forward lean. Pelvis (iliac wing + sacrum) at the hip, hip joint in the middle of the hip, femur down the raised
  thigh to the knee. All inside the body and matching the side-on pose. OK.

RED GLOW
- Back glow [0.396,0.271,0.437,0.340] on the thoracolumbar junction, the lower end of the "mid back". Acceptable.
  Measured centroid (846,414) = (0.413,0.304), ~75% of the way from the neck base (y~142) to the iliac crest (y~504),
  about T12-L1 (r3c3_glow.py).
- Hip glow [0.418,0.420,0.468,0.495] centred on the hip joint. Measured centroid (922,615) = (0.450,0.452). OK.

SCENE NOTE (not a defect): the practitioner's hands rest ON her lower back and buttock rather than hovering.
TEXT: monitor on the right fully blurred. No readable text.
PAGE CROP 7:5 (trims 72 px / 3.5% each side, keeps x 72-1976): nothing important within 72 px of either side.
  Her head, both feet, all hands and the treated area stay in frame. Her crown just touches the top edge (original
  framing, not the page crop).
PREVIOUS FAILURE (ribbon-strip hanging hand): FIXED. Her free arm is out of view and every visible hand is natural.

## 4. cond-osteo-assess-b (2048x1360) -- verdict MINOR (previous failure FIXED)

Crops read: pat_left_hand_table, pat_left_hand_digits_zoom, pat_left_hand_enh, pat_fingertips_enh (8x),
pat_arm_hand_1x, prac_hands, prac_upper_arm_end_zoom, prac_arms_context, foot_standing, foot_standing_toes_zoom,
foot_raised, foot_raised_toes_zoom, legs (1x), knee, overlay, prac_face_topedge, pat_head_topedge, monitor_text.
Glow centroids measured with r3c3_glow.py.

Composition: same brief as -a. Seen from her left side (slightly behind), facing image-left. Left hand on the table
edge, right arm out of view. She stands on her right leg with her LEFT knee lifted FORWARD and bent ~120 deg, the shin
running back and the foot hanging behind. Practitioner behind her; frame cut at his collar (sliver of neck only, no
chin/lips/nose/beard).

HANDS
- Patient LEFT hand on the table [0.164,0.474,0.244,0.533]: 3 visible from the little-finger side, thumb hidden on the
  far side (correct side). Wrist, veined back and finger length (~1.1x the back of the hand) are natural.
  MINOR: the fingers are low-detail. At 4-8x they are flat, tapering strips with no visible nails or knuckle creases
  and pointed tips. At 1x (pat_arm_hand_1x) it reads as a normal flat hand on the table edge. Not a ribbon-strip
  defect at page size, but clearly weaker than -a's crisp hand (ring, nails, creases).
- Practitioner LEFT hand (near arm) on her buttock [0.483,0.324,0.554,0.423]: 5 digits (thumb forward toward her
  waist + 4 fingers down, 4 nails). Back of hand to camera with fingers down puts the thumb on the image left =
  correct for a left hand. OK.
- Practitioner RIGHT arm (far) [0.439,0.265,0.483,0.324]: the forearm reaches past her lower back and the hand is
  hidden behind her torso (0 digits visible). The forearm is not merged into her body. Nothing wrong.

FEET / BODY
- Raised (near, left) foot [0.493,0.651,0.569,0.820]: 5 toes, each with a nail tip, curled down. Plantar-flexed,
  natural size, attached at the ankle.
- Standing (far, right) foot [0.369,0.923,0.479,0.993]: side view of the inner arch, big toe in front with the small
  toes behind it. Flat on the floor, natural.
- Legs: raised thigh ~333 px hip-to-knee, raised shin ~332 px, standing leg ~650 px hip-to-ankle, all consistent.
  Knee fold natural [0.320,0.581,0.371,0.669]. No extra, missing or over-long limbs.

OVERLAY [0.349,0.096,0.503,0.676]
- Spine: S-curved column just inside her back contour, neck to sacrum, following the forward lean. Pelvis (iliac
  wing + sacrum) and the hip joint are inside the hip. OK.
- MINOR: the femur shaft [0.410,0.471,0.449,0.618] drops almost vertically (~77 deg) from the hip joint, while her
  visible near (left) thigh angles forward to the knee (~53 deg). The femur does not follow the lifted thigh and stops
  mid-thigh. It reads as the hidden standing leg's femur. Stylised, but a chiropractor may notice. (In -a the femur
  follows the lifted thigh to the knee.)

RED GLOW
- Hip glow centroid (907,623) = (0.443,0.458), on the hip joint [0.425,0.430,0.461,0.489]. OK.
- MINOR: back glow centroid (851,446) = (0.415,0.328) [0.386,0.287,0.447,0.360] sits ~83% of the way from the neck
  base (y~141) to the iliac crest (y~510), about L1-L2 just above the pelvis. It reads more as lower back than mid
  back. (-a: centroid (846,414), ~75%, about T12-L1.)

TEXT: monitor and wall art fully blurred. No readable text.
PAGE CROP 7:5 (keeps x 72-1976): nothing important within 72 px of either side. Head, feet, hands and treated area
  stay in frame. Her crown just touches the top edge (original framing).
PREVIOUS FAILURE (ribbon-strip hanging hand): FIXED. Her free arm is out of view. The only patient hand is on the
  table and is structurally sound, though low-detail (see MINOR above).
PAIR PICK cond-osteo-assess: -a (crisper table hand, femur follows the lifted thigh, back glow higher on the back).

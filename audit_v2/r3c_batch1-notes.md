# r3c_batch1 review notes (round-3c re-renders)

Method: full image read + fraction-grid overview (scratchpad) + crops in audit_v2/crops/r3c__<name>__*.png
(2-3x LANCZOS, full-image fraction ticks in the margin). Numeric checks with scratchpad r3c_b1_measure.py.
Boxes are full-image fractions [x0,y0,x1,y1].

## 1. cond-auto-assess-a (2048x1360, 3:2) -- provisional verdict MINOR

Crops read: prac_R_hand, prac_R_arm, prac_L_hand, prac_L_arm, pat_L_arm, pat_R_arm, overlay_neck, overlay_full,
head_top, bg_text_left, bg_text_right, lower_body.

HANDS
- Practitioner RIGHT hand on the patient's right upper back [0.44,0.27,0.54,0.44]: 5 digits (little tip 0.445,0.38; ring 0.45,0.41;
  middle 0.465,0.43; index 0.49,0.43; thumb tip 0.52,0.405 on the image-right). Dorsum toward the camera, fingers pointing down-left:
  a thumb on the image-right is correct for a right hand. Natural size (wrist to middle fingertip about 222 px; patient head about 313 px).
  Wrist (0.50-0.54,0.27-0.30) -> forearm -> rolled sleeve (0.55-0.64,0.12-0.25) -> upper arm to the top edge at x 0.60-0.70, next to his torso
  (right shoulder just above the frame). OK. The upper arm is fairly foreshortened, but still plausible.
- Practitioner LEFT hand hanging by the thigh [0.78,0.66,0.87,0.88]: 5 digits (thumb tip 0.79,0.815 on the image-left; index, middle and ring tips
  about y 0.865-0.875; little finger curled at 0.86,0.84). Thumb on the medial (image-left) side, correct for his left hand with the back of the hand
  toward the camera. About 267 px long; forearm (elbow 0.915,0.42 to wrist 0.845,0.68) about 382 px, a ratio of 1.43, natural. The arm joins the left shoulder
  at the top right. OK.
- Patient hands: not visible (forearms go forward to the lap, hidden by his torso). Nothing to count.

BODY
- Patient: 2 arms, both complete (sleeve, bare upper arm, elbow at 0.22,0.72 and 0.60,0.73, forearms forward). The left thigh is visible at the lower left
  (legs apart), which is natural. No third arm or hand anywhere: the camera side and the bottom-left are clean.
- Practitioner: 2 arms (the right reaches the patient, the left hangs), torso from chest to trousers, legs in dark trousers. No extra limbs.

OVERLAY
- Back view, correct. Cervical column from the hairline (y 0.21) down the midline (x 0.43-0.445, matching the neck and torso centre of about 0.425-0.43).
  Scapulae on the upper back, one each side (left 0.31-0.41, right 0.48-0.57, y 0.375-0.555), inferior angles pointing down.
- MINOR (brief): the spine continues well below the shoulder blades, to about y 0.80 (waist or lumbar level) [0.41,0.56,0.48,0.81]. The brief said
  "nothing below the shoulder blades". Placement is still anatomically plausible (midline column).
- MINOR (stylised): the scapulae are drawn a little narrow. The acromions sit about 0.04-0.07 medial of the shoulder tips. Not gross.
- RED GLOW (measured, red-pixel share in the band x 0.40-0.47): 0.000 at every row from y 0.20 to 0.33; it starts at y 0.34 (0.10) and is strong from 0.35 to 0.48,
  gone by 0.50. The t-shirt collar at the midline is at y 0.285-0.30. The glow therefore sits on the upper thoracic spine and the muscles between the
  shoulder blades. The lowest neck vertebrae (visible neck above the collar) are still NOT red, so this part of the round-2 failure is NOT fixed.

FACE / DEVICES / TEXT
- Practitioner cut at chest level; no face. Patient's profile is visible (allowed).
- No instrument in this shot (hands-only assessment, as briefed). Background: blank monitor at the far left, blurred bottles, no readable text.

COMPOSITION / PAGE CROP 7:5 (trims x<0.035 and x>0.965)
- The crop cuts nothing important. The practitioner's left sleeve edge (x of about 0.96) may just touch the right trim line; no hand is near it.
- MINOR: the top of the hair touches the top frame edge (row 0 is 90% dark across x 0.38-0.48), so the crown is clipped slightly [0.36,0.0,0.48,0.03].
  This is in the source; the page crop does not change the top.

BRIEF
- MINOR: the practitioner's fingertips point down-left toward the spine, not up toward the neck as briefed. The hand sits on the red area.

PREVIOUS FAILURE: third arm FIXED; 3-finger hand FIXED; lower-neck red glow NOT fixed. previous_failure_fixed = false (2 of 3 items fixed).

## 2. cond-auto-assess-b (2048x1360, 3:2) -- provisional verdict MINOR

Crops read: prac_R_hand, prac_R_arm, prac_L_hand, prac_L_arm, pat_L_hand, pat_R_hand, pat_L_arm, pat_R_arm, overlay_neck,
overlay_full, head_top, bg_text, bg_device_screen, right_edge, lower_body.

HANDS
- Practitioner RIGHT hand on the top of the patient's right trapezius, at the base of the neck [0.43,0.22,0.56,0.37]: 5 digits. There are 4 fingertips pointing
  left toward the neck and spine (0.441,0.319; 0.4375,0.337; 0.437,0.354; 0.45,0.36), and the thumb below them (tip 0.497,0.357). Back of the hand toward the camera, fingers pointing left:
  a thumb on the lower side is correct for a right hand. About 205 px, slightly foreshortened over the curved shoulder; natural. Wrist (0.50-0.54,0.24-0.30),
  then forearm, rolled cuff (0.58-0.63,0.16-0.24), and sleeve up to his right shoulder at the top edge, next to his torso (x of about 0.73). OK.
- Practitioner LEFT hand hanging by the thigh [0.78,0.68,0.87,0.88]: 5 digits (thumb tip 0.788,0.82 on the image-left; index 0.801,0.872;
  middle 0.821,0.877; ring 0.835,0.871; little 0.852,0.855). Correct side for a left hand with the back of the hand toward the camera. About 243 px. The arm is continuous
  (sleeve, cuff at 0.86-0.94,0.42-0.49, forearm, wrist) to the left shoulder. OK.
- Patient LEFT hand on the table beside his hip [0.15,0.88,0.22,0.95]: only the wrist and the heel of the hand show. The thumb-side bulge faces
  his body (image-right), which is correct. The fingers are hidden behind the padded table ridge at y 0.94. Nothing to count, no anomaly.
- Patient RIGHT hand gripping the right edge of the table [0.58,0.89,0.68,0.97]: the thumb shows at about 0.60,0.915, pointing toward his body (correct for his right hand);
  the fingers wrap over the edge, out of view. No anomaly.

BODY
- Patient: 2 arms hang straight down to the table edges. Both are complete (shoulder, sleeve, elbow at 0.21,0.734 and 0.635,0.735, forearm, wrist, hand). The forearms
  look shorter than the upper arms in projection (about 258 px against 462 px). The upper arm is 1.48 head heights, which is natural, so this fits elbows bent slightly forward
  (the olecranon shows) to grip the table beside the thighs. Not flagged. Seated hips and thighs on the table look natural.
- Practitioner: 2 arms, torso, belt and trousers. No third arm or hand anywhere (bottom-left and camera side are clean).

OVERLAY
- Back view, correct. The cervical column runs from the hairline (y 0.21) down the midline (x 0.42-0.44; neck centre about 0.43). Scapulae on the upper back, one each side
  (left 0.30-0.40, right 0.48-0.58, y 0.36-0.545), inferior angles pointing down. Small humeral heads at the shoulder joints (not named in the brief, but
  anatomically placed). The scapulae and humeral heads are drawn slightly medial of the real shoulder tips (left by about 0.03). Stylised, not gross.
- MINOR (brief): the spine continues below the shoulder blades to about y 0.73 (full thoracic spine) [0.41,0.55,0.47,0.74]; the brief said "nothing below the shoulder blades".
  It stops higher than in variant a (0.80).
- RED GLOW (measured, red share in the band x 0.40-0.47): 0.000 from y 0.18 to 0.28; 0.17 at 0.29 (the collar line), 0.38-0.52 from 0.30 to 0.36, 0.84-0.97 from 0.37 to 0.42, fading by 0.46.
  The glow starts at the base of the neck at the collar and covers the drawn lowest cervical vertebrae (C6-C7 at about 0.29-0.33) and the muscles
  between the shoulder blades. The practitioner's hand rests on the red area. The round-2 failure "lower neck had no red glow" is FIXED.

FACE / DEVICES / TEXT
- Practitioner cut at chest level; no face. Patient's profile is visible (allowed). No instrument, as briefed (hands only).
- Background: the device screen (0.10-0.15,0.36-0.40) is blurred and shows no text; the wall picture is an abstract image; towels and plants. No readable text.

COMPOSITION / PAGE CROP 7:5 (trims x<0.035 and x>0.965)
- There is clear space above the hair (row 0 is 0% dark across x 0.36-0.46; hair top at y of about 0.015). The crop cuts nothing important. The practitioner's left cuff edge
  reaches x of about 0.965, so only a sliver is trimmed and no hand. The patient's hands (x 0.15-0.68) are safe.

PREVIOUS FAILURE: third arm FIXED; 3-finger hand FIXED; lower-neck glow FIXED. previous_failure_fixed = true.
PAIR (provisional): b is better. It has the neck glow fixed and headroom, and its only issue is the minor spine extension (shared with a, but shorter in b).

## 3. cond-fibro-treat-a (2048x1360, 3:2) -- provisional verdict MINOR

Crops read: prac_R_hand_instrument, instrument_tip, prac_R_fingers_enh (5x, contrast-enhanced), prac_R_leftfingers_enh (6x),
prac_R_hand_wide, prac_L_hand, prac_L_arm, prac_R_arm, pat_L_arm, pat_R_arm, pat_L_elbow_junction, pat_R_elbow_junction,
overlay_full, overlay_upper, head_cradle, top_edge_face, bg_text_left, bg_text_right, bottom_band.

SCENE: camera at the foot end, prone patient, face in the cradle, blanket over the hips and legs. The spine runs up the middle of the frame, as briefed.
The practitioner stands at the HEAD end, behind the face cradle, facing the camera, not "at the side of the table" (MINOR brief deviation;
the pose is still clinically plausible).

HANDS
- Practitioner RIGHT hand (image-left) holding the instrument [0.34,0.23,0.46,0.42]: 5 digits. There are 3 curled fingers on the back of the hand (leftmost knuckle
  about 0.355,0.35; two more bands with knuckle creases at about 0.38-0.40,0.35-0.39), one fingertip with a nail along the instrument (0.425,0.40), a second
  tip tucked just under it (0.415,0.408), and the thumb wrapping the instrument on the image-right (nail 0.445,0.355). The thumb is on the medial side, correct for
  a pronated right hand of a man facing the camera. About 203 px. Wrist (0.36-0.42,0.24-0.27), forearm, rolled cuff (0.33-0.44,0.02-0.10), and the sleeve
  runs off the top edge beside his torso. OK. (Tight grip; no extra or missing digit found at 6x.)
- Practitioner LEFT hand (image-right) flat on the patient's right shoulder blade [0.55,0.40,0.69,0.59]: 5 digits (thumb nail 0.555,0.465 at the upper-left;
  index 0.565,0.55; middle 0.58,0.57; ring 0.60,0.575; little 0.63,0.565). The thumb is on the medial (image-left) side, correct for his left hand seen from the back. About 251 px.
  Wrist (0.63-0.68,0.40-0.46), forearm, cuff (0.70-0.78,0.13-0.24), and the sleeve runs to the top edge at the torso. OK.
- Patient hands: not visible. Both forearms fold under the blanket (see BODY). Nothing to count.

BODY
- Patient: 2 arms lie along the sides on the table. Each runs from the shoulder (0.31,0.46 and 0.70,0.47) to a flexed elbow at the bottom corners (0.14-0.20,0.84-0.905
  and 0.80-0.855,0.85-0.905). The forearm's lower contour turns inward, with an inner-elbow crease at about 0.23,0.85 and 0.77,0.86, and slides under the blanket edge.
  They are continuous, not stumps. Projection check: upper-arm vertical span 598 px against spine C7-to-waist 564 px, which is consistent with natural proportions for an elevated
  foot-end camera (the elbows sit at lower-rib level). Legs are under the blanket. No extra limbs.
- Practitioner: 2 arms (both join his torso above the frame), shirt, belt, trousers behind the cradle. No face (frame cut at chest level).

OVERLAY
- FIXED orientation. The spine is one straight column up the middle of the frame (x 0.49-0.50, the body midline) from the base of the neck (y 0.36) to the blanket (0.785).
  The shoulder blades are back views on the upper back (left 0.31-0.43 and right 0.56-0.69, y 0.46-0.70), one each side, acromion and glenoid at the upper-lateral,
  inferior angles pointing toward the camera. They sit just below the shoulders. The right blade sits slightly farther from the spine (0.075 against 0.06); not gross.
- RED: 7 small scattered tender points on both sides of the upper and mid spine ((0.45,0.465), (0.54,0.43), (0.535,0.505), (0.445,0.545), (0.45,0.635), (0.54,0.625),
  (0.55,0.755)) plus a soft warm wash over the paraspinals. The instrument tip sits on the top-left point. Matches the brief.

DEVICE / TEXT
- Instrument: chrome, pen-shaped, a few ring grooves, flat black rubber tip, no needle. Plausible. No readable text: the device screen at the far left is dark,
  the cart has a small blurred label-sized patch that is not legible, and the shelves are blurred.

PAGE CROP 7:5 (trims x<0.035, x>0.965): nothing important at the edges (elbows at x 0.135 and 0.855). OK.

PREVIOUS FAILURE (overlay rotated 60-90 deg across the back): FIXED. previous_failure_fixed = true.

## 4. cond-fibro-treat-b (2048x1360, 3:2) -- provisional verdict MINOR

Crops read: prac_R_hand_instrument, prac_R_fingers_enh (5x), prac_L_hand, prac_arms_top, pat_L_arm, pat_R_arm, bottom_band,
overlay_full, overlay_upper, head_cradle, bg_device_right, bg_left.

SCENE: same set-up as variant a. Foot-end camera, prone patient, grey blanket, practitioner at the HEAD end behind the cradle (MINOR brief deviation:
the brief says "at the side of the table").

HANDS
- Practitioner RIGHT hand (image-left) with the instrument [0.32,0.26,0.44,0.44]: 5 digits. The curled little and ring fingers show on the back of the hand (about 0.33-0.38,
  0.34-0.42), the middle fingertip is tucked (0.404,0.427), the index runs along the instrument (tip and nail 0.41,0.415), and the thumb wraps the instrument on the image-right
  (nail 0.422,0.368). The thumb is on the medial side, correct for a pronated right hand of a man facing the camera. The wrist (0.33-0.37,0.26-0.30) runs to the rolled sleeve
  and his right shoulder above the frame. OK.
- Practitioner LEFT hand (image-right) flat on the patient's right upper back and trapezius [0.50,0.37,0.65,0.54]: 5 digits (thumb tip 0.515,0.485 at the upper-left;
  index 0.52,0.52; middle 0.54,0.53; ring 0.565,0.525; little 0.595,0.515). The thumb is on the medial side, correct for his left hand. About 241 px. Wrist (0.59-0.64,0.37-0.42),
  forearm, cuff (0.68-0.75,0.10-0.23), torso. OK.
- Patient hands: not visible; the forearms are tucked under the blanket.

BODY
- Patient: 2 arms. Each runs from the shoulder (0.30,0.46 and 0.70,0.46) along the table to a flexed elbow at the bottom corners (0.13-0.17,0.87-0.96 and 0.80-0.86,0.86-0.955).
  The inner contour turns under the blanket (0.17-0.20,0.92-0.96 and 0.78-0.80,0.93-0.95). Continuous. The upper arm is about 0.83 of the shoulder width (natural). The elbows sit
  closer to the bottom edge than in a (0.96 against 0.905), and the arm-to-spine projection ratio is 1.21 against 1.06 in a: slightly longer-looking arms, but not flagged.
- Practitioner: 2 arms joining the torso; shirt and trousers behind the cradle. No face (frame cut at the upper chest).

OVERLAY
- FIXED. One straight spine column up the middle (x of about 0.465-0.48; body midline about 0.48) from the neck base (y 0.37) to the blanket (0.78). The shoulder blades are back views
  on the upper back (left 0.29-0.43 and right 0.54-0.66, y 0.46-0.69), one each side, inferior angles toward the camera. The left blade is a bit closer to the spine
  (medial border about 0.04-0.05 against 0.06-0.07). Not gross.
- RED: about 7 scattered tender points on both sides of the upper and mid spine ((0.43,0.49) under the instrument tip, (0.52,0.455), (0.515,0.515), (0.535,0.555),
  (0.425,0.585), (0.52,0.625), (0.42,0.665)) plus a warm wash along the paraspinals. Matches the brief.

DEVICE / TEXT
- Instrument: chrome, pen-shaped, a knurled grip band (a texture, not text), a black end cap, a flat black rubber tip. Plausible. The background device screen (0.93-0.99,0.13-0.17)
  is dark. No readable text anywhere.

PAGE CROP 7:5: nothing important at the side trims (elbows at x 0.12 and 0.86). OK.

PREVIOUS FAILURE (overlay rotated across the back): FIXED. previous_failure_fixed = true.
PAIR (provisional): a is slightly better. Its spine sits exactly on the midline, the blades are more symmetric, and the arm proportions are a touch more natural. Both are usable (MINOR).

## 5. cond-lbp-assess-a (2336x1744, 4:3) -- provisional verdict FAIL (head cut off at the left edge)

Crops read: head_left_edge, raised_foot, raised_toes_enh (6x), resting_foot, resting_toes_enh (7x), resting_toes_6x, prac_hand_leg,
prac_hand_hip, pat_arm, pat_hand, pat_hand_enh (7x), legs, overlay_full, overlay_pelvis, prac_top_face, prac_arms, bg_shelves.
Numeric: r3c_b1_edges.py (left and right edge columns), plus a skin-column scan.

SCENE: the patient lies supine, head at the image-left on a pillow, right side toward the camera. The near RIGHT leg is raised at about 30 deg; it passes in front of the resting
far LEFT leg at the hip. The practitioner stands behind the table: his left hand is flat on the distal shin of the raised leg (about 0.05-0.10 above the ankle),
and his right hand is on the patient's hip or iliac crest. The brief is met (the hand is "just above the ankle" roughly, on the distal third of the shin).

COMPOSITION -- KEY DEFECT
- The back of the patient's HEAD IS CUT OFF by the left frame edge [0.0,0.38,0.06,0.53]. Column 0 is 59% dark (hair) across rows 0.38-0.54; the hair runs off the
  edge from y 0.40 to 0.52 and the ear sits only at x 0.04-0.08. The brief asked for "clear space beyond the top of his head". The round-2 item "back of his head touched
  the frame edge" is NOT fixed; it is worse (now clipped). The 7:5 page crop trims only top and bottom, so it neither fixes nor worsens this.
- The resting foot's toes reach x 0.9889 (rightmost skin column 2310 of 2336, a 25 px or 1.1% margin): tight, not touching. The raised toes reach x 0.955 and y of about 0.10 (safe from the 2.16% top trim).

HANDS
- Practitioner LEFT hand on the raised shin [0.735,0.21,0.825,0.315]: 5 digits (thumb tip 0.74,0.295 on the image-left; index 0.79,0.305; middle 0.805,0.31; ring 0.815,0.305;
  little 0.82,0.29). Back of the hand toward the camera, man facing the camera: the thumb on the medial side is correct. Knuckle width about 117 px (natural); the length is foreshortened over the curved shin.
  The arm is continuous from the left shoulder, through the rolled sleeve (0.66-0.72,0.06-0.13) and forearm, to the wrist (0.745-0.775,0.21-0.24).
- Practitioner RIGHT hand on the hip [0.385,0.415,0.465,0.50]: 5 digits (thumb 0.455,0.455 on the image-right; 4 fingertips at x 0.405-0.45, y 0.485-0.495). Correct side. The arm
  is continuous from the right shoulder, down his side, through the rolled sleeve (0.34-0.40,0.25-0.30) and forearm.
- Patient RIGHT hand flat on the table by the hip [0.41,0.595,0.555,0.65]: seen from the little-finger side. 3 fingertips show (little 0.51,0.643; ring 0.53,0.64;
  middle 0.545,0.636, the longest); the index and thumb are hidden behind on the medial side, consistent with the view. About 280 px, natural. The arm is continuous (sleeve, elbow at 0.285,0.645,
  forearm, wrist at 0.415,0.625). The patient's far LEFT arm is hidden behind the torso (occluded; not a defect).

FEET
- Raised RIGHT foot [0.87,0.09,0.96,0.29]: a dorsal view, the leg turned outward and the foot pointed. 5 toes clearly (big toe on top at 0.935,0.10, then 4 stepping down to 0.955,0.15).
  Natural size, and it sits on the raised leg. OK.
- Resting LEFT foot [0.90,0.46,0.995,0.62]: seen from the inner side, the toe row foreshortened. The big toe is in front (0.979-0.989,0.48-0.505), the taller second toe
  behind (nail 0.975,0.477), and 2-3 small toe outlines further back (0.95-0.97). Not all 5 can be separated, but there is no extra lobe, no fused or odd shape, and the ankle
  shows only the malleolus bump. It sits on the resting leg. OK.

BODY
- The raised leg's thigh-to-shin ratio is 1.22 (natural).
- MINOR (proportion): the torso is somewhat long for the legs. Shoulder joint (about 0.16) to hip joint (about 0.49) is about 771 px, against hip joint to heel (about 0.96) about 1098 px, a ratio
  of 1.42 where a real adult is about 1.8. The legs are longer than the torso, as briefed, but the legs look short or the torso long by about 20%.
- Patient: 2 legs (both complete); 1 arm visible plus 1 occluded. Practitioner: 2 arms, torso, trousers. No extra limbs.

OVERLAY
- Correct placement and orientation. The lumbar spine runs horizontally along the torso (0.23-0.41, y 0.52-0.57); the pelvis is a side view at the hip (0.41-0.51, 0.49-0.60);
  the femur runs from the femoral head (0.49,0.50) up the RAISED thigh to the knee (0.68,0.37). There is no bone in the resting leg, so the round-2 "femur in the wrong leg" item is FIXED.
- MINOR (brief): the overlay also draws the tibia, fibula and ankle bones in the raised shin (0.69-0.87, 0.25-0.38); the brief named only the lumbar spine, pelvis and thigh bone.
  The drawn spine is longer than 5 lumbar segments (about 9 segments; stylised, not failed).
- RED: the lumbosacral junction and lower lumbar spine, running over the pelvic rim toward the hip flexor and femoral head (0.37-0.49, 0.47-0.56). Matches the brief.

FACE / DEVICES / TEXT
- The practitioner is cut at the collar; only a sliver of neck shows in the collar opening (no chin, lips or beard), and the top trim removes it. The patient's face is visible (allowed).
- No instrument in this shot. The background device screen is dark and blank; the shelf boxes are blank; there is an anatomical figurine. No readable text.

PREVIOUS FAILURE: femur-in-wrong-leg FIXED; no toe lobe on the resting ankle (FIXED or absent); head at the frame edge NOT fixed (clipped). previous_failure_fixed = false.

Addendum to #5 (cond-lbp-assess-a), crops read afterwards: hipjoint_5x, prac_legs_floor, bg_left.
- Hip joint: the raised femur's head abuts a socket ring at the anterior pelvis (0.465-0.50, 0.47-0.52). There is no second femoral head. Stylised but plausible.
- Under the table: the practitioner has 2 trouser legs (his left leg at 0.555-0.63 down to the shoe at 0.945; his right leg mostly hidden behind the lift column at 0.38-0.40). OK.
- Left background: window, plant, blurred buildings. No text.
- Patient hand-to-forearm ratio about 0.83 (slightly large; not flagged, the arm is foreshortened).

## 6. cond-lbp-assess-b (2336x1744, 4:3) -- provisional verdict FAIL (head cut off at the left edge; toes at the right edge)

Crops read: head_left_edge, raised_foot, raised_toes_7x, resting_foot, resting_toes_edge_8x, prac_hand_leg, prac_leg_hand_thumb_enh (8x),
prac_hand_hip, pat_hand, pat_fingers_enh (9x), pat_arm, prac_L_arm, legs, overlay_full, overlay_pelvis, hipjoint_5x, prac_top_face,
bg_right, bg_left, prac_legs_floor. Numeric: r3c_b1_edges.py, plus a per-pixel RGB scan of the last 40 columns through each toe row.

SCENE: the same set-up as variant a, on a wooden folding table. The raised right leg is about 26 deg (hip 0.47,0.52 to ankle 0.89,0.29). The practitioner's left hand is on the distal
shin just above the trouser cuff and ankle; his right hand is on the patient's iliac crest or hip. It matches the brief.

COMPOSITION -- KEY DEFECTS
- The back of the patient's HEAD IS CUT OFF by the left frame edge [0.0,0.42,0.05,0.56]: hair runs off the edge from y 0.445 to 0.555, with the ear at x 0.045-0.075 (column 0 is 47% dark
  across rows 0.40-0.58). The round-2 item "head touched the frame edge" is NOT fixed (clipped).
- The resting foot's toes nearly touch the right edge [0.97,0.49,1.0,0.56]. The toe tips end at about column 2325 of 2336 (a toe-edge pixel of 141/93/71 at col 2324, then wall
  pixels of 174/151/134 from col 2328), a margin of about 10 px (0.4%). The brief's "clear space beyond his toes" is not met. The 7:5 page crop trims only the top and bottom,
  so it changes neither edge.

HANDS
- Practitioner LEFT hand on the raised shin [0.74,0.27,0.83,0.37]: 4 fingers drape over the near side of the shin, fingertips at about (0.78,0.35), (0.79,0.353), (0.80,0.345),
  (0.805,0.32); the middle finger reaches farthest and the little finger is shortest. The thumb base folds over the top of the shin on the image-left (0.745,0.30-0.32) with its tip on the
  far side (hidden), which is correct for a left hand of a man facing the camera. Knuckle width about 128 px, natural. The arm is continuous: shoulder, rolled sleeve at 0.62-0.66,0.14-0.21,
  forearm, wrist 0.75-0.77,0.27-0.29.
- Practitioner RIGHT hand on the hip [0.39,0.42,0.47,0.50]: 5 digits (4 fingertips at x 0.40-0.44, y 0.477-0.49, with the middle finger lowest; the thumb extends to the image-right
  at 0.455-0.465,0.445), correct side for a right hand. The arm is continuous from the right shoulder through the sleeve (0.30-0.36,0.25-0.29).
- Patient RIGHT hand on the table [0.41,0.61,0.54,0.67]: seen from the ulnar side. 4 fingertips (little 0.495,0.662; ring 0.513,0.657; middle 0.527,0.652, the longest;
  index 0.522,0.647 behind), with the thumb hidden medially. Wrist to fingertip about 245 px; hand-to-forearm ratio about 0.75 (natural). The left arm is occluded by the torso.

FEET
- Raised RIGHT foot [0.87,0.15,0.96,0.33]: 5 toes clearly (big toe 0.93,0.16; then 0.945,0.162; 0.948,0.172; 0.949,0.18; 0.947,0.19). Natural size, and it is on the raised leg.
- Resting LEFT foot [0.87,0.49,1.0,0.64]: 5 toes clearly (nails at 0.98,0.505; 0.985,0.515; 0.987,0.525; 0.987,0.535; 0.985,0.546). Natural size. The ankle shows a normal medial
  malleolus (0.905,0.60) and NO toe-like lobe, so the round-2 lobe item is FIXED.

BODY
- Proportions are natural. Shoulder joint about 0.155 to hip about 0.455 is 701 px; hip to heel about 0.955 is 1168 px; the ratio of 1.67 is close to a real adult's 1.7 and better than a's 1.42.
  Upper arm about 352 px against forearm 327 px. Thigh about 519 px against shin about 529 px (the shin is slightly long; within stylisation).
- Patient: 2 legs, 1 visible arm plus 1 occluded. Practitioner: 2 arms, 2 trouser legs under the table (0.36-0.43 and 0.52-0.56) to shoes at the bottom edge (shod, so not checked as feet).

OVERLAY
- Correct orientation. The lumbar spine runs horizontally in the torso (0.22-0.40, y 0.53-0.575); a side-view pelvis sits at the hip (0.39-0.50, 0.48-0.61); the femur runs up the RAISED thigh
  to the knee (0.673,0.385), which is close to the expected 0.688,0.398. There is no bone in the resting thigh, so the round-2 femur item is FIXED in this variant too.
- MINOR (anatomy, stylised): the hip joint is muddled [0.43,0.47,0.50,0.61]. The raised femur's proximal end meets the pelvis at the front of the iliac crest or ASIS (0.44-0.49, 0.48-0.535),
  while a separate, shaftless femoral head sits in the acetabulum lower down (0.44-0.47, 0.565-0.60). A chiropractor looking closely would see that the raised thigh bone is not seated in the socket.
  Not gross at page size.
- MINOR (brief): the overlay also draws the tibia and fibula in the raised shin (0.68-0.80), and the spine is about 9 segments (brief: lumbar only).
- RED: the lower lumbar spine and lumbosacral junction (0.36-0.40, 0.53-0.57), sweeping over the iliac crest toward the hip flexor under the practitioner's hand (0.38-0.47, 0.47-0.52). Matches the brief.

FACE / DEVICES / TEXT
- The practitioner is cut at the collar; only a throat sliver shows in the collar opening (0.465-0.505, 0-0.03), with no chin, lips or beard. The page crop's top trim (0.0216) removes most of it.
- No instrument. The background device screen (0.22-0.26,0.26-0.31) is blurred and blank; the wall art is a landscape. No readable text.

PREVIOUS FAILURE: toe lobe FIXED; femur in the raised leg FIXED; head at the frame edge NOT fixed (clipped). previous_failure_fixed = false.
PAIR: neither variant passes, because both clip the back of the head at the left edge, and the toes are within 1.1% (a) or 0.4% (b) of the right edge. If one is salvaged by
extending the canvas, b is the better base (natural proportions, 5 distinct toes on both feet); a has the cleaner hip joint but a long torso.

## Cross-check notes (written before the report)
- The auto-assess-a neck glow was re-measured over a wide band (x 0.34-0.54): red share is 0.000 for every row from y 0.22 to 0.33, and the glow starts at 0.34. In b the same band shows red from 0.28-0.29.
  A visual recheck crop (r3c__cond-auto-assess-a__neck_recheck.png) confirms the cervical column is pure teal through the collar. The a verdict stays at not fixed.
- lbp leg-to-torso ratio depends on the hip-joint reference (overlay femoral head against socket), about +-0.1. Robust ranges: a is about 1.41-1.48, b about 1.58-1.67; an adult is about 1.7.
- Report boxes use full-image fractions for both hands and defects (the same convention as r2_*-report.json).

# r3c_batch2 review notes (round-3c re-renders)

Method: full image read, then 2-3.5x LANCZOS crops via scratchpad r3c2_crop.py into
audit_v2/crops/r3c2__<name>__<what>.png. Boxes are full-image fractions [x0,y0,x1,y1].

## 1. cond-osteo-treat-a (2048x1360) -- provisional verdict FAIL (overlay brief / previous failure)

Crops read: hand-prac-right-instrument, hand-prac-right-fingers-zoom, hand-prac-left-shoulder, overlay, tip,
arm-patient-left, arm-patient-right, device-screen.

Composition: camera at the foot end, patient face down, silver hair at the top centre, blanket over hips/legs.
Practitioner stands at the HEAD end of the table facing the camera (brief said "at the side"); his face is out of
frame (cut at the chest). OK.

HANDS
- Practitioner RIGHT hand (image left) gripping the chrome instrument [0.32,0.24,0.47,0.43]: 5 digits. Little,
  ring and middle curled (tips at crop-zoom x 270/400/530), index extended down the barrel with its nail visible,
  thumb on the image-right of the barrel behind it. Thumb on the image-right is correct for a right hand seen from
  in front (palm down, fingers toward camera). Natural size, attached to his right forearm/rolled sleeve. OK.
- Practitioner LEFT hand (image right) resting on her right shoulder [0.58,0.37,0.70,0.53]: 5 digits, thumb along the
  top of the shoulder on the image-left (medial) side, 4 fingers draped down with nails. Correct side for a left hand.
  OK.
- Patient hands: not visible (both forearms hang down beyond the table edges). Not assessable, nothing wrong.

FEET / BODY
- No bare feet in frame (blanket). Both patient upper arms run from the shoulders down to the elbows resting on the
  table edge, forearms dropping out of view; symmetric, natural length for the foreshortened view. No extra limbs.

OVERLAY [0.35,0.41,0.60,0.72]
- Column runs straight up the midline of the back (x ~0.477 orig 976 px, table centre ~988 px), vertical, from
  the base of the neck down to the blanket. Orientation fixed vs round 2.
- BUT it is not "a short mid-back column with only the inner ends of a few ribs": about 11-12 pairs of long curved
  ribs (reaching ~60% of the way to each flank) fill the whole back, and the lowest ribs reach the blanket/waist line
  (y ~0.71-0.72, box [0.35,0.62,0.60,0.72]). This is the same "ribs down to the waist" failure named for round 2.
  A visitor would not notice, a chiropractor would see ribs over the lumbar zone. Not failing on rib count itself.

RED GLOW / TREATMENT
- Glow centred on the spine in the upper-mid thoracic region [0.44,0.45,0.52,0.60] = mid back. OK.
- Instrument (chrome pen, black flat rubber tip, no needle) lands just left of the spine at the TOP edge of the glow
  [0.453,0.46,0.473,0.48]; touches the glow, hottest zone is a little below the tip. Acceptable.

FACE / DEVICES / TEXT
- Practitioner face not in frame. Left-edge device screen is blurred, no readable text. No text elsewhere.

PAGE CROP 7:5 (72 px off each side): left elbow at x ~280 px and right elbow at ~1720 px stay in. Nothing cut.

PREVIOUS FAILURE: spine angle fixed; ribs still full back length down to the waist -> NOT fixed.

## 2. cond-osteo-treat-b (2048x1360) -- verdict MINOR (better of the pair)

Crops read: hand-prac-right-instrument, hand-prac-right-fingers-zoom, hand-prac-left-shoulder(-wide),
hand-prac-left-fingertips-zoom, arm-hand-patient-left/right, hand-patient-left-zoom, hand-patient-right-zoom,
overlay, tip, monitor, spine-model.

Composition: same as -a (practitioner at the HEAD end facing the camera, face out of frame, cut at the chest).

HANDS
- Practitioner RIGHT hand (image left) on the instrument [0.34,0.25,0.48,0.44]: 5 digits: little, ring, middle curled,
  index extended down the barrel (nail visible), thumb on the image-right behind the barrel. Correct side. OK.
- Practitioner LEFT hand (image right) on her right shoulder [0.62,0.34,0.74,0.54]: 5 digits: thumb on the image-left
  (medial) pointing down onto the shoulder top, index/middle/ring with nails, little finger mostly behind the ring
  finger, its nail edge visible in the 5x zoom. Correct side. OK.
- Patient RIGHT hand (image right, tucked beside the chest, fingers toward her head) [0.78,0.59,0.86,0.72]:
  4 visible fingertips with pale nails in a natural descending row, thumb hidden under her upper arm. Natural size
  (4-finger span ~97 px vs upper-arm width ~180 px). OK. At 4x the blurred stubby tips could read as toes, but
  at page size they read as fingertips.
- Patient LEFT hand (image left) [0.17,0.60,0.25,0.70]: 2-3 blurred fingertips visible beyond the upper arm, rest hidden.
  Nothing wrong.

FEET / BODY
- No feet in frame (blanket). Arms in a push-up-start pose: upper arms back to elbows at the table edge near the
  camera (x ~0.17 and ~0.87), forearms folded forward under them, hands beside the chest. Plausible, symmetric,
  natural lengths. No extra limbs.

OVERLAY [0.39,0.36,0.65,0.70]
- Column straight and vertical in the midline (x ~1054 px; back edges at y 800 about 707-1423 px, centre ~1065).
  From the base of the neck to the blanket, so longer than the "short mid-back column" asked for (brief gap, not an
  anatomy error).
- Ribs: about 7 pairs of 2/3-length arcs sloping down and out (correct posterior-view direction). They end about
  50 px above the blanket (lowest tips y ~0.655, blanket ~0.69), and the bottom 2-3 vertebrae have no ribs beside them.
  So they no longer run down to the waist. MINOR: the ribs float 20-35 px clear of the transverse processes (not
  joined to the column), and there are more and longer ribs than "inner ends of a few" [0.40,0.42,0.64,0.66].

RED GLOW / TREATMENT
- Glow on the spine in the upper-mid thoracic region [0.45,0.45,0.56,0.57] = mid back. The instrument (chrome pen,
  threaded collar, black flat rubber tip, no needle) lands on the glow just left of the spine at orig (997,657). OK.

FACE / DEVICES / TEXT
- No practitioner face. Background monitor screen is blank/blurred; a blurred spine model on a stand at the top right.
  No readable text.

PAGE CROP 7:5 (72 px off each side): elbows at x ~348 and ~1787 px stay in. Nothing cut.

PREVIOUS FAILURE: column straight up the midline; ribs no longer full length or down to the waist -> FIXED (rib
extent still more than "inner ends", minor).

-a FINAL: FAIL (only failing item: overlay ribs still reach the waist line, i.e. the round-2 failure persists;
hands/body are clean). Pair pick: -b.

## 3. cond-plantar-treat-a (2048x2048) -- provisional verdict FAIL (laser does not land on the glow)

Crops read: foot-full, toes, toes-zoom, toes-redchan (red channel, overlay suppressed; helper r3c2_redchan.py),
overlay-heel, laser-lines, hand-prac-right-laser, hand-prac-right-fingers-zoom, hand-prac-left, hand-prac-left-full,
hand-prac-left-digits-zoom, bg-window, bg-plant-monitor.
(The blotchy/posterised window seen in the downscaled full view is a viewer artefact: the 1x crops are smooth
bokeh, and the file has 370k unique colours.)

Composition: close side view of ONE bare right foot, medial arch toward the camera, heel on a folded towel, toes to
the right. Practitioner behind the table, face out of frame (cut at the chest). He holds the white laser head, which
hangs from a white articulated arm coming in from the top-left. Head ~300 px above the skin, no contact.

HANDS
- Practitioner RIGHT hand (image left) gripping the laser head [0.00,0.14,0.18,0.31]: 4 fingers wrap the housing
  (4 knuckles, 3 nails at the fingertips), thumb hidden behind the housing -> "4 visible". Natural, attached to his
  hairy forearm. OK.
- Practitioner LEFT hand hanging by the foot [0.52,0.41,0.62,0.58]: soft focus; thumb pointing down with a broad nail,
  index curled beside it, other fingers hidden behind -> "2 visible". Relaxed, plausible, no malformation. OK.

FOOT / BODY
- One foot, attached to the lower leg at the ankle. Heel on the towel, forefoot slightly raised. Length about 1120 px
  vs lower-leg thickness about 400 px, so it looks natural for a close foreground view (no longer oversized).
- Toes [0.65,0.60,0.83,0.74]: 5. Big toe on top with a nail, 2nd toe with a nail, and 3 smaller toes stacked
  below-left, seen as pads (the red-channel crop separates them). The stacked arrangement is a bit unusual for a
  medial view, but reads as a normal foot at page size. OK.

OVERLAY
- Side-view skeleton oriented correctly: calcaneus fills the heel, talus above it, midfoot bones, metatarsals running
  toward the toes. Not upside down. Plantar fascia band runs from the underside of the calcaneus along the sole to the
  ball of the foot. Good.
- MINOR: the toe-bone chains end inside toes 2-5, but the BIG TOE has no bones. The skeleton stops about 110 px short
  of the big-toe tip [0.77,0.65,0.83,0.70].

RED GLOW / TREATMENT
- Glow on the underside of the calcaneus at the fascia attachment [0.29,0.61,0.36,0.67]. Correct site.
- FAIL: the three red lines hit the skin at the back of the ANKLE above the heel (Achilles region, about orig
  600-660,1000-1020), fade out inside the ankle by about y 1190, and never reach the glow (centre about 692,1350).
  They land about 250-300 px (about 6 cm) above the pain site [0.29,0.48,0.34,0.59]. The brief says the glow must sit
  where the laser lands.
- Device: white head on a white articulated arm, three thin parallel red lines, no contact. Plausible.

FACE / TEXT: no face; blank monitor; no readable text.
PAGE CROP 1:1: no crop.

PREVIOUS FAILURE: toe count (5), orientation (heel bone in the heel) and size are fixed. "Red glow under the heel
where the laser lands" is NOT met, so marked not fixed.

## 4. cond-plantar-treat-b (2048x2048) -- verdict MINOR (better of the pair)

Crops read: foot-full, toes, toes-redchan, toes-low, toes-low-redchan, overlay-heel, laser-lines,
hand-prac-right-laser, hand-prac-right-fingers-zoom, hand-prac-left-on-foot, hand-prac-left-wide, bg-right,
bg-shelves. (The posterised look in the downscaled view is a viewer artefact; the 1x crops are smooth.)

Composition: close side view of ONE bare right foot, medial side toward the camera, lying on a folded towel. The
patient's dark trouser leg is rolled to mid-calf at the far left. The practitioner behind the table has his face out
of frame. A white laser head sits on a white articulated arm, with the stand's white pole visible behind. He steadies
the head with his right hand. Head about 250 px above the skin, no contact.

HANDS
- Practitioner RIGHT hand (image left) on the laser head [0.085,0.195,0.19,0.305]: soft focus, 4 fingers curled round
  the housing, thumb hidden behind it -> "4 visible". Attached to the forearm under a rolled sleeve. OK.
- Practitioner LEFT hand (image right) [0.43,0.415,0.54,0.515]: back of the hand and knuckles visible behind the foot's
  dorsum, fingers hidden behind the foot (resting on its far side) -> "0 visible". Attached to the left forearm.
  No malformation. OK.

FOOT / BODY
- One foot, attached at the ankle to a bare calf. Length about 1000 px vs lower-leg thickness about 380 px and
  ankle height about 375 px: natural proportions for a close foreground view.
- Toes [0.65,0.57,0.81,0.67]: medial view. Big toe in front with a correct nail; 3 lesser-toe pads clearly visible
  below-behind it, and a probable 4th partly under the overlay. No extra or fused toe, nothing malformed.
  Count "4-5 visible". The view hides the rest; nothing looks wrong.

OVERLAY
- Correct side view, not upside down. Distal tibia/fibula at the ankle, talus below them, calcaneus filling the heel,
  midfoot bones, 5 metatarsals running forward, toe-bone chains in the forefoot. Plantar fascia band runs from the
  underside of the calcaneus along the sole to the ball of the foot. Good.
- MINOR: as in -a, the toe chains stop about 95 px short of the big-toe tip. The nail half of the big toe has no
  bone [0.76,0.61,0.81,0.645].

RED GLOW / TREATMENT
- Glow at the underside of the calcaneus where the fascia attaches [0.36,0.625,0.40,0.655]. Correct site.
- The three thin red lines leave 3 emitters, cross the skin at the back of the ankle, and are drawn on through the
  heel so they converge exactly on the glow. The treatment lands on the pain site [0.25,0.35,0.40,0.655]. Stylised:
  lines visible inside tissue. Acceptable for an overlay.

FACE / TEXT: no face; framed picture, monitor and shelves are blurred; no readable text.
PAGE CROP 1:1: no crop.

PREVIOUS FAILURE: one foot, natural size, no 6/4-toe foot, skeleton the right way up with the heel bone in the heel,
toe bones toward the toes, fascia along the sole, glow under the heel where the laser lines end -> FIXED.

-a FINAL: FAIL (laser lands on the back of the ankle about 6 cm above the glow and fades out before reaching it).
Pair pick: -b.

## 5. svc-fx635-device-a (2048x2048) -- verdict MINOR

Crops read: hand-prac-right-arm, hand-prac-left-hanging, hand-prac-left-digits-zoom, foot-full, toes, toes-redchan,
toes-wide, toes-wide-redchan, overlay-heel, laser-lines, bg-monitor.

Composition: large white laser head [0.365,0.045,0.52,0.31] on a single articulated white arm entering from the left,
in the upper half of the frame. Practitioner's right hand rests on the arm, his face is out of frame (cut at the
chest). ONE bare right foot and lower leg on a folded towel below, medial side toward the camera. Head about 480 px
(about 11 cm) above the ankle skin, no contact.

HANDS
- Practitioner RIGHT hand on the arm bar [0.165,0.027,0.325,0.165]: back of the hand, 4 fingers draped over the bar
  (index at the top, little finger nearest the camera, 4 nails), thumb hidden behind the bar -> "4 visible".
  Natural, attached to a hairy forearm. (Middle-finger nail slightly yellow-tinted at 2x, not noticeable at page size.)
  OK.
- Practitioner LEFT hand hanging [0.52,0.415,0.60,0.567]: soft focus. Thumb pointing down with a broad nail, 2 curled
  finger tips below it, the rest hidden -> "3 visible". No malformation. OK.

FOOT / BODY
- One foot attached to the lower leg. Foot length about 1150 px vs calf thickness about 430 px: natural for the
  foreground.
- Toes [0.83,0.65,0.92,0.76]: 5 (3 upper toes with nails, 2 lower toes seen as pads; the red-channel crop confirms).
  Seen from the dorsal-medial angle. Natural lengths (free toe about 130 px, about 12% of the foot). OK.

OVERLAY
- Side-view skeleton the right way up. Distal tibia/fibula, talus, and a large calcaneus filling the heel (the heel
  bone is present now), midfoot, metatarsals forward. Plantar fascia band runs from under the calcaneus along the sole.
  Good.
- MINOR: the phalanx chains run into only the LOWER two toes (ending at about orig 1778,1457). The upper three toes
  (with nails) have no bones [0.835,0.655,0.915,0.71]. Visible to a careful viewer, not at a glance.

RED GLOW / TREATMENT
- ONE glow, at the underside of the calcaneus where the fascia attaches [0.365,0.69,0.42,0.75]. No second glow on the
  ball of the foot (checked the forefoot crops).
- Three thin red lines from 3 emitters cross the ankle skin and are drawn on to the back-lower calcaneus, ending
  inside the glow's halo (about 60 px from its centre). Lands on the pain site. OK.

FACE / TEXT: no face; background monitor blurred, no readable text.
PAGE CROP 1:1: no crop.

PREVIOUS FAILURE (no heel bone; second glow on the ball of the foot): heel bone present in the heel, single glow
under the heel where the lines end -> FIXED.

fx635-a extra checks (done while reviewing -b):
- toes-grid / toes-top-zoom: 5 toes confirmed. Toe 1 (top) has its nail at (1770-1805, 1344-1360) with a dark rim
  (cosmetic, only visible at 3x). Toe 2's nail is at (1810-1848, 1363-1390) and toe 3 at (1800-1840, 1390-1418) with
  a large rounded tip. Toe 4's nail is at (1755-1778, 1448-1468). Toe 5 is the lowest pad, with its tip at
  (1735, 1525).
- Redness map (r3c2_redness.py): the only red blob is the heel glow (redness mean 79 vs forefoot underside 17, skin
  about 43). The lines end at the upper-left edge of the glow halo, about 60-80 px from its core. Acceptable.
- Page-size (800 px) view reads cleanly.

## 6. svc-fx635-device-b (2048x2048) -- verdict MINOR

Crops read: hand-prac-knob, hand-prac-fingers-zoom, foot-full, toes-wide, toes-wide-redchan, toes-tips,
toes-tips-redchan, toes-top-zoom, toes-tip-edges (equalised, r3c2_edges.py), toes-grid and toes-top-grid (orig-px
grid, r3c2_grid.py), ball-of-foot, overlay-heel, laser-lines, laser-end-glow, arm-top, bg-monitor, pagesize,
redness-map.

Composition: a large white laser head [0.235,0.0,0.485,0.31]. Its top runs out of the frame; a horizontal arm runs
right to a joint knob, and the practitioner's right hand grips the knob. The practitioner stands at the right edge,
face out of frame (only shoulder, sleeve, shirt front, belt, trousers). ONE bare right foot and lower leg lie on a
folded towel, medial side toward the camera. Head about 480 px (about 10 cm) above the ankle skin, no contact.

HANDS
- Practitioner RIGHT hand on the arm joint [0.47,0.09,0.62,0.26]: 5 digits. 4 fingers curl round the joint on the
  image-left and front (2 nails visible at the bottom); the thumb presses the right side of the knob, nail visible.
  A right-hand thumb on the image-right is correct for his pose (facing image-left and toward the camera, palm down).
  Attached to his forearm under a rolled sleeve. OK.
- Left hand: not in frame.

FOOT / BODY
- One foot, attached at the ankle to a bare calf on the towel. Foot length about 1210 px vs leg thickness about 435 px
  (ratio 2.8, the same as the other foot shots). Natural.
- Toes [0.78,0.66,0.915,0.75]: 5. From the bottom: big toe (broad pad, nail at 1705-1720,1458-1475), 2nd (nail at
  1760-1795,1445-1468), 3rd and 4th (nails stacked at 1805-1845,1417-1440 and 1805-1850,1402-1420), little toe
  (nail at 1780-1808,1386-1398). The skin bump at (1772,1383) looks like the little toe's nail fold, not a 6th toe.
  MINOR (zoom only): the 3rd and 4th toe tips are pressed into one rounded outline carrying two stacked nails. At
  page size this reads as two toes side by side; at 4x it could read as one toe with two nails
  [0.879,0.683,0.911,0.73]. The lesser toes reach further right than the big toe, consistent with a slightly
  front-medial camera. Looks natural at page size.

OVERLAY
- Correct side view, not upside down. Tibia/fibula ends, talus, a calcaneus filling the heel, midfoot bones,
  metatarsals, 4 phalanx chains. Plantar fascia band runs from under the calcaneus along the sole. Good.
- MINOR: the chains end at x about 1656-1718, inside the proximal toes. The distal halves of the four lesser toes
  (tips at 1805-1862) have no bones [0.83,0.68,0.915,0.73]. The big-toe chain reaches its nail.

RED GLOW / TREATMENT
- ONE glow, under the calcaneus where the fascia attaches (core about 720-760,1440-1500) [0.33,0.69,0.39,0.74].
  Redness mean 102 vs skin 34-48. The pink underside of the big toe measures 34, which is skin, not a glow. No second
  glow on the ball of the foot.
- Three thin red lines fan out from the emitter at (714-764, 640). The middle line lands straight on the glow.
  MINOR: the left line runs down the back of the heel and then bends about 90 degrees at the bottom
  (about 660,1457) to run along the sole into the glow. The right line also angles in. A real beam cannot bend.
  Barely visible at page size [0.31,0.635,0.405,0.73].
- Device: plausible. The white head is on an articulated arm; the arm ends in a joint knob in his hand and the mount
  is above the frame (no stand visible, not wrong). No contact.

FACE / TEXT: no face; background monitor blurred (bg-monitor crop), no readable text.
PAGE CROP 1:1: no crop.

PREVIOUS FAILURE (no heel bone; second glow on the ball of the foot): the calcaneus is present and fills the heel,
there is a single glow under the heel, and the lines converge on it -> FIXED.

## Pair picks
- cond-osteo-treat: -b (-a FAIL: ribs still run down to the waist).
- cond-plantar-treat: -b (-a FAIL: the laser lands on the back of the ankle, about 6 cm above the glow).
- svc-fx635-device: -a (both MINOR; -a has straight parallel beams and a clearer articulated-arm device. -b has a
  bent beam, a larger toe-bone gap, and the zoom-only double-nail look).

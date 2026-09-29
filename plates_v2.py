"""Redraw the anatomy plates that failed the audit (owner likes the plate style; the anatomy has to be right for a
chiropractic site). Higgsfield Marketing Studio 2.5 Flare, direct mode, with the site's own plates as STYLE references.
Two variants per new plate (-a, -b) so the anatomy review can pick an accurate one. Two plates the owner likes are
EDITED instead (the current plate as the reference, targeted fixes only).
Audit findings driving each spec: audit/batch4-report.json.  Writes plates_v2_jobs.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "site", "assets")
STYLE_REFS = [os.path.join(A, f) for f in ("gen_anatomy_vertebra_disc.jpg", "gen_anatomy_shoulder_joint.jpg", "gen_anatomy_knee_joint.jpg")]
STYLE = ("The reference images show the house illustration style of a clinic website. Create a NEW illustration in "
         "exactly that style: a vintage medical engraving printed in deep teal ink with pale teal fills, crisp dark "
         "outlines and fine engraved hatching, on warm cream paper with a soft vignette; one subject centred with generous "
         "empty margins on every side; no background scene, no panel or frame behind the subject. ")
RULES = (" Anatomically exact: a chiropractor will check every bone and count. No text, letters, numbers, labels, "
         "arrows or leader lines anywhere.")

PLATES = {
    "cond-lbp-hero": ("3:2",
        "the lumbar spine in a true side view: EXACTLY FIVE lumbar vertebrae stacked above the sacrum. Each has a large, "
        "rounded vertebral body at the front (left of the image) and a short, thick, squared-off spinous process pointing "
        "straight back (right of the image); an intervertebral disc sits between every pair of bodies, five discs in all "
        "counting the one between the lowest lumbar vertebra and the sacrum, and an oval intervertebral foramen opens "
        "behind each disc. The column follows the gentle inward curve of the lower back. Below it the triangular sacrum "
        "and the small coccyx curve backward."),
    "cond-carpal-hero": ("3:2",
        "a palm-up view of the right hand and wrist skeleton: the ends of the radius and ulna on the left, the eight "
        "carpal bones in two rows, five metacarpals and all finger bones (three per finger, two in the thumb). A broad, "
        "semi-transparent pale band, the transverse carpal ligament, spans the WHOLE width of the wrist from the thumb "
        "side to the little-finger side. The median nerve is a single smooth pale-teal cord that runs from the forearm and "
        "passes UNDERNEATH the ligament band: the band is drawn on top of the nerve, the nerve is hidden beneath it and "
        "reappears below it, then divides into branches to the thumb, the index finger, the middle finger and the thumb "
        "side of the ring finger."),
    "cond-headache-hero": ("3:2",
        "the skull and the upper neck in a TRUE SIDE VIEW, every bone seen from the same side: a complete skull in profile "
        "facing right, with the rounded cranial vault, forehead, eye socket, cheekbone, upper and lower jaw with teeth, "
        "the ear opening and the mastoid process behind it; the skull rests on the atlas (C1) and the axis (C2), both "
        "also seen from the side, and below them C3, C4 and C5, each vertebra with its body at the front and a short "
        "spinous process pointing back. The skull is whole, not cut off at the top or the front."),
    "cond-osteo-hero": ("3:2",
        "two upper thigh bones (proximal femurs) side by side, each cut lengthwise and seen from the front, both drawn "
        "correctly: the round femoral head at the top on the inner side, the femoral neck angled up and inward from the "
        "shaft at about 125 degrees, the large greater trochanter at the upper outer corner, the small lesser trochanter "
        "on the inner side just below the neck, and the shaft continuing straight down, all inside a thin dense outer "
        "shell. Inside the cut surface of the LEFT bone the spongy bone is a dense, strong lattice of fine struts; inside "
        "the RIGHT bone the same lattice is visibly sparse, thin and porous, showing bone that has lost density."),
    "cond-pinched-hero": ("3:2",
        "two NECK (cervical) vertebrae in a true side view, one stacked on the other: small, short vertebral bodies at the "
        "front (left) with a thin disc between them, and short spinous processes at the back (right), clearly neck "
        "vertebrae, not the large lower-back kind. Behind the disc, between the two vertebrae, is the round intervertebral "
        "foramen. The disc, drawn in a warm pale cream tone, bulges backward into that opening and presses on a nerve "
        "root; the nerve root, a smooth pale-teal cord, passes out through the opening toward the front and down, and is "
        "visibly pinched narrower exactly where the bulging disc touches it."),
    "cond-frozen-hero": ("3:2",
        "the right shoulder seen from the front: the collarbone, the shoulder blade and the upper arm bone (humerus) "
        "hanging straight down at the side with its ball seated in the shallow socket. Two arcs share ONE centre, the ball "
        "of the shoulder joint: a long dotted arc tracing the full path the elbow travels when the arm is raised out to "
        "the side from hanging down all the way to straight overhead, and on that very same path a short solid pale-teal "
        "arc covering only the first part of it, from hanging down to about 70 degrees, showing the restricted range."),
    "cond-fibro-hero": ("3:2",
        "a standing human figure seen from behind, drawn in fine outline like an anatomical muscle study, arms relaxed "
        "slightly away from the sides with the palms facing forward, no facial features, no genitals, no jewellery, no "
        "wrist bands. Small solid deep-teal dots sit ON the body surface at the tender points visible from behind, the "
        "same on both sides, fourteen in all: at the base of the skull either side of the spine; at the midpoint of the "
        "top of each shoulder; just above the inner end of each shoulder blade; on the outer side of each elbow; in the "
        "upper OUTER quarter of each buttock; just behind the bony point of each outer hip; on the INNER side of each "
        "knee. The whole figure, head to feet, sits well inside the frame."),
    "cond-auto-hero": ("3:2",
        "the complete neck spine, all seven cervical vertebrae C1 to C7, in a true side view with the neck bent slightly "
        "forward, each vertebra with its body at the front (left) and its spinous process at the back (right), and above "
        "C1 only the base of the skull, cleanly outlined. Three thin concentric pale-teal rings centred on the middle of "
        "the neck pass through it like a shockwave, and no more than three."),
    "svc-hormone-thyroid": ("1:1",
        "the thyroid gland seen from the front at normal size: two slim, smooth lobes on either side of the windpipe, "
        "joined across the front of the windpipe by a NARROW, thin isthmus (a slim bridge, much smaller than the lobes); "
        "above it the thyroid cartilage (Adam's apple) and the ring of the cricoid cartilage, below it the ringed "
        "cartilage of the windpipe. Healthy and normal, not enlarged."),
}
EDITS = {  # the owner likes these two: keep the drawing, fix only what the audit found
    "cond-carpal-assess": ("3:2", os.path.join(HERE, "final", "full", "cond-carpal-assess.jpg"),
        "Keep this exact illustration: the same composition, pose, style, colours and line work. Change only these "
        "anatomical details: the vertebral stack at the top right is the LOWER neck (its top vertebra is an ordinary "
        "neck vertebra, not the ring-shaped atlas) and the nerve cords leave from its lowest levels; the inner end of the "
        "collarbone ends at a small piece of breastbone and does not touch the spine; remove the loose teal wash under "
        "the shoulder blade; the nerve's thumb branch continues into the thumb instead of ending in a starburst."),
    "cond-oa-hero": ("3:2", os.path.join(HERE, "final", "full", "cond-oa-hero.jpg"),
        "Keep this exact illustration: the same composition, style, colours and line work. Change only these details: "
        "draw the kneecap faintly with a thin light outline and low contrast; remove the three small circles on the "
        "inner rounded end of the thigh bone; draw the ligament in the notch between the bones as a thin fibrous band in "
        "a lighter tone than bone, clearly not bone."),
}

jobs = []
for name, (ar, subject) in PLATES.items():
    for v in ("a", "b"):
        jobs.append({"name": f"{name}-{v}", "model": "marketing-studio/image/flare", "images": STYLE_REFS,
                     "input": {"prompt": STYLE + "Subject: " + subject + RULES, "quality": "high", "moderation": "auto",
                               "resolution": "2k", "aspect_ratio": ar, "enhance_prompt": False}})
for name, (ar, ref, change) in EDITS.items():
    jobs.append({"name": f"{name}-edit", "model": "marketing-studio/image/flare", "images": [ref],
                 "input": {"prompt": change + RULES, "quality": "high", "moderation": "auto", "resolution": "2k",
                           "aspect_ratio": ar, "enhance_prompt": False}})
json.dump(jobs, open(os.path.join(HERE, "plates_v2_jobs.json"), "w"), indent=1)
print(f"{len(jobs)} plate jobs")

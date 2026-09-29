"""Round-3 fixes for the clinical photos where both round-2 variants failed review (audit_v2/r2_batch*-report.json),
plus shots whose composition doesn't survive the crop to the page slot.

What round 2 taught:
  - a face-down patient seen from the SIDE gets the overlay's spine drawn upright in the frame, across her body
    (fibro-treat a and b); seen from the foot or head end, the spine runs up the frame and the overlay lands right
    (stress-treat, disc-treat, scoliosis-treat-b all passed). Face-down shots are now taken from the foot end.
  - asking for "one hand on each side of the spine" while the practitioner stands to one side makes the model add an
    arm from the camera side (auto-assess a and b). One hand on the patient, the other at his side.
  - a whole-body shot generated at 3:2 loses its head or toes in the 7:5 crop; it is generated at 4:3 instead, where
    the crop trims the top and bottom.
Two variants per shot (-a, -b) into v2/round3c/.  python shots_v2r3c.py [1|2|3]  (sets FIX, FIX2, FIX3)
Writes jobs_v2r3c.json or jobs_v2r3c2.json."""
import json
import os

import shots_v2 as V
from shots_v2r2 import BODY, ONLY, PRONE, SCAP

HERE = os.path.dirname(os.path.abspath(__file__))
FOOT_END = ("the camera stands at the foot end of the treatment table looking along the patient's back toward her head, "
            "so her spine runs straight up the middle of the frame")

FIX = {  # name: dict(scene, anat, pain, guide[, gen, who])
    "cond-auto-assess": dict(
        scene="the patient sits on the edge of the treatment table, seen from behind; the practitioner stands at the "
              "patient's right side and rests only his RIGHT hand flat on the patient's upper back just beside the spine, "
              "fingertips pointing toward the neck, while his left arm hangs relaxed at his side; nothing else touches "
              "the patient, and no arm or hand enters the frame from the camera side or from any edge",
        anat="the neck and upper back only: the seven neck vertebrae and the upper thoracic spine in one midline column, "
             "with the two shoulder blades on either side, seen from behind; nothing below the shoulder blades",
        pain="the lowest neck vertebrae and the muscles between the shoulder blades", guide=SCAP + ONLY),
    "cond-fibro-treat": dict(
        scene=FOOT_END + ": the patient lies face down with her face in the face cradle and a soft blanket over her hips "
              "and legs; the practitioner stands at the side of the table and holds " + V.TOOL + " gently against the "
              "muscles beside her upper spine, his other hand resting flat on her back",
        anat="the upper and mid back only: the spine as one straight midline column running up the middle of the frame "
             "to the base of her neck, with the two shoulder blades on either side of it",
        pain="a few small scattered tender points on the muscles on either side of the upper spine",
        guide=PRONE + SCAP + ONLY),
    "cond-lbp-assess": dict(
        scene="the patient lies on his back on the treatment table, one leg raised straight to about 30 degrees; the "
              "practitioner's flat hand presses gently down just above that ankle while his other hand steadies the "
              "patient's hip; the camera is far enough back that the patient's whole body fits inside the frame with "
              "clear space beyond the top of his head and beyond his toes; natural adult proportions: the legs are "
              "longer than the torso",
        anat="the lumbar spine, the pelvis, and the thigh bone drawn inside the RAISED thigh", pain="the lower back and "
        "the hip flexor where it attaches to the lumbar spine", guide=ONLY, gen="4:3"),
}

FOOT_SIDE = ("a SIDE VIEW of the foot skeleton inside the foot: the heel bone (calcaneus) filling the heel, the ankle bone "
             "(talus) above it, the arch of the midfoot bones, the five long metatarsals and the toe bones running into the "
             "toes, and the plantar fascia as a band along the sole from the underside of the heel bone to the ball of the foot")
# second set (r2 batch 4 and 6): osteo-treat from the foot end; plantar and the FX-635 hero as ONE foot seen from the
# side (both round-2 plantar variants failed on toes, and the fx635 overlay had no heel bone)
FIX2 = {
    "cond-osteo-treat": dict(
        scene=FOOT_END + ": the patient, a woman in her seventies with short silver hair, lies face down on a well-padded "
              "treatment table with a pillow under her chest and a light blanket over her hips and legs; the practitioner "
              "stands at the side of the table and holds " + V.TOOL + " lightly against her mid back, his other hand "
              "resting still on her shoulder",
        anat="the mid back only: a short straight column of vertebrae running up the middle of her back, with the inner "
             "ends of a few ribs on either side", pain="the mid back", guide=PRONE + ONLY),
    "cond-plantar-treat": dict(
        scene="a close side view of the patient's bare right foot and ankle resting on a folded white towel at the end of "
              "the treatment table, the inner arch of the foot facing the camera; only this one foot is in the frame, "
              "natural adult size; " + V.FX.format(target="the heel"),
        anat=FOOT_SIDE, pain="where the plantar fascia attaches to the underside of the heel bone", guide=ONLY,
        who="an adult; only the lower leg and the right foot are in frame"),
    "svc-fx635-device": dict(
        scene="the white stand-mounted low-level laser on its single articulated arm fills the upper half of the frame, "
              "its head a hand's width above the patient's heel and projecting three thin red laser lines onto it without "
              "touching; below it, the patient's bare right foot and lower leg lie on a folded white towel at the end of "
              "the treatment table, seen from the side with the inner arch facing the camera; only this one foot is in "
              "the frame, natural adult size; the practitioner's hand rests on the laser arm",
        anat=FOOT_SIDE, pain="where the plantar fascia attaches to the underside of the heel bone", guide=ONLY,
        who="an adult; only the lower leg and the right foot are in frame"),
}

# third set (r2 batch 3): neck-treat seen from the head end got upside-down shoulder blades; osteo-assess's relaxed
# hanging hand came out as ribbon-strip fingers in both variants
FIX3 = {
    "cond-neck-treat": dict(
        scene=FOOT_END + ": the patient lies face down with her face in the face cradle and a light blanket over her hips "
              "and legs; the practitioner stands at the side of the table with his two hands resting one over the other "
              "on her upper back between the shoulder blades",
        anat="the upper back only: the upper thoracic spine in one midline column running up the middle of the frame to "
             "the base of her neck, and the two shoulder blades on either side of it, each with its broad top edge near "
             "the shoulder and its lower tip pointing down the back toward her feet",
        pain="between the shoulder blades and the base of the neck", guide=PRONE + SCAP + ONLY),
    "cond-osteo-assess": dict(
        scene="the patient, a woman in her seventies with short silver hair in a soft cardigan and slacks, stands on one "
              "foot beside the treatment table, seen from her left side: her left hand holds the edge of the table, and "
              "her right arm is on the far side of her body, out of view; the practitioner stands just behind her with "
              "both hands hovering close to her waist, ready to steady her",
        anat="the spine, the pelvis and the hip joints", pain="the mid back and the hip", guide=ONLY),
}

if __name__ == "__main__":
    import sys
    S = {s["name"]: s for s in json.load(open(os.path.join(HERE, "shotlist_v2.json")))}
    arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    SET = {"1": FIX, "2": FIX2, "3": FIX3}[arg]
    out = {"1": "jobs_v2r3c.json", "2": "jobs_v2r3c2.json", "3": "jobs_v2r3c3.json"}[arg]
    jobs = []
    for name, f in SET.items():
        who = f.get("who", S[name]["who"])
        p = (V.STYLE + "The scene is set in " + V.ROOM + ". Scene: " + f["scene"] + ". " + f["guide"]
             + V.OVERLAY.format(anat=f["anat"], pain=f["pain"]) + " " + V.PRACT + V.PATIENT.format(who=who) + BODY)
        gen = f.get("gen", S[name]["gen"])
        assert gen in V.FLARE_AR, (name, gen)
        for v in ("a", "b"):
            jobs.append({"name": f"{name}-{v}", "model": V.MODEL,
                         "input": {"prompt": p, "quality": "high", "moderation": "auto", "resolution": "2k",
                                   "aspect_ratio": gen, "enhance_prompt": False}})
    json.dump(jobs, open(os.path.join(HERE, out), "w"), indent=1)
    json.dump({**FIX, **FIX2, **FIX3}, open(os.path.join(HERE, "v2", "round3c_briefs.json"), "w"), indent=1)
    print(len(jobs), "jobs for", len(SET), "shots ->", out)

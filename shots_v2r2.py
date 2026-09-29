"""Round-2 fixes for the v2 photos that failed review (audit_v2/batch*-report.json).

The same look, with these changes:
  - overlays limited to the treated region, described as a BACK VIEW seen from above for face-down patients
    (spine = one midline row of spinous processes toward the skin; shoulder blades pinned to the upper back);
  - simpler poses and fewer hands in frame (the failures were mirrored/3-4-finger hands, 3 legs, 6 toes, long limbs);
  - a stronger anatomy rule block.
Two variants per shot (-a, -b) into v2/round2/.  Writes jobs_v2r2.json."""
import json
import os

import shots_v2 as V

HERE = os.path.dirname(os.path.abspath(__file__))
BODY = (" Anatomy of the people: every hand has exactly five digits (one thumb and four fingers) with the thumb on the "
        "correct side for that left or right hand, is natural adult size in proportion to its body, and joins its own "
        "arm through a visible wrist. Every bare foot has exactly five toes and natural adult size. Each person has "
        "exactly two arms and two legs, all complete and joined to the body, in natural adult proportions. Every body "
        "is complete and continuous. No text, logos, labels or readable screens.")
PRONE = ("Because the patient lies face down and the camera looks down at the back, the overlay is a BACK VIEW (posterior "
         "view) seen from above: the spine is a single straight column along the midline groove of the back, its row of "
         "spinous processes pointing up toward the skin and the camera, the vertebral bodies hidden beneath. ")
SCAP = "The shoulder blades sit on the UPPER back, one on each side of the spine, just below the shoulders. "
ONLY = "Draw only the structures named, not the whole skeleton. "

FIX = {  # name: (scene, overlay anatomy, pain site, extra overlay guidance)
    "cond-auto-assess": (
        "the patient sits on the edge of the treatment table, seen from behind; the practitioner's two hands rest flat on the upper back, one on each side of the spine",
        "the neck and upper back only: the seven neck vertebrae and the upper part of the thoracic spine with the two shoulder blades, seen from behind; nothing below the shoulder blades",
        "the lower neck and the muscles between the shoulder blades", SCAP + ONLY),
    "cond-fibro-treat": (
        "the patient lies face down on the treatment table with a soft blanket over her legs; the practitioner holds " + V.TOOL + " gently against the muscles beside her upper spine, his other hand resting flat on her back",
        "the upper and mid back only: the spine's midline column and the two shoulder blades", "a few small scattered tender points on the muscles either side of the upper spine", PRONE + SCAP + ONLY),
    "cond-lbp-treat": (
        "the patient lies face down on the treatment table, a light blanket over his legs, his lower back bare; " + V.FX.format(target="the lower back") + "; the practitioner's hand rests on his upper back",
        "the lower back only: five lumbar vertebrae in a straight midline column ending at the triangular sacrum, with the two hip bones spreading to either side of the lower back like wings; the tailbone points toward his feet",
        "the two lowest lumbar vertebrae and the muscles beside them", PRONE + ONLY),
    "cond-osteo-treat": (
        "the patient, a woman in her seventies with short silver hair, lies face down on a well-padded treatment table with a pillow under her chest; the practitioner holds " + V.TOOL + " lightly against her upper back, his other hand resting still on her shoulder",
        "the mid back only: a short straight midline column of vertebrae with the inner ends of a few ribs on either side", "the mid back", PRONE + ONLY),
    "cond-pinched-treat": (
        "the patient lies face down on the treatment table, a light blanket over his legs; " + V.PEMF.format(target="his upper back between the shoulder blades") + ", the console standing on a small side table beside the table",
        "the neck and upper back: the column of vertebrae aligned exactly with the groove down the middle of his back, with one small nerve branch leaving the spine at the base of the neck",
        "that nerve branch at the base of the neck", PRONE + ONLY),
    "cond-scoliosis-treat": (
        "the patient lies face down on the treatment table with her arms resting along her sides; the practitioner's two hands rest on the muscles beside her mid spine",
        "the mid and lower back only: the spine as a single column along the middle of the back with a gentle sideways S-curve", "the muscles on the side of the curve carrying the uneven load", PRONE + ONLY),
    "cond-stress-treat": (
        "the patient lies face down on the treatment table with her face in the face cradle; the practitioner's thumbs press into the thick muscles running from her neck to the tops of her shoulders",
        "the neck vertebrae in a midline column and the trapezius muscle fanning from the base of the skull out to each shoulder, with the tops of the shoulder blades just below the shoulders",
        "the tops of the shoulders and the base of the neck", PRONE + SCAP + ONLY),
    "cond-neck-treat": (
        "the patient lies face down on the treatment table with her face in the face cradle; the practitioner's two hands rest one over the other on her upper back between the shoulder blades",
        "the upper back only: the upper thoracic spine in a midline column and the two shoulder blades on either side", "between the shoulder blades and the base of the neck", PRONE + SCAP + ONLY),
    "cond-shoulder-treat": (
        "the patient, a man in his forties in a grey tank top, sits on the edge of the treatment table seen from behind and slightly to the side; the practitioner's fingertips work along the inner edge of his shoulder blade while his other hand supports the front of his shoulder",
        "the shoulder blade, the rotator cuff muscles and the shoulder joint, seen from behind, sitting on the upper back exactly where his shoulder blade is", "the rotator cuff tendon at the top of the shoulder", SCAP + ONLY),
    "cond-disc-treat": (
        "the patient lies face down on the treatment table, a light blanket over his legs; " + V.PEMF.format(target="his lower back") + ", the console standing on a side table; the practitioner checks the console",
        "the lower back only: five lumbar vertebrae in a straight midline column ending at the sacrum", "between the two lowest lumbar vertebrae", PRONE + ONLY),
    "cond-pregnancy-treat": (
        "the patient sits upright on the edge of the treatment table in side profile, her whole head inside the frame and her rounded pregnant belly clearly visible, both feet on a small wooden step; the practitioner stands behind her with both hands resting gently on her lower back",
        "a SIDE VIEW of the lower spine and pelvis matching her side-on pose: the lumbar vertebrae stacked vertically with their bodies toward her belly and their spinous processes toward her back, the sacrum curving backward at the base, and the hip bone seen from the side",
        "the sacroiliac joint at the back of the pelvis", ONLY),
    "cond-tennis-treat": (
        "a close view of the patient's bent arm resting on a folded white towel, the elbow joint clearly in the centre of the frame and the whole forearm and hand in view; the practitioner holds " + V.COLD.format(target="the bony point on the OUTER side of the elbow (the lateral epicondyle)") + ", its cable hanging freely from the probe",
        "the elbow joint (the lower end of the upper arm bone and the upper ends of both forearm bones, which run all the way to the wrist) and the extensor tendons running from the outer elbow down the forearm",
        "the tendon attachment on the outer side of the elbow", ONLY),
    "ak-legit-hero": (
        "an intimate close-up of a manual muscle test: the patient's forearm is held level with the elbow bent and the fist closed; the practitioner's FLAT palm rests on the back of her wrist pressing gently down, his other hand steadying her elbow; only the two pairs of hands and forearms fill the frame",
        "the two forearm bones (radius and ulna) and the forearm muscles only, no hand bones", "the forearm muscle being tested", ONLY),
    "cond-carpal-treat": (
        "a close view from above at table height: the patient's right forearm and open right hand rest palm-up on a folded white towel, the hand natural adult size with the thumb on its correct side; the practitioner holds " + V.COLD.format(target="the crease of the wrist") + "; his other hand is out of frame",
        "the wrist and hand bones, each finger's bones running the full length of the finger, and the median nerve passing through the carpal tunnel", "the carpal tunnel at the base of the palm", ONLY),
    "cond-headache-assess": (
        "the patient sits upright on the treatment table seen from behind and slightly to the side; the practitioner stands behind her and only his two hands are visible, resting on either side of the back of her neck just below the base of her skull, fingertips pressing gently",
        "the skull base and the upper neck vertebrae", "the muscles at the base of the skull and the upper neck", ONLY),
    "cond-lbp-assess": (
        "the patient lies on his back on the treatment table with his whole body in frame from head to feet, one leg raised straight to about 30 degrees; the practitioner's flat hand presses gently down just above that ankle while his other hand steadies the patient's hip; natural adult proportions: the legs are longer than the torso",
        "the lumbar spine, the pelvis and the hip joint of the raised leg", "the lower back and the hip flexor where it attaches to the lumbar spine", ONLY),
    "cond-oa-assess": (
        "the patient stands barefoot on a pale wooden floor in a shallow squat with his hands resting on his own thighs; the practitioner kneels on one knee beside him in a natural kneeling pose, one hand on the outer side of the patient's knee",
        "the knee joint with the thigh and shin bones", "the inner side of the knee joint", ONLY),
    "cond-oa-treat": (
        "the patient sits on the treatment table leaning back on his hands with BOTH legs straight out in front of him along the table, side by side; " + V.FX.format(target="the knee of the leg nearer the camera"),
        "the knee joint with the thigh bone, shin bone and kneecap of that leg", "the inner side of that knee joint", ONLY),
    "cond-osteo-assess": (
        "the patient, a woman in her seventies with short silver hair in a soft cardigan and slacks, stands on one foot beside the treatment table holding its edge with ONE hand, her other arm relaxed at her side; the practitioner's hands hover close to her waist, ready to steady her",
        "the spine, the pelvis and the hip joints", "the mid back and the hip", ONLY),
    "cond-plantar-treat": (
        "a close view of the patient's two bare feet resting side by side over the end of the table on a rolled towel, soles toward the camera, natural adult size with five toes each; " + V.FX.format(target="the heel of one foot"),
        "the bones of the foot and the plantar fascia band running from the heel to the toes", "the plantar fascia where it attaches to the heel", ONLY),
    "svc-cold-hero": (
        "the patient sits on the treatment table with one leg extended and grey trousers rolled above the knee; the practitioner holds " + V.COLD.format(target="the side of the knee") + " with one hand; his other hand is out of frame",
        "the knee joint", "the inner side of the knee joint", ONLY),
    "svc-fx635-device": (
        "a close view of the laser head on its single articulated arm above the patient's heels: both bare feet side by side over the end of the table on a rolled towel, soles toward the camera, natural adult size with five toes each; " + V.FX.format(target="one heel"),
        "the bones of the foot and the plantar fascia", "the heel", ONLY),
}

WHO = {  # patient descriptions that must follow the new poses
    "cond-shoulder-treat": "a man in his forties in a plain grey tank top, seated",
    "cond-disc-treat": "a man in his thirties, lying face down, a light blanket over his legs",
}

if __name__ == "__main__":
    S = {s["name"]: s for s in json.load(open(os.path.join(HERE, "shotlist_v2.json")))}
    jobs = []
    for name, (scene, anat, pain, guide) in FIX.items():
        s = dict(S[name], scene=scene, anat=anat, pain=pain)
        s["who"] = WHO.get(name, s["who"])
        p = (V.STYLE + "The scene is set in " + V.ROOM + ". Scene: " + scene + ". " + guide
             + V.OVERLAY.format(anat=anat, pain=pain) + " " + V.PRACT + V.PATIENT.format(who=s["who"]) + BODY)
        for v in ("a", "b"):
            jobs.append({"name": f"{name}-{v}", "model": V.MODEL,
                         "input": {"prompt": p, "quality": "high", "moderation": "auto", "resolution": "2k",
                                   "aspect_ratio": s["gen"], "enhance_prompt": False}})
    json.dump(jobs, open(os.path.join(HERE, "jobs_v2r2.json"), "w"), indent=1)
    json.dump(FIX, open(os.path.join(HERE, "v2", "round2_briefs.json"), "w"), indent=1)
    print(len(jobs), "jobs for", len(FIX), "shots")

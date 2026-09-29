"""Photo set v2 (owner, 2026-09-28): the "anatomy overlay" direction on Higgsfield Marketing Studio 2.5 Flare.

Owner direction:
  - the overlay look (owner-approved), always in a REAL clinic scene (a plain backdrop "looks fake/lame");
  - a soft red "reddening" at the painful / tense structure, with the treatment focused on it, on every clinical shot;
  - hands reviewed hard (fingers are the weak spot of every model);
  - mixed with the illustration-only plates, which stay.
Every clinical photo: real room behind, teal engraving-line overlay of the relevant anatomy, red glow at the pain site.
Non-body shots (desk, forms, consultation) are premium editorial scenes without the overlay.
Builds jobs_v2.json for hf-batch.mts.  python shots_v2.py [pilot]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = "marketing-studio/image/flare"

ROOM = ("a real, modern physical-medicine clinic fills the background: pale oak cabinetry, open shelves with folded "
        "towels and a few plants, a large window with soft daylight, contemporary medical equipment; shallow depth of "
        "field, so the room is softly blurred but clearly a real place, never a plain studio backdrop")
OVERLAY = ("Over the patient's body, a luminous augmented-reality anatomy overlay: {anat}, drawn in delicate glowing teal "
           "engraving lines exactly where they sit under the skin, crisp and anatomically precise, like a living "
           "anatomical plate. The painful area glows with a soft, diffuse red-orange warmth inside the body at {pain}, "
           "subtle, like inflamed tissue seen through the skin, and the treatment is focused precisely on that red area. "
           "The overlay follows the body's real position and orientation: it lies inside the body exactly where those "
           "structures are for this pose (for a person lying down, the spine runs along the length of the body, "
           "horizontal in the frame), never pasted flat or upright across it.")
FX = ("a white stand-mounted low-level laser head on an articulated arm, positioned a hand's width above {target} and "
      "projecting three thin red laser lines onto the skin without touching it")
COLD = "a small white handheld low-level laser probe held just above {target}, casting a small red glow on the skin"
PEMF = "a flat white ring-shaped PEMF coil resting on {target} over a thin cloth, its cable running to a small white console"
TOOL = "a small chrome spring-loaded adjusting instrument shaped like a thick pen with a flat rubber tip (no needle)"
PRACT = ("The practitioner is a man in a crisp white dress shirt with the sleeves rolled to the forearm and dark trousers, "
         "framed from the chest down so his head and face are out of the frame.")
PATIENT = " The patient is {who}; the patient's face may be seen, relaxed, eyes closed or looking away."
HANDS = (" Hands: every hand anatomically perfect, five fingers each with natural joints and nails, a natural grip, no "
         "fused, extra or missing fingers. Every body complete and continuous. No text, logos, labels or readable screens.")
STAFF = ("This practice has exactly one clinician: a man in a crisp white dress shirt with the sleeves rolled and dark "
         "trousers, always framed so his head is out of the frame. There is no receptionist, nurse or other staff, and "
         "nobody wears a white coat or scrubs.")
STYLE = "Premium editorial photograph for a luxury health-technology brand campaign, not stock photography. "

S = []  # dicts: name, page, section, slot, kind(overlay|editorial), gen, crop, who, scene, anat, pain


def clin(name, page, section, slot, gen, crop, who, scene, anat, pain):
    S.append(dict(name=name, page=page, section=section, slot=slot, kind="overlay", gen=gen, crop=crop, who=who,
                  scene=scene, anat=anat, pain=pain))


def edit(name, page, section, slot, gen, crop, scene):
    S.append(dict(name=name, page=page, section=section, slot=slot, kind="editorial", gen=gen, crop=crop, scene=scene))


# ---------------------------------------------------------------- conditions (older nine: assessment + treatment)
clin("cond-auto-assess", "conditions/auto-accident-injury", "The questions this examination is built to answer", "assessment", "3:2", "7:5",
     "a man in his thirties in a plain navy t-shirt",
     "the patient sits on the edge of the treatment table, seen from behind and slightly to the side; the practitioner's two hands rest flat on either side of the patient's mid back and lower ribs, examining how they move",
     "the cervical and thoracic spine, the rib cage and the shoulder blades", "the muscles of the lower neck and between the shoulder blades")
clin("cond-auto-treat", "conditions/auto-accident-injury", "Settle the irritated tissue, then restore what stopped moving", "treatment", "3:2", "7:5",
     "a man in his thirties, lying face down, a light blanket over his legs",
     "the patient lies face down on the treatment table; " + FX.format(target="the base of the neck and the upper back") + "; the practitioner's hand rests on the patient's shoulder blade",
     "the cervical and upper thoracic spine and the shoulder blades", "the base of the neck and the top of the shoulders")
clin("cond-carpal-assess", "conditions/carpal-tunnel", "We follow the nerve from the neck to the fingertip", "assessment", "3:2", "7:5",
     "a woman in her forties in a sleeveless top",
     "the patient sits on the treatment table holding one arm straight out to the side; the practitioner's fingertips trace along the inside of her upper arm, following the nerve",
     "the median nerve running from the lower neck, under the collarbone, down the inner arm and through the wrist into the thumb and first fingers, with the arm bones faintly drawn", "the carpal tunnel at the wrist")
clin("cond-carpal-treat", "conditions/carpal-tunnel", "Free the tunnel, then unload the path into it", "treatment", "3:2", "7:5",
     "a woman in her forties; only her forearm and open hand are in frame",
     "a close view at table height: the patient's forearm and open hand rest palm-up on a folded white towel; the practitioner holds " + COLD.format(target="the crease of the wrist"),
     "the wrist and hand bones and the median nerve passing through the carpal tunnel", "the carpal tunnel at the base of the palm")
clin("cond-fibro-assess", "conditions/fibromyalgia", "One appointment that looks at the whole load", "assessment", "3:2", "7:5",
     "a woman in her fifties in a soft oatmeal sweater",
     "the patient sits upright on the treatment table seen from behind; the practitioner's hands rest lightly on the tops of both shoulders, feeling the muscles",
     "the spine from neck to pelvis and the shoulder blades, with the major back muscles in fine lines", "several small, scattered tender points: the base of the neck, the tops of the shoulders and beside the shoulder blades")
clin("cond-fibro-treat", "conditions/fibromyalgia", "Low force first, and less of it than you expect", "treatment", "3:2", "7:5",
     "a woman in her fifties, lying face down, a soft blanket over her legs",
     "the patient lies face down on the treatment table; the practitioner holds " + TOOL + " gently against the muscles beside her mid spine, his other hand resting flat on her back",
     "the thoracic and lumbar spine with the muscles beside it", "a few scattered tender points along the upper and mid back")
clin("cond-frozen-assess", "conditions/frozen-shoulder", "We test what the arm is standing on", "assessment", "3:2", "7:5",
     "a woman in her sixties in a sleeveless sage top",
     "the patient sits on the treatment table seen from behind and slightly to the side, slowly raising one arm forward; the practitioner's hand rests on her shoulder blade and his other hand lightly guides her elbow",
     "the shoulder joint, the shoulder blade, the collarbone and the upper arm bone", "the shoulder joint capsule")
clin("cond-frozen-treat", "conditions/frozen-shoulder", "Give the capsule a reason to let go", "treatment", "3:2", "7:5",
     "a woman in her sixties in a sleeveless sage top, seated, her head and face in soft profile clearly visible",
     "the patient sits upright on the edge of the treatment table, her whole upper body, head and both arms in frame; the practitioner stands beside and slightly behind her, one hand resting on her shoulder blade to steady it and the other hand supporting her elbow from below, gently guiding her arm up and out to the side in a slow, supported arc",
     "the shoulder joint, the shoulder blade, the collarbone and the upper arm bone", "the shoulder joint capsule")
clin("cond-headache-assess", "conditions/headache-migraine", "We look hardest at the days between the headaches", "assessment", "3:2", "7:5",
     "a woman in her thirties with her hair tied up",
     "the patient sits upright on the treatment table seen from behind and slightly to the side; the practitioner's fingertips rest at the base of her skull and on the jaw joint just in front of her ear",
     "the skull base, the jaw joint and the upper neck vertebrae", "the muscles at the base of the skull and the upper neck")
clin("cond-headache-treat", "conditions/headache-migraine", "Work the neck, the jaw and the load behind them", "treatment", "3:2", "7:5",
     "a woman in her thirties with her hair tied up",
     "the patient sits upright on the treatment table seen from behind; the practitioner holds " + COLD.format(target="the base of her skull where the neck meets the head") + ", his other hand steadying her shoulder",
     "the skull base and the upper neck vertebrae", "the muscles at the base of the skull")
clin("cond-lbp-assess", "conditions/low-back-pain", "We test the whole chain, not only the sore part", "assessment", "3:2", "7:5",
     "a man in his forties in a grey t-shirt and dark training trousers, lying on his back with his head on a pillow",
     "the patient lies on his back on the treatment table with one straight leg raised to about 30 degrees; the practitioner's flat hand presses gently down just above the ankle while his other hand steadies the opposite hip",
     "the lumbar spine, the pelvis and the hip joint of the raised leg", "the lower back and the hip flexor where it attaches to the lumbar spine")
clin("cond-lbp-treat", "conditions/low-back-pain", "Hands and instruments, in the same room", "treatment", "3:2", "7:5",
     "a man in his forties, lying face down, a light blanket over his legs, lower back bare",
     "the patient lies face down on the treatment table; " + FX.format(target="the lower back") + "; the practitioner's hand rests on the patient's upper back",
     "the lumbar vertebrae, the sacrum and the pelvis", "the two lowest lumbar vertebrae and the muscles beside them")
clin("cond-oa-assess", "conditions/osteoarthritis", "We measure what the joint is being asked to carry", "assessment", "3:2", "7:5",
     "a man in his sixties in grey trousers rolled to mid-calf, barefoot",
     "the patient stands barefoot on a pale wooden floor and bends his knees into a shallow squat; the practitioner kneels beside him with one hand on the side of the knee and the other at the hip, watching how the knee tracks",
     "the knee joint, the hip joint and the thigh and shin bones", "the inner side of the knee joint")
clin("cond-oa-treat", "conditions/osteoarthritis", "Change the load before you change the joint", "treatment", "3:2", "7:5",
     "a man in his sixties in dark shorts and a t-shirt, sitting on the treatment table leaning back on his hands",
     "both of the patient's legs are on the table and clearly visible: one leg extended straight along the table and the other knee bent with that foot flat on the table beside it; " + FX.format(target="the knee of the extended leg"),
     "the knee joint with the thigh bone, shin bone and kneecap", "the inner side of the knee joint")
clin("cond-osteo-assess", "conditions/osteoporosis", "The examination sets the force ceiling before anything else", "assessment", "3:2", "7:5",
     "a woman in her seventies with short silver hair, in a soft cardigan and slacks",
     "the patient stands on one foot beside the treatment table, fingertips of one hand resting on its edge, while the practitioner's hands hover close to her waist, ready to steady her",
     "the spine, the pelvis and the hip joints", "the mid back and the hip")
clin("cond-osteo-treat", "conditions/osteoporosis", "Low force, and the parts of this that are not adjusting at all", "treatment", "3:2", "7:5",
     "a woman in her seventies with short silver hair, lying face down with a pillow under her chest and a bolster under her ankles",
     "the patient lies face down on a well-padded treatment table; the practitioner holds " + TOOL + " lightly against her upper back, his other hand resting still on her shoulder",
     "the thoracic spine and the rib cage", "the mid back")
clin("cond-pinched-assess", "conditions/pinched-nerve", "We test the whole run of the nerve", "assessment", "3:2", "7:5",
     "a man in his fifties in a short-sleeved grey t-shirt",
     "a reflex check: the patient sits on the treatment table, his relaxed forearm resting on the practitioner's forearm with the elbow bent, while the practitioner taps the inside of his elbow with a small rubber reflex hammer",
     "the nerve running from the lower neck down the arm, with the neck vertebrae and the arm bones", "where the nerve leaves the lower neck")
clin("cond-pinched-treat", "conditions/pinched-nerve", "Take the pressure off, then keep it off", "treatment", "3:2", "7:5",
     "a man in his fifties, lying face down, a light blanket over his legs",
     "the patient lies face down on the treatment table; " + PEMF.format(target="his upper back between the shoulder blades") + "; the practitioner's hand adjusts the cable",
     "the cervical and upper thoracic spine with the nerve roots leaving it", "a nerve root at the base of the neck")

# ---------------------------------------------------------------- conditions (newer ten + sciatica: one treatment photo)
def newer(name, page, who, scene, anat, pain, gen="1:1", crop="1:1", section="What treatment involves"):
    clin(name, page, section, "new frame beside the treatment section", gen, crop, who, scene, anat, pain)


newer("cond-plantar-treat", "conditions/plantar-fasciitis", "a woman in her forties, lying face down, bare feet over the end of the table on a rolled towel",
      "a close view of the feet: " + FX.format(target="the heel and the arch of one foot"),
      "the bones of the foot and the plantar fascia band running from the heel to the toes", "the plantar fascia where it attaches to the heel")
newer("cond-pregnancy-treat", "conditions/pregnancy-pain", "a pregnant woman in her third trimester in a soft oatmeal knit dress, her rounded pregnant belly clearly visible in side profile",
      "the patient sits upright on the edge of the treatment table in side profile, her pregnant belly clearly visible, both feet resting on a small wooden step; the practitioner stands behind her with both hands resting gently on her lower back and the back of her pelvis",
      "the pelvis, the sacrum and the lower lumbar spine, upright inside her body as she sits", "the sacroiliac joint at the back of the pelvis")
newer("cond-sciatica-treat", "conditions/sciatica", "a man in his fifties in soft grey leggings, lying face down",
      "the patient lies face down on the treatment table; the practitioner holds " + COLD.format(target="the outer side of the hip, over the deep buttock muscles") + ", his other hand resting on the back of the thigh",
      "the lower spine, the pelvis and the sciatic nerve running from the lower back through the buttock and down the back of the thigh", "the sciatic nerve where it passes under the deep buttock muscle",
      gen="3:2", crop="3:2")
newer("cond-scoliosis-treat", "conditions/scoliosis", "a woman in her twenties in a sage sports top, lying face down",
      "the patient lies face down on the treatment table; the practitioner's hands work slowly along the muscles on one side of her mid back",
      "a spine with a gentle sideways curve and the rib cage", "the muscles on the side carrying the uneven load")
newer("cond-shoulder-treat", "conditions/shoulder-pain", "a man in his forties in a plain grey tank top, lying on his side with his head on a pillow",
      "the patient lies on his side on the treatment table; the practitioner's fingertips hook gently under the inner edge of his shoulder blade while his other hand cups the front of his shoulder",
      "the shoulder blade, the rotator cuff muscles and the shoulder joint", "the rotator cuff tendon at the top of the shoulder")
newer("cond-disc-treat", "conditions/slipped-disc", "a man in his thirties lying on his back with his knees over a soft bolster",
      "the patient lies on his back on the treatment table; " + PEMF.format(target="the table directly under his lower back") + "; the practitioner checks the console",
      "the lumbar vertebrae with the discs between them, one disc bulging slightly", "the bulging disc between the two lowest lumbar vertebrae")
newer("cond-stress-treat", "conditions/stress", "a woman in her thirties, lying face down with her face in the face cradle",
      "the patient lies face down on the treatment table; the practitioner's thumbs press slowly into the thick muscles running from her neck to the tops of her shoulders",
      "the neck vertebrae, the shoulder blades and the trapezius muscle in fine lines", "the tops of the shoulders and the base of the neck")
newer("cond-tennis-treat", "conditions/tennis-elbow", "a man in his fifties; only his arm is in frame, sleeve rolled well above the elbow",
      "a close view: the patient's arm rests on a folded white towel, fist loosely closed, the outer side of the elbow facing up; the practitioner holds " + COLD.format(target="the bony point on the outer side of the elbow"),
      "the elbow joint and the forearm extensor tendons", "the tendon attachment on the outer side of the elbow")
newer("cond-neck-treat", "conditions/upper-back-neck-pain", "a woman in her forties, lying face down with her face in the face cradle",
      "the patient lies face down on the treatment table; the practitioner's two hands rest one over the other on her upper back between the shoulder blades, setting up a gentle adjustment",
      "the cervical and upper thoracic spine and the shoulder blades", "between the shoulder blades and the base of the neck")
newer("cond-whiplash-treat", "conditions/whiplash", "a woman in her twenties with her hair tied up, seen from directly behind",
      "a close view from behind the seated patient: the back of her head, her neck and the tops of her shoulders fill the frame; the practitioner's two hands rest on either side of the base of her neck, thumbs easing into the muscles beside the spine",
      "the neck vertebrae and the base of the skull", "the deep muscles at the front and sides of the neck")
newer("cond-work-treat", "conditions/work-injury", "a man in his forties in a faded denim work shirt, work trousers and leather work boots",
      "in the treatment room the patient squats with a straight back to lift a plain cardboard box from the floor, while the practitioner's hand rests lightly on his lower back, coaching the lift",
      "the lumbar spine and the pelvis", "the lower back")

# ---------------------------------------------------------------- services, applied kinesiology, about, patient info
clin("svc-cold-hero", "services/cold-laser-therapy", "Cold Laser Therapy in Roseville", "hero", "1:1", "1:1",
     "a woman in her fifties sitting on the treatment table with one leg extended, grey trousers rolled above the knee",
     "the practitioner holds " + COLD.format(target="the side of the knee"), "the knee joint", "the inner side of the knee joint")
clin("svc-fx635-device", "services/fx-635-laser-therapy", "The device, described honestly", "frame", "1:1", "1:1",
     "a woman in her forties, lying still, face down, bare feet over the end of the table on a rolled towel",
     "a close view of the device and the foot: " + FX.format(target="the bare heel"), "the bones of the foot and the plantar fascia", "the heel")
clin("svc-pemf-hero", "services/pemf-therapy", "PEMF Therapy in Roseville", "hero", "1:1", "1:1",
     "a man in his forties lying face down, a light blanket over his legs",
     "the patient lies still on the treatment table; " + PEMF.format(target="his lower back") + "; nobody touches him",
     "the lumbar spine and the pelvis", "the lower back")
clin("ak-mtest", "applied-kinesiology (+ first-visit)", "Muscle testing, in plain terms", "frame", "3:2", "5:4",
     "a woman in her thirties in a sleeveless top",
     "a manual muscle test: the patient sits on the edge of the treatment table holding one arm straight out to the side at shoulder height; the practitioner's flat hand presses gently down just above her wrist and his other hand steadies her shoulder",
     "the shoulder joint, the shoulder blade and the muscles of the raised arm", "the shoulder muscle being tested, at the top of the arm")
clin("ak-roof", "applied-kinesiology", "The method and the instruments, under one roof", "frame", "1:1", "1:1",
     "a man in his fifties in a plain grey sweater, seated, seen from behind",
     "the practitioner's hand rests on the seated patient's shoulder; just beyond them, in the room, stands the white stand-mounted laser on its articulated arm, not in use",
     "the neck and the shoulder girdle", "the top of the shoulder")
clin("ak-legit-hero", "applied-kinesiology/is-muscle-testing-legitimate (+ faq)", "Is Muscle Testing Real? An Honest Answer", "hero", "3:2", "7:5",
     "a woman in her thirties; only her forearm and hand are in frame",
     "an intimate close-up of a manual muscle test: the patient's forearm is held level with the elbow bent and the fist closed; the practitioner's flat palm rests on the back of her wrist pressing gently down, his other hand steadying her elbow; only the two pairs of hands and forearms fill the frame",
     "the forearm bones and the forearm muscles", "the forearm muscle being tested")
clin("about-hero", "about", "Sacramento Applied Kinesiology, Roseville", "hero", "3:2", "3:2",
     "a woman in her forties in a sleeveless top, seated on the table, seen from behind and slightly to the side",
     "in the foreground a manual muscle test, her arm held straight out to the side with the practitioner's hand pressing gently above the wrist; in the softly blurred background the white stand-mounted laser and a small side table with a white ring-shaped PEMF coil",
     "the shoulder joint and the muscles of the raised arm", "the shoulder")
clin("pi-first-hero", "patient-info/first-visit", "Your First Visit: What to Expect", "hero", "3:2", "7:5",
     "a man in his forties sitting on the edge of the treatment table",
     "the practitioner stands facing the seated patient holding a clipboard of notes and explaining; a small anatomical spine model sits on the counter behind them",
     "the patient's spine from neck to pelvis, faint and elegant", "the lower back")
edit("svc-hub-hero", "services", "Our Treatments in Roseville", "hero", "1:1", "1:1",
     "the treatment room that holds both halves of the practice, no people: a padded pale sage adjusting table with a folded towel, the white stand-mounted laser on its articulated arm parked beside it, and on a small white side table a white ring-shaped PEMF coil with its console; morning light through a large window")
edit("ak-who-imaging", "applied-kinesiology/who-its-for", "What the assessment actually covers", "motif", "3:4", "4:5",
     "across a small pale oak table, the patient's hands pass a large paper imaging envelope to the practitioner's hands; an X-ray film showing a lower spine is half drawn out of the envelope; hands and forearms only")
edit("pi-faq-hero", "patient-info/faq", "Frequently Asked Questions", "hero", "4:3", "4:3",
     "two people talking at a small round pale oak table by the window, framed at chest height so no faces are in view: the patient in a knit sweater with hands open mid-question, and the practitioner in his crisp white dress shirt with rolled sleeves, his hands resting on a closed notebook; two cups of tea between them")
edit("pi-first-bring", "patient-info/first-visit", "Five minutes of preparation saves half the appointment", "frame", "3:2", "7:5",
     "a styled flat lay on a pale oak table of what to bring to a first visit: a paper imaging envelope with an X-ray film edge showing, a folded blank sheet, a weekly pill organiser, two plain unlabelled medicine boxes, a blank intake form on a clipboard with a pen, and reading glasses; soft window light")
edit("pi-forms-hero", "patient-info/forms", "The forms are not downloadable here yet", "hero", "3:2", "5:3",
     "no people anywhere in the frame: on the counter by the window, a clipboard holding a blank paper intake form with a pen resting on it, and next to it a simple white desk telephone")
edit("book-hero", "book", "Tell us what is going on", "hero", "16:9", "7:4",
     "no people anywhere in the frame: a calm front desk by a large window with a white desk telephone, a small paper appointment book open to blank pages with a pen, and a sprig of eucalyptus in a glass; the treatment area softly blurred behind")
edit("about-drvw-learning", "about/dr-van-wagenen", "Still learning", "new frame", "1:1", "1:1",
     "a study corner by a window: a pale oak desk with a stack of closed clinical textbooks with plain unmarked spines, a small anatomical spine model on a stand, reading glasses on an open notebook of soft, unreadable handwritten notes, and a cup of coffee; no people")
edit("svc-nutrition-consult", "services/nutritional-counseling", "Who is actually giving the advice", "new frame", "1:1", "1:1",
     "a nutrition consultation at a pale oak table by the window, framed at table height: the practitioner (the man in the white shirt, head out of frame) sits on one side with his hand resting on a food diary open to blank ruled pages, and the patient's hands rest on the other side; on the table a glass of water, a ceramic bowl of leafy greens, lentils and berries, and three plain amber supplement bottles with blank labels")

PILOT = ["cond-lbp-treat", "ak-mtest", "cond-carpal-treat", "cond-pregnancy-treat", "cond-oa-treat", "cond-headache-assess"]
FLARE_AR = {"1:1", "3:2", "2:3", "4:3", "3:4", "16:9", "9:16", "21:9"}


def prompt(s):
    if s["kind"] == "editorial":
        return (STYLE + "The scene is set in " + ROOM + ". Scene: " + s["scene"] + ". Clean, modern, warm and precise; "
                "crisp detail and fresh true-to-life colour. " + STAFF + HANDS)
    return (STYLE + "The scene is set in " + ROOM + ". Scene: " + s["scene"] + ". " + OVERLAY.format(anat=s["anat"], pain=s["pain"])
            + " " + PRACT + PATIENT.format(who=s["who"]) + HANDS)


if __name__ == "__main__":
    names = set(PILOT) if len(sys.argv) > 1 and sys.argv[1] == "pilot" else None
    jobs = []
    for s in S:
        if names and s["name"] not in names:
            continue
        assert s["gen"] in FLARE_AR, (s["name"], s["gen"])
        jobs.append({"name": s["name"], "model": MODEL,
                     "input": {"prompt": prompt(s), "quality": "high", "moderation": "auto", "resolution": "2k",
                               "aspect_ratio": s["gen"], "enhance_prompt": False}})
    out = "jobs_v2_pilot.json" if names else "jobs_v2.json"
    json.dump(jobs, open(os.path.join(HERE, out), "w"), indent=1)
    json.dump(S, open(os.path.join(HERE, "shotlist_v2.json"), "w"), indent=1)
    print(f"{len(jobs)} jobs -> {out}; total shots {len(S)} ({sum(1 for s in S if s['kind'] == 'overlay')} overlay, "
          f"{sum(1 for s in S if s['kind'] == 'editorial')} editorial)")
    if names:
        print(jobs[0]["input"]["prompt"])

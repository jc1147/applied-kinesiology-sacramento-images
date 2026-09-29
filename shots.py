"""Shot list for the Sacramento Applied Kinesiology inner pages (every page except home). Builds jobs.json for
fal-batch.mjs (Nano Banana Pro edit, 2K, the home page's own images as style references).

Each entry: name, page, section it goes with, slot it fills, style (photo|plate), generation aspect, final crop
aspect, subject. Reused images (already rendered in the bake-off) are listed in REUSE, not re-generated."""
import json

A = "site/assets/"
PLATE_REFS = [A + "gen_anatomy_vertebra_disc.jpg", A + "gen_anatomy_knee_joint.jpg", A + "gen_anatomy_shoulder_joint.jpg"]
HANDS_REFS = [A + "img_clinic_method_muscle_test.jpg", A + "img_clinic_method_shoulder.jpg", A + "img_clinic_method_palpation.jpg"]
INSTR_REFS = [A + "img_clinic_instr_laser_head.jpg", A + "img_clinic_instr_room.jpg", A + "img_clinic_method_palpation.jpg"]
ROOM_REFS = [A + "img_clinic_instr_room.jpg", A + "img_clinic_method_table.jpg", A + "img_clinic_frontdesk.jpg"]
DESK_REFS = [A + "img_clinic_method_notes.jpg", A + "img_clinic_frontdesk.jpg", A + "img_clinic_method_table.jpg"]

PLATE_STYLE = ("The reference images show the house illustration style of a clinic website. Create a NEW illustration in "
               "exactly that style: a vintage medical engraving printed in deep teal ink with pale teal fills, crisp dark "
               "outlines, fine engraved hatching for shading, on warm cream paper with a soft vignette, one subject centred "
               "with generous empty margins, no background scene. ")
PHOTO_STYLE = ("The reference photos show the house photography style of a clinic website. Create a NEW photograph in "
               "exactly that style: warm soft daylight from a window at the side, cream and warm-beige walls, pale sage and "
               "muted-teal linens, white towels, a calm private treatment room, shallow depth of field with a creamy "
               "blurred background, low contrast, gentle warmth, editorial and uncluttered. ")
PEOPLE = (" People: the practitioner is a man in a white dress shirt with the sleeves rolled to the forearm, no white "
          "coat and no stethoscope. COMPOSITION RULE: the top edge of the photo crops the practitioner at the chest or "
          "shoulders, so his head, face, chin and beard are entirely outside the frame. The patient is an adult in soft "
          "neutral clothing (oatmeal, grey or sage knitwear, or a plain t-shirt), and the patient's face is never visible: "
          "turned fully away from the camera, cropped out of frame, or pressed straight down into the opening of the "
          "table's face cradle so only the back of the head and hair show. Photorealistic, natural skin, anatomically "
          "correct hands with five fingers each.")
NO_TEXT = " No text, letters, numbers, labels, logos, brand markings, readable screens or watermark anywhere."
ANAT = " Anatomically accurate."
FX = ("a stand-mounted low-level laser with no brand markings (a rounded white head about the size of a dinner plate on "
      "an articulated arm from a wheeled white floor stand)")


def FX_ON(target):
    return f"{FX} is positioned a hand's width above {target}, casting three thin soft red light lines across the skin without touching it"


FX_PARKED = f"{FX}, parked beside the table and not in use"
COLD = "a small white handheld low-level laser probe on a thin cable, casting a faint soft red glow on the skin"
PEMF = ("a flat white ring-shaped PEMF coil about 30 cm across, like a large smooth doughnut, connected by a thin cable to "
        "a small white console with a blank dark screen")
TOOL = ("a small handheld chiropractic adjusting instrument shaped like a thick marker pen, brushed chrome with a visible "
        "coiled-spring section and a flat black rubber tip, held like a pen; clearly not a syringe, with no needle and no finger rings")

S = []  # (name, page, section, slot, style, gen_aspect, crop, subject)


def add(name, page, section, slot, style, gen, crop, subject):
    S.append(dict(name=name, page=page, section=section, slot=slot, style=style, gen=gen, crop=crop, subject=subject))


# ---------------------------------------------------------------- conditions: the nine pages with placeholder drawings
add("cond-auto-hero", "conditions/auto-accident-injury", "Auto Accident Injury Care in Roseville", "hero (placeholder: collision impact through the neck)", "plate", "3:2", "7:5",
    "the cervical spine and the base of the skull in side profile, the neck bent slightly forward, with three thin concentric "
    "pale teal ripple lines passing through the upper neck like a travelling shockwave. The vertebrae carry no labels: "
    "no letters or numbers such as C3 or C7 anywhere." + ANAT)
add("cond-auto-assess", "conditions/auto-accident-injury", "The questions this examination is built to answer", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a patient sits on the edge of the treatment table with their back to the camera; the practitioner's two hands rest flat "
    "on either side of the patient's mid back and lower rib cage, feeling how the ribs move as the patient breathes, "
    "examining the region after a car collision. Framed from the shoulders to the waist.")
add("cond-auto-treat", "conditions/auto-accident-injury", "Settle the irritated tissue, then restore what stopped moving", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"a close view at table height of a patient lying face down: the upper back and shoulder blades fill the frame and the "
    f"patient's head is completely outside the left edge of the frame; {FX_ON('the upper back, where the neck meets the shoulders')}, "
    f"its white head entering from the top of the frame on its arm; the practitioner's hand rests lightly on one shoulder blade.")

add("cond-carpal-hero", "conditions/carpal-tunnel", "Carpal Tunnel Treatment in Roseville", "hero (placeholder: carpal tunnel and the nerve path through the wrist)", "plate", "3:2", "7:5",
    "the bones of the hand and wrist seen palm-up, with the median nerve drawn as a fine continuous pale teal line running "
    "from the forearm through the carpal tunnel beneath a band of ligament across the wrist, and branching into the thumb, "
    "index, middle and half of the ring finger." + ANAT)
add("cond-carpal-assess", "conditions/carpal-tunnel", "We follow the nerve from the neck to the fingertip", "assessment (placeholder: nerve root leaving the spine)", "plate", "3:2", "7:5",
    "one whole arm and shoulder with the lower neck vertebrae and the collarbone drawn in outline, and a single fine pale "
    "teal nerve traced continuously from the lower neck, under the collarbone, down the inner arm and forearm, through the "
    "wrist and into the thumb and first fingers, showing the whole path of the nerve from neck to fingertip." + ANAT)

add("cond-fibro-hero", "conditions/fibromyalgia", "Fibromyalgia Care in Roseville", "hero (placeholder: body map with widespread tender points)", "plate", "3:2", "7:5",
    "a full standing human figure seen from behind, drawn in fine outline like an anatomical study (no facial features, no "
    "genitals), with eighteen small solid deep-teal dots placed symmetrically at the classic tender points: the base of "
    "the skull, the lower neck, the tops of the shoulders, beside the shoulder blades, the elbows, the upper buttocks, the "
    "outer hips and the inner knees. Every dot sits ON the body surface exactly at its tender point; no dot floats beside "
    "the body. Plain warm cream paper background with no panel, card or frame behind the figure.")
add("cond-fibro-assess", "conditions/fibromyalgia", "One appointment that looks at the whole load", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a first-appointment history taking: at a small pale wood table by the window, the patient's hands rest around a cup "
    "of tea while across the table the practitioner's hands write in a notebook with a pen (the handwriting is too small "
    "and soft to read); a closed folder of reports lies beside the cup. Framed at table height, only hands and forearms.")
add("cond-fibro-treat", "conditions/fibromyalgia", "Low force first, and less of it than you expect", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"a patient lies face down on a pale sage treatment table, face in the face cradle, a soft blanket over the legs; the "
    f"practitioner holds {TOOL} gently against the muscles beside the mid spine, his other hand resting flat on the "
    f"patient's back, conveying very light, careful force.")

add("cond-frozen-hero", "conditions/frozen-shoulder", "Frozen Shoulder Treatment in Roseville", "hero (placeholder: shoulder joint with a restricted arc)", "plate", "3:2", "7:5",
    "the shoulder joint seen from the front: collarbone, shoulder blade and the upper arm bone hanging down, with a large "
    "dotted arc showing the full range the arm should travel overhead and a much shorter solid pale teal arc showing the "
    "restricted range it actually reaches." + ANAT)
add("cond-frozen-assess", "conditions/frozen-shoulder", "We test what the arm is standing on", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a patient sits on the treatment table with their back to the camera and slowly raises one arm forward; the "
    "practitioner's hand rests on the patient's shoulder blade feeling it glide across the rib cage, his other hand "
    "lightly guiding the patient's elbow. Framed from the shoulders to the waist, hair tied up.")
add("cond-frozen-treat", "conditions/frozen-shoulder", "Give the capsule a reason to let go", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    "a patient lies on their back on the treatment table, seen from the chest down; the practitioner gently holds the "
    "patient's arm at the elbow and the wrist and eases it out to the side in a slow, supported arc, a folded towel under "
    "the shoulder. The patient's head is out of frame.")

add("cond-headache-hero", "conditions/headache-migraine", "Headache and Migraine Care in Roseville", "hero (placeholder: head and neck with the upper cervical segments)", "plate", "3:2", "7:5",
    "the base of the skull and the top two neck vertebrae (the ring-shaped atlas and the axis with its upright peg) in a "
    "three-quarter rear view, showing how the skull rests on the atlas, with the next three cervical vertebrae below." + ANAT)
add("cond-headache-assess", "conditions/headache-migraine", "We look hardest at the days between the headaches", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a patient sits upright on the treatment table seen from behind, hair tied up; the practitioner's fingertips rest "
    "lightly on the jaw joints just in front of both ears and at the base of the skull, examining the jaw and the upper "
    "neck. Framed from the top of the head to the shoulders, the face turned away from the camera.")
add("cond-headache-treat", "conditions/headache-migraine", "Work the neck, the jaw and the load behind them", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"a patient sits upright on the treatment table seen from behind, hair tied up; the practitioner holds {COLD} at the "
    f"base of the skull where the neck meets the head, his other hand steadying the patient's shoulder.")

add("cond-lbp-hero", "conditions/low-back-pain", "Low Back Pain Treatment in Roseville", "hero (placeholder: lumbar spine seen from the side)", "plate", "3:2", "7:5",
    "the five lumbar vertebrae and the sacrum in side profile, with the discs between them and the gentle inward curve of "
    "the lower back, the spinous processes pointing to the right." + ANAT)
add("cond-lbp-assess", "conditions/low-back-pain", "We test the whole chain, not only the sore part", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "seen along the table from its foot end: a patient lies flat on their back with the head on a pillow at the far end, "
    "outside the frame; one straight leg is raised to about 30 degrees; the practitioner's flat hand presses gently and "
    "steadily down just above the ankle while his other hand steadies the opposite hip, testing the hip muscles away "
    "from the sore low back. Framed from the waist to the feet.")
add("cond-lbp-treat", "conditions/low-back-pain", "Hands and instruments, in the same room", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"a patient lies face down on the treatment table, face pressed into the face cradle at the far left; the soft sweater "
    f"is lifted a little to bare the low back just above the waistband; {FX_ON('the bare low back')} (the red lines fall "
    f"only on the low back, nowhere near the head), while "
    f"the practitioner's hand rests on the patient's sacrum; on a small side table in the soft background sits {PEMF}.")

add("cond-oa-hero", "conditions/osteoarthritis", "Osteoarthritis Care in Roseville", "hero (placeholder: joint surfaces with a narrowed space)", "plate", "3:2", "7:5",
    "the knee joint seen from the front: the lower thigh bone, the shin bone and the fibula, with the joint space visibly "
    "narrowed on the inner side and a few small bony spurs at its edges, the kneecap drawn faintly." + ANAT)
add("cond-oa-assess", "conditions/osteoarthritis", "We measure what the joint is being asked to carry", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a patient in soft grey trousers rolled to mid-calf stands barefoot on a pale wooden floor and bends the knees into a "
    "shallow squat; the practitioner kneels beside them with one hand on the side of the patient's knee and the other at "
    "the hip, watching how the knee tracks. Framed from the waist to the floor.")
add("cond-oa-treat", "conditions/osteoarthritis", "Change the load before you change the joint", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"a patient sits on the treatment table with one leg extended along it, grey trousers rolled above the knee; "
    f"{FX_ON('the knee')}. Framed from the hips to the feet.")

add("cond-osteo-assess", "conditions/osteoporosis", "The examination sets the force ceiling before anything else", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a balance check for an older patient (silver hair, soft cardigan, seen from behind): the patient stands on one foot "
    "beside the treatment table with the fingertips of one hand resting on its edge, while the practitioner's hands hover "
    "close to the patient's waist, ready to steady them. Framed from the shoulders to the floor.")
add("cond-osteo-treat", "conditions/osteoporosis", "Low force, and the parts of this that are not adjusting at all", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"an older patient (silver hair tied back) lies face down on a well-padded treatment table with a soft bolster under "
    f"the ankles and a pillow under the chest, face in the face cradle; the practitioner holds {TOOL} lightly against the "
    f"upper back, his other hand resting flat and still on the patient's shoulder, conveying the lowest possible force.")

add("cond-pinched-hero", "conditions/pinched-nerve", "Pinched Nerve Treatment in Roseville", "hero (placeholder: nerve root at a compressed segment)", "plate", "3:2", "7:5",
    "two neck vertebrae in side profile with the disc between them bulging slightly backward and pressing on a nerve root "
    "as it leaves through the opening between the vertebrae; the nerve root is drawn in pale teal and narrows visibly at "
    "the pinch point, then continues outward." + ANAT)
add("cond-pinched-assess", "conditions/pinched-nerve", "We test the whole run of the nerve", "assessment (placeholder: one link in a chain)", "photo", "3:2", "7:5",
    "a reflex check: the patient's relaxed forearm rests on the practitioner's forearm with the elbow bent, and the "
    "practitioner taps the inside of the elbow with a small rubber reflex hammer; the patient sits on the treatment table "
    "and is framed from the shoulder down.")
add("cond-pinched-treat", "conditions/pinched-nerve", "Take the pressure off, then keep it off", "treatment (placeholder: hands, laser, coil)", "photo", "3:2", "7:5",
    f"a patient lies face down on the treatment table, face in the face cradle; {PEMF} rests flat on the patient's upper "
    f"back between the shoulder blades, over a thin sage cloth, while the practitioner's hand adjusts the cable.")

# ---------------------------------------------------------------- conditions: the ten newer pages (one treatment photo each)
def cond_photo(name, page, section, subject):
    add(name, page, section, "new frame for the treatment section (1:1 like the page's other frames)", "photo", "1:1", "1:1", subject)


cond_photo("cond-plantar-treat", "conditions/plantar-fasciitis", "What treatment involves",
           f"a patient lies face down on the treatment table with bare feet resting over its end on a rolled towel; "
           f"{FX_ON('the heel and the arch of one foot')}. Framed from the calves to the feet.")
cond_photo("cond-pregnancy-treat", "conditions/pregnancy-pain", "What treatment involves",
           "a pregnant patient in her third trimester lies on her side on the treatment table, supported by pillows under "
           "her head (face out of frame), between her knees and under her bump, wearing a soft oatmeal knit dress; her rounded "
           "pregnant belly is clearly visible in profile, resting on the pillow; the "
           "practitioner's hands rest gently on the back of her pelvis and sacrum, conveying calm, careful, low-force care.")
cond_photo("cond-sciatica-treat", "conditions/sciatica", "What treatment involves",
           f"a patient in soft grey leggings lies face down on the treatment table, face in the face cradle; the "
           f"practitioner holds {COLD} over the outer side of the hip, where the deep buttock muscles lie, his other hand "
           f"resting on the back of the patient's thigh.")
cond_photo("cond-scoliosis-assess", "conditions/scoliosis", "How we assess it",
           "a patient in a plain sage sports top stands barefoot with their back to the camera; the practitioner's two hands "
           "rest level on the tops of the patient's hip bones, comparing the height of the left and right sides; one "
           "shoulder sits very slightly higher than the other. Framed from the shoulders to the knees.")
cond_photo("cond-shoulder-assess", "conditions/shoulder-pain", "How we assess it",
           "a rotator cuff muscle test: the patient sits on the treatment table with the elbow bent at a right angle and "
           "tucked against the side; the practitioner's hand holds the patient's elbow still while his other hand presses "
           "inward against the back of the patient's wrist as the patient pushes outward. Framed from the shoulder down.")
cond_photo("cond-disc-treat", "conditions/slipped-disc", "Instruments, where they are indicated",
           f"photographed from the foot end of the table: a patient lies on their back with the knees over a soft sage bolster "
           f"and the head beyond the frame at the far end; {PEMF} lies flat on the table directly under the patient's low "
           f"back, its rim just visible at the waist, its cable running to the console. Framed from the chest to the knees.")
cond_photo("cond-stress-assess", "conditions/stress", "How we assess it",
           "a patient sits upright on the treatment table seen from behind, shoulders visibly hunched up toward the ears, "
           "hair tied up; the practitioner's hands rest on the tops of both shoulders, thumbs on the muscles beside the "
           "neck, feeling the tension. Framed from the head to the mid back, face turned away.")
cond_photo("cond-tennis-treat", "conditions/tennis-elbow", "Instruments, where they are indicated",
           f"a patient's arm rests on a folded white towel with the sleeve rolled well above the elbow, the fist loosely closed "
           f"and the outer side of the elbow facing up; the practitioner holds {COLD} at the bony point on the outer side of "
           f"the elbow joint itself, not on the forearm or the wrist.")
cond_photo("cond-neck-treat", "conditions/upper-back-neck-pain", "Instruments, where they are indicated",
           "a patient lies face down on the treatment table with the face in the face cradle; the practitioner's two hands "
           "rest one over the other on the upper back between the shoulder blades, setting up a gentle adjustment. Framed "
           "from the head of the table to the lower back.")
cond_photo("cond-whiplash-assess", "conditions/whiplash", "How we assess it",
           "a patient lies on their back on the treatment table, photographed from above and behind the head so only the "
           "top and back of the head and the neck are visible, never the face; the practitioner's two hands cradle the "
           "base of the skull and the back of the neck, testing the deep neck muscles with gentle support.")
cond_photo("cond-work-assess", "conditions/work-injury", "How we assess it",
           "a patient in a faded blue denim work shirt sits on the treatment table and holds one arm straight out in front "
           "at shoulder height; the practitioner presses gently and steadily down on the forearm while his other hand "
           "steadies the patient's shoulder, testing the shoulder muscles after a repetitive work strain. Framed from the "
           "shoulder down, the face out of frame.")

# treatment scenes for the five newer pages whose first photo was an examination (added after reading each page's
# "What treatment involves" text; the examination photos stay as extras for the "How we assess it" sections)
cond_photo("cond-scoliosis-treat", "conditions/scoliosis", "What treatment involves",
           "a patient lies face down on the treatment table with the face in the face cradle, a light blanket over the "
           "legs; the practitioner's hands work slowly along the muscles on one side of the mid back, beside the spine, "
           "easing the side that carries the uneven load; supportive, gentle hands-on work.")
cond_photo("cond-shoulder-treat", "conditions/shoulder-pain", "What treatment involves",
           "a patient lies on their side on the treatment table with the head on a pillow out of frame; the practitioner's "
           "fingertips hook gently under the inner edge of the patient's shoulder blade while his other hand cups the "
           "front of the shoulder, easing the shoulder blade across the rib cage. Framed from the neck to the waist.")
cond_photo("cond-stress-treat", "conditions/stress", "What treatment involves",
           "a patient lies face down on the treatment table with the face in the face cradle; the practitioner's thumbs "
           "press slowly into the thick muscles running from the neck to the tops of the shoulders, releasing muscles "
           "that have been held short; calm, quiet, unhurried.")
cond_photo("cond-whiplash-treat", "conditions/whiplash", "What treatment involves",
           "a tight close-up from directly behind a seated patient: only the back of the head (hair tied up), the back of "
           "the neck and the tops of the shoulders fill the frame; the practitioner's two hands enter from both sides and "
           "rest on either side of the base of the neck, thumbs easing gently into the muscles beside the spine; nothing of "
           "the practitioner is visible except his hands and shirt cuffs.")
cond_photo("cond-work-treat", "conditions/work-injury", "What treatment involves",
           "in the treatment room, a patient in a faded blue denim work shirt, work trousers and leather work boots squats "
           "with a straight back to lift a plain cardboard box from the floor, while the practitioner's hand rests lightly "
           "on the patient's low back, coaching the lift. Framed from the shoulders to the floor, the face out of frame.")

# ---------------------------------------------------------------- services
add("svc-hub-hero", "services", "Our Treatments in Roseville", "hero (currently the reused spine plate)", "photo", "1:1", "1:1",
    f"the empty treatment room that holds both halves of the practice: a padded pale sage adjusting table with a folded "
    f"towel, {FX_PARKED}, and on a small white side table {PEMF}; warm window light, no people in the room.")
add("svc-cold-hero", "services/cold-laser-therapy", "Cold Laser Therapy in Roseville", "hero (currently the reused knee plate)", "photo", "1:1", "1:1",
    f"a patient sits on the treatment table with one leg extended along it and grey trousers rolled above the knee; the "
    f"practitioner holds {COLD} over the side of the knee. Framed from the hips to the feet.")
add("svc-fx635-device", "services/fx-635-laser-therapy", "The device, described honestly", "frame (currently the reused knee plate)", "photo", "1:1", "1:1",
    f"a patient lies still, face down, with bare feet resting over the end of the table on a rolled towel; "
    f"{FX_ON('the bare heel')}. Close view of the laser head and the foot, the room softly blurred.")
add("svc-hormone-thyroid", "services/hormone-therapy-management", "Hormone Therapy Management in Roseville", "hero (replaces the thyroid plate, which does not show a thyroid)", "plate", "1:1", "1:1",
    "the thyroid gland: a butterfly-shaped gland with two lobes joined by a narrow bridge, wrapped across the front of the "
    "windpipe just below the larynx, with the ringed cartilage of the windpipe running below it." + ANAT)
add("svc-nutrition-consult", "services/nutritional-counseling", "How the nutrition work runs", "new frame", "photo", "1:1", "1:1",
    "a nutrition consultation laid out on a pale wooden table by the window: a food diary open to blank ruled pages with "
    "a pen, a glass of water, a small ceramic bowl of leafy greens, lentils and berries, and three plain amber supplement "
    "bottles with blank labels; the practitioner's hand rests on the diary. No readable writing.")
add("svc-pemf-hero", "services/pemf-therapy", "PEMF Therapy in Roseville", "hero (currently the reused vertebra plate)", "photo", "1:1", "1:1",
    f"a patient lies face down on the treatment table, a light blanket over the legs, framed from the shoulders to the "
    f"knees so the head is outside the frame; {PEMF} rests flat on the patient's low back over a thin sage cloth. The "
    f"patient lies still; nobody touches them.")

# ---------------------------------------------------------------- applied kinesiology
add("ak-balance", "applied-kinesiology (+ is-muscle-testing-legitimate, faq, first-visit)", "Applied Kinesiology in Roseville; A balance weighing what a method can and cannot claim", "motif / balance placeholders", "plate", "1:1", "1:1",
    "a classical two-pan balance scale: an upright central post on a round base, a level beam across the top, and a "
    "shallow pan hanging from each end on fine chains; the beam is perfectly level; three small circular marks run up "
    "the central post.")
add("ak-roof", "applied-kinesiology", "The method and the instruments, under one roof", "frame (placeholder: roofline over hand and wave)", "photo", "1:1", "1:1",
    f"in one room: in the foreground the practitioner's hand rests on the shoulder of a patient seated on the treatment "
    f"table (seen from behind), and just beyond them, softly out of focus, stands {FX}, its head folded down, not in use.")
add("ak-legit-hero", "applied-kinesiology/is-muscle-testing-legitimate", "Is Muscle Testing Real? An Honest Answer", "hero (placeholder: a muscle held against steady pressure)", "photo", "3:2", "7:5",
    "an intimate close-up of a manual muscle test: the patient's forearm is held level with the elbow bent and the fist "
    "closed, and the practitioner's flat palm rests on the back of the patient's wrist, pressing gently and steadily "
    "down; the practitioner's other hand steadies the patient's elbow. Only the two pairs of hands and forearms fill the "
    "frame.")
add("ak-chain", "applied-kinesiology/is-muscle-testing-legitimate (+ condition pages' chain concept)", "One input, always corroborated", "frame (placeholder: one link in a chain)", "plate", "3:2", "7:5",
    "a short horizontal chain of seven oval links lying across the page; the middle link is drawn thicker and filled pale "
    "teal, visibly carrying the strain, while the links either side are thinner and slightly stretched.")
add("ak-who-imaging", "applied-kinesiology/who-its-for", "What the assessment actually covers", "motif (160x200)", "photo", "4:5", "4:5",
    "across a small pale wooden table, the patient's hands pass a large paper imaging envelope to the practitioner's "
    "hands; an X-ray film showing the silhouette of a lower spine is half drawn out of the envelope. Framed at table "
    "height, hands and forearms only.")

# ---------------------------------------------------------------- about
add("about-hero", "about", "Sacramento Applied Kinesiology, Roseville", "hero (placeholder: two overlapping fields, method and equipment)", "photo", "3:2", "3:2",
    f"one treatment room holding both the method and the equipment: in the foreground a manual muscle test, the patient "
    f"seated on the table with an arm held straight out to the side and the practitioner's hand pressing gently above the "
    f"wrist (framed from the chest down, the patient seen from behind); in the softly blurred background {FX_PARKED} "
    f"and a small white side table with {PEMF}.")
add("about-drvw-learning", "about/dr-van-wagenen", "Still learning", "new frame", "photo", "1:1", "1:1",
    "a study corner by a window: a pale wooden desk with a stack of closed clinical textbooks with plain unmarked spines, "
    "a small anatomical model of the spine on a stand, reading glasses resting on an open notebook of handwritten notes "
    "(too soft to read), and a cup of coffee. No people.")

# ---------------------------------------------------------------- patient info, book
add("pi-faq-hero", "patient-info/faq", "Frequently Asked Questions", "hero (placeholder: questions patients ask)", "photo", "4:3", "4:3",
    "two people talking at a small round pale wood table by the window, framed at chest height so the top edge of the "
    "photo cuts across both people's chests, with no faces, mouths or chins in view: the patient's "
    "hands open mid-question, the practitioner's hands resting on a closed notebook, two cups of tea between them; "
    "a relaxed, unhurried conversation.")
add("pi-first-hero", "patient-info/first-visit", "Your First Visit: What to Expect", "hero (placeholder: history, testing, findings, plan)", "photo", "3:2", "7:5",
    "a first visit: the patient sits on the edge of the treatment table, seen from the shoulders down, while the "
    "practitioner, seen from the chest down, stands facing them holding a clipboard of notes and explains; on the counter "
    "behind them a small anatomical spine model and a paper imaging envelope.")
add("pi-first-bring", "patient-info/first-visit", "Five minutes of preparation saves half the appointment", "frame (placeholder: balance)", "photo", "3:2", "7:5",
    "a flat lay on a warm wooden table of what to bring to a first visit: a paper imaging envelope with an X-ray film "
    "edge showing, a folded sheet of blank lab results, a weekly pill organiser, two plain unlabelled medicine boxes, a "
    "blank intake form on a clipboard with a pen, and reading glasses; soft window light from the left. No readable text.")
add("pi-forms-hero", "patient-info/forms", "The forms are not downloadable here yet", "hero (placeholder: two routes to one appointment)", "photo", "3:2", "5:3",
    "on the reception counter by the window: a clipboard holding a blank paper intake form with a pen resting on it, and "
    "next to it a simple white desk telephone; two routes to the same appointment. No readable text.")
add("book-hero", "book", "Tell us what is going on", "hero (placeholder: form to calendar)", "photo", "16:9", "7:4",
    "a calm reception desk by a window: a simple white desk telephone, a small paper appointment book lying open to blank "
    "pages with a pen, and a sprig of eucalyptus in a glass; the waiting room softly blurred behind. No people, no "
    "readable text.")

REUSE = {  # already rendered in the bake-off (Nano Banana Pro)
    "cond-carpal-treat": ("bakeoff/t-wrist-nbp.png", "conditions/carpal-tunnel", "Free the tunnel, then unload the path into it", "treatment (placeholder: hands, laser, coil)", "7:5"),
    "cond-osteo-hero": ("bakeoff/t-osteo-nbp.png", "conditions/osteoporosis", "Osteoporosis Care in Roseville", "hero (placeholder: trabecular bone becoming less dense)", "7:5"),
    "ak-mtest": ("bakeoff/t-mtest-nbp.png", "applied-kinesiology (+ faq, first-visit)", "Muscle testing, in plain terms", "frame (placeholder: arm held against pressure)", "5:4"),
}

if __name__ == "__main__":
    jobs = []
    for s in S:
        if s["style"] == "plate":
            prompt, refs = PLATE_STYLE + "Subject: " + s["subject"] + NO_TEXT, PLATE_REFS
        else:
            nobody = s["name"] in ("svc-hub-hero", "about-drvw-learning", "book-hero", "pi-forms-hero", "pi-first-bring")
            prompt = PHOTO_STYLE + "Scene: " + s["subject"] + (" No people in the frame." if nobody else PEOPLE) + NO_TEXT
            subj = s["subject"]
            refs = (ROOM_REFS if s["name"] in ("svc-hub-hero", "book-hero", "pi-forms-hero") else
                    DESK_REFS if s["name"] in ("about-drvw-learning", "pi-first-bring", "svc-nutrition-consult", "cond-fibro-assess", "pi-faq-hero", "ak-who-imaging") else
                    INSTR_REFS if any(k in subj for k in ("laser", "PEMF", "coil")) else HANDS_REFS)
        jobs.append({"name": s["name"], "endpoint": "fal-ai/nano-banana-pro/edit", "prompt": prompt, "refs": refs,
                     "params": {"aspect_ratio": s["gen"], "resolution": "2K", "output_format": "png"}})
    json.dump(jobs, open("jobs.json", "w"), indent=1)
    json.dump({"shots": S, "reuse": REUSE}, open("shotlist.json", "w"), indent=1)
    print(f"{len(jobs)} new renders (+{len(REUSE)} reused) -> est ${len(jobs) * 0.15:.2f}")

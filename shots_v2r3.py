"""Round-3 fixes for the v2 editorial shots that missed their brief in review (audit_v2/batch4-report.json).

The round-1 editorial prompt always carried the STAFF block (the description of the one clinician), and the model put
him into scenes that were meant to be empty (book-hero, pi-forms-hero) and added a seated woman to the flat lay
(pi-first-bring, which also had a three-fingered hand). Empty scenes now get their own prompt: no STAFF block and an
explicit no-people rule. Desk telephones are turned so the keypad faces away (the book-hero keypad was melted), and
the PEMF coil's cable is spelled out end to end (svc-hub-hero's cable dead-ended on a shelf).
Two variants per shot (-a, -b) into v2/round3/.  Writes jobs_v2r3.json."""
import json
import os

import shots_v2 as V

HERE = os.path.dirname(os.path.abspath(__file__))
EMPTY = (" This is an empty still life: there are no people, no hands, no arms and no body parts anywhere in the frame. "
         "No text, logos, labels, letters or readable screens; every object is plain and unbranded.")
PHONE = "a white desk telephone seen from the side, its handset resting in the cradle and its keypad turned away from the camera"

EDIT = {  # name: scene (all empty scenes)
    "pi-first-bring": (
        "a still life on a pale oak table by the window, seen at a low three-quarter angle with the clinic softly blurred "
        "behind: what to bring to a first visit, neatly arranged: a large paper imaging envelope with the edge of an X-ray "
        "film showing, a folded blank sheet of paper, a small clear pill organiser with plain unmarked lids, two plain white "
        "unlabelled medicine boxes, a blank intake form on a clipboard with a pen resting on it, and a pair of reading "
        "glasses; soft window light"),
    "book-hero": (
        "a calm front desk by a large window: " + PHONE + ", a small paper appointment book open to blank pages with a "
        "pen, and a sprig of eucalyptus in a glass; the treatment area softly blurred behind"),
    "pi-forms-hero": (
        "on the counter by the window, a clipboard holding a blank paper intake form with a pen resting on it, and next "
        "to it " + PHONE + "; the treatment room softly blurred behind"),
    "svc-hub-hero": (
        "the treatment room that holds both halves of the practice: a padded pale sage adjusting table with a folded "
        "towel, the white stand-mounted laser on its articulated arm parked beside it, and on a small white side table "
        "a white ring-shaped PEMF coil with its small white console beside it, one continuous white cable running from "
        "the base of the coil straight into the console; morning light through a large window"),
}

if __name__ == "__main__":
    S = {s["name"]: s for s in json.load(open(os.path.join(HERE, "shotlist_v2.json")))}
    jobs = []
    for name, scene in EDIT.items():
        p = (V.STYLE + "The scene is set in " + V.ROOM + ". Scene: " + scene + ". Clean, modern, warm and precise; "
             "crisp detail and fresh true-to-life colour." + EMPTY)
        for v in ("a", "b"):
            jobs.append({"name": f"{name}-{v}", "model": V.MODEL,
                         "input": {"prompt": p, "quality": "high", "moderation": "auto", "resolution": "2k",
                                   "aspect_ratio": S[name]["gen"], "enhance_prompt": False}})
    json.dump(jobs, open(os.path.join(HERE, "jobs_v2r3.json"), "w"), indent=1)
    json.dump(EDIT, open(os.path.join(HERE, "v2", "round3_briefs.json"), "w"), indent=1)
    print(len(jobs), "jobs for", len(EDIT), "shots")
    print(jobs[0]["input"]["prompt"])

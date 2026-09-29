"""Apply the round-3 editorial picks (checked at zoom: no people or hands, no readable text, phone keypad turned away,
PEMF cable continuous from coil to console). The replaced render goes to v2/rejected/<shot>-r1.png.
Writes v2/r3_applied.json."""
import json
import os
import filecmp
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def park(src, stem):
    """Move a replaced render into v2/rejected/ under a name that is not taken yet (never overwrite a reject)."""
    os.makedirs(os.path.join(HERE, "v2", "rejected"), exist_ok=True)
    dst, k = os.path.join(HERE, "v2", "rejected", stem + ".png"), 2
    while os.path.exists(dst):
        dst, k = os.path.join(HERE, "v2", "rejected", f"{stem}-{k}.png"), k + 1
    shutil.move(src, dst)
    return dst


PICKS = {  # shot: (pick, why the other variant lost)
    "pi-first-bring": ("pi-first-bring-a", "b's intake form carries faint pseudo-text and the glasses a tiny mark"),
    "book-hero": ("book-hero-b", "a shows a faint row of keys behind the handset"),
    "pi-forms-hero": ("pi-forms-hero-a", "b shows a small label under the handset"),
    "svc-hub-hero": ("svc-hub-hero-b", "a has a tiny pseudo-text strip on the laser head"),
}
done = {}
for shot, (pick, why) in PICKS.items():
    dst = os.path.join(HERE, "v2", "renders", shot + ".png")
    src = os.path.join(HERE, "v2", "round3", pick + ".png")
    if os.path.exists(dst) and not filecmp.cmp(dst, src, shallow=False):
        park(dst, shot + "-r1")
    shutil.copy(src, dst)
    shutil.copy(os.path.join(HERE, "v2", "round3", pick + ".result.json"), os.path.join(HERE, "v2", "renders", shot + ".result.json"))
    done[shot] = {"pick": pick, "other": why}
json.dump(done, open(os.path.join(HERE, "v2", "r3_applied.json"), "w"), indent=1)
print(json.dumps(done, indent=1))

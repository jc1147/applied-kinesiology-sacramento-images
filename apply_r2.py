"""Apply round-2 review results: for each re-rendered shot, take the better variant that passed (PASS > MINOR, the
reviewer's pick first); move the failed original to v2/rejected/ and copy the pick into v2/renders/<shot>.png.
Shots where both variants failed are listed for round 3. Also applies plate picks from the r2 plate review.
Writes v2/r2_applied.json."""
import glob
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


rank = {"PASS": 0, "MINOR": 1, "FAIL": 2}
reps = []
for p in sorted(glob.glob(os.path.join(HERE, "audit_v2", "r2_batch*-report.json"))):
    reps += json.load(open(p, encoding="utf-8"))
# v2/r2_waivers.json: {variant: {"verdict", "by", "reason"}}: a review point I overruled on purpose (with the reason),
# e.g. a framing complaint against a brief line that the one-clinician rule already covers
wv_path = os.path.join(HERE, "v2", "r2_waivers.json")
waivers = json.load(open(wv_path)) if os.path.exists(wv_path) else {}
for r in reps:
    if r["name"] in waivers:
        r["verdict"] = waivers[r["name"]]["verdict"]
PLATES = ("cond-auto-hero", "cond-carpal-hero")
by_pair = {}
for r in reps:
    # plate variants are grouped by their plate name (r2_plates.json paired cond-carpal-hero-b-edit with
    # "cond-carpal-hero-b", which is a variant, not a slot)
    pair = next((p for p in PLATES if r["name"].startswith(p + "-")), None) or r.get("pair") or r["name"].rsplit("-", 1)[0]
    by_pair.setdefault(pair, []).append(r)
# the reviewers name the better variant of each pair in their reply (not in the JSON); those picks are copied into
# v2/r2_reviewer_picks.json ({pair: variant}) and break ties between equal verdicts
rp_path = os.path.join(HERE, "v2", "r2_reviewer_picks.json")
reviewer_pick = json.load(open(rp_path)) if os.path.exists(rp_path) else {}
applied, still_failing, plates = {}, [], {}
for pair, rs in sorted(by_pair.items()):
    ok = sorted([r for r in rs if r.get("verdict") in ("PASS", "MINOR")],
                key=lambda r: (rank[r["verdict"]], r["name"] != reviewer_pick.get(pair), r["name"]))
    if pair in PLATES:  # plates
        if ok:
            plates[pair] = f"v2/plates/{ok[0]['name']}.png"
        else:
            still_failing.append(pair)
        continue
    if not ok:
        still_failing.append(pair)
        continue
    pick = ok[0]["name"]
    src = os.path.join(HERE, "v2", "round2", pick + ".png")
    dst = os.path.join(HERE, "v2", "renders", pair + ".png")
    if os.path.exists(dst) and not filecmp.cmp(dst, src, shallow=False):
        park(dst, pair + "-r1fail")
    shutil.copy(src, dst)
    rj = os.path.join(HERE, "v2", "round2", pick + ".result.json")
    if os.path.exists(rj):
        shutil.copy(rj, os.path.join(HERE, "v2", "renders", pair + ".result.json"))
    applied[pair] = {"pick": pick, "verdict": ok[0]["verdict"]}
picks_path = os.path.join(HERE, "v2", "plate_picks.json")
picks = json.load(open(picks_path)) if os.path.exists(picks_path) else {}
picks.update(plates)
json.dump(picks, open(picks_path, "w"), indent=1)
json.dump({"applied": applied, "still_failing": still_failing, "plates": plates}, open(os.path.join(HERE, "v2", "r2_applied.json"), "w"), indent=1)
print(f"applied {len(applied)} photo picks; plate picks {plates}; still failing: {still_failing}")

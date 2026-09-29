"""Apply the round-3 clinical review (audit_v2/r3c_batch*-report.json): per shot, the best verdict wins (PASS > MINOR),
then the reviewer's pick. The pick is copied from v2/round3c/ into v2/renders/<shot>.png; the render it replaces is
parked in v2/rejected/ (never overwriting). Shots with no usable variant keep whatever is in v2/renders/ and are listed.
Run after apply_r2.py. Writes v2/r3c_applied.json."""
import filecmp
import glob
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
rank = {"PASS": 0, "MINOR": 1, "FAIL": 2}


def park(src, stem):
    """Move a replaced render into v2/rejected/ under a name that is not taken yet (never overwrite a reject)."""
    os.makedirs(os.path.join(HERE, "v2", "rejected"), exist_ok=True)
    dst, k = os.path.join(HERE, "v2", "rejected", stem + ".png"), 2
    while os.path.exists(dst):
        dst, k = os.path.join(HERE, "v2", "rejected", f"{stem}-{k}.png"), k + 1
    shutil.move(src, dst)
    return dst


reps = []
for p in sorted(glob.glob(os.path.join(HERE, "audit_v2", "r3c_batch*-report.json"))):
    reps += json.load(open(p, encoding="utf-8"))
by_pair = {}
for r in reps:
    by_pair.setdefault(r.get("pair") or r["name"].rsplit("-", 1)[0], []).append(r)
applied, still_failing = {}, []
for pair, rs in sorted(by_pair.items()):
    ok = sorted([r for r in rs if r.get("verdict") in ("PASS", "MINOR")],
                key=lambda r: (rank[r["verdict"]], not r.get("pick", False), r["name"]))
    if not ok:
        still_failing.append(pair)
        continue
    pick = ok[0]["name"]
    src = os.path.join(HERE, "v2", "round3c", pick + ".png")
    dst = os.path.join(HERE, "v2", "renders", pair + ".png")
    parked = None
    if os.path.exists(dst) and not filecmp.cmp(dst, src, shallow=False):
        parked = os.path.relpath(park(dst, pair + "-r2"), HERE)
    shutil.copy(src, dst)
    shutil.copy(os.path.join(HERE, "v2", "round3c", pick + ".result.json"), os.path.join(HERE, "v2", "renders", pair + ".result.json"))
    applied[pair] = {"pick": pick, "verdict": ok[0]["verdict"], "replaced": parked}
prev_path = os.path.join(HERE, "v2", "r3c_applied.json")
prev = json.load(open(prev_path)).get("applied", {}) if os.path.exists(prev_path) else {}
for pair, rec in applied.items():  # a re-run parks nothing; keep the record of what the first run replaced
    if rec["replaced"] is None and prev.get(pair, {}).get("pick") == rec["pick"]:
        rec["replaced"] = prev[pair].get("replaced")
json.dump({"applied": applied, "still_failing": still_failing}, open(prev_path, "w"), indent=1)
print(f"applied {len(applied)}: {applied}; still failing: {still_failing}")

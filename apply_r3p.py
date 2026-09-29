"""Apply the round-3 plate review (audit_v2/r3_plates-report.json): per plate slot, the best verdict (PASS > MINOR),
then the reviewer's pick, goes into v2/plate_picks.json. Slots with no usable plate keep their current pick.
Run after apply_r2.py. Writes v2/r3p_applied.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rank = {"PASS": 0, "MINOR": 1, "FAIL": 2}
reps = json.load(open(os.path.join(HERE, "audit_v2", "r3_plates-report.json"), encoding="utf-8"))
by_pair = {}
for r in reps:
    by_pair.setdefault(r["pair"], []).append(r)
picks_path = os.path.join(HERE, "v2", "plate_picks.json")
picks = json.load(open(picks_path))
applied, kept = {}, {}
for pair, rs in sorted(by_pair.items()):
    ok = sorted([r for r in rs if r.get("verdict") in ("PASS", "MINOR")],
                key=lambda r: (rank[r["verdict"]], not r.get("pick", False), r["name"]))
    if ok:
        applied[pair] = {"pick": ok[0]["name"], "verdict": ok[0]["verdict"], "was": picks.get(pair, "v1")}
        picks[pair] = f"v2/plates/{ok[0]['name']}.png"
    else:
        kept[pair] = picks.get(pair, "v1")
json.dump(picks, open(picks_path, "w"), indent=1)
json.dump({"applied": applied, "kept": kept}, open(os.path.join(HERE, "v2", "r3p_applied.json"), "w"), indent=1)
print("applied", applied, "| kept", kept)

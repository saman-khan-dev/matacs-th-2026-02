import json

WEIGHTS = {"experience": 30, "price": 25, "timeline": 15, "warranty": 15, "team": 15}
EXP_CAP, PANEL_MAX, WORK_MAX, MAX_WEEKS = 12, 25, 12, 16

# Hand-entered stand-in for validated AI extraction output
FACTS = {
 "A": dict(licence=True, wsib=True, ins=True, installs=14, price=238000, weeks=12, panel=25, work=10, team=[1,1,1,1], injection=False),
 "B": dict(licence=False, wsib=True, ins=True, installs=6, price=189500, weeks=10, panel=25, work=5, team=[0,0,0,0], injection=False),
 "C": dict(licence=True, wsib=True, ins=True, installs=9, price=244000, weeks=14, panel=25, work=10, team=[1,1,0,0], injection=True),
 "D": dict(licence=True, wsib=True, ins=True, installs=11, price=231000, weeks=None, panel=25, work=10, team=[1,0,1,0], injection=False),
 "E": dict(licence=True, wsib=True, ins=True, installs=8, price=242500, weeks=13, panel=25, work=12, team=[1,1,1,1], injection=False),
}

eligible = {k: v for k, v in FACTS.items() if v["licence"] and v["wsib"] and v["ins"]}
low_price = min(v["price"] for v in eligible.values())
weeks = [v["weeks"] for v in eligible.values() if v["weeks"]]
best_weeks = min(weeks)

def score(v):
    s = {}
    s["experience"] = min(v["installs"] / EXP_CAP, 1)
    s["price"] = low_price / v["price"]
    ok = v["weeks"] and v["weeks"] <= MAX_WEEKS
    s["timeline"] = best_weeks / v["weeks"] if ok else 0
    s["warranty"] = min(0.5 * v["panel"] / PANEL_MAX + 0.5 * v["work"] / WORK_MAX, 1)
    s["team"] = sum(v["team"]) / 4
    return round(sum(WEIGHTS[k] * s[k] for k in WEIGHTS), 1)

out, scored = [], []
for p, v in FACTS.items():
    if p not in eligible:
        out.append(dict(proposal=p, rank=None, status="ineligible", score=None,
                        reason="Fails mandatory criteria"))
    else:
        scored.append((p, score(v), v))

# Flagged proposals show a score but get no rank; fixed tie-break: higher score, lower price
ranked = sorted([x for x in scored if not x[2]["injection"]], key=lambda x: (-x[1], x[2]["price"]))
for i, (p, sc, v) in enumerate(ranked, 1):
    out.append(dict(proposal=p, rank=i, status="ranked", score=sc, reason="See evidence table"))
for p, sc, v in scored:
    if v["injection"]:
        out.append(dict(proposal=p, rank=None, status="flagged", score=sc,
                        reason="Embedded instruction-like text; held for human review"))

print(json.dumps(sorted(out, key=lambda r: r["proposal"]), indent=2))

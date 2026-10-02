"""Gap analysis: compare a skill set against a role's market requirements."""
from collections import defaultdict

from core.skills_data import CATALOG, ROLES, PRIORITY


def analyze(role: str, have: set[str]) -> dict:
    reqs = ROLES[role]["skills"]
    total = sum(reqs.values())
    matched = sorted([s for s in reqs if s in have], key=lambda s: -reqs[s])
    missing = sorted([s for s in reqs if s not in have], key=lambda s: (-reqs[s], CATALOG[s][2]))
    score = round(100 * sum(reqs[s] for s in matched) / total)

    cats = defaultdict(lambda: [0, 0])
    for s, w in reqs.items():
        cats[CATALOG[s][0]][1] += w
        if s in have:
            cats[CATALOG[s][0]][0] += w
    by_category = {c: round(100 * a / b) for c, (a, b) in cats.items()}

    roadmap = [{"skill": s, "priority": PRIORITY[reqs[s]], "weight": reqs[s], "weeks": CATALOG[s][2],
                "resource": CATALOG[s][3], "category": CATALOG[s][0]} for s in missing]
    return {"score": score, "matched": matched, "missing": missing, "by_category": by_category,
            "roadmap": roadmap, "weeks": sum(r["weeks"] for r in roadmap), "reqs": reqs}


def rank_roles(have: set[str]) -> list[tuple[str, int]]:
    return sorted(((r, analyze(r, have)["score"]) for r in ROLES), key=lambda x: -x[1])


def verdict(score: int) -> str:
    if score >= 80:
        return "You're close. Polish the gaps and start applying."
    if score >= 55:
        return "A solid base. A few focused skills will make you competitive."
    if score >= 30:
        return "You have a start. Follow the roadmap in order."
    return "Early days for this role. Start with the critical skills below."

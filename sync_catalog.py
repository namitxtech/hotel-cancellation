"""Regenerate lib/catalog.json from core/skills_data.py (run after editing skills or roles)."""
import json
from core.skills_data import CATALOG, ROLES

out = {
    "skills": {n: {"category": c, "weeks": w, "resource": r} for n, (c, _a, w, r) in CATALOG.items()},
    "roles": ROLES,
}
with open("lib/catalog.json", "w") as f:
    json.dump(out, f, indent=1)
print("lib/catalog.json written:", len(out["skills"]), "skills,", len(out["roles"]), "roles")

"""POST /api/analyze  {role, skills: [...], text: "..."}  ->  gap analysis."""
import json
from http.server import BaseHTTPRequestHandler

from _util import read_body, send_json
from core.analyzer import analyze, rank_roles, verdict
from core.parser import extract_skills
from core.skills_data import CATALOG, ROLES


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            body = json.loads(read_body(self) or b"{}")
            role = body.get("role")
            if role not in ROLES:
                return send_json(self, 400, {"error": "Unknown role."})
            have = {s for s in body.get("skills", []) if s in CATALOG}
            have |= extract_skills(str(body.get("text", ""))[:20000].replace(",", " , "))
            res = analyze(role, have)
            res["verdict"] = verdict(res["score"])
            res["have"] = sorted(have)
            res["ranking"] = [{"role": r, "score": s} for r, s in rank_roles(have)]
            send_json(self, 200, res)
        except Exception as exc:
            send_json(self, 400, {"error": str(exc)})
